import asyncio
import websockets
import json

# gets the data from the client, feed it to the ML and send back the result
# sample frame:
# {
#     "info": {
#         "format": "NV12",
#         "width": 1280,
#         "height": 720,
#         "origWidth": 1280,
#         "origHeight": 720,
#         "stride": 1280,
#         "timestamp": 38726963153613230,
#         "mirror": true,
#         "padding": {
#             "leftOffset": 0,
#             "rightOffset": 0,
#             "topOffset": 0,
#             "bottomOffset": 0
#         },
#         "cropInfo": {
#             "leftOffset": 0,
#             "rightOffset": 0,
#             "topOffset": 0,
#             "bottomOffset": 0
#         }
#     },
#     "data": { '0': 123, '1': 123 ... },
#     "isSharedArrayBuffer": true
# }


async def processws(websocket):
    async for message in websocket:
        print('Received message')
        data = json.loads(message)
        await websocket.send('Hi from the server')


async def main():
    async with websockets.serve(processws, "localhost", 16745, max_size=None):
        await asyncio.Future()

asyncio.run(main())
