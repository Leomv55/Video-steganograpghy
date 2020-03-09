from stegano import lsb
from os.path import isfile,join

import time                                                                
import cv2
import numpy as np
import math
import os
import shutil


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
def make_video(pathIn="./tmp/",pathOut="video.avi"):
    fps = 30
    frame_array = []
    files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]#for sorting the file names properly
    files.sort(key = lambda x: x[5:-4])
    files.sort()
    
    for i in range(len(files)):
        filename=pathIn + files[i]
        #reading each files
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
    
        #inserting the frames into an image array
        frame_array.append(img)
    out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
    for i in range(len(frame_array)):
        # writing to a image array
        out.write(frame_array[i])
    out.release()
    print("[INFO] The encoded video is made named {}".format(pathOut))

def clean_tmp(temp_path="./tmp"):
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)
        print("[INFO] tmp files are cleaned up")

def main():
    input_string = input("Enter the input string :")
    total_frames=frame_extraction("./rain_132.mp4")
    encode_string(input_string,total_frames)
    make_video("./tmp/","output.avi")
    clean_tmp()

if __name__ == "__main__":
    main()