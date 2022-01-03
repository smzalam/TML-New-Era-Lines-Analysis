import mysql.connector
from mysql.connector import errorcode
from database_connection import db, cursor
import database_functions as dbf
from yearly_team_records import yearvalues_db, leaguestandings_db, playoffresults_db
from yearly_roster import yearlyrosters_db, rostercount_db
from yearly_player_stats import rosterstats_db
 
DB_NAME = 'leafsroster'

# cursor.execute(f"DROP DATABASE {DB_NAME}")

TABLES = {}

TABLES['mainroster'] = (
    "CREATE TABLE `mainroster` ("
    " `year` int(4) NOT NULL,"
    " `season_wins` int(5) NOT NULL,"
    " `season_losses` int(5) NOT NULL,"
    " `season_overtime` int(5) NOT NULL,"
    " `division` varchar(250) NOT NULL,"
    " `division_ranking` int(1) NOT NULL,"
    " `league_ranking` int(1) NOT NULL,"
    " `playoff_round` varchar(250) NOT NULL,"
    " `playoff_wins` int(1) NOT NULL,"
    " `playoff_losses` int(1) NOT NULL,"
    " `roster_id` int(11) NOT NULL AUTO_INCREMENT,"
    " PRIMARY KEY (`roster_id`)"
    ") ENGINE=InnoDB"
)

# TABLES['yearlyroster'] = (
#     "CREATE TABLE `yearlyroster` ("
#     " `name` varchar(250) NOT NULL,"
#     " `role` varchar(250) NOT NULL,"
#     " `position` varchar(250) NOT NULL,"
#     " `player_id` int(11) NOT NULL AUTO_INCREMENT,"
#     " `roster_id` int(11),"
#     " PRIMARY KEY (`player_id`),"
#     " FOREIGN KEY (`roster_id`) REFERENCES mainroster(`roster_id`)"
#     ") ENGINE=InnoDB"
# )

# TABLES['playerstats'] = (
#     "CREATE TABLE `playerstats` ("
#     " `name` varchar(250) NOT NULL,"
#     " `games_played` int(5) NOT NULL,"
#     " `goals` int(5) NOT NULL,"
#     " `assist` int(5) NOT NULL,"
#     " `points` int(5) NOT NULL,"  
#     " `plus_minus` int(5) NOT NULL,"
#     " `penalty_mins` int(5) NOT NULL,"
#     " `powerplay_goals` int(5) NOT NULL,"
#     " `powerplay_points` int(5) NOT NULL,"
#     " `shorthanded_goals` int(5) NOT NULL,"
#     " `shorthanded_points` int(5) NOT NULL,"
#     " `game_winning_goals` int(5) NOT NULL,"
#     " `overtime_goals` int(5) NOT NULL,"
#     " PRIMARY KEY"
#     ") ENGINE=InnoDB"
# )

years = ["2016", "2017", "2018", "2019", "2020", "2021"]

for i in range(len(years)):
    TABLES[f"{years[i]}_roster"] = (
        f"CREATE TABLE `{years[i]}_roster` ("
        " `name` varchar(250) NOT NULL,"
        " `role` varchar(250) NOT NULL,"
        " `position` varchar(250) NOT NULL,"
        " `player_id` int(11) NOT NULL AUTO_INCREMENT,"
        " `roster_id` int(11) NOT NULL,"
        " PRIMARY KEY (`player_id`),"
        " FOREIGN KEY (`roster_id`) REFERENCES mainroster(`roster_id`)"
        ") ENGINE=InnoDB"
    )
    dbf.create_tables(DB_NAME, TABLES)
    dbf.add_onto_mainroster(yearvalues_db[i]["year"], yearvalues_db[i]["s_w"], yearvalues_db[i]['s_l'], yearvalues_db[i]["s_ot"],yearvalues_db[i]["div"], yearvalues_db[i]["div_rank"], leaguestandings_db[i]["league_rank"], playoffresults_db[i]["playoff_rnd"], playoffresults_db[i]["playoff_w"], playoffresults_db[i]["playoff_l"])
    
