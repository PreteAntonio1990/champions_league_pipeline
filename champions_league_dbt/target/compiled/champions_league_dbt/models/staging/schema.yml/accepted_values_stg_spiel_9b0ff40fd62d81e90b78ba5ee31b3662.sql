
    
    

with all_values as (

    select
        status as value_field,
        count(*) as n_records

    from CHAMPIONS_LEAGUE.DBT_DEV.stg_spiel
    group by status

)

select *
from all_values
where value_field not in (
    'FINISHED','SCHEDULED','IN_PLAY','POSTPONED','TIMED','LIVE','PAUSED'
)


