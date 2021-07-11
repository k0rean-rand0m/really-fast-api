import time
import json


class RequestWrappers:
    @staticmethod
    def log(func):
        async def wrapper(method, payload):
            started = time.time()
            resp = await func(method, payload)
            log = json.dumps(
                {"timestamp": time.time(), "method": method, "payload": payload,
                 "response": resp, "request_time": (time.time() - started) * 1000.0},
                ensure_ascii=False
            )
            print(log)
            return resp

        return wrapper
