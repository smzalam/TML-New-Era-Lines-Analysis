"""
1. get one player's stats (for a particular year or all years in record)
2. get two player's stats (for a particular year or all years in record)
3. get year roster (by year)
4. get team stats for year (for a particular year or all years in record) 
5. team stats vs another team
"""

from fastapi import FastAPI, Response, status
from typing import Optional
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

@app.get("/tml")
async def root():
    return {"message": "Welcome to the Toronto Maple Leafs Stats API."}

@app.get("/tml/players/{name}")
async def root():
    return {"message": "Hello World"}

@app.get("/tml/players/{name1}&{name2}")
async def root():
    return {"message": "Hello World"}

@app.get("tml/rosters/{year}")
async def root():
    return {"message": "Hello World"}

@app.get("tml/stats/{year}")
async def root():
    return {"message": "Hello World"}

@app.get("tml/records/{team}&{year}")
async def root():
    return {"message": "Hello World"}

# @app.get("players/")
# async def root():
#     return {"message": "Hello World"}