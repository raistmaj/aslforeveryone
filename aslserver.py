import asyncio
from inspect import currentframe
import websockets
import numpy as np
import pyttsx3
import cv2
from modelevaluator import ModelEvaluator

from digitalOceanExample.step_5_camera import center_crop

currentPrediction = None
currentFrame = None
index_to_letter = list('ABCDEFGHIKLMNOPQRSTUVWXY')
mean = 0.485 * 255.
std = 0.229 * 255.

async def processws(websocket):
    async for message in websocket:
        global currentPrediction, currentFrame
        print('Received message')
        if (message == "getPrediction"):
            print("sending message back")
            await websocket.send(currentPrediction)

        # convert text into sound and output it to the virtual audio device
        # engine.say(f'received frame at {currentPrediction}')
        # engine.runAndWait()

        # await websocket.send('Hi from the server')


async def every(__seconds: float, func, *args, **kwargs):
    while True:
        func(*args, **kwargs)
        await asyncio.sleep(__seconds)

def predict():
    global currentPrediction, currentframe
    _, frame = cap.read()
    text = model.Predict(frame)
    frame = model.ProcessImageFrame(frame)
    cv2.imshow("Sign Language Translator", frame)
    cv2.waitKey(1)
    print(text)
    currentPrediction = text
    currentframe = frame
    
async def main():
    loop = asyncio.get_event_loop()
    loop.create_task(every(0.05, predict))

    async with websockets.serve(processws, "localhost", 16745, max_size=None):
        await asyncio.Future()

engine = pyttsx3.init()
cap = cv2.VideoCapture(0)
# load the model
model = ModelEvaluator(model_json='model/model.json', model_weights='model/model-weights.h5')
asyncio.run(main())
