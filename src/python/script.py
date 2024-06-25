from dotenv import load_dotenv
from sqlalchemy import create_engine
import requests
import json
import os
import pandas as pd
import time

def fn_execute_api_call_competition(headers: dict) -> list:
    """
        fn_execute_api_call_competition -> list
        @type headers   dict
        Function defined to get all the competitions from API.
    """
    uri = "https://api.football-data.org/v4/competitions"
    arr_competition_id = []
    response = requests.get(uri,headers=headers)
    if response.status_code == 200:   
        with open('./data_json/competitions.json', 'w') as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=4)
        for competition in response.json()['competitions']:
            arr_competition_id.append(competition['id'])
    else:
        print(f'API Status ... ... [LIMIT ERROR {response.status_code}]')
    
    return arr_competition_id

def fn_execute_api_call_competition_teams(headers: dict, list_competition_id: list) -> None:
    """
        fn_execute_api_call_competition_teams -> None
        @type headers   dict
        @type list_competition_id   list
        Function defined to get all the info from competitions at teams.
    """
    json_competition_teams = []

    for competition_id in list_competition_id: 
        uri_competition_teams = f"https://api.football-data.org/v4/competitions/{competition_id}/teams"
        response = requests.get(uri_competition_teams,headers=headers)
        if response.status_code == 429:
            print('API Status ... ... [LIMIT ERROR]')
            time.sleep(60)
            print('API Status ... ... [CHECKING]')
            response = requests.get(uri_competition_teams,headers=headers)
            print('API Status ... ... [OK]')

        if response.status_code == 200:
            json_competition_teams.append(response.json())
        else:
            print('Error' + str(response.status_code))

    with open('./data_json/competition_teams.json', 'w') as f:
        json.dump(json_competition_teams, f, ensure_ascii=False, indent=4)
    
def fn_execute_db_bulk() -> None:
    """
        fn_execute_db_bulk -> None
        Function defined to insert data into database.
    """
    try:
        engine = create_engine('sqlite:///./data/db_bcg_project.db') 

        data_competitions = None
        with open('./data_json/competitions.json', 'r') as file:
            data_competitions = json.loads(file.read())

        pd_series_competitions = pd.Series(data_competitions['competitions'])

        df_competitions = pd_series_competitions.to_frame()
        df_competitions = pd.json_normalize(df_competitions[0])
        df_competitions = df_competitions[['id','name']]

        dim_competitions = 'dim_competitions'
        df_competitions.head(n=0).to_sql(name=dim_competitions, con=engine, index=False, if_exists='replace')
        df_competitions.to_sql(name=dim_competitions, con=engine, index=False, if_exists='append')
        print(f'Dimension {dim_competitions} ... ... [OK]')
    except:
        print(f'Dimension {dim_competitions} ... ... [ERROR]')

    try:
        data_competition_teams = None
        with open('./data_json/competition_teams.json', 'r') as file:
            data_competition_teams = json.loads(file.read())

        pd_serie_competition_teams = pd.Series(data_competition_teams)

        df_competition_teams = pd_serie_competition_teams.to_frame()
        df_competition_teams = pd.json_normalize(df_competition_teams[0],'teams',[['competition','id'],['competition','name']])
        df_competition_teams = df_competition_teams.rename(columns={'competition.id':'fact_competitions','competition.name':'competition_name','id':'team_id'})
        df_competition_teams = df_competition_teams[['team_id','name','shortName','tla','fact_competitions','competition_name']]
        
        df_competition_teams_fact = df_competition_teams[['fact_competitions','team_id']]

        df_teams_dim = df_competition_teams[['team_id','name']]
        df_teams_dim = df_teams_dim.rename(columns={'team_id':'id'})
        df_teams_dim = df_teams_dim.drop_duplicates()

        # fact
        fact_competitions = 'fact_competitions'
        df_competition_teams_fact.head(n=0).to_sql(name=fact_competitions, con=engine, index=False, if_exists='replace')
        df_competition_teams_fact.to_sql(name=fact_competitions, con=engine, index=False, if_exists='append')
        print(f'Fact {fact_competitions} ... ... [OK]')
    except:
        print(f'Fact {fact_competitions} ... ... [ERROR]')
    
    try:
        # dimension
        dim_teams = 'dim_teams'
        df_teams_dim.head(n=0).to_sql(name=dim_teams, con=engine, index=False, if_exists='replace')
        df_teams_dim.to_sql(name=dim_teams, con=engine, index=False, if_exists='append')
        print(f'Dimension {dim_teams} ... ... [OK]')
    except:
        print(f'Dimension {dim_teams} ... ... [ERROR]')

def fn_export_summary() -> bool:
    """
        fn_export_summary   -> bool
        Function created to export a summary from data.
    """
    try:
        engine = create_engine('sqlite:///./data/db_bcg_project.db') 
        df_export = pd.read_sql('''
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
                left join dim_competitions_cte  on dim_competitions_cte.id = fact_competitions_cte.fact_competitions
                left join dim_teams_cte         on dim_teams_cte.id = fact_competitions_cte.team_id
                group by 
                    dim_competitions_cte.name
                order by nm_teams desc
            )
            select * from final
        ''',engine)

        df_export.to_csv('./outputs/summary_data.csv', index=False)
        print('Data exported ... ... [OK]')  
        return True
    except:
        print('Error exporting file ... ... [ERROR]')

def main():
    """
        Main -> None
        Main process.
    """
    print('Starting process ... ... [OK]')
    load_dotenv()
    api_token = os.getenv("API_Token")
    headers = {'X-Auth-Token': api_token}
    list_competition_id = fn_execute_api_call_competition(headers)
    fn_execute_api_call_competition_teams(headers, list_competition_id)
    fn_execute_db_bulk()
    fn_export_summary()
    print('Finishing process ... ... [OK]')

if __name__ == '__main__':
    main()