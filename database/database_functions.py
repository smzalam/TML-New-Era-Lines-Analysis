import mysql.connector
from mysql.connector import errorcode
from database_connection import db, cursor

def add_onto_mainroster(year, szn_w, szn_l, szn_ot, division, div_rank, league_rank, playoff_rnd, playoff_w, playoff_l):
    sql = (f"INSERT INTO leafsroster.mainroster(year, season_wins, season_losses, season_overtime, division, division_ranking, league_ranking, playoff_round, playoff_wins, playoff_losses) VALUES ({year}, {szn_w}, {szn_l}, {szn_ot}, '{division}', {div_rank}, {league_rank}, '{playoff_rnd}', {playoff_w}, {playoff_l})")
    cursor.execute(sql)
    db.commit()
    
def add_onto_yearlyroster(year, name, role, position, roster_id):
    sql = (f"INSERT INTO leafsroster.{year}_roster(name, role, position, roster_id) VALUES ('{name}', '{role}', '{position}', {roster_id})")
    cursor.execute(sql)
    db.commit()

def add_onto_playerroster(year, j, name, gp, g, a, p, p_m, pen_min, pp_g, pp_p, sh_g, sh_p, g_w_g, ot_g, p_id):
    sql = (f"INSERT INTO leafsroster.{year}_{j}_player(name, games_played, goals, assist, points, plus_minus, powerplay_goals, powerplay_points, shorthanded_goals, shorthanded_points, game_winning_goals, overtime_goals, player_id) VALUES ('{name}', {gp}, {g}, {a}, {p}, {p_m}, {pen_min}, {pp_g}, {pp_p}, {sh_g}, {sh_p}, {g_w_g}, {ot_g}, {p_id})")
    cursor.execute(sql)
    db.commit()

def add_onto_goalieroster(year, j, name, gp, gs, w, l, ot_l, s_a, g_a, g_a_a, s, s_p, sh, p_id ):
    sql = (f"INSERT INTO leafsroster.{year}_{j}_player(name, games_played, games_saved, wins, losses, ot_losses, shots_against, goals_against, goals_against_average, saves, saves_percentage, shutouts, player_id) VALUES ('{name}', {gp}, {gs}, {w}, {l}, {ot_l}, {s_a}, {g_a}, {g_a_a}, {s}, {s_p}, {sh}, {p_id})")
    cursor.execute(sql)
    db.commit()
    
def create_tables(DB_NAME, TABLES):
    cursor.execute(f"USE {DB_NAME}")
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print(f"Creating table ({table_name})")
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno== errorcode.ER_TABLE_EXISTS_ERROR:
                print("Already exists")
            else:
                print(err.msg)

def clear_table(table_name, id, number):
    for i in range(number+2):
        sql = (f"DELETE FROM leafsroster.{table_name} WHERE {id} = {i}")
        cursor.execute(sql)
        db.commit()
        