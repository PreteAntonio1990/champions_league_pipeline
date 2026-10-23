
    
    

select
    spiel_id as unique_field,
    count(*) as n_records

from CHAMPIONS_LEAGUE.DBT_DEV.stg_spiel
where spiel_id is not null
group by spiel_id
having count(*) > 1


