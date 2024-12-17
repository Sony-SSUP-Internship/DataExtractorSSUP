import pandas as pd
import streamlit as st
from ffmpy import FFmpeg
import datetime
import random
import string
import os
import json


def name_file():
    st = ''.join(random.choices(string.ascii_letters,k=7))
    finalnam = f'Audio-{st}.wav'
    return finalnam

def append_data(SOURCE_FILE,AUDIO_FILE_PATH,START_TIMESTAMP,END_TIMESTAMP,CLASS_LABEL):
    df = {'SOURCE_FILE' : SOURCE_FILE,
                       'AUDIO_FILE_PATH' : AUDIO_FILE_PATH,
                       'START_TIMESTAMP' : START_TIMESTAMP,
                       'END_TIMESTAMP' : END_TIMESTAMP,
                       'CLASS_LABEL' : CLASS_LABEL}


    return df


browse_path = "E:\\Projects Continued\\DataExtractorSSUP\\testvid\\20240608_100239.mp4"
save_path =  "E:\\Projects Continued\\DataExtractorSSUP\\AUDIOSAVES"
output_file_path = "E:\\Projects Continued\\DataExtractorSSUP\\output_data.json"
START_TIMESTAMP = 0
IS_PLAYING = False

video_file = open(browse_path,'rb')
video_bytes = video_file.read()
st.video(video_bytes)

start_ts = st.text_input('enter starting timestamp HH:MM:SS')
end_ts = st.text_input('enter ending timestamp HH:MM:SS')

class_name = st.text_input('enter class name')

if(st.button("run")):
    filename = os.path.join(save_path,name_file())

    ff = FFmpeg(
        inputs={browse_path : None},
        outputs={filename: f"-ss {start_ts} -to {end_ts} -q:a 0 -map a"}
    )

    ff.run()
    st.success(f'successfully saved file {filename}')
    retdf = append_data(browse_path,filename,start_ts,end_ts,class_name)

    with open(output_file_path) as fp:
        listobj = json.load(fp)

    listobj.append(retdf)

    with open(output_file_path,'w') as towri:
        json.dump(listobj,towri,indent=4,separators=(',',':'))

    st.toast("Updated Json File")
    st.balloons()






