import websockets as ws
import asyncio
import json


class WsConnector:
    port = 9090
    loop = asyncio.get_event_loop()
    sessions = []
    db = None
    
    @classmethod
    async def init(cls, port, db):
        cls.db = await db().init()
        cls.port = port
    
    @classmethod
    async def run(cls):
        await ws.serve(cls._ws_server, "0.0.0.0", cls.port, ping_interval=10)

    @classmethod
    async def _ws_server(cls, websocket: ws.WebSocketServerProtocol):
        if websocket not in cls.sessions:
            cls.sessions.append(websocket)
            await websocket.send(json.dumps({"type": "welcome_message",
                                             "details": "You are subscribed to all topics!"}))
        else:
            await websocket.send(json.dumps({"type": "pong",
                                             "details": {
                                                 "sessions": len(cls.sessions)
                                             }}))

    @classmethod
    def send(cls, connection, pid, channel, payload):
        asyncio.create_task(cls.ws_send(payload))

    @classmethod
    async def ws_send(cls, message):
        if len(cls.sessions) > 0:
            for i in reversed(range(len(cls.sessions))):
                if cls.sessions[i].closed:
                    del cls.sessions[i]
                else:
                    await cls.sessions[i].send(message)
