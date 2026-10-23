
  
    

create or replace transient table CHAMPIONS_LEAGUE.DBT_DEV.fct_team_performance
    
    
    
    as (with spiele as (
    select * from CHAMPIONS_LEAGUE.DBT_DEV.stg_spiel
    where status = 'FINISHED'
),

teams as (
    select * from CHAMPIONS_LEAGUE.DBT_DEV.stg_team
),

heim_perspektive as (
    select
        heim_team_id as team_id,
        tore_heim as tore_eigene,
        tore_gast as tore_gegner,
        case
            when tore_heim > tore_gast then 'sieg'
            when tore_heim < tore_gast then 'niederlage'
            else 'unentschieden'
        end as ergebnis
    from spiele
),

gast_perspektive as (
    select
        gast_team_id as team_id,
        tore_gast as tore_eigene,
        tore_heim as tore_gegner,
        case
            when tore_gast > tore_heim then 'sieg'
            when tore_gast < tore_heim then 'niederlage'
            else 'unentschieden'
        end as ergebnis
    from spiele
),

alle_spiele as (
    select * from heim_perspektive
    union all
    select * from gast_perspektive
),

aggregiert as (
    select
        team_id,
        count(*) as spiele_gesamt,
        sum(case when ergebnis = 'sieg' then 1 else 0 end) as siege,
        sum(case when ergebnis = 'niederlage' then 1 else 0 end) as niederlagen,
        sum(case when ergebnis = 'unentschieden' then 1 else 0 end) as unentschieden,
        sum(tore_eigene) as tore_erzielt,
        sum(tore_gegner) as tore_kassiert,
        sum(tore_eigene) - sum(tore_gegner) as tor_differenz
    from alle_spiele
    group by team_id
),

final as (
    select
        t.team_id,
        t.team_name,
        t.land,
        a.spiele_gesamt,
        a.siege,
        a.niederlagen,
        a.unentschieden,
        a.tore_erzielt,
        a.tore_kassiert,
        a.tor_differenz,
        (a.siege * 3 + a.unentschieden) as punkte
    from aggregiert a
    inner join teams t on a.team_id = t.team_id
)

select * from final
order by punkte desc
    )
;


  