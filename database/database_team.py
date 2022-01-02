import mysql.connector
from database_connection import db, cursor
from requests_html import HTMLSession
import requests
from pprint import pprint
import database_functions as dbf

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
  
yearvalues_db = yearvalues
leaguestandings_db = leaguestandings_l
playoffresults_db = playoffresults_l

# def add_onto_mainroster(year, szn_w, szn_l, szn_ot, division, div_rank, league_rank, playoff_rnd, playoff_w, playoff_l):
#     sql = (f"INSERT INTO leafsroster.mainroster(year, season_wins, season_losses, season_overtime, division, division_ranking, league_ranking, playoff_round, playoff_wins, playoff_losses) VALUES ({year}, {szn_w}, {szn_l}, {szn_ot}, '{division}', {div_rank}, {league_rank}, '{playoff_rnd}', {playoff_w}, {playoff_l})")
#     cursor.execute(sql)
#     db.commit()
    
# for i in range(len(years)):
    # pprint(yearvalues[i]["year"])
    # pprint(yearvalues[i]["s_w"])
    # pprint(yearvalues[i]['s_l'])
    # pprint(yearvalues[i]["s_ot"])
    # pprint(yearvalues[i]["div"])
    # pprint(yearvalues[i]["div_rank"])
    # pprint(leaguestandings_l[i]["league_rank"])
    # print(playoffresults_l[i]["playoff_rnd"])
    # pprint(playoffresults_l[i]["playoff_w"])
    # pprint(playoffresults_l[i]["playoff_l"])
    # dbf.add_onto_mainroster(yearvalues[i]["year"], yearvalues[i]["s_w"], yearvalues[i]['s_l'], yearvalues[i]["s_ot"],yearvalues[i]["div"], yearvalues[i]["div_rank"], leaguestandings_l[i]["league_rank"], playoffresults_l[i]["playoff_rnd"], playoffresults_l[i]["playoff_w"], playoffresults_l[i]["playoff_l"])

# cursor.execute("DELETE * FROM db")
