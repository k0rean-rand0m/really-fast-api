import asyncpg
from abc import ABC, abstractmethod
import json
from config import Config


async def set_json_codec(connection):
    await connection.set_type_codec(
        'json',
        encoder=json.dumps,
        decoder=json.loads,
        schema='pg_catalog'
    )


class Db(ABC):
    _pool = None

    @abstractmethod
    async def init(self):
        """Create database configuration, ensure one entity"""

    @abstractmethod
    async def connect(self):
        """Connect to the specific database"""

    async def fetchall(self, query: str, *args) -> list:
        async with self._pool.acquire() as connection:
            return [dict(record) for record in await connection.fetch(query, *args, timeout=10000)]

    async def fetchval(self, query: str, args: tuple = ()):
        async with self._pool.acquire() as connection:
            return await connection.fetchval(query, *args)

    async def execute(self, query: str):
        async with self._pool.acquire() as connection:
            await connection.execute(query, timeout=10000)

    async def execute_function(self, function: str, params: dict = {}):
        params = json.dumps(params, ensure_ascii=False)
        async with self._pool.acquire() as connection:
            async with connection.transaction():
                try:
                    resp = dict(await connection.fetchrow("SELECT * FROM {} ($1::JSONB);".format(function),
                                                          params))[function]

                    return json.loads(resp)
                except Exception as database_exception:
                    print(database_exception)


class DbMaster(Db):
    entity = None

    async def init(self):
        if DbMaster.entity:
            return DbMaster.entity
        else:
            await self.connect()
            DbMaster.entity = self
            return self

    async def connect(self):
        self._pool = await asyncpg.create_pool(user=Config.DbMaster.user,
                                               password=Config.DbMaster.password,
                                               database=Config.DbMaster.dbname,
                                               host=Config.DbMaster.host,
                                               port=Config.DbMaster.port,
                                               min_size=2, max_size=4)


class DbDev(Db):
    entity = None

    async def init(self):
        if DbDev.entity:
            return DbDev.entity
        else:
            await self.connect()
            DbDev.entity = self
            return self

    async def connect(self):
        self._pool = await asyncpg.create_pool(user=Config.DbDev.user,
                                               password=Config.DbDev.password,
                                               database=Config.DbDev.dbname,
                                               host=Config.DbDev.host,
                                               port=Config.DbDev.port,
                                               min_size=2, max_size=4)


class DbLocal(Db):
    entity = None

    async def init(self):
        if DbLocal.entity:
            return DbLocal.entity
        else:
            await self.connect()
            DbLocal.entity = self
            return self

    async def connect(self):
        self._pool = await asyncpg.create_pool(user=Config.DbLocal.user,
                                               password=Config.DbLocal.password,
                                               database=Config.DbLocal.dbname,
                                               host=Config.DbLocal.host,
                                               port=Config.DbLocal.port,
                                               min_size=2, max_size=4)
