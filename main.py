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
    with open("./ou_lines_list/%s/%s.json" % (date.split("-")[0], date), "w") as f: json.dump(response.json(), f)

def concat_ou_line_to_df(df):
    games_with_lines = pd.DataFrame()
    for i, game in tqdm(df.iterrows()):
        if "%s.json" % game.Date not in os.listdir("./ou_lines_list/%s" % game.Date.split("-")[0]): get_lines_on_day(game.Date) #check if odds data exists
        with open("./ou_lines_list/%s/%s.json" % (game.Date.split("-")[0], game.Date), "r") as read_content:
            for game_odds in json.load(read_content)["data"]:
                if game.Home == game_odds["home_team"] and game.Away == game_odds["away_team"]:
                    for bookmaker in game_odds["bookmakers"]:
                       game[bookmaker["title"]] = bookmaker["markets"][0]["outcomes"][0]["point"]
        games_with_lines = pd.concat([games_with_lines, game], axis=1)
    return games_with_lines.T

if __name__ == "__main__":
    df = pd.DataFrame()
    for file in os.listdir("./games_list/cleaned_data"):
        filename = os.fsdecode(file)
        if filename.endswith(".xlsx"):
            df = pd.concat([df, pd.read_excel("./games_list/cleaned_data/" + filename)], axis=0)
    games_with_lines = concat_ou_line_to_df(df)
    games_with_lines.to_excel("Full_Dataset.xlsx")
