import mysql.connector
from database_fill.database_connection import db, cursor
from requests_html import HTMLSession
from pprint import pprint
import database_fill.database_functions as dbf

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

    table = f"CREATE TABLE `{years[year]}_playerstats` (`name` varchar(250) NOT NULL, `shoots` varchar(250) NOT NULL, `position` varchar(250) NOT NULL, `games_played` int(5) NOT NULL, `goals` int(5) NOT NULL, `assists` int(5) NOT NULL, `points` int(5) NOT NULL, `plus_minus` int(5) NOT NULL, `penalty_mins` int(5) NOT NULL, `points_per_game` decimal(8, 3) NOT NULL, `even_strength_goals` int(5) NOT NULL, `powerplay_goals` int(5) NOT NULL, `powerplay_points` int(5) NOT NULL, `shorthanded_goals` int(5) NOT NULL, `shorthanded_points` int(5) NOT NULL, `game_winning_goals` int(5) NOT NULL, `overtime_goals` int(5) NOT NULL, `shots` int(5) NOT NULL, `shot_percentage` decimal(8, 3) NOT NULL, `time_on_ice_per_game` varchar(250) NOT NULL, `faceoff_win_percentage` decimal(4,1) NOT NULL, `roster_id` int(5) NOT NULL, PRIMARY KEY (`name`)) ENGINE=InnoDB"
    
    dbf.create_tables(DB_NAME, table)
    
    p_id = int(years[year]) - 2015
    
    for i in range(len(playerstats)):
        dbf.add_onto_playerroster(years[year], playerstats[i]['name'], playerstats[i]['shoots'], playerstats[i]['position'], playerstats[i]['games_played'], playerstats[i]['goals'], playerstats[i]['assists'], playerstats[i]['points'], playerstats[i]['plus_minus'], playerstats[i]['penalty_mins'], playerstats[i]['points_per_game'], playerstats[i]['evs_goals'], playerstats[i]['pp_goals'], playerstats[i]['pp_points'], playerstats[i]['sh_goals'], playerstats[i]['sh_points'], playerstats[i]['gw_goals'], playerstats[i]['ot_goals'], playerstats[i]['shots'], playerstats[i]['shot_percentage'], playerstats[i]['toi_per_game'], playerstats[i]['faceoff_win_percentage'], p_id)
        
        pprint(f"{years[year]}_{i} done!")