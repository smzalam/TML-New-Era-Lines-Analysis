import mysql.connector
from database_connection import db, cursor
from requests_html import HTMLSession
import requests
from pprint import pprint


# variables
years = ["2016", "2017", "2018", "2019", "2020", "2021"]
yearlyrosters_l = []
rostercount_l = []
playerslinks_l = []

# starting new HTMLSession()
session = HTMLSession()

# ========================================YEARLY ROSTER=================================================================

for i in range(len(years)):
    roster = session.get(f"https://www.nhl.com/mapleleafs/roster/{years[i]}")

    # for the player names and roles
    roster_al = roster.html.find(".split-table-td.pinned")    
    players_pos = roster.html.find(".position-col.fixed-width-font")
    players_f_d_g_l = []
    players_forwards = {}
    players_defense = {}
    players_goalies = {}
    counter = 0
    for i in range(len(roster_al)):
        players_f_d_g_l.append(roster_al[i].text.split("\n"))
    for k in range(len(players_f_d_g_l[0])):
        players_forwards[f"{counter}"] = f"{players_f_d_g_l[0][k]}"
        players_forwards[f"{counter}_role"] = "Forward"
        players_forwards[f"{counter}_pos"] = f"{players_pos[k].text}"
        counter += 1
    for k in range(len(players_f_d_g_l[1])):
        players_defense[f"{counter}"] = f"{players_f_d_g_l[1][k]}"
        players_defense[f"{counter}_role"] = "Defenseman"
        players_defense[f"{counter}_pos"] = "D"
        counter += 1
    for k in range(len(players_f_d_g_l[2])):
        players_goalies[f"{counter}"] = f"{players_f_d_g_l[2][k]}"
        players_goalies[f"{counter}_role"] = "Goalie"
        players_goalies[f"{counter}_pos"] = "G"
        counter += 1
    players_l = [players_forwards, players_defense, players_goalies]
    yearlyrosters_l.append(players_l)
    rostercount_l.append(counter)

    # for the links to the players
    players_link = roster.html.find(".name-col")
    players_a = []
    for i in range(len(players_link)):
        players_a.append(players_link[i].find("a"))
    playerslinks_l.append(players_a)

    
# pprint(f"{players_l}, {players_a} done!")

# pprint(yearlyrosters_l)

# ========================================DATABASE FUNCTIONS=============================================================

yearlyrosters_db = yearlyrosters_l
rostercount_db = rostercount_l
playerslinks_db = playerslinks_l

# dbf.clear_table(22, 'player_id')
# for i in range(len(yearlyrosters_l)):
#     for k in range(len(yearlyrosters_l[i])):
#         for j in range(rostercount_l[i]):
#             try:@
#                 if (yearlyrosters_l[i][k][f"{j}"] == 'Player'):
#                     continue
#                 dbf.add_onto_yearlyroster(yearlyrosters_l[i][k][f"{j}"], yearlyrosters_l[i][k][f"{j}_role"], yearlyrosters_l[i][k][f"{j}_pos"])
#             except KeyError:
#                 continue

session.close()