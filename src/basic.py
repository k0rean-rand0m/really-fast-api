from contextlib import asynccontextmanager
from fastapi import HTTPException
from db import Db


@asynccontextmanager
async def get(model, db: Db):
    cond = " AND ".join([f"{k}={v}" if type(v) in [int, float] else f"{k}='{v}'" for k, v in model.__dict__.items() if v])
    if cond:
        query = f"select * from {model._table} where {cond};"
    else:
        query = f"select * from {model._table};"
    resp = await db.fetchall(query)
    yield {"count": len(resp), "items": resp} if resp else {"count": 0, "items": []}


@asynccontextmanager
async def delete(model, db: Db):
    if model.id:
        query = f"delete from {model._table} where id = {model.id};"
        await db.execute(query)
        yield {"id": model.id}


@asynccontextmanager
async def update(model, db: Db):
    try:
        if model.id:
            upd = " ".join([f"{k}={v}" for k, v in model.__dict__.items() if k != "id" and v is not None])
            upd = ""
            for k, v in model.__dict__.items():
                if k != "id" and v is not None:
                    if type(v) in [int, float]:
                        upd += f" {k}={v}"
                    else:
                        upd += f" {k}='{v}'"
            upd = upd[1:]
            if upd:
                query = f"update {model._table} set {upd} where id={model.id} returning {model.id};"
                yield (await db.fetchall(query))[0]
            else:
                raise HTTPException(status_code=400, detail="Pass model's params to update!")
        else:
            raise HTTPException(status_code=400, detail="Pass id to update model!")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500)


@asynccontextmanager
async def create(model, db: Db):
    try:
        cols = ""
        vals = ""
        for k, v in model.__dict__.items():
            if v is not None:
                cols += f", {k}"
                if type(v) in [int, float]:
                    vals += f", {v}"
                else:
                    vals += f", '{v}'"
        cols = cols[2:]
        vals = vals[2:]

        if model._table:
            query = f"insert into {model._table} ({cols}) values ({vals}) returning id, {cols};"
            yield (await db.fetchall(query))[0]
        else:
            raise HTTPException(status_code=400, detail="You can't create an instance of this type!")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500)


@asynccontextmanager
async def pass_to(function, db: Db, model):
    if function:
        try:
            yield await db.execute_function(function, dict(model.__dict__.items()))
        except Exception as e:
            raise HTTPException(status_code=500)
