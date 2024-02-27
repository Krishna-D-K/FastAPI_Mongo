from fastapi import APIRouter, Request, Body
from models.playerModels import Player
from bson import ObjectId

router = APIRouter(prefix="", tags=['Players'])

@router.get("/")
async def getPlayers(request: Request)->list[Player]:
    db = request.app.players
    response = list(db.find({}))
    for item in response:
        item["_id"] = str(item["_id"])
    return response

@router.post("/")
async def addPlayer(request: Request, player: Player = Body(...)):
    db = request.app.players
    response = db.insert_one(player.model_dump())
    return {"id": str(response.inserted_id), "acknowledged": response.acknowledged}

@router.delete("/{id}")
async def deletePlayer(request: Request, id):
    _id = ObjectId(id)
    db = request.app.players
    response = db.delete_one({"_id": _id})
    return {"deleted_count": response.deleted_count, "acknowledged": response.acknowledged}

@router.put("/{id}")
async def updatePlayer(request: Request, id, player: Player = Body(...)):
    _id = ObjectId(id)
    db = request.app.players
    response = db.update_one({"_id": _id}, {"$set": player.model_dump()})
    return {"updated_count": response.modified_count, "acknowledged": response.acknowledged}