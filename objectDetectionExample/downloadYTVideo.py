
from os.path import join
from pytube import YouTube
import pandas as pd

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
    for index, row in MSASL_Data.iterrows():
        url = row['url']
        clean_name = row['clean_text']
        video_name = row['VideoName']
        if clean_name not in classesToDownload:
            continue

        try:
            yt = YouTube(url)
            stream = yt.streams.filter(
                progressive=True, file_extension='mp4').get_highest_resolution()
            stream.download('data/videos/' +
                            clean_name + '/', filename=video_name + ".mp4")
        except Exception as e:
            print("Error downloading video: " + clean_name + "=>" + str(e))
            continue


classesToDownload = set(["thank you", "goodbye", "hello", "yes", "no"])
download_videos(classesToDownload)
