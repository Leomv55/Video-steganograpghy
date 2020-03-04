from stegano import lsb
from os.path import isfile,join

import time                                                                 #install time ,opencv,numpy modules
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

def frame_extraction(video_path="input.mp4",root="./tmp/"):
    p_thres=0
    if not os.path.exists("./tmp"):
        os.makedirs("tmp")
        print("[INFO] tmp directory is created")
    cap = cv2.VideoCapture(video_path)
    ret, prev_frame = cap.read()
    count=0
    while ret:
        ret, curr_frame = cap.read()
        if ret:
            diff = cv2.absdiff(curr_frame, prev_frame)
            non_zero_count = np.count_nonzero(diff)
            if non_zero_count > p_thres:
                cv2.imwrite("{}frame{}.jpg".format(root,count), curr_frame)           # frames extracted
                count+=1
            prev_frame = curr_frame
    print("[INFO] Total number of Frames obtained: {}".format(count))

def encode_string(input_string,root="./tmp/"):
    split_string_list=split_string(input_string)
    for i in range(0,len(split_string_list)):
        f_name="{}frame{}.jpg".format(root,i)
        secret_enc=lsb.hide(f_name,split_string_list[i])
        secret_enc.save(f_name)
        print("[INFO] frame {} holds {}".format(f_name,split_string_list[i]))

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

def clean_tmp(path="./tmp"):
    if os.path.exists(path):
        shutil.rmtree(path)
        print("[INFO] tmp files are cleaned up")

def main():
    input_string = input("Enter the input string :")
    frame_extraction("./rain_132.mp4")
    encode_string(input_string)
    make_video("./tmp/","output.avi")
    clean_tmp()

if __name__ == "__main__":
    main()