
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    datum_id as unique_field,
    count(*) as n_records

from CHAMPIONS_LEAGUE.DBT_DEV.stg_datum
where datum_id is not null
group by datum_id
having count(*) > 1



  
  
      
    ) dbt_internal_test