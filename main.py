from stegano import lsb
from os.path import isfile,join

import time                                                                
import cv2
import numpy as np
import math
import os
import shutil
import subprocess
import os

from moviepy.editor import *
# from progressbar import Progressbar,Percentage,Bar

def split_string(s_str,count=10):
    per_c=math.ceil(len(s_str)/count)
    c_cout=0
    out_str=''
    split_list=[]
    for s in s_str:
        out_str+=s
        c_cout+=1
        if c_cout == per_c:
            split_list.append(out_str)
            out_str=''
            c_cout=0
    if c_cout!=0:
        split_list.append(out_str)
    return split_list

def frame_extraction(video_path="input.mp4",temp_path="./tmp/"):
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
        print("[INFO] tmp directory is created")
    else:
        clean_tmp(temp_path)
        os.makedirs(temp_path)
    cap = cv2.VideoCapture(video_path)
    # ret, prev_frame = cap.read()
    count=0
    while True:
        ret, curr_frame = cap.read()
        if ret:
            f_name = "{}frame{}.png".format(temp_path,count)
            cv2.imwrite(f_name, curr_frame)           # frames extracted
            # jpg_to_png = Image.open(f_name)
            # jpg_to_png.save("{}frame{}.png".format(temp_path,count))
            count+=1
        else:
            break
    print("[INFO] Total number of Frames obtained: {}".format(count))
    return count

def encode_string(input_string,total_frames,temp_path="./tmp/"):
    split_string_list=split_string(input_string)
    index=0
    for i in range(0,total_frames):
        try:
            if i%10==0:
                f_name="{}frame{}.png".format(temp_path,i)
                secret_enc=lsb.hide(f_name,split_string_list[index])
                secret_enc.save(f_name)
                print(lsb.reveal(f_name))
                print("[INFO] frame {} holds {}".format(f_name,split_string_list[index]))
                index+=1
        except:
            print("OPENCV exceptions")

def decode_string(video_p="final.mp4",temp_p="./tmp/"):
    decoded_string =  ""
    total = frame_extraction(video_path=video_p,temp_path=temp_p)
    for f in range(0,20):
        f_name="{}frame{}.png".format(temp_p,f)
        secret = lsb.reveal(f_name)
        if secret is not None:
            decoded_string += secret
        # pbar.update(f)
    # pbar.finish()
    return decoded_string
    
def make_video(pathIn="./tmp",pathOut="video.avi"):
    fps = 30
    os.chdir(pathIn)
    subprocess.call("ffmpeg -r {} -i \"frame%d.png\"  -c:v huffyuv {}".format(fps,pathOut),shell=True)
    print("[INFO] The encoded video is made named {}".format(pathOut))
    os.chdir("../")
    

def integrate_audio_video(encoded_video_path="output.avi",audio_path="default.aac"):
    command = "ffmpeg -i {} -i {} -codec copy -shortest {}".format(encoded_video_path,audio_path,"final.avi")
    subprocess.call(command,shell=True)
    print("[INFO] Integration completed")

def get_audio(video_path = "output.avi" ,output_audio_path="default.aac"):
    audio = "ffmpeg -i {} -vn -acodec copy {}".format(video_path,output_audio_path)
    subprocess.call(audio,shell=True)


def clean_tmp(temp_path="./tmp"):
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)
        print("[INFO] tmp files are cleaned up")

def main():
    
    ORIGINAL_VIDEO_FILE="Wildlife.mp4"

    input_string = input("Enter the input string :")
    total_frames=frame_extraction(ORIGINAL_VIDEO_FILE)
    encode_string(input_string,total_frames)
    make_video("./tmp/","../output.avi")
    get_audio(video_path=ORIGINAL_VIDEO_FILE)
    integrate_audio_video()
    clean_tmp()

    # print(decode_string(video_p="final.avi"))
    # clean_tmp()

if __name__ == "__main__":
    main()