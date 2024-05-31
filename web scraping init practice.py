import requests
import time 
from bs4 import BeautifulSoup
import pandas as pd

standings_url= "https://fbref.com/en/comps/9/Premier-League-Stats"

"""data= requests.get(standings_url)

#print(data.text)---- This is all the html of the link above

soup = BeautifulSoup(data.text)

#This helps me parse the data by selecting the first table class[0]
standings_table=soup.select("table.stats_table")[0]

#This parse the new data and find all the elements there with a tags
links = standings_table.find_all('a')

#This parses through the new data and get all the href elements that contain /squads/
links= [l.get ("href") for l in links]
links = [l for l in links if "/squads/" in l]

#Format the string to provide a full url link
team_urls = [f"https://fbref.com{l}" for l in links]

team_url = team_urls[0]

data = requests.get(team_url)
import pandas as pd
matches = pd.read_html(data.text, match="Scores & Fixtures")
#print (matches[0])

soup = BeautifulSoup(data.text)
links = soup.find_all("a")
links = [l.get("href") for l in links]
links = [l for l in links if l and "all_comps/shooting/" in l]

data = requests.get(f"https://fbref.com{links[0]}")
shooting = pd.read_html(data.text, match="Shooting")[0]

shooting.columns = shooting.columns.droplevel()

team_data = matches[0].merge(shooting[["Date", "Sh", "SoT", "Dist", "FK", "PK", "PKatt"]], on="Date")"""

years = list(range(2022, 2020,-1))

for year in years:
    data = requests.get(standings_url)
    soup = BeautifulSoup(data.text)
    standings_table=soup.select("table.stats_table")[0]
    
    links = standings_table.find_all('a')
    links= [l.get ("href") for l in links]
    links = [l for l in links if "/squads/" in l]
    team_urls = [f"https://fbref.com{l}" for l in links]

    previous_season = soup.select("a.prev")[0].get("href")
    standings_url = f"https://fbref.com{previous_season}"

    for team_url in team_urls:
        team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
        data = requests.get(team_url)
        matches = pd.read_html(data.text, match="Scores & Fixtures")[0]

        soup = BeautifulSoup (data.text)
        links = [l.get("href") for l in soup.find_all("a")]
        links = [l for l in links if l and "all_comps/shooting/" in l]
        data = requests.get(f"https://fbref.com{links[0]}")
        shooting = pd.read_html(data.text, match="Shooting")[0]
        shooting.columns = shooting.columns.droplevel()
        try:
            team_data = matches[0].merge(shooting[["Date", "Sh", "SoT", "Dist", "FK", "PK", "PKatt"]], on="Date")
        except ValueError:
            continue

        team_data = team_data[team_data["Comp"]] == "Premier League"
        team_data["Season"] = year
        all_matches.append(team_data)
        time.sleep()

match_df = pd.concat(all_matches)
match_df.columns = [c.lower() for c in match_df.columns]
match_df.to_csv("matches.csv")
