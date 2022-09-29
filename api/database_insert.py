from sqlalchemy.orm import Session
import models, json
from datetime import datetime
from database import engine, get_db, SessionLocal

db = SessionLocal()

years = []
for i in range(datetime.now().year-2016+1):
    years.append(2016+i)
print(years)

for i in range(datetime.now().year-2016):
    new_dict = {}
    with open('api/JSON/season_results.json') as outfile:
        data = json.load(outfile)
        new_dict.update([('year', data[i]['year']), ('season_wins', data[i]['s_w']), ('season_losses', data[i]['s_l']), ('season_overtime', data[i]['s_ot']), ('division', data[i]['div']), ('division_ranking', data[i]['div_rank'])])
    with open('api/JSON/leaguerank.json') as outfile:
        data = json.load(outfile)
        new_dict.update({'league_ranking':data[i]['league_rank']})
    with open('api/JSON/playoff_results.json') as outfile:
        data = json.load(outfile)
        new_dict.update([('playoff_round', data[i]['playoff_rnd']), ('playoff_wins', data[i]['playoff_w']), ('playoff_losses', data[i]['playoff_l'])])
        season_new = models.SeasonResults(**new_dict)
        db.add(season_new)
        db.commit()
        db.refresh(season_new)

for i in years:
    if f'{i+1}' == f'{datetime.now().year+1}':
        break
    with open(f'api/JSON/{i}{i+1}_playerstats.json') as outfile:
        data = json.load(outfile)   
        for j in range(len(data)):
            roster_id = i-2015
            roster_new = models.MainRoster(roster_id=roster_id, year=i, name=data[j]['name'], position=data[j]['position'])
            skater_stats = models.SkaterStats(roster_id=roster_id, name=data[j]['name'], position=data[j]['position'], shoots=data[j]['shoots'], games_played=data[j]['games_played'], goals=data[j]['goals'], assists=data[j]['assists'], points=data[j]['points'], plus_minus=data[j]['plus_minus'], penalty_mins=data[j]['penalty_mins'], points_per_game=data[j]['points_per_game'], even_strength_goals=data[j]['evs_goals'], powerplay_goals=data[j]['pp_goals'], powerplay_points=data[j]['pp_points'], shorthanded_goals=data[j]['sh_goals'], shorthanded_points=data[j]['sh_points'], game_winning_goals=data[j]['gw_goals'], overtime_goals=data[j]['ot_goals'], shot_percentage=data[j]['shot_percentage'], time_on_ice_per_game=data[j]['toi_per_game'], faceoff_win_percentage=data[j]['faceoff_win_percentage'])
            db.add(roster_new)
            db.add(skater_stats)
            db.commit()
            db.refresh(roster_new)
    with open(f'api/JSON/{i}{i+1}_goaliestats.json') as outfile:
        data = json.load(outfile)   
        for j in range(len(data)):
            roster_id = i-2015
            roster_new = models.MainRoster(roster_id=roster_id, year=i, name=data[j]['name'], position=data[j]['position'])
            goalie_stats = models.GoalieStats(roster_id=roster_id, name=data[j]['name'], games_played=data[j]['games_played'], games_saved=data[j]['games_saved'], wins=data[j]['wins'], losses=data[j]['losses'], ot_losses=data[j]['ot_losses'], shots_against=data[j]['shots_against'], goals_against=data[j]['goals_against'], goals_against_average=data[j]['goals_against_average'], saves=data[j]['saves'], saves_percentage=data[j]['saves_percentage'], shutouts=data[j]['shutouts'])
            db.add(roster_new)
            db.add(goalie_stats)
            db.commit()
            db.refresh(roster_new)

# for instance in db.query(models.MainRoster):
#     print(instance.roster_id, instance.name, instance.year, instance.position)
