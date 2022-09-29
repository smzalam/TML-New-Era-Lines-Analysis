from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..database_queries import *
from .. import oauth2

router = APIRouter(
    tags=['Maple Leafs']
)

@router.get("/tml")
def root():
    return {"message": "Welcome to the Toronto Maple Leafs Stats API."}

@router.post("/tml/players/", status_code=status.HTTP_200_OK) #response_model=schemas.allPlayerStatsResponse
def root(name: schemas.allPlayerStats, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    return getSkaterStats(name.player_name)

@router.post("/tml/rosters/", status_code=status.HTTP_200_OK) # , response_model=schemas.yearlyRosterResponse
def root(year: schemas.yearlyRoster, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    return getRosters(year.year)

@router.post("/tml/players/stats", status_code=status.HTTP_200_OK) # , response_model=schemas.specificSkaterStatsResponse
def root(year: int, goals: int,  lesser: bool = False, greater: bool = True, assists: int | None = None, points: int | None = None, position: str | None = None, shoots: str | None = None, games_played: int | None = None, plus_minus: int | None = None, penalty_mins: int | None = None, points_per_game: int | None = None, even_strength_goals: int | None = None, powerplay_goals: int | None = None, powerplay_points: int | None = None, shorthanded_goals: int | None = None, shorthanded_points: int | None = None, game_winning_goals: int | None = None, overtime_goals: int | None = None, shot_percentage: str | None = None, time_on_ice_per_game: str | None = None, faceoff_win_percentage: str | None = None, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)): 
    return {"message": "Hello World"}

@router.post("/tml/season/", status_code=status.HTTP_200_OK) # , response_model=schemas.seasonRecordsResponse
def root(year: schemas.seasonRecords, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    print(user)
    return getSeasonRecords(year.year)

@router.post("/tml/testsqlalchem")
def testsql(db: Session = Depends(get_db)):
    return {"status": "success"}