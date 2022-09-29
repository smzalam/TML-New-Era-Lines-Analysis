# import mysql.connector
# from database_fill.database_connection import db, cursor
from requests_html import HTMLSession
import requests, json
from pprint import pprint
# import database_fill.database_functions as dbf

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
    # print(f"{i} done")

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
                # print(f"{year} done!")

print('YearValues: \n')     
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
                # print(f"{league_standings} done!")
            
print('LeagueStandings \n')
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
                # pprint(f"{playoffs} done!")
    
print('PlayoffResults \n')
pprint(playoffresults_l)

# ========================================DATABASE FILL=============================================================

with open('season_results.json', 'w') as outfile:
    json.dump(yearvalues, outfile, indent=4)

with open('leaguerank.json', 'w') as outfile:
    json.dump(leaguestandings_l, outfile, indent=4)

with open('playoff_results.json', 'w') as outfile:
    json.dump(playoffresults_l, outfile, indent=4)

session.close()
