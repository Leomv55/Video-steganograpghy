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
            cv2.imwrite("{}frame{}.jpg".format(temp_path,count), curr_frame)           # frames extracted
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
                f_name="{}frame{}.jpg".format(temp_path,i)
                secret_enc=lsb.hide(f_name,split_string_list[index])
                secret_enc.save(f_name)
                print("[INFO] frame {} holds {}".format(f_name,split_string_list[index]))
                index+=1
        except:
            break
def make_video(pathIn="./tmp",pathOut="video.avi"):
    fps = 30
    # frame_array = []
    # files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]#for sorting the file names properly
    # files.sort(key =lambda x: x[5:-4])
    
    # for i in range(len(files)):
    #     filename=pathIn + files[i]
    #     #reading each files
    #     img = cv2.imread(filename)
    #     height, width, layers = img.shape
    #     size = (width,height)
    
    #     #inserting the frames into an image array
    #     frame_array.append(img)
    # out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
    # for i in range(len(frame_array)):
    #     # writing to a image array
    #     out.write(frame_array[i])
    # cv2.destroyAllWindows()
    # out.release()
    os.chdir(pathIn)
    subprocess.call("ffmpeg -r {} -i \"frame%d.jpg\" -vb 20M -vcodec mpeg4 {}".format(fps,pathOut),shell=True)
    print("[INFO] The encoded video is made named {}".format(pathOut))
    os.chdir("../")
    

def integrate_audio_video(video_path_original="rain_132.mp4",encoded_video_path="./tmp/output.avi"):
    original_video = VideoFileClip(encoded_video_path)
    encoded_video = original_video.set_audio(VideoFileClip(video_path_original).audio)
    encoded_video.write_videofile("final.mp4")
    print("[INFO] Integration completed")

def clean_tmp(temp_path="./tmp"):
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)
        print("[INFO] tmp files are cleaned up")

def main():
    
    ORIGINAL_VIDEO_FILE="Wildlife.mp4"
    input_string = input("Enter the input string :")
    total_frames=frame_extraction(ORIGINAL_VIDEO_FILE)
    encode_string(input_string,total_frames)
    make_video("./tmp/","output.avi")
    integrate_audio_video(video_path_original=ORIGINAL_VIDEO_FILE)
    clean_tmp()

if __name__ == "__main__":
    main()