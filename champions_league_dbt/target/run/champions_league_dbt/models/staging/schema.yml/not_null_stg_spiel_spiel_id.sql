
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select spiel_id
from CHAMPIONS_LEAGUE.DBT_DEV.stg_spiel
where spiel_id is null



  
  
      
    ) dbt_internal_test