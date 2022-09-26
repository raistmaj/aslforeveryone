import os


VIDEO_DOWNLOAD_PATH = os.path.join(os.getcwd(), 'data', 'videos')
TRIMMED_VIDEO_PATH = os.path.join(
    os.getcwd(), 'data', 'videos', 'trimmedVideos')
VIDEO_FRAME_PATH = os.path.join(os.getcwd(), 'data', 'videos', 'frames')
VIDEO_TRAIN_PATH = os.path.join(os.getcwd(), 'data', 'videos', 'train')
VIDEO_TEST_PATH = os.path.join(os.getcwd(), 'data', 'videos', 'test')
WORKSPACE_PATH = os.path.join(os.getcwd(), 'workspace')
SCRIPTS_PATH = os.path.join(os.getcwd(), 'scripts')
MODEL_PATH = os.path.join(os.getcwd(), 'models')
PRETRAINED_MODEL_PATH = os.path.join(os.getcwd(), 'pre-trained-models')
APIMODEL_PATH = os.path.join(WORKSPACE_PATH, 'models')
ANNOTATION_PATH = os.path.join(WORKSPACE_PATH, 'annotations')
CONFIG_PATH = os.path.join(MODEL_PATH, 'pipeline.config')
