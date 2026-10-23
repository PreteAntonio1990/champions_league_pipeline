
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select datum
from CHAMPIONS_LEAGUE.DBT_DEV.stg_datum
where datum is null



  
  
      
    ) dbt_internal_test