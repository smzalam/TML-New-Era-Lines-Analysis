from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class allPlayerStats(BaseModel):
    player_name: list[str]
    year: Optional[int]

class yearlyRoster(BaseModel):
    year: list[int]
    position: Optional[str]
    goals: Optional[int]
    assists: Optional[int] 
    save_percentage: Optional[int]

class seasonRecords(BaseModel):
    year: list[int]
    
class specificSkaterStats(BaseModel):
    year: list[int] 
    lesser: bool = False
    greater: bool = True
    goals: Optional[int]
    assists: Optional[int]
    points: Optional[int]
    position: Optional[str]
    shoots: Optional[str]
    games_played: Optional[int]
    plus_minus: Optional[int]
    penalty_mins: Optional[int]
    points_per_game: Optional[int]
    even_strength_goals: Optional[int]
    powerplay_goals: Optional[int]
    powerplay_points: Optional[int]
    shorthanded_goals: Optional[int]
    shorthanded_points: Optional[int]
    game_winning_goals: Optional[int]
    overtime_goals: Optional[int]
    shot_percentage: Optional[str]
    time_on_ice_per_game: Optional[str]
    faceoff_win_percentage: Optional[str]


class allPlayerStatsResponse(allPlayerStats):
    position: str 
    shoots: str
    games_played: int 
    goals: int 
    assists: int
    points: int 
    plus_minus: int 
    penalty_mins: int 
    points_per_game: int 
    even_strength_goals: int 
    powerplay_goals: int 
    powerplay_points: int 
    shorthanded_goals: int 
    shorthanded_points: int 
    game_winning_goals: int 
    overtime_goals: int 
    shot_percentage: str
    time_on_ice_per_game: str 
    faceoff_win_percentage: str

class specificSkaterStatsResponse(BaseModel):
    year: int 
    name: list[str]

class seasonRecordsResponse(BaseModel):
    year: int
    season_wins: int
    season_losses: int
    season_overtim: int
    division: str
    division_ranking: str  
    league_ranking: int
    playoff_round: str
    playoff_wins: int
    playoff_losses: int

class yearlyRosterResponse(BaseModel):
    year: int
    name: list[str]
    position: list[str]

class UserCreate(BaseModel):
    email: EmailStr 
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr 
    created_at: datetime 

    class Config:
        orm_mode = True 

class UserLogin(BaseModel):
    email: EmailStr 
    password: str

class Token(BaseModel):
    access_token: str 
    token_type: str 

class TokenData(BaseModel):
    id: Optional[str]
