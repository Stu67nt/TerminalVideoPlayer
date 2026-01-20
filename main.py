import yt_dlp
import numpy
from decord import VideoReader
from decord import cpu, gpu
import os
import fpstimer
import sys
from playsound3 import playsound

URLS = ['https://www.youtube.com/watch?v=FtutLA63Cp8']
YDL_VID = {'format': 'bestvideo'}
YDL_AUD = {'format': 'bestaudio'}

def downloader(ydl_opts: dict, urls: list):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(URLS)
    return error_code

def create_video_obj(video_file: str):
    """
    Converts a video file in a processable video object
    :param video_file: File path for video file either relevative or exact.
    :return: decord VideoReader Object
    """
    with open(video_file, 'rb') as f:
        try:
            vr = VideoReader(f, ctx=cpu(0), width=os.get_terminal_size().columns, height=os.get_terminal_size().lines)
        except OSError:  # Caused when running program in an IDE
            print("Could not get terminal size defaulting to 144p resolution")
            vr = VideoReader(f, ctx=cpu(0), width=256, height=144)
        f.close()
    return vr

def video_to_arr(vr, frame_skip: int=4):
    """
    Converts Video Object into a list of RGB frames which are each numpy arrays.
    :param vr: decord VideoReader Object
    :param frame_skip: Determines how many frames should be skipped for each frame processed
    :return: list of frames each held in a numpy array
    """
    print("Converting to arr")
    all_frames = []

    for i in range(0,len(vr),frame_skip):
        frame = vr[i].asnumpy()
        all_frames.append(frame)
        print(f"{i}/{len(vr)}", end="\r")
    return all_frames


def convert_video_to_GS(frames: list):
    """
    Returns list of greyscaled frames in the video
    :param frames: list of RBG numpy frames
    :return: list of greyscaled numpy frames
    """
    print("Converting to Greyscale")
    frame_count = 0
    total = len(frames)
    for current_frame in frames:
        # vector method. Applies calc to each pixel of each row. 0, 1, 2 represent red green and blye respectively
        current_frame = (current_frame[:,:,0]*0.299)+(current_frame[:,:,1]*0.587)+(current_frame[:,:,2]*0.114)
        frames[frame_count] = current_frame
        frame_count += 1
        print(f"{frame_count}/{total}", end="\r")
    return frames

def video_to_ascii(frames, resolution_mode: str = "h", reverse_map: str = "y"):
    """
    :param frames: List of greyscaled numpy frames
    :param resolution_mode: accepts 'h' or 'l'. Determines how large the colourmap should be (70 chars vs 10).
    Larger colourmap is better for higher video resolutions
    :param reverse_map: accepts 'y' or 'n'. Determines whether the colourmap should be reversed depending on terminal
    style.
    :return: list of ascii frames in a 2d list. List structure as follows. Video consists of frames which consists
     of rows.
    """
    print("Converting to ascii")
    if resolution_mode == "h":
        ASCII_COLOURMAP = list(r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^`'. ")
    else:
        ASCII_COLOURMAP = list(r"@%#*+=-:. ")
    if reverse_map == "y":
        ASCII_COLOURMAP.reverse()

    frame_count = 0
    total = len(frames)
    all_ascii_frames = []

    for current_frame in frames:
        ascii_frame = []
        # Formula for calcing ascii value stolen from stackoverflow
        # colourmap length subtracted from 1 due to potential index errors.
        indexed_frame = ((current_frame[:] * (len(ASCII_COLOURMAP)-1)) // 255)

        for row in indexed_frame:
            # generates list of each char in the row then adds it to the string at once.
            row_string = "".join(ASCII_COLOURMAP[int(p)] for p in row)
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
    """
    :param frames: ASCIIfied frames in a 2D list
    :param framerate: How fast the video should play
    :return: A good time :D
    """
    timer = fpstimer.FPSTimer(framerate)

    for frame_number in range(len(frames)):
        frame = ""
        for row in frames[frame_number]:
            frame += row+"\n"
        # Flush forces print to output as it is processing rather than wait until done processing
        print(frame, flush=True)
        timer.sleep()
        os.system('cls' if os.name == 'nt' else 'clear')


print("Any entries marked with a (*) are required. Rest can be left blank for default")

resolution_mode = input("Enter resolution mode (h/l): ").lower()
colourmap_reversed = input("Reverse Colourmap(y/n): ").lower()
enable_audio = input("Enable audio(y/n): ").lower()

if enable_audio == "y":
    audio_file = input("Enter fill file path of audio file (default no audio): ")
if colourmap_reversed != "y":
    colourmap_reversed = "n"
if resolution_mode != "h":
    resolution_mode = "l"

video_obj = None
while video_obj == None:
    try:
        video_file = input("Enter full file path of video (*): ")
        input("Adjust Resolution before pressing enter. ")
        print("Decoding File")
        video_obj = create_video_obj(video_file)
    except Exception as err:
        print(f"Ran into an error whilst truing to process the video.\n {err}")


video_fps = video_obj.get_avg_fps()
print(f"Original video framerate: {video_fps}")
requested_framerate = ""

while not requested_framerate.isdigit():
    requested_framerate = input("Enter framerate (should be a factor of num above to avoid desync): ")
requested_framerate = int(requested_framerate)

if requested_framerate > video_fps:
    requested_framerate = video_fps
    print("framerate set to video fps")
elif requested_framerate <= 0:
    requested_framerate = 1
    print("framerate set to 1 fps")

frame_skip = int(video_fps//requested_framerate)

frames = video_to_arr(video_obj, frame_skip=frame_skip)
frames = convert_video_to_GS(frames)
frames = video_to_ascii(frames, reverse_map = colourmap_reversed, resolution_mode = resolution_mode)

input("Press enter to start: ")
os.system('cls' if os.name == 'nt' else 'clear')

if enable_audio == "y":
    try:
        sound = playsound(audio_file, block=False)
    except Exception as err:
        print(f"Ran into an error whilst truing to process the video.\n {err}")

draw_video(frames, requested_framerate)
os.system('cls' if os.name == 'nt' else 'clear')