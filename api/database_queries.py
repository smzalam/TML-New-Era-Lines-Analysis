from sqlalchemy.orm import Session
from sqlalchemy import select, and_, insert
from .models import *
from pprint import pprint
import json
from datetime import datetime
from .database import engine, get_db, SessionLocal

db = SessionLocal()

def getSkaterStats(name: list[str]):
    values = {}
    for i in range(len(name)):
        stmt = select(SkaterStats).where(SkaterStats.name == name[i])
        result = db.execute(stmt)
        player_list = []
        for row in result.scalars():
            row_dict = row.__dict__
            for k in list(row_dict.keys()):
                if k[0] == '_':
                    del row_dict[k]
            player_list.append(row_dict)
        player_dict = {name[i]: player_list}
        values.update(player_dict)

    return values

def getRosters(year: list[int]):
    values = {}
    for i in range(len(year)):
        stmt = select(MainRoster).where(MainRoster.year == year[i])
        result = db.execute(stmt)
        roster_list = []
        for row in result.scalars():
            row_dict = row.__dict__
            for k in list(row_dict.keys()):
                if k[0] == '_':
                    del row_dict[k]
            roster_list.append(row_dict)
        roster_dict = {year[i]: roster_list}
        values.update(roster_dict)
    
    return values

def getSeasonRecords(year: list[int]):
    values = {}
    for i in range(len(year)):
        stmt = select(SeasonResults).where(SeasonResults.year == year[i])
        result = db.execute(stmt)
        roster_list = []
        for row in result.scalars():
            row_dict = row.__dict__
            for k in list(row_dict.keys()):
                if k[0] == '_':
                    del row_dict[k]
            roster_list.append(row_dict)
        roster_dict = {year[i]: roster_list}
        values.update(roster_dict)
    
    return values

def getSpecificSkaterStats(year: int, goals: int,  lesser: bool = False, greater: bool = True, assists: int | None = None, points: int | None = None, position: str | None = None, shoots: str | None = None, games_played: int | None = None, plus_minus: int | None = None, penalty_mins: int | None = None, points_per_game: int | None = None, even_strength_goals: int | None = None, powerplay_goals: int | None = None, powerplay_points: int | None = None, shorthanded_goals: int | None = None, shorthanded_points: int | None = None, game_winning_goals: int | None = None, overtime_goals: int | None = None, shot_percentage: str | None = None, time_on_ice_per_game: str | None = None, faceoff_win_percentage: str | None = None):
    values = {}
    operator = "<" if lesser == True else ">"
    for i in range(len(year)):
        stmt = select(SkaterStats).where(and_(SkaterStats.year == year[i]), int(SkaterStats.time_on_ice_per_game) > int() )
        result = db.execute(stmt)
        roster_list = []
        for row in result.scalars():
            row_dict = row.__dict__
            for k in list(row_dict.keys()):
                if k[0] == '_':
                    del row_dict[k]
            roster_list.append(row_dict)
        roster_dict = {year[i]: roster_list}
        values.update(roster_dict)
    
    return values

def createNewUser(user: dict):
    new_user = User(**user)
    db.add(new_user)
    db.commit() 
    db.refresh(new_user)

    return "Successfully created new user!"


# pprint(getSkaterStats(['Auston Matthews', 'William Nylander', 'John Tavares']))
# pprint(getRosters([2016, 2017, 2018]))
# pprint(getSeasonRecords([2016, 2017, 2018]))
   


