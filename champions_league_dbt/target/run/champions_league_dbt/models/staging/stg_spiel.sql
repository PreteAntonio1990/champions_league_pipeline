
  create or replace   view CHAMPIONS_LEAGUE.DBT_DEV.stg_spiel
  
  
  
  
  as (
    with source as (
    select * from CHAMPIONS_LEAGUE.STAR_SCHEMA.FACT_SPIEL
),

renamed as (
    select
        SPIEL_ID as spiel_id,
        DATUM_ID as datum_id,
        HEIM_TEAM_ID as heim_team_id,
        GAST_TEAM_ID as gast_team_id,
        STATUS as status,
        MATCHDAY as matchday,
        TORE_HEIM as tore_heim,
        TORE_GAST as tore_gast,
        TORE_GESAMT as tore_gesamt
    from source
)

select * from renamed
  );

