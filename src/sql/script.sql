with dim_teams_cte as (
    select * from dim_teams
),
dim_competitions_cte as (
    select * from dim_competitions
),
fact_competitions_cte as (
    select * from fact_competitions
),
final as (
    select  
        dim_competitions_cte.name,  
        count(dim_teams_cte.id) nm_teams
    from fact_competitions_cte
    left join dim_competitions_cte on dim_competitions_cte.id = fact_competitions_cte.fact_competitions
    left join dim_teams_cte on dim_teams_cte.id = fact_competitions_cte.team_id
    group by dim_competitions_cte.name
    order by nm_teams desc
)
select * from final