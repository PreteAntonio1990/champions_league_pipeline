
  create or replace   view CHAMPIONS_LEAGUE.DBT_DEV.stg_team
  
  
  
  
  as (
    with source as (
    select * from CHAMPIONS_LEAGUE.STAR_SCHEMA.DIM_TEAM
),

renamed as (
    select
        TEAM_ID as team_id,
        NAME as team_name,
        SHORT_NAME as short_name,
        TLA as tla,
        LAND as land,
        GEGRUENDET as gegruendet,
        STADION as stadion
    from source
)

select * from renamed
  );

