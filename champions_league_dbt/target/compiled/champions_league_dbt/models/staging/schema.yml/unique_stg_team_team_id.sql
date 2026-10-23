
    
    

select
    team_id as unique_field,
    count(*) as n_records

from CHAMPIONS_LEAGUE.DBT_DEV.stg_team
where team_id is not null
group by team_id
having count(*) > 1


