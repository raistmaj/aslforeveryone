## SSD-MobileNet

Used for detecting objects in images and videos. [Repo](https://github.com/abhileshborode/SSD-MobileNet)

## Cannot import name 'model_lib_v2' from 'object_detection'
https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/install.html

cd models/research
### Compile protos.

protoc object_detection/protos/*.proto --python_out=.
### Install TensorFlow Object Detection API.
cp object_detection/packages/tf2/setup.py .
python -m pip install --use-feature=2020-resolver .