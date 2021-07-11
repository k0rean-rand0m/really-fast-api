from ws_daemon.ws_connector import WsConnector
from ws_daemon.db_connector import Db


import asyncio


async def main(port, listen_notify_from):
    print("Creating WS instance")
    await WsConnector.init(port=port, db=listen_notify_from)
    asyncio.create_task(WsConnector.run())
    if listen_notify_from:
        db = Db(user=listen_notify_from.user,
                password=WsConnector.db.password,
                database=WsConnector.db.dbname,
                host=WsConnector.db.host,
                port=WsConnector.db.port)
        asyncio.create_task(db.listen())
    print(f"Serving WS connections on {WsConnector.port}")


if __name__ == '__main__':
    main_loop = asyncio.get_event_loop()
    main_loop.create_task(main(main_loop, listen_notify_from=None))
    main_loop.run_forever()
