# BCG Project
## Summary

This repository presents a solution to the Lighthouse Data Engineer Challenge provided by BCG, providing a broad explanation of how the problem was addressed and how a solution was given which was implemented using python. In this repository you can find all the scripts and schemas to build in by yourself.

## Prerequisites
* [Python=3.12.4](https://www.python.org/downloads/)
* [sqlite](https://www.sqlite.org/download.html)
* [anaconda](https://docs.anaconda.com/anaconda/install/windows/)
* [API_KEY](https://www.football-data.org/client/register), save it at .env as `API_Token='you_api_key'`

## Usage

> As part of the project, generate a new [API_KEY](https://www.football-data.org/client/register) and save it at .env as `API_Token='you_api_key'` 

### Windows

> Please verify that you have [sqlite](https://www.sqlite.org/download.html) and [anaconda](https://docs.anaconda.com/anaconda/install/windows/) already intalled.

Execute the next command to be able to run the project, those commands can be executed at your cmd but we highly suggest you to run those on the terminal where you are able to run python3.

Also you can use [WSL](https://learn.microsoft.com/es-es/windows/wsl/install) for this.

```bash
conda env create -f ./python/environment.yaml
conda init
conda activate bcg_project
pip3 -r install ./python/requirements.txt
python3 ./python/script.py
conda deactivate 
```

### Linux or MacOs
Execute the next commands on your terminal, it is going to install all the dependencies for this project and also execute the conteiners.

```bash
sudo chmod +x executor.sh
./executor.sh
```

## Possible issues
> :warning: **Warning:** The summary export provided for this project and the summary in the PDF file display discrepancies in specific numerical values. I am currently investigating whether there have been changes to the data sourced from the API over time, as there seems to be an increase in the number of rows. Furthermore, it is pertinent to note that I have utilized the following URI for the API request: 
> * https://api.football-data.org/v4/competitions
> * https://api.football-data.org/v4/competitions/{competition_id}/teams

## Project layout

    └─ src/                 Source code.
       ├─ python/           Python code and data.
       │    ├─ data/        SQLite database.
       │    ├─ data_json/   Temp json files from API.
       │    └─ outputs/     Output report when script.py ends.                    
       └─ sql/              SQL Script.
    
## References
* https://www.football-data.org/documentation/quickstart
* https://docs.sqlalchemy.org/en/20/dialects/sqlite.html
* https://www.sqlalchemy.org/
* https://docs.football-data.org/general/v4/errors.html#_429_too_many_requests
* https://docs.football-data.org/general/v4/coding/python.html