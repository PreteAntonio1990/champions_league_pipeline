"""
Great Expectations Validation Skript
Prüft Datenqualität der Snowflake Tabellen
"""

import os
from dotenv import load_dotenv
import great_expectations as gx
from great_expectations.checkpoint import UpdateDataDocsAction, Checkpoint

load_dotenv("../.env")

context = gx.get_context(mode="file")

# Data Docs Site konfigurieren
site_config = {
    "class_name": "SiteBuilder",
    "store_backend": {
        "class_name": "TupleFilesystemStoreBackend",
        "base_directory": "data_docs/local_site/"
    },
    "site_index_builder": {
        "class_name": "DefaultSiteIndexBuilder"
    }
}

try:
    context.add_data_docs_site(site_name="local_site", site_config=site_config)
except Exception:
    pass

connection_string = (
    f"snowflake://{os.getenv('SNOWFLAKE_USER')}:{os.getenv('SNOWFLAKE_PASSWORD')}"
    f"@{os.getenv('SNOWFLAKE_ACCOUNT')}/{os.getenv('SNOWFLAKE_DATABASE')}/{os.getenv('SNOWFLAKE_SCHEMA')}"
    f"?warehouse={os.getenv('SNOWFLAKE_WAREHOUSE')}&role=ACCOUNTADMIN"
)

datasource = context.data_sources.add_or_update_snowflake(
    name="snowflake_source",
    connection_string=connection_string
)

# DIM_TEAM
team_asset = datasource.add_table_asset(name="dim_team_asset", table_name="DIM_TEAM")
team_batch = team_asset.add_batch_definition_whole_table(name="dim_team_full")
team_suite = context.suites.add_or_update(gx.ExpectationSuite(name="dim_team_quality"))
team_suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="TEAM_ID"))
team_suite.add_expectation(gx.expectations.ExpectColumnValuesToBeUnique(column="TEAM_ID"))
team_suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="NAME"))
team_suite.add_expectation(gx.expectations.ExpectColumnValueLengthsToBeBetween(column="TLA", min_value=2, max_value=10))
team_validation = context.validation_definitions.add_or_update(
    gx.ValidationDefinition(data=team_batch, suite=team_suite, name="dim_team_validation")
)

# DIM_DATUM
datum_asset = datasource.add_table_asset(name="dim_datum_asset", table_name="DIM_DATUM")
datum_batch = datum_asset.add_batch_definition_whole_table(name="dim_datum_full")
datum_suite = context.suites.add_or_update(gx.ExpectationSuite(name="dim_datum_quality"))
datum_suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="DATUM_ID"))
datum_suite.add_expectation(gx.expectations.ExpectColumnValuesToBeUnique(column="DATUM_ID"))
datum_suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="DATUM"))
datum_suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(column="MONAT", min_value=1, max_value=12))
datum_suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(column="TAG", min_value=1, max_value=31))
datum_validation = context.validation_definitions.add_or_update(
    gx.ValidationDefinition(data=datum_batch, suite=datum_suite, name="dim_datum_validation")
)

# FACT_SPIEL
spiel_asset = datasource.add_table_asset(name="fact_spiel_asset", table_name="FACT_SPIEL")
spiel_batch = spiel_asset.add_batch_definition_whole_table(name="fact_spiel_full")
spiel_suite = context.suites.add_or_update(gx.ExpectationSuite(name="fact_spiel_quality"))
spiel_suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="SPIEL_ID"))
spiel_suite.add_expectation(gx.expectations.ExpectColumnValuesToBeUnique(column="SPIEL_ID"))
spiel_suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="HEIM_TEAM_ID"))
spiel_suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="GAST_TEAM_ID"))
spiel_suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(column="TORE_HEIM", min_value=-1, max_value=20))
spiel_suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(column="TORE_GAST", min_value=-1, max_value=20))
spiel_suite.add_expectation(gx.expectations.ExpectColumnValuesToBeInSet(
    column="STATUS",
    value_set=["FINISHED", "SCHEDULED", "IN_PLAY", "POSTPONED", "TIMED", "LIVE", "PAUSED"]
))
spiel_validation = context.validation_definitions.add_or_update(
    gx.ValidationDefinition(data=spiel_batch, suite=spiel_suite, name="fact_spiel_validation")
)

# Checkpoint mit allen Validations und Data Docs Action
checkpoint = context.checkpoints.add_or_update(
    Checkpoint(
        name="champions_league_checkpoint",
        validation_definitions=[team_validation, datum_validation, spiel_validation],
        actions=[UpdateDataDocsAction(name="update_docs", site_names=["local_site"])]
    )
)

print("=" * 70)
print("Great Expectations Data Quality Validation")
print("=" * 70)

result = checkpoint.run()

for validation_name, validation_result in result.run_results.items():
    stats = validation_result.statistics
    print(f"\nValidation: {validation_name}")
    print(f"  Erfolgreich: {validation_result.success}")
    print(f"  Tests gesamt: {stats['evaluated_expectations']}")
    print(f"  Erfolgreich: {stats['successful_expectations']}")
    print(f"  Fehlgeschlagen: {stats['unsuccessful_expectations']}")

print("\n" + "=" * 70)
print(f"Checkpoint Status: {'Erfolgreich' if result.success else 'Fehlgeschlagen'}")
print("=" * 70)

# Data Docs bauen und öffnen
context.build_data_docs()
context.open_data_docs()

print("\nData Docs im Browser geöffnet.")
