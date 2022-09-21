import numpy as np
import os
import six.moves.urllib as urllib  
import sys
import tarfile
import string
import tensorflow as tf
from keras.models import model_from_json
import zipfile
import pathlib
import operator
import cv2
from PIL import Image

class ModelEvaluator:
    def __init__(self, model_json, model_weights, on_text_callback):
        if not model_json:
            raise('Provide a model definition')
        if not model_weights:
            raise('Provide model weights')

        self.__load_model(model_json, model_weights)
        self.on_text_callback = on_text_callback

    def __load_model(self, model_json, model_weights):
        with open(model_json, 'r') as json_file:
            self.json_content = json_file.read()

        self.model = model_from_json(self.json_content)
        self.model.load_weights(model_weights)

    def __inference_single_image(self, image_raw_data):
        # Resize image if necessary
        image_size = 500
        resized_image = cv2.resize(image_raw_data, (image_size, image_size))
        # This returns numpy value
        prediction_result = self.model.predict(resized_image.reshape(1, image_size, image_size, 1))
        # This returns a tensor
        # prediction_result = self.model(resized_image.reshape(1, image_size, image_size, 1))
        prediction={}
        prediction['blank'] = prediction_result[0][0]
        index = 0
        for i in string.ascii_uppercase:
            prediction[i] = prediction_result[0][index]
            index +=1
            if index >= 26:
                break

        prediction = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True)
        return prediction[0][0]

        # image_from_array = Image.fromarray(image_raw_data)
        # # transform the input using numpy 
        # image = np.asarray(image_from_array)
        # input_tensor = tf.convert_to_tensor(image)
        # # Depending on the model we may need to expand the tensor, with an extra dimension
        # # Some models expect a bunch of input images for examples as first dimension,
        # # if we run a single image we may still need to expand the tensor
        # # input_tensor = input_tensor[tf.newaxis, ...]

        # # Tensor flow uses serving_default as default signature, you may
        # # add different ones during the model creation
        # model_default_signature = self.model.signatures['serving_default']
        # model_dictionary = model_default_signature(input_tensor)

        # # Outputs usually are batches of tensors
        # detection_cardinality = int(model_dictionary.pop('num_detections'))
        # # Depending on the model we may need to remove the batch extra dimention 
        # # output_dict = {key:value[0, :num_detections].numpy() for key,value in output_dict.items()}
        # # output_dict['num_detections'] = num_detections

        # # cast the detection classes to the desired type
        # model_dictionary['detection_classes'] = model_dictionary['detection_classes'].astype(np.int64)

        # # if needed compute masks

        # # the model will have the following, entries for us
        # # detction_boxes
        # # detection_classes
        # # detection_scores
        # return model_dictionary
    
    def ProcessStream(self, video_stream):
        video_source = cv2.VideoCapture(video_stream)
        print('Capturing')
        while True:
            re, frame = video_source.read()
            if re:
                filpped_frame = cv2.flip(frame,1)
                region_to_evalue = filpped_frame[10:510, 220:720]
                image_blur = cv2.GaussianBlur(region_to_evalue,(3,3), 0)
                bw_image = cv2.cvtColor(image_blur, cv2.COLOR_BGR2GRAY)
                
                # evaluate the same region we did with the model frame[10:510, 220:720]
                # Sobel edge detection
                sobelxy = cv2.Sobel(src=bw_image, ddepth=cv2.CV_8U, dx=1, dy=1, ksize=5)
                cv2.imshow("test", sobelxy)
                output = self.__inference_single_image(sobelxy)
                if output == "":
                    output = "nothing detected"
                #cv2.putText(frame, output, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), thickness=2)
                self.on_text_callback(output)
            if cv2.waitKey(1) & 0xFF == ord('q'): # exit
                break
        video_source.release()
        cv2.destryAllWindows()

    def ProcessImageRawData(self, image_raw_data):
        model_result = self.__inference_single_image(image_raw_data)
        self.on_text_callback(model_result)

def test_call_back(one_text):
    print(one_text)

me = ModelEvaluator(model_json='model/model.json', model_weights='model/model-weights.h5', on_text_callback=test_call_back)

me.ProcessStream(0)