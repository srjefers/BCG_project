from dotenv import load_dotenv
import requests
import json
import os

def fn_execute_api_call():
    """
        ...
    """
    load_dotenv()
    api_token = os.getenv("API_Token")
    uri = "https://api.football-data.org/v4/competitions/CL/matches"
    headers = {'X-Auth-Token': api_token}

    response = requests.get(uri,headers=headers)
    for match in response.json()['matches']:
        print(match)

def main():
    """
        ...
    """
    fn_execute_api_call()

if __name__ == '__main__':
    fn_execute_api_call()