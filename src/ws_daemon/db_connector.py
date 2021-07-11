import asyncpg
from ws_daemon.ws_connector import WsConnector


class Db:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    async def connect(self):
        print("PGSql's connecting...")
        if not self.connection:
            self.connection: asyncpg.Connection = await asyncpg.connect(host=self.host,
                                                                        port=self.port,
                                                                        user=self.user,
                                                                        password=self.password,
                                                                        database=self.database)

    async def listen(self):
        await self.connect()
        notify_channel = "alert"
        await self.connection.add_listener(notify_channel, WsConnector.send)
        print(f"Listening for \"{notify_channel}\" notify channel")
