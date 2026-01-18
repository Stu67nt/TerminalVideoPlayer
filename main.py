import yt_dlp
import numpy
from decord import VideoReader
from decord import cpu, gpu
import os
import fpstimer
import sys
from playsound3 import playsound

URLS = ['https://www.youtube.com/watch?v=FtutLA63Cp8']

YDL_OPTS = {
    'format': 'bestaudio'
}

def downloader(ydl_opts: dict, urls: list):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(URLS)
    return error_code

def create_video_obj(video_file: str="tester.mp4"):
    with open(video_file, 'rb') as f:
        #print(os.get_terminal_size().columns, os.get_terminal_size().lines)
        try:
            vr = VideoReader(f, ctx=cpu(0), width=os.get_terminal_size().columns, height=os.get_terminal_size().lines)
        except OSError:
            print("Could not get terminal size defaulting to 144p resolution")
            vr = VideoReader(f, ctx=cpu(0), width=256, height=144)
        f.close()
    return vr

def video_to_arr(vr, frame_skip: int=4):
    all_frames = []

    for i in range(0,len(vr),frame_skip):
        frame = vr[i].asnumpy()
        all_frames.append(frame)
        print(f"{i}/{len(vr)}", end="\r")
    return all_frames


def convert_video_to_GS(frames):
    frame_count = 0
    total = len(frames)
    for current_frame in frames:
        # vector method
        gs_frame = (current_frame[:,:,0]*0.299)+(current_frame[:,:,1]*0.587)+(current_frame[:,:,2]*0.114)
        """
        #for loop method
        row_i, column_i = 0, 0

        for row in current_frame:
            for pixel in row:
                r,g,b = pixel[0], pixel[1], pixel[2]
                grey_val = (0.299*r)+(0.587*g)+(0.114*b)
                gs_frame[row_i][column_i] = grey_val
                column_i += 1
            column_i = 0
            row_i += 1
"""
        frames[frame_count] = gs_frame
        frame_count += 1
        print(f"{frame_count}/{total}", end="\r")
    return frames

def video_to_ascii(frames, resolution_mode: str = "high", reverse_map: bool = False):
    ASCII_COLOURMAP = list(r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^`'. ")
    if reverse_map:
        ASCII_COLOURMAP.reverse()

    frame_count = 0
    total = len(frames)
    all_ascii_frames = []
    for current_frame in frames:
        ascii_frame = []
        indexed_frame = ((current_frame[:] * (len(ASCII_COLOURMAP)-1)) // 255)

        for row in indexed_frame:
            row_string = ""
            for pixel in row:
                row_string += ASCII_COLOURMAP[int(pixel)]
            ascii_frame.append(row_string)
        all_ascii_frames.append(ascii_frame)
        frame_count += 1
        print(f"{frame_count}/{total}", end="\r")

    return all_ascii_frames

def store_frames(file, frames):
    with open(file, "w") as f:
        for frame in frames:
            for row in frame:
                f.write(str(row)+"\n")
        f.close()

def draw_video(frames, framerate):
    timer = fpstimer.FPSTimer(framerate)

    for frame_number in range(len(frames)):
        frame = ""
        for row in frames[frame_number]:
            frame+= row+"\n"
        print(frame)
        timer.sleep()
        os.system('cls' if os.name == 'nt' else 'clear')

print("Decoding File")
video_obj = create_video_obj()

video_fps = video_obj.get_avg_fps()
print(video_fps)
requested_framerate = int(input("Enter framerate: "))
if requested_framerate > video_fps:
    requested_framerate = video_fps
elif requested_framerate <= 0:
    requested_framerate = 1

print("Converting to arr")
frames = video_to_arr(video_obj, frame_skip=int(video_fps//requested_framerate))

print("Converting to Greyscale")
frames = convert_video_to_GS(frames)

print("Converting to ascii")
frames = video_to_ascii(frames, reverse_map = True)

input("Press enter to start: ")
os.system('cls' if os.name == 'nt' else 'clear')

sound = playsound("tester.mp3", block=False)

draw_video(frames, requested_framerate)
os.system('cls' if os.name == 'nt' else 'clear')