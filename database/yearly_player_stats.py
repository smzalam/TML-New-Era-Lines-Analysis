import mysql.connector
from database_connection import db, cursor
from requests_html import HTMLSession
import requests
from pprint import pprint
from yearly_roster import playerslinks_db

session = HTMLSession()

years = ["2016", "2017", "2018", "2019", "2020", "2021"]
rosterstats_l = []
yearlystats_l = []
playerstats = []

# pprint(str(playerslinks_db[0][24])[20:-3])    
    # player_stats = session.get(f"https://www.nhl.com/player/curtis-mcelhinney-8470147")
    # player_stats.html.render(sleep=1, keep_page=True, scrolldown=8, timeout=60)    
    # player_yearly_stat = player_stats.html.find(".player-jumbotron-vitals__attributes")
    # role = player_yearly_stat[0].text[0]

for year in range(len(playerslinks_db)):
    for player in range(len(playerslinks_db[year])):
        print(year, player)
        
        player_role = session.get(f"https://www.nhl.com/player/curtis-mcelhinney-8470147")
        player_role.html.render(sleep=1, keep_page=True, scrolldown=8, timeout=60)    
        player_yearly_role = player_role.html.find(".player-jumbotron-vitals__attributes")
        role = player_yearly_role[0].text[0]
        
        if (str(playerslinks_db[year][player])[20:-3] == ""):
            continue
        player_stats = session.get(f"https://www.nhl.com/{str(playerslinks_db[year][player])[20:-3]}")
        player_stats.html.render(sleep=1, keep_page=True, scrolldown=8, timeout=60)    
        player_yearly_stat = player_stats.html.find("#careerTable")
        player_yearly_stats = player_yearly_stat[0].text.split("\n")
        player_yearly_stats_l = []

        for i in range(len(player_yearly_stats)):
            for k in range(len(player_yearly_stats[i])):
                if (player_yearly_stats[i][k:k+3] == "TOR"):
                    if (int(player_yearly_stats[i-1][:4]) == 2016 or int(player_yearly_stats[i-1][:4]) > 2016):
                        player_yearly_stats_l.append(player_yearly_stats[i-1:i+13])

        # pprint(player_yearly_stats_l[:int((len(player_yearly_stats_l)/2))])
        
        for i in range(len(player_yearly_stats_l[:int((len(player_yearly_stats_l)/2))])):
            if (role == 'G'):
                player_yearly_stats_dict = {
                    "games_played": f"{player_yearly_stats_l[i][2]}",
                    "games_saved":f"{player_yearly_stats_l[i][3]}",
                    "wins":f"{player_yearly_stats_l[i][4]}",
                    "losses":f"{player_yearly_stats_l[i][5]}",
                    "ot_losses":f"{player_yearly_stats_l[i][6]}",
                    "shots_against":f"{player_yearly_stats_l[i][7]}",
                    "goals_against":f"{player_yearly_stats_l[i][8]}",
                    "gaa":f"{player_yearly_stats_l[i][9]}",
                    "saves":f"{player_yearly_stats_l[i][10]}",
                    "saves_%":f"{player_yearly_stats_l[i][11]}",
                    "shutouts":f"{player_yearly_stats_l[i][12]}"
                }
                playerstats.append(player_yearly_stats_dict)
            else:   
                player_yearly_stats_dict = {
                    "games_played": f"{player_yearly_stats_l[i][2]}",
                    "goals":f"{player_yearly_stats_l[i][3]}",
                    "assists":f"{player_yearly_stats_l[i][4]}",
                    "points":f"{player_yearly_stats_l[i][5]}",
                    "plus_minus":f"{player_yearly_stats_l[i][6]}",
                    "penalty_mins":f"{player_yearly_stats_l[i][7]}",
                    "pp_goals":f"{player_yearly_stats_l[i][8]}",
                    "pp_points":f"{player_yearly_stats_l[i][9]}",
                    "sh_goals":f"{player_yearly_stats_l[i][10]}",
                    "sh_points":f"{player_yearly_stats_l[i][11]}",
                    "gw_goals":f"{player_yearly_stats_l[i][12]}",
                    "ot_goals":f"{player_yearly_stats_l[i][13]}"
                }
                playerstats.append(player_yearly_stats_dict)

        yearlystats_l.append(player_stats)
        pprint(f"{year}_{player} done!")
        
    rosterstats_l.append(yearlystats_l)
    pprint(f"{year} done!")
    
pprint(rosterstats_l[0][1])
rosterstats_db = rosterstats_l