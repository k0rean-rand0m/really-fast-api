from db import Db, DbLocal, DbDev, DbMaster


async def get_db(stage: bool = False, local: bool = False) -> Db:
    if local:
        return await DbLocal().init()
    elif stage:
        return await DbDev().init()
    else:
        return await DbMaster().init()
