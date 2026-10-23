
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select datum_id
from CHAMPIONS_LEAGUE.DBT_DEV.stg_datum
where datum_id is null



  
  
      
    ) dbt_internal_test