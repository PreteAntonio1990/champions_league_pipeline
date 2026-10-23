
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select team_name
from CHAMPIONS_LEAGUE.DBT_DEV.stg_team
where team_name is null



  
  
      
    ) dbt_internal_test