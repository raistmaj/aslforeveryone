import os
from os.path import join
from pytube import YouTube
import pandas as pd
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

MSASL_trainData = pd.read_json('msasl/MSASL_train.json')
MSASL_valData = pd.read_json('msasl/MSASL_val.json')
MSASL_testData = pd.read_json('msasl/MSASL_test.json')
MSASL_classes = pd.read_json('msasl/MSASL_classes.json')
MSASL_classes.columns = ['class']
MSASL_Data = pd.concat([MSASL_trainData, MSASL_valData,
                       MSASL_testData], ignore_index=True)
split_df = MSASL_Data["url"].str.split("=", n=1, expand=True)
MSASL_Data["VideoName"] = split_df[1]


def download_videos(classesToDownload):
    for _, row in MSASL_Data.iterrows():
        url = row['url']
        clean_text = row['clean_text']
        video_name = row['VideoName']
        if clean_text not in classesToDownload:
            continue

        try:
            yt = YouTube(url)
            stream = yt.streams.filter(
                progressive=True, file_extension='mp4').get_highest_resolution()
            dir = 'data/videos/' + clean_text + '/'
            path = f'{dir}{video_name}.mp4'
            stream.download(dir, filename=video_name + ".mp4")
            print("Downloaded: ", video_name)

            # trim the video by the start and end time
            TrimVideoClip(path, dir, video_name, clean_text)
        except Exception as e:
            print("Error downloading video: " + clean_text + "=>" + str(e))
            continue


def TrimVideoClip(video_path, video_dir, video_name, clean_text):
    fileName = video_name
    # Filter for the file name in the df
    VideoNameDF = MSASL_Data.loc[(MSASL_Data['VideoName'] == fileName) & (
        MSASL_Data['clean_text'] == clean_text)]
    if VideoNameDF.empty:
        print("No video found" + fileName)
        return

    # read the corresponding start and end time for the video from the df; min(), max() are just a proxy; we expect start and end time to be same for a given video name in case multiple enteries are present for the video
    start_time = VideoNameDF['start_time'].min()
    end_time = VideoNameDF['end_time'].max()
    print(fileName, start_time, end_time)

    TrimmedVideo_TargetPath = video_dir + "TrimmedVideos/"

    if not os.path.exists(TrimmedVideo_TargetPath):
        os.mkdir(TrimmedVideo_TargetPath)

    ffmpeg_extract_subclip(video_path, start_time,
                           end_time, targetname=f'{TrimmedVideo_TargetPath}{video_name}.mp4')


classesToDownload = set(["thank you", "goodbye", "hello", "yes", "no"])
download_videos(classesToDownload)
