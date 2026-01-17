import yt_dlp
import numpy
from decord import VideoReader
from decord import cpu, gpu
from matplotlib import pyplot as plt
import os
import fpstimer
import sys

URLS = ['https://www.youtube.com/watch?v=FtutLA63Cp8']

YDL_OPTS = {
    'format': 'bestvideo[ext=mp4]/bestvideo'
}

def downloader(ydl_opts: dict, urls: list):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(URLS)
    return error_code


def video_to_arr(video_file: str="tester.mp4", frame_skip: int=4):
    all_frames = []
    with open('tester.mp4', 'rb') as f:
      vr = VideoReader(f, ctx=cpu(0), width=256, height=144, num_threads=4)

    for i in range(0,len(vr),frame_skip):
        frame = vr[i].asnumpy()
        all_frames.append(frame)
        print(f"{i}/{len(vr)}", end="\r")
    return all_frames


def convert_video_to_GS(frames):
    frame_count = 0
    total = len(frames)
    for current_frame in frames:
        gs_frame = numpy.zeros((len(current_frame), len(current_frame[0]),1))
        row_i, column_i = 0, 0
        for row in current_frame:
            for pixel in row:
                r,g,b = pixel[0], pixel[1], pixel[2]
                grey_val = (0.299*r)+(0.587*g)+(0.114*b)
                gs_frame[row_i][column_i] = grey_val
                column_i += 1
            column_i = 0
            row_i += 1
        frames[frame_count] = gs_frame
        frame_count += 1
        print(f"{frame_count}/{total}", end="\r")
    return frames

def video_to_ascii(frames):
    ASCII_COLOURMAP = list(" .-:=+*#@")
    frame_count = 0
    total = len(frames)
    all_ascii_frames = []
    for current_frame in frames:
        ascii_frame = []
        for row in current_frame:
            row_string = ""
            for pixel in row:
                x = sum(pixel) // 3  # integer division
                x = (x * len(ASCII_COLOURMAP)) // 255  # rescaling
                row_string += ASCII_COLOURMAP[int(x)]
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

def draw_video_matplot(frames):
    for current_frame in frames:
        plt.imshow(current_frame, interpolation='nearest', cmap="gray")
        plt.show()

framerate = int(input("Enter framerate: "))
if framerate > 60:
    framerate = 60
print("Converting to arr")
frames = video_to_arr(frame_skip=int(60/framerate))
print("Converting to BW")
simplified_frames = convert_video_to_GS(frames)
print("Converting to ascii")
ascii_frames = video_to_ascii(simplified_frames)
input("Press enter to start")
draw_video(ascii_frames, framerate)