import asyncio
import websockets

# gets the data from the client, feed it to the ML and send back the result
async def processws(websocket):
    async for message in websocket:
        print('Received message')
        await websocket.send('Hi from the server')

async def main():
    async with websockets.serve(processws, "localhost", 16745):
        await asyncio.Future()

asyncio.run(main())

