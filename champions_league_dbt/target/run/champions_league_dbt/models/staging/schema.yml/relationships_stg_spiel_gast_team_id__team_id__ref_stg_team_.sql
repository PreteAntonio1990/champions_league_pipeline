
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with child as (
    select gast_team_id as from_field
    from CHAMPIONS_LEAGUE.DBT_DEV.stg_spiel
    where gast_team_id is not null
),

parent as (
    select team_id as to_field
    from CHAMPIONS_LEAGUE.DBT_DEV.stg_team
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null



  
  
      
    ) dbt_internal_test