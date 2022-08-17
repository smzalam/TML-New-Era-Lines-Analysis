import mysql.connector
from database_fill.database_connection import db, cursor
from requests_html import HTMLSession
import requests
from pprint import pprint
import database_fill.database_functions as dbf

#constants 
TABLES = {}
DB_NAME = 'leafsroster'

# variables
years = ["2016", "2017", "2018", "2019", "2020", "2021"]
index = 0   
indexvalue = ""
atlanticstandings_l = []
yearvalues = []
leaguestandings_l = []
playoffresults_l = []

# start HTMLSession
session = HTMLSession()

# ========================================DIVISION=================================================================

# store pointers to the different htmls for each year - DIVISION
for i in range(len(years)):
    division = session.get(f"https://www.nhl.com/standings/{years[i]}/division")
    division.html.render(sleep=1, keep_page=True, scrolldown=8, timeout=60)
    standings = division.html.find('.responsive-datatable__pinned')
    if (years[i] == "2020"):
        atlanticstandings = standings[3].text.split("\n")   
    else: 
        atlanticstandings = standings[1].text.split("\n")
    atlanticstandings_l.append(atlanticstandings)
    print(f"{i} done")

# populate data for each year - DIVISION
for year in range(len(years)):
    atlanticstandings = atlanticstandings_l[year]
    for i in range(len(atlanticstandings)):
        for k in range(len(atlanticstandings[i])):
            if (atlanticstandings[i][k:k+7] == "Toronto"):
                year = {
                    "year":int(f"{years[year]}"),
                    "s_w":int(f"{atlanticstandings[i+2]}"),
                    "s_l":int(f"{atlanticstandings[i+3]}"),
                    "s_ot":int(f"{atlanticstandings[i+4]}"),
                    "div":f"{atlanticstandings[0]}",
                    "div_rank":int(f"{atlanticstandings[i-1]}"),
                    "pts":int(f"{atlanticstandings[i+5]}") 
                }
                yearvalues.append(year)
                print(f"{year} done!")
            
pprint(yearvalues)

# ========================================LEAGUE===================================================================

for i in range(len(years)):
    league = session.get(f"https://www.nhl.com/standings/{years[i]}/league")
    league.html.render(sleep=1, keep_page=True, scrolldown=8, timeout=60)
    standings = league.html.find(".responsive-datatable__pinned")
    standings_l = standings[0].text.split("\n")
    for i in range(len(standings_l)):
        for k in range(len(standings_l[i])):
            if (standings_l[i][k:k+7] == "Toronto"):
                league_standings = {"league_rank":int(f"{standings_l[i-1]}")}
                leaguestandings_l.append(league_standings)
                print(f"{league_standings} done!")
            

print(leaguestandings_l)

# ========================================PLAYOFFS=================================================================

for i in range(len(years)):
    playoffs = session.get(f"https://records.nhl.com/history/yearly-playoff-results?year={years[i]}{str(int(years[i])+1)}")
    playoffs.html.render(sleep=1, keep_page=True, scrolldown=8, timeout=60)
    results = playoffs.html.find(".table-layout-container")
    results_l = []
    for i in range(len(results)):
        results_l.append(results[i].text.split("\n"))
        
    for i in range(len(results_l)):
        for k in range(len(results_l[i])):
            if results_l[i][k] == "Toronto Maple Leafs":
                playoffs = {
                    "playoff_rnd":f"{results_l[i][0]}",
                }
                if (k % 2 == 0):
                    playoffs['playoff_w'] = int(f"{results_l[i][k+1][4]}")
                    playoffs['playoff_l'] = int(f"{results_l[i][k+1][0]}")
                else:
                    playoffs['playoff_w'] = int(f"{results_l[i][k+2][0]}")
                    playoffs['playoff_l'] = int(f"{results_l[i][k+2][4]}")
                playoffresults_l.append(playoffs)
                pprint(f"{playoffs} done!")
    
pprint(playoffresults_l)

# ========================================DATABASE FILL=============================================================
  
table = "CREATE TABLE `tml_rosters` (`year` int(4) NOT NULL, `season_wins` int(5) NOT NULL, `season_losses` int(5) NOT NULL, `season_overtime` int(5) NOT NULL, `division` varchar(250) NOT NULL, `division_ranking` int(1) NOT NULL, `league_ranking` int(1) NOT NULL, `playoff_round` varchar(250) NOT NULL, `playoff_wins` int(1) NOT NULL, `playoff_losses` int(1) NOT NULL, `roster_id` int(11) NOT NULL AUTO_INCREMENT, `team_id` varchar(250) NOT NULL, PRIMARY KEY (`roster_id`)) ENGINE=InnoDB"

dbf.create_tables(DB_NAME, table)

for i in range(len(years)):
    dbf.add_onto_mainroster(yearvalues[i]["year"], yearvalues[i]["s_w"], yearvalues[i]['s_l'], yearvalues[i]["s_ot"], yearvalues[i]["div"], yearvalues[i]["div_rank"], leaguestandings_l[i]["league_rank"], playoffresults_l[i]["playoff_rnd"], playoffresults_l[i]["playoff_w"], playoffresults_l[i]["playoff_l"], "TML")

session.close()
