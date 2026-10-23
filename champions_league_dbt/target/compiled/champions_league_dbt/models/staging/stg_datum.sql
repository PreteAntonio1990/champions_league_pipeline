with source as (
    select * from CHAMPIONS_LEAGUE.STAR_SCHEMA.DIM_DATUM
),

renamed as (
    select
        DATUM_ID as datum_id,
        DATUM as datum,
        JAHR as jahr,
        MONAT as monat,
        TAG as tag,
        WOCHENTAG as wochentag,
        MONAT_NAME as monat_name
    from source
)

select * from renamed