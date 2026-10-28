from fastapi import FastAPI, HTTPException, Path
from dataclasses import dataclass, asdict
from typing import Union
import json
import math


import json

with open("anime_characters_250.json", "r", encoding="utf-8") as f:
    anime_list = json.load(f)

list_of_anime = {
    k + 1: v
    for k, v in enumerate(anime_list)
}


@dataclass
class AnimeCharacter:
    id: int
    name: str
    anime: str
    age: int
    rank: str
    team: str
    types: list[str]
    total: int
    hp: int
    attack: int
    defense: int
    attack_special: int
    defense_special: int
    speed: int
    techniques: list[str]
    rival_id: Union[int, None] = None
    
app = FastAPI()


@app.get("/total_personnage")
def get_total_anime()->dict:
    return{"total":len(list_of_anime)}

@app.get("/personnage")
def get_all_anime() -> list[AnimeCharacter]:
    res = []

    for id in list_of_anime:
        res.append(AnimeCharacter(**list_of_anime[id]))

    return res

@app.get("/personnage/{id}")
def get_anime_by_id(id: int = Path(ge=1)) -> AnimeCharacter:
    if id not in list_of_anime:
        raise HTTPException(
            status_code=404,
            detail="Ce personnage n'existe pas"
        )

    return AnimeCharacter(**list_of_anime[id])


@app.post("/personnage")
def create_personnage(personnage:AnimeCharacter) -> AnimeCharacter:
    if personnage.id in list_of_anime:
            raise HTTPException(
            status_code=404,
            detail=f"Ce personnage {personnage.id} existe déjà "
        )
    list_of_anime[personnage.id]=asdict(personnage)
    return personnage
        
@app.put("/personnage/{id}")
def update_personnage(personnage:AnimeCharacter, id: int= Path(ge=1)) -> AnimeCharacter:
    if id not in list_of_anime:
            raise HTTPException(
            status_code=404,
            detail=f"Ce personnage {personnage.id} n'existe pas "
        )
    list_of_anime[id] =asdict[personnage]
    return personnage
@app.delete("/personnage/{id}")
def delete_personnahge(id: int = Path(ge=1)) -> AnimeCharacter:
    if id in list_of_anime:
        personnage = AnimeCharacter(**list_of_anime[id])
        del list_of_anime[id]
        raise HTTPException( 
            detail=f"Ce personnage {personnage.id} n'existe pas "
        )
    return personnage