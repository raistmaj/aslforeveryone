from fileinput import filename
import os
import random
import shutil
import cv2
from os.path import join
from pytube import YouTube
import pandas as pd
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from os.path import join, exists

MSASL_trainData = pd.read_json(os.path.join(
    os.getcwd(), 'msasl/MSASL_train.json'))
MSASL_valData = pd.read_json(os.path.join(os.getcwd(), 'msasl/MSASL_val.json'))
MSASL_testData = pd.read_json(os.path.join(
    os.getcwd(), 'msasl/MSASL_test.json'))
MSASL_classes = pd.read_json(os.path.join(
    os.getcwd(), 'msasl/MSASL_classes.json'))
MSASL_classes.columns = ['class']
MSASL_Data = pd.concat([MSASL_trainData, MSASL_valData,
                       MSASL_testData], ignore_index=True)
split_df = MSASL_Data["url"].str.split("=", n=1, expand=True)
MSASL_Data["VideoName"] = split_df[1]

VIDEO_DOWNLOAD_PATH = os.path.join(os.getcwd(), 'data', 'videos')
TRIMMED_VIDEO_PATH = os.path.join(
    os.getcwd(), 'data', 'videos', 'trimmedVideos')
VIDEO_FRAME_PATH = os.path.join(os.getcwd(), 'data', 'videos', 'frames')
VIDEO_TRAIN_PATH = os.path.join(os.getcwd(), 'data', 'videos', 'train')
VIDEO_TEST_PATH = os.path.join(os.getcwd(), 'data', 'videos', 'test')

def process_videos():
    gestureList = set(["letter"])
    download_videos(gestureList)

    # trim the video by the start and end time
    files = [f for f in os.listdir(VIDEO_DOWNLOAD_PATH) if os.path.isfile(
        join(VIDEO_DOWNLOAD_PATH, f))]
    for file in files:
        TrimVideoClip(file)

    # convert the video to frames
    files = [f for f in os.listdir(TRIMMED_VIDEO_PATH) if os.path.isfile(
        join(TRIMMED_VIDEO_PATH, f))]
    for file in files:
        convert_to_frames(file)


def createPath(path):
    if not os.path.exists(path):
        os.makedirs(path)


def download_videos(classesToDownload):
    for _, row in MSASL_Data.iterrows():
        url = row['url']
        cleanText = row['clean_text']
        videoName = row['VideoName']
        if cleanText not in classesToDownload:
            continue

        try:
            yt = YouTube(url)
            stream = yt.streams.filter(
                progressive=True, file_extension='mp4').get_highest_resolution()
            stream.download(VIDEO_DOWNLOAD_PATH,
                            filename=f'{cleanText}_{videoName}.mp4')
            print("Downloaded: ", videoName)
        except Exception as e:
            print("Error downloading video: " + cleanText + " => " + str(e))
            continue


def getVideoName(file):
    return file.split('_', 1)[1][:-4]


def getLabel(file):
    return file.split('_')[0]


def TrimVideoClip(file):
    fileName = getVideoName(file)
    cleanText = getLabel(file)

    VideoNameDF = MSASL_Data.loc[(MSASL_Data['VideoName'] == fileName) & (
        MSASL_Data['clean_text'] == cleanText)]
    if VideoNameDF.empty:
        print("No video found: " + fileName)
        return

    start_time = VideoNameDF['start_time'].min()
    end_time = VideoNameDF['end_time'].max()
    print(fileName, start_time, end_time)
    ffmpeg_extract_subclip(os.path.join(VIDEO_DOWNLOAD_PATH, str(file)), start_time,
                           end_time, targetname=os.path.join(TRIMMED_VIDEO_PATH, str(file)))


def convert_to_frames(file):
    fileName = getVideoName(file)
    label = getLabel(file)

    print("Converting to frame for video_name: ", file)
    vidcap = cv2.VideoCapture(os.path.join(TRIMMED_VIDEO_PATH, file))
    success, image = vidcap.read()
    frame_count = 0
    while success:
        # image = cv2.cvtcolor(image,cv2.color_bgr2gray) # to convert image to grayscale
        # save frame as jpeg file
        frameName = f'{fileName}_{label}_frame{frame_count}.jpg'
        cv2.imwrite(os.path.join(VIDEO_FRAME_PATH, str(frameName)), image)
        success, image = vidcap.read()
        print('read a new frame: ', success)
        frame_count += 1


def removeFramesWithoutLabel():
    files = [f for f in os.listdir(VIDEO_FRAME_PATH) if os.path.isfile(
        join(VIDEO_FRAME_PATH, f))]
    for file in files:
        if (file.split('.')[1] != 'jpg'):
            continue
        if not os.path.exists(os.path.join(VIDEO_FRAME_PATH, file.split('.')[0] + '.xml')):
            os.remove(os.path.join(VIDEO_FRAME_PATH, file))


def splitTrainAndTestData():
    files = [f for f in os.listdir(VIDEO_FRAME_PATH) if os.path.isfile(
        join(VIDEO_FRAME_PATH, f))]
    for file in files:
        if (file.split('.')[1] != 'jpg'):
            continue
        xmlFileName = file.split('.')[0] + '.xml'
        xmlFile = os.path.join(VIDEO_FRAME_PATH, xmlFileName)
        frameFile = os.path.join(VIDEO_FRAME_PATH, file)
        # 80% train and 20% test
        if random.random() < 0.8:
            shutil.copy(frameFile, os.path.join(
                VIDEO_TRAIN_PATH, file))
            shutil.copy(xmlFile, os.path.join(
                VIDEO_TRAIN_PATH, xmlFileName))
        else:
            shutil.copy(frameFile, os.path.join(
                VIDEO_TEST_PATH, file))
            shutil.copy(xmlFile, os.path.join(
                VIDEO_TEST_PATH, xmlFileName))


createPath(VIDEO_DOWNLOAD_PATH)
createPath(TRIMMED_VIDEO_PATH)
createPath(VIDEO_FRAME_PATH)
createPath(VIDEO_TRAIN_PATH)
createPath(VIDEO_TEST_PATH)

# step1: download the videos
# process_videos()

# step2: label your data using labelImg after download, then run the following commands

# step3: remove the frames without label
# removeFramesWithoutLabel()

# step4: split the train and test data
# splitTrainAndTestData()