for i in range(len(years)):
    for k in range(len(yearlyrosters_db[i])):
        for j in range(rostercount_db[i]):
            try:
                if (yearlyrosters_db[i][k][f"{j}"] == 'Player'):
                    continue
                print(i)
                print(i+1)
                dbf.add_onto_yearlyroster(years[i], yearlyrosters_db[i][k][f"{j}"], yearlyrosters_db[i][k][f"{j}_role"], yearlyrosters_db[i][k][f"{j}_pos"], i+1)
                print("done!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!111")
            except KeyError:
                continue
            if (yearlyrosters_db[i][k][f"{j}_pos"] == "G"):
                TABLES[f"{years[i]}_{j}_player"] = (
                    f"CREATE TABLE `{years[i]}_{j}_player` ("
                        " `name` varchar(250) NOT NULL,"
                        " `games_played` int(5) NOT NULL,"
                        " `games_saved` int(5) NOT NULL,"
                        " `wins` int(5) NOT NULL,"
                        " `losses` int(5) NOT NULL,"  
                        " `ot_losses` int(5) NOT NULL,"
                        " `shots_against` int(5) NOT NULL,"
                        " `goals_against` int(5) NOT NULL,"
                        " `goals_against_average` int(5) NOT NULL,"
                        " `saves` int(5) NOT NULL,"
                        " `saves_percentage` int(5) NOT NULL,"
                        " `shutouts` int(5) NOT NULL,"
                        " `player_id` int(11) NOT NULL,"
                        " PRIMARY KEY (`player_id`),"
                        f" FOREIGN KEY (`player_id`) REFERENCES {years[i]}_roster(`player_id`)"
                        ") ENGINE=InnoDB"
                )
                dbf.create_tables(DB_NAME, TABLES)
                for z in range(len(rosterstats_db[i][j])):
                    dbf.add_onto_goalieroster(years[i], j, yearlyrosters_db[i][k][f"{j}"], rosterstats_db[i][j][z]["games_played"], rosterstats_db[i][j][z]["games_saved"], rosterstats_db[i][j][z]["wins"], rosterstats_db[i][j][z]["losses"], rosterstats_db[i][j][z]["ot_losses"], rosterstats_db[i][j][z]["shots_against"], rosterstats_db[i][j][z]["goals_against"], rosterstats_db[i][j][z]["gaa"], rosterstats_db[i][j][z]["saves"], rosterstats_db[i][j][z]["saves_%"], rosterstats_db[i][j][z]["shutouts"], j+1)
            else:
                TABLES[f"{years[i]}_{j}_player"] = (
                        f"CREATE TABLE `{years[i]}_{j}_player` ("
                        " `name` varchar(250) NOT NULL,"
                        " `games_played` int(5) NOT NULL,"
                        " `goals` int(5) NOT NULL,"
                        " `assist` int(5) NOT NULL,"
                        " `points` int(5) NOT NULL,"  
                        " `plus_minus` int(5) NOT NULL,"
                        " `penalty_mins` int(5) NOT NULL,"
                        " `powerplay_goals` int(5) NOT NULL,"
                        " `powerplay_points` int(5) NOT NULL,"
                        " `shorthanded_goals` int(5) NOT NULL,"
                        " `shorthanded_points` int(5) NOT NULL,"
                        " `game_winning_goals` int(5) NOT NULL,"
                        " `overtime_goals` int(5) NOT NULL,"
                        " `player_id` int(11) NOT NULL,"
                        " PRIMARY KEY (`player_id`),"
                        f" FOREIGN KEY (`player_id`) REFERENCES {years[i]}_roster(`player_id`)"
                        ") ENGINE=InnoDB"
                    )
                dbf.create_tables(DB_NAME, TABLES)
                for z in range(len(rosterstats_db[i][j])):
                    dbf.add_onto_playerroster(years[i], j, yearlyrosters_db[i][k][f"{j}"], rosterstats_db[i][j][z]["games_played"], rosterstats_db[i][j][z]["goals"], rosterstats_db[i][j][z]["assists"], rosterstats_db[i][j][z]["points"], rosterstats_db[i][j][z]["plus_minus"], rosterstats_db[i][j][z]["penalty_mins"], rosterstats_db[i][j][z]["pp_goals"], rosterstats_db[i][j][z]["pp_points"], rosterstats_db[i][j][z]["sh_goals"], rosterstats_db[i][j][z]["sh_points"], rosterstats_db[i][j][z]["gw_goals"],rosterstats_db[i][j][z]["ot_goals"], j+1)
            