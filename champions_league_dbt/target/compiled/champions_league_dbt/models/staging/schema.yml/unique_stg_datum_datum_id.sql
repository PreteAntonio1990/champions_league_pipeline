
    
    

select
    datum_id as unique_field,
    count(*) as n_records

from CHAMPIONS_LEAGUE.DBT_DEV.stg_datum
where datum_id is not null
group by datum_id
having count(*) > 1


