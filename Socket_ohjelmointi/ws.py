import asyncio
import datetime
import random
import websockets

async def myServ(ws):
    while True:
        now = 'e2301760' + datetime.datetime.now(datetime.timezone.utc).isoformat()
        await ws.send(now)
        await asyncio.sleep(1 + random.random() * 3)

async def main():
    async with websockets.serve(myServ, "localhost", 11111):
        await asyncio.Future()  # run forever

asyncio.run(main())