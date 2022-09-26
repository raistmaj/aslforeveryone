import asyncio
from inspect import currentframe
import json
from operator import mod
import os
import websockets
import numpy as np
import pyttsx3
import cv2
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import config_util
from object_detection.builders import model_builder
from objectDetectionExample.constants import ANNOTATION_PATH, MODEL_PATH, CONFIG_PATH
from digitalOceanExample.step_5_camera import center_crop

currentPrediction = None
# Load module
# Load pipeline config and build a detection model
configs = config_util.get_configs_from_pipeline_file(CONFIG_PATH)
detection_model = model_builder.build(
    model_config=configs['model'], is_training=False)

# Restore checkpoint
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
# change this to the latest checkpoint
ckpt.restore(os.path.join(MODEL_PATH, 'ckpt-62')).expect_partial()
category_index = label_map_util.create_category_index_from_labelmap(
    os.path.join(MODEL_PATH, 'label_map.pbtxt'))


async def processws(websocket):
    async for message in websocket:
        global currentPrediction
        print('Received message')
        if (message == "getPrediction"):
            print("sending message back")
            if currentPrediction is not None:
                await websocket.send(currentPrediction["name"])
                # convert text into sound and output it to the virtual audio device
                engine.say(f'received frame at {currentPrediction}')
                engine.runAndWait()
            else:
                await websocket.send("")


async def every(__seconds: float, func, *args, **kwargs):
    while True:
        func(*args, **kwargs)
        await asyncio.sleep(__seconds)


@tf.function
def detect_fn(input_tensor):
    image, shapes = detection_model.preprocess(input_tensor)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)
    return detections


def predict():
    global currentPrediction, currentframe
    _, frame = cap.read()
    frame = cv2.flip(frame,1)
    image_np = np.array(frame)

    input_tensor = tf.convert_to_tensor(
        np.expand_dims(image_np, 0), dtype=tf.float32)
    detections = detect_fn(input_tensor)
    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy()
                  for key, value in detections.items()}
    detections['detection_classes'] = detections['detection_classes'].astype(
        np.int64)

    predictedClass = category_index.get(detections['detection_classes'][0] + 1)
    if (detections['detection_scores'][0] > 0.4):
        currentPrediction = predictedClass
        print(str(predictedClass) + " | probability: " +
              str(detections['detection_scores'][0]))
    else:
        currentPrediction = None

    # cv2.imshow("Sign Language Translator", frame)
    # cv2.waitKey(1)


async def main():
    loop = asyncio.get_event_loop()
    loop.create_task(every(0.1, predict))
    async with websockets.serve(processws, "localhost", 16745, max_size=None):
        await asyncio.Future()

engine = pyttsx3.init()
cap = cv2.VideoCapture(0)
asyncio.run(main())
