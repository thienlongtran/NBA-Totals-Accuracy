import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import os
import pandas as pd
from tqdm import tqdm

team_codes = {
    "Atlanta": "Atlanta Hawks",
    "NewJersey": "New Jersey Nets",
    "Boston": "Boston Celtics",
    "Brooklyn": "Brooklyn Nets",
    "Charlotte": "Charlotte Hornets",
    "Chicago": "Chicago Bulls",
    "Cleveland": "Cleveland Cavaliers",
    "Dallas": "Dallas Mavericks",
    "Denver": "Denver Nuggets",
    "Detroit": "Detroit Pistons",
    "GoldenState": "Golden State Warriors",
    "Houston": "Houston Rockets",
    "Indiana": "Indiana Pacers",
    "LAClippers": "Los Angeles Clippers",
    "LALakers": "Los Angeles Lakers",
    "Memphis": "Memphis Grizzlies",
    "Miami": "Miami Heat",
    "Milwaukee": "Milwaukee Bucks",
    "Minnesota": "Minnesota Timberwolves",
    "NewOrleans": "New Orleans Pelicans",
    "NewYork": "New York Knicks",
    "OklahomaCity": "Oklahoma City Thunder",
    "Seattle": "Seattle SuperSonics",
    "Orlando": "Orlando Magic",
    "Philadelphia": "Philadelphia 76ers",
    "Phoenix": "Phoenix Suns",
    "Portland": "Portland Trail Blazers",
    "Sacramento": "Sacramento Kings",
    "SanAntonio": "San Antonio Spurs",
    "Toronto": "Toronto Raptors",
    "Utah": "Utah Jazz",
    "Washington": "Washington Wizards",
}

fall_months = set([9, 10, 11, 12])
spring_months = set([1, 2, 3, 4, 5, 6, 7, 8])

for file in tqdm(os.listdir(".")):
    filename = os.fsdecode(file)
    if filename.endswith(".xlsx"):
        start_year, end_year = filename.split("-")[0], "20" + filename.split("-")[1].replace(".xlsx", "")
        df = pd.read_excel(filename)
        x = pd.DataFrame(columns=["Date", "Home", "Away", "Points"])
        count = 2
        date = home = away = points = None
        for row in df.itertuples():
            if count % 2 == 0:
                date = str("0" + str(row[1])) if len(str(row[1])) == 3 else str(str(row[1]))
                year = start_year if int(date[:2]) in fall_months else end_year if int(date[:2]) in spring_months else "N/A"
                date = year + "-" + date[:2] + "-" + date[2:]
                away = team_codes.get(str(row[4]))
                points = row[9]
                count += 1
            else:
                home = team_codes.get(str(row[4]))
                points += row[9]
                game = {
                    "Date": date,
                    "Home": home,
                    "Away": away,
                    "Points": points,
                }
                x = x.append(game, ignore_index=True)
                count += 1
        name = "./cleaned_data/" + filename
        x.to_excel(name)