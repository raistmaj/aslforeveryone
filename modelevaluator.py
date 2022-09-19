import numpy as np
import os
import six.moves.urllib as urllib  
import sys
import tarfile
import tensorflow as tf
import zipfile
import pathlib
import cv2
from PIL import Image

class ModelEvaluator:
    def __init__(self, model_path, on_text_callback):
        if not model_path:
            raise('Provide a model')
        self.model = self.__load_model(model_path)
        self.on_text_callback = on_text_callback;

    def __load_model(self, model_path):
        return tf.saved_model.load(str(model_path))

    def __inference_single_image(self, image_raw_data):
        image_from_array = Image.fromarray(image_raw_data)
        # transform the input using numpy 
        image = np.asarray(image_from_array)
        input_tensor = tf.convert_to_tensor(image)
        # Depending on the model we may need to expand the tensor, with an extra dimension
        # Some models expect a bunch of input images for examples as first dimension,
        # if we run a single image we may still need to expand the tensor
        # input_tensor = input_tensor[tf.newaxis, ...]

        # Tensor flow uses serving_default as default signature, you may
        # add different ones during the model creation
        model_default_signature = self.model.signatures['serving_default']
        model_dictionary = model_default_signature(input_tensor)

        # Outputs usually are batches of tensors
        detection_cardinality = int(model_dictionary.pop('num_detections'))
        # Depending on the model we may need to remove the batch extra dimention 
        # output_dict = {key:value[0, :num_detections].numpy() for key,value in output_dict.items()}
        # output_dict['num_detections'] = num_detections

        # cast the detection classes to the desired type
        model_dictionary['detection_classes'] = model_dictionary['detection_classes'].astype(np.int64)

        # if needed compute masks

        # the model will have the following, entries for us
        # detction_boxes
        # detection_classes
        # detection_scores
        return model_dictionary
    
    def ProcessStream(self, video_stream):
        video_source = cv2.VideoCapture(video_stream)
        while True:
            re, frame = video_source.read()
            if re:
                output = self.__inference_single_image(frame);
                self.on_text_callback(output)
            if cv2.waitKey(1) & 0xFF == ord('q'): # test remove
                break
        video_source.release()
        cv2.destryAllWindows()

    def ProcessImageRawData(self, image_raw_data):
        model_result = self.__inference_single_image(image_raw_data);

def test_call_back(one_text):
    print('yey')

me = ModelEvaluator(model_path='test', on_text_callback=test_call_back)
me.ProcessStream(video_stream='rtmp://localhost/show/stream')