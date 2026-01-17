from idlelib.debugger_r import frametable

import yt_dlp
import numpy
from decord import VideoReader
from decord import cpu, gpu
from matplotlib import pyplot as plt
import os

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
      vr = VideoReader(f, ctx=cpu(0), width=256, height=144)

    for i in range(0,len(vr),frame_skip):
        frame = vr[i].asnumpy()
        all_frames.append(frame)
    return all_frames

def convert_video_to_BW(frames):
    frame_count = 0
    total = len(frames)
    for current_frame in frames:
        row_i, column_i = 0, 0
        for row in current_frame:
            for pixel in row:
                r,g,b = pixel[0], pixel[1], pixel[2]
                if ((0.299*r)+(0.587*g)+(0.114*b)) < 128:
                    current_frame[row_i][column_i] = [0,0,0]
                else:
                    current_frame[row_i][column_i] = [255,255,255]
                column_i += 1
            column_i = 0
            row_i += 1
        frames[frame_count] = current_frame
        frame_count += 1
        print(f"{frame_count}/{total}")
    return frames

def convert_to_ascii():


def draw_video(video_frames):
    for current_frame in video_frames:
        plt.imshow(current_frame, interpolation='nearest')
        plt.show()

frames = video_to_arr(frame_skip=20)
simplified_frames = convert_video_to_BW(frames)
draw_video(simplified_frames)