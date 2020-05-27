from stegano import lsb
from os.path import isfile,join

import time                                                                
import cv2
import numpy as np
import math
import os
import shutil
import subprocess
import argparse

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
    print("Please wait till all frames is being scaned this may take minutes to hours... ")
    total = frame_extraction(video_path=video_p,temp_path=temp_p)
    for f in range(0,total):
        f_name="{}frame{}.png".format(temp_p,f)
        secret = lsb.reveal(f_name)
        if secret is not None:
            decoded_string += secret
    return decoded_string
    
def make_video(pathIn="./tmp/",pathOut="video.avi"):
    fps = 30
    os.chdir(pathIn)
    subprocess.call("ffmpeg -r {} -i \"frame%d.png\"  -c:v huffyuv {}".format(fps,pathOut),shell=True)
    print("[INFO] The encoded video is made named {}".format(pathOut))
    os.chdir("../")
    

def integrate_audio_video(encoded_video_path="output.avi",audio_path="default.aac",destination="final.avi"):
    command = "ffmpeg -i {} -i {} -codec copy -shortest {}".format(encoded_video_path,audio_path,destination)
    subprocess.call(command,shell=True)
    os.remove(audio_path)
    os.remove(encoded_video_path)
    print("[INFO] Integration completed")

def get_audio(video_path = "output.avi" ,output_audio_path="default.aac"):
    audio = "ffmpeg -i {} -vn -acodec copy {}".format(video_path,output_audio_path)
    subprocess.call(audio,shell=True)


def clean_tmp(temp_path="./tmp"):
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)
        print("[INFO] tmp files are cleaned up")

def main():
    parser = argparse.ArgumentParser(description="Command-line tool for video steganography")
    parser.add_argument('-es','--encode-string',metavar='S',type=str,help='string for encryption')
    parser.add_argument('-s','--source',metavar='U',type=str,help='source for video path')
    parser.add_argument('-d','--destination',metavar='D',nargs="?",const="final.avi",type=str,help='destination for video path')
    parser.add_argument('--encryption',action='store_true',help="for encryption")
    arg_dict = parsed_dict(parser)
    
    if arg_dict['encryption']:
        #Encryption
        if arg_dict['encode_string'] is None:
            parser.print_usage()
            parser.exit(status=1,message="encode string is required in encryption\n")
        elif arg_dict['source'] is None:
            parser.print_usage()
            parser.exit(status=1,message="source should be specified for encryption\n")
        clean_tmp()
        total_frames=frame_extraction(arg_dict['source'])
        encode_string(arg_dict['encode_string'],total_frames)
        make_video("./tmp/","../output.avi")
        get_audio(video_path=arg_dict['source'])
        integrate_audio_video(destination=arg_dict['destination'])
        clean_tmp()
    else:
        #Decryption
        if arg_dict['encode_string'] is not None or arg_dict['destination'] is not None:
            parser.print_usage()
            parser.exit(status=1,message="-es / -d is not required for decryption\n")
        elif arg_dict['source'] is None:
            parser.print_usage()
            parser.exit(status=1,message="-s is required for decryption\n")            
        clean_tmp()
        print("Decoded string: "+decode_string(video_p=arg_dict['source']))
        clean_tmp()

    # ORIGINAL_VIDEO_FILE="Wildlife.mp4"

    # input_string = input("Enter the input string :")
    # total_frames=frame_extraction(ORIGINAL_VIDEO_FILE)
    # encode_string(input_string,total_frames)
    # make_video("./tmp/","../output.avi")
    # get_audio(video_path=ORIGINAL_VIDEO_FILE)
    # integrate_audio_video()
    # clean_tmp()

    # print(decode_string(video_p="final.avi"))
    # clean_tmp()
def parsed_dict(parser):
    return parser.parse_args().__dict__


if __name__ == "__main__":
    main()


# Encryption example
# python main.py -es "leo is good" -s /home/leo/Projects/steganography/Wildlife.mp4 -d ./final.avi --encryption

# Decryption example
# python main.py -s final.avi