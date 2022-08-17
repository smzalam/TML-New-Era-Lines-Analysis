import mysql.connector
from mysql.connector import errorcode
from database_fill.database_connection import db, cursor

#POST FUNCTIONS

def add_onto_mainroster(year, szn_w, szn_l, szn_ot, division, div_rank, league_rank, playoff_rnd, playoff_w, playoff_l, team):
    sql = (f"INSERT INTO leafsroster.mainroster(year, season_wins, season_losses, season_overtime, division, division_ranking, league_ranking, playoff_round, playoff_wins, playoff_losses, team_id) VALUES ({year}, {szn_w}, {szn_l}, {szn_ot}, '{division}', {div_rank}, {league_rank}, '{playoff_rnd}', {playoff_w}, {playoff_l}, '{team}')")
    cursor.execute(sql)
    db.commit()
    
def add_onto_yearlyroster(year, name, role, position, roster_id):
    sql = (f"INSERT INTO leafsroster.{year}_roster(name, role, position, roster_id) VALUES ('{name}', '{role}', '{position}', {roster_id})")
    cursor.execute(sql)
    db.commit()

def add_onto_playerroster(z, name, shoot, pos, gp, g, a, p, p_m, pen_min, points_game, evsg, pp_g, pp_p, sh_g, sh_p, g_w_g, ot_g, shot, shot_percentage, toi, faceoff, p_id):
    sql = (f"INSERT INTO leafsroster.{z}_playerstats(name, shoots, position, games_played, goals, assists, points, plus_minus, penalty_mins, points_per_game, even_strength_goals, powerplay_goals, powerplay_points, shorthanded_goals, shorthanded_points, game_winning_goals, overtime_goals, shots, shot_percentage, time_on_ice_per_game, faceoff_win_percentage, roster_id) VALUES ('{name}', '{shoot}', '{pos}', {gp}, {g}, {a}, {p}, {p_m}, {pen_min}, {points_game}, {evsg}, {pp_g}, {pp_p}, {sh_g}, {sh_p}, {g_w_g}, {ot_g}, {shot}, {shot_percentage}, '{toi}', {faceoff}, {p_id})")
    cursor.execute(sql)
    db.commit()

def add_onto_goalieroster(z, name, gp, gs, w, l, ot_l, s_a, g_a, g_a_a, s, s_p, sh, p_id):
    sql = (f"INSERT INTO leafsroster.{z}_player(name, games_played, games_saved, wins, losses, ot_losses, shots_against, goals_against, goals_against_average, saves, saves_percentage, shutouts, player_id) VALUES ('{name}', {gp}, {gs}, {w}, {l}, {ot_l}, {s_a}, {g_a}, {g_a_a}, {s}, {s_p}, {sh}, {p_id})")
    cursor.execute(sql)
    db.commit()
    
def create_tables(DB_NAME, TABLES):
    cursor.execute(f"USE {DB_NAME}")
    try:
        cursor.execute(TABLES)
    except mysql.connector.Error as err:
        if err.errno== errorcode.ER_TABLE_EXISTS_ERROR:
            print("Already exists")
        else:
            print(err.msg)
    # for table_name in TABLES:
    #     table_description = TABLES[table_name]
    #     try:
    #         print(f"Creating table ({table_name})")
    #         cursor.execute(table_description)
    #         print(f"{table_name} created!")
    #     except mysql.connector.Error as err:
    #         if err.errno== errorcode.ER_TABLE_EXISTS_ERROR:
    #             print("Already exists")
    #         else:
    #             print(err.msg)


#GET FUNCTIONS

def get_yearly_record(year: int) -> list:
    try: 
        sql = (f"SELECT * FROM mainroster WHERE year = {year}")
        cursor.execute(sql)
        query = []
        headers = ["year", "season_wins", "season_losses", "season_ot", "division", "division_ranking", "league_ranking", "playoff_round", "playoff_wins", "playoff_losses"]
        for i in cursor:
            line = {}
            counter = 0
            for k in i:
                try:
                    line[f"{headers[counter]}"] = f"{k}"
                    counter += 1
                except IndexError:
                    print("skipped")
            query.append(line)
    except mysql.connector.Error as err:
        print(err.msg)
        
    return query
              
def get_yearly_records(years: list) -> list:
    try: 
        query = []
        for i in range(len(years)):
            sql = (f"SELECT * FROM mainroster WHERE year = {years[i]}")
            cursor.execute(sql)
            headers = ["year", "season_wins", "season_losses", "season_ot", "division", "division_ranking", "league_ranking", "playoff_round", "playoff_wins", "playoff_losses"]
            for i in cursor:
                line = {}
                counter = 0
                for k in i:
                    try:
                        line[f"{headers[counter]}"] = f"{k}"
                        counter += 1
                    except IndexError:
                        print("skipped")
                query.append(line)
    except mysql.connector.Error as err:
        print(err.msg)
        
    return query

def get_yearly_roster(year: int) -> list:
    try:
        sql = (f"SELECT * FROM leafsroster.{year}_roster")
        cursor.execute(sql)
        query = []
        headers = ["name", "role", "position", "player_id"]
        for i in cursor:
            line = {}
            counter = 0
            for k in i:
                try: 
                    line[f"{headers[counter]}"] - f"{k}"
                    counter += 1
                except IndexError:
                    print("skipped")
        query.append(line)
    except mysql.connector.Error as err:
        print(err.msg)

    return cursor

def get_yearly_rosters(years: list) -> list:
    try:
        query = []
        for i in range(len(years)):
            sql = (f"SELECT * FROM leafsroster.{years}_roster")
            cursor.execute(sql)
            roster = []
            headers = ["name", "role", "position", "player_id"]
            for i in cursor:
                line = {}
                counter = 0
                for k in i:
                    try: 
                        line[f"{headers[counter]}"] - f"{k}"
                        counter += 1
                    except IndexError:
                        print("skipped")
                roster.append(line)
            query.append(roster)
    except mysql.connector.Error as err:
        print(err.msg)

    return cursor

def get_table_names(match: str) -> list:
    try:
        cursor.execute("SHOW TABLES")
        table_names = cursor.fetchall()
        table_name = []
        for i in table_names:
            for k in i:
                for l in range(len(k)):
                    if (k[l:l+7] == match):
                        table_name.append(k)
    except mysql.connector.Error as err:
        print(err.msg) 
    
    return table_name

def get_player_id(name: str) -> int:
    try:
        table_names = get_table_names("_roster")
        for i in range(len(table_names)):
            sql = (f"SELECT player_id FROM leafsroster.{table_names[i]} WHERE name = '{name}'")
            cursor.execute(sql)
            p_id = cursor.fetchall()
            if p_id != []:
                return {"player_id":f"{p_id[0][0]}"}
    except mysql.connector.Error as err:
        return "Player doesn't exist"
    
    return "Player doesn't exist"

def get_player_position(p_id: str) -> str:
    try:
        table_names = get_table_names("_roster")
        for i in range(len(table_names)):
            sql = (f"SELECT position FROM leafsroster.{table_names[i]} WHERE player_id = {p_id}")
            cursor.execute(sql)
            p_pos = cursor.fetchall()
            if p_pos != []:
                return {"position":f"{p_id[0][0]}"}
    except mysql.connector.Error as err:
        return "Player doesn't exist"
    
    return "Player doesn't exist"

def get_yearly_player_stats(p_id: int) -> list:
    try:
        sql = (f"SELECT * FROM leafsroster.{p_id}_player")
        cursor.execute(sql)
        data = cursor.fetchall()
        query = []
        pos = get_player_position(p_id)
        headers = ["name", "games_played", "goals", "assists", "points", "plus_minus", "penalty_mins", "powerplay_goals", "powerplay_points", "shorthanded_goals", "shorthanded_points", "game_winning_goals", "overtime_goals"]
        headers_g = ["name", 'games_played', "games_saved", "wins", "losses", "ot_losses", "shots_against", "goals_against", "goals_against_average", "saves", "saves_percentage", "shutouts"]
        for i in data:
            line = {}
            counter = 0
            for k in i:
                if (pos == "G"):
                    line[f"{headers_g[counter]}"] = f"{k}"
                else:
                    line[f"{headers[counter]}"] = f"{k}"
    except mysql.connector.Error as err:
        print(err.msg)

    return data

def get_year_player_stats(p_id: int, year: int) -> list:
    try:
        sql = (f"SELECT * FROM leafsroster.{p_id}_player WHERE year = {year}")
        cursor.execute(sql)
        data = cursor.fetchall()
        query = []
        pos = get_player_position(p_id)
        headers = ["name", "games_played", "goals", "assists", "points", "plus_minus", "penalty_mins", "powerplay_goals", "powerplay_points", "shorthanded_goals", "shorthanded_points", "game_winning_goals", "overtime_goals"]
        headers_g = ["name", 'games_played', "games_saved", "wins", "losses", "ot_losses", "shots_against", "goals_against", "goals_against_average", "saves", "saves_percentage", "shutouts"]
        for i in data:
            line = {}
            counter = 0
            for k in i:
                if (pos == "G"):
                    line[f"{headers_g[counter]}"] = f"{k}"
                else:
                    line[f"{headers[counter]}"] = f"{k}"   
    except mysql.connector.Error as err:
        print(err.msg)

    return data


#DELETE FUNCTIONS

def clear_table(table_name, id, number):
    for i in range(number+2):
        sql = (f"DELETE FROM leafsroster.{table_name} WHERE {id} = {i}")
        cursor.execute(sql)
        db.commit()
        