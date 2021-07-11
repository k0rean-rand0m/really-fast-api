from fastapi import APIRouter, Depends
from dependencies import get_db
import basic
from ws_daemon.ws_connector import WsConnector
from pydantic import BaseModel
import json

router = APIRouter()


class Model(BaseModel):
    _table = 'model'
    id: int
    name: str


@router.post("/model", tags=["Models"], name="Create a new model")
async def create_event(body: Model,
                       db=Depends(get_db)):
    # An example of easy to use basic creation method
    async with basic.create(body, db) as model:
        # WS notify example
        await WsConnector.ws_send(json.dumps({
            "type": "new_model",
            "details": {
                "model_id": model["id"]
            }
        }))
        return model


@router.put("/model", tags=["Models"], name="Get the model")
async def get_event(params: Model = Depends(),
                    db=Depends(get_db)):
    # An example of easy to use basic update method
    async with basic.update(params, db) as model:
        return model


@router.get("/model_process", tags=["Models"], name="Process the model using PG procedure")
async def get_event(params: Model = Depends(),
                    db=Depends(get_db)):
    # An example to redirect input to PG procedure
    async with basic.pass_to("procedure_template", db, params) as model:
        return model


@router.delete("/model", tags=["Models"], name="Delete the model")
async def get_event(params: Model = Depends(),
                    db=Depends(get_db)):
    # An example of easy to use basic delete method
    async with basic.delete(params, db) as model:
        return model


@router.put("/model", tags=["Models"], name="Get the model")
async def get_event(params: Model = Depends(),
                    db=Depends(get_db)):
    # An example of easy to use basic get method
    async with basic.get(params, db) as model:
        return model
