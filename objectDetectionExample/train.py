from google.protobuf import text_format
from object_detection.protos import pipeline_pb2
from object_detection.utils import config_util
import tensorflow as tf
import os

from downloadYTVideo import createPath, VIDEO_TRAIN_PATH, VIDEO_TEST_PATH

WORKSPACE_PATH = os.path.join(os.getcwd(), 'workspace')
SCRIPTS_PATH = os.path.join(os.getcwd(), 'scripts')
MODEL_PATH = os.path.join(os.getcwd(), 'models')
PRETRAINED_MODEL_PATH = os.path.join(os.getcwd(), 'pre-trained-models')
APIMODEL_PATH = os.path.join(WORKSPACE_PATH, 'models')
ANNOTATION_PATH = os.path.join(WORKSPACE_PATH, 'annotations')
CONFIG_PATH = os.path.join(MODEL_PATH, 'pipeline.config')

createPath(WORKSPACE_PATH)
createPath(SCRIPTS_PATH)
createPath(APIMODEL_PATH)
createPath(ANNOTATION_PATH)
createPath(MODEL_PATH)
createPath(PRETRAINED_MODEL_PATH)


labels = [
    {"name": "yes", "id": 1},
    {"name": "no", "id": 2},
    {"name": "thank you", "id": 3},
    {"name": "hello", "id": 4},
    {"name": "A", "id": 5},
    {"name": "B", "id": 6},
    {"name": "C", "id": 7},
    {"name": "D", "id": 8},
    {"name": "E", "id": 9},
    {"name": "F", "id": 10},
    {"name": "G", "id": 11},
    {"name": "H", "id": 12},
    {"name": "I", "id": 13},
    {"name": "J", "id": 14},
    {"name": "K", "id": 15},
    {"name": "L", "id": 16},
    {"name": "M", "id": 17},
    {"name": "N", "id": 18},
    {"name": "O", "id": 19},
    {"name": "P", "id": 20},
    {"name": "Q", "id": 21},
    {"name": "R", "id": 22},
    {"name": "S", "id": 23},
    {"name": "T", "id": 24},
    {"name": "U", "id": 25},
    {"name": "V", "id": 26},
    {"name": "W", "id": 27},
    {"name": "X", "id": 28},
    {"name": "Y", "id": 29},
    {"name": "Z", "id": 30},
]

with open(os.path.join(ANNOTATION_PATH, 'label_map.pbtxt'), 'w') as f:
    for label in labels:
        f.write('item { \n')
        f.write('\tname:\'{}\'\n'.format(label['name']))
        f.write('\tid:{}\n'.format(label['id']))
        f.write('}\n')

# step2: generate tfrecords
# print(f'python {os.path.join(SCRIPTS_PATH, "generate_tfrecord.py")} -x {VIDEO_TRAIN_PATH} -l {os.path.join(ANNOTATION_PATH, "label_map.pbtxt")} -o {os.path.join(ANNOTATION_PATH, "train.record")}')
# print(f'python {os.path.join(SCRIPTS_PATH, "generate_tfrecord.py")} -x {VIDEO_TEST_PATH} -l {os.path.join(ANNOTATION_PATH, "label_map.pbtxt")} -o {os.path.join(ANNOTATION_PATH, "test.record")}')


# step3
# git clone https://github.com/tensorflow/models into workspace folder

# step4: update config file
config = config_util.get_configs_from_pipeline_file(CONFIG_PATH)
pipeline_config = pipeline_pb2.TrainEvalPipelineConfig()
with tf.io.gfile.GFile(CONFIG_PATH, "r") as f:
    proto_str = f.read()
    text_format.Merge(proto_str, pipeline_config)
pipeline_config.model.ssd.num_classes = 30 # change this to the number of classes
pipeline_config.train_config.batch_size = 4
pipeline_config.train_config.fine_tune_checkpoint = os.path.join(
    PRETRAINED_MODEL_PATH, 'ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8', 'checkpoint', 'ckpt-0')
pipeline_config.train_config.fine_tune_checkpoint_type = "detection"
pipeline_config.train_input_reader.label_map_path = os.path.join(
    ANNOTATION_PATH, 'label_map.pbtxt')
pipeline_config.train_input_reader.tf_record_input_reader.input_path[:] = [
    os.path.join(
        ANNOTATION_PATH, 'train.record')]
pipeline_config.eval_input_reader[0].label_map_path = os.path.join(
    ANNOTATION_PATH, 'label_map.pbtxt')
pipeline_config.eval_input_reader[0].tf_record_input_reader.input_path[:] = [os.path.join(
    ANNOTATION_PATH, 'test.record')]

config_text = text_format.MessageToString(pipeline_config)
with tf.io.gfile.GFile(CONFIG_PATH, "wb") as f:
    f.write(config_text)

# step5: train model
# run pip install tf-models-official before executing this command
print(f'python {os.path.join(APIMODEL_PATH, "research", "object_detection", "model_main_tf2.py")} --model_dir={MODEL_PATH} --pipeline_config_path={CONFIG_PATH} --num_train_steps=20000')
