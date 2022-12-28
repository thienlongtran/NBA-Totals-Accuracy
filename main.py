import os
import pandas as pd
import requests
import json
from tqdm import tqdm

THE_ODDS_API_URL = "https://api.the-odds-api.com/v4/sports/basketball_nba/odds-history/?&regions=eu,us&markets=totals"
THE_ODDS_API_KEY = os.environ["THE_ODDS_API_KEY"]

def get_lines_on_day(date):
    params = {
        "date": "%sT12:00:00Z" % date,
        "apiKey": THE_ODDS_API_KEY
    }
    response = requests.get(THE_ODDS_API_URL, params=params)
    with open("./ou_lines_list/%s/%s.json" % (date.split("-")[0] ,date), "w") as f: json.dump(response.json(), f)

if __name__ == "__main__":
    for file in os.listdir("./games_list/cleaned_data"):
        filename = os.fsdecode(file)
        print(filename)
        if filename.endswith(".xlsx"):
            df = pd.read_excel("./games_list/cleaned_data/" + filename)
            for row in tqdm(df.itertuples()):
                if "%s.json" % row.Date not in os.listdir("./ou_lines_list/%s" % row.Date.split("-")[0]): get_lines_on_day(row.Date)