# import mysql.connector
# from database_fill.database_connection import db, cursor
from requests_html import HTMLSession
from pprint import pprint
import json
# import database_fill.database_functions as dbf

session = HTMLSession()

# constants 
DB_NAME = 'leafsroster'

# variables
years = ["2016", "2017", "2018", "2019", "2020", "2021", "2022"]
rosterstats_l = []
yearlystats_l = []
playerstats = []
player_l = []


for year in range(len(years)):
    playerstats = []
    if years[year] == "2022":
        continue
    season = f"{years[year]}{years[year+1]}"
    player_page = session.get(f"https://www.nhl.com/stats/skaters?aggregate=0&reportType=season&seasonFrom={season}&seasonTo={season}&gameType=2&playerPlayedFor=franchise.5&filter=gamesPlayed,gte,1&sort=points,goals,assists&page=0&pageSize=50")
    player_page.html.render(sleep=1, keep_page=True, scrolldown=8, timeout=60)    
    player_stats = player_page.html.find(".rt-tr-group")
    for j in range(len(player_stats)):
        one_player = player_stats[j].text.split("\n")
        p_dict = {
            "name": one_player[1],
            "shoots": one_player[4],
            "position": one_player[5],
            "games_played": one_player[6],
            "goals": one_player[7],
            "assists": one_player[8],
            "points": one_player[9],
            "plus_minus": one_player[10],
            "penalty_mins": one_player[11],
            "points_per_game": one_player[12],
            "evs_goals": one_player[13],
            "pp_goals": one_player[15],
            "pp_points": one_player[16],
            "sh_goals": one_player[17],
            "sh_points": one_player[18],
            "gw_goals": one_player[20],
            "ot_goals": one_player[21],
            "shots": one_player[21],
            "shot_percentage": 0 if one_player[22] == "--" else one_player[22],
            "toi_per_game": one_player[23],
            "faceoff_win_percentage": 0 if one_player[24] == "--" else one_player[24]
        }
        playerstats.append(p_dict)

    with open(f"{season}_playerstats.json", "w") as outfile:
        json.dump(playerstats, outfile, indent=4)


for year in range(len(years)):
    goaliestats = []
    if years[year] == "2022":
        continue
    season = f"{years[year]}{years[year+1]}"
    player_page = session.get(f"https://www.nhl.com/stats/goalies?reportType=season&seasonFrom={season}&seasonTo={season}&gameType=2&playerPlayedFor=franchise.5&filter=gamesPlayed,gte,1&sort=wins,savePct&page=0&pageSize=50")
    player_page.html.render(sleep=1, keep_page=True, scrolldown=8, timeout=60)    
    player_stats = player_page.html.find(".rt-tr-group")
    for j in range(len(player_stats)):
        one_player = player_stats[j].text.split("\n")
        p_dict = {
                "name": one_player[1],
                "position": "G",
                "games_played": one_player[5],
                "games_saved": one_player[6],
                "wins": one_player[7],
                "losses": one_player[8],
                "ot_losses": one_player[10],
                "shots_against": one_player[11],
                "goals_against": one_player[13],
                "goals_against_average": one_player[15],
                "saves": one_player[12],
                "saves_percentage": one_player[14],
                "shutouts": one_player[17]
            }
        goaliestats.append(p_dict)

    with open(f"{season}_goaliestats.json", "w") as outfile:
        json.dump(goaliestats, outfile, indent=4)