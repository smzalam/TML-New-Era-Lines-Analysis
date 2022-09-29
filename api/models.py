from __future__ import division
from sqlite3 import Timestamp
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP, text
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class SeasonResults(Base):
    __tablename__ = "seasons"

    year = Column(Integer, nullable=False, primary_key=True)
    season_wins = Column(Integer, nullable=False)
    season_losses = Column(Integer, nullable=False)
    season_overtime = Column(Integer, nullable=False)
    division = Column(String, nullable=False)
    division_ranking = Column(Integer, nullable=False)  
    league_ranking = Column(Integer, nullable=False)
    playoff_round = Column(String, nullable=False)
    playoff_wins = Column(Integer, nullable=False)
    playoff_losses = Column(Integer, nullable=False)

class MainRoster(Base):
    __tablename__ = "rosters"

    id = Column(Integer, primary_key=True, nullable=False)
    roster_id = Column(Integer, nullable=False)
    year = Column(Integer, ForeignKey("seasons.year", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    position = Column(String, nullable=False)

class SkaterStats(Base):
    __tablename__ = "skater_stats"

    roster_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    position = Column(String, nullable=False)
    shoots = Column(String, nullable=False)
    games_played = Column(Integer, nullable=False)
    goals = Column(Integer, nullable=False)
    assists = Column(Integer, nullable=False)
    points = Column(Integer, nullable=False)
    plus_minus = Column(Integer, nullable=False)
    penalty_mins = Column(Integer, nullable=False)
    points_per_game = Column(Integer, nullable=False)
    even_strength_goals = Column(Integer, nullable=False)
    powerplay_goals = Column(Integer, nullable=False)
    powerplay_points = Column(Integer, nullable=False)
    shorthanded_goals = Column(Integer, nullable=False)
    shorthanded_points = Column(Integer, nullable=False)
    game_winning_goals = Column(Integer, nullable=False)
    overtime_goals = Column(Integer, nullable=False)
    shot_percentage = Column(String, nullable=False)
    time_on_ice_per_game = Column(String, nullable=False)
    faceoff_win_percentage = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)

class GoalieStats(Base):
    __tablename__ = "goalie_stats"

    roster_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    games_played = Column(Integer, nullable=False)
    games_saved = Column(Integer, nullable=False)
    wins = Column(Integer, nullable=False)
    losses = Column(Integer, nullable=False)
    ot_losses = Column(Integer, nullable=False)
    shots_against = Column(Integer, nullable=False)
    goals_against = Column(Integer, nullable=False)
    goals_against_average = Column(Integer, nullable=False)
    saves = Column(Integer, nullable=False)
    saves_percentage = Column(String, nullable=False)
    shutouts = Column(Integer, nullable=False)
    id = Column(Integer, primary_key=True,  nullable=False)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True,  nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))