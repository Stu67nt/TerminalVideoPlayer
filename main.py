import numpy
from decord import VideoReader
from decord import cpu
import os
import fpstimer
from playsound3 import playsound
from colorama import just_fix_windows_console  # Fixes Issue with ANSII codes not working
import time

def create_video_obj(video_file: str):
    """
    Converts a video file in a processable video object
    :param video_file: File path for video file either relevative or exact.
    :return: decord VideoReader Object
    """
    with open(video_file, 'rb') as f:
        try:
            vr = VideoReader(f, width=os.get_terminal_size().columns, height=os.get_terminal_size().lines-2)
        except OSError:  # Caused when running program in an IDE
            print("Could not get terminal size defaulting to 144p resolution")
            vr = VideoReader(f, width=256, height=144)
        f.close()
    return vr

def video_to_ascii(vr, colourmap, frame_skip: int=4):
    """
    Converts Video Object into a list of RGB frames which are each numpy arrays.
    :param vr: decord VideoReader Object
    :param colourmap: numpy array of each ascii character allowed
    :param frame_skip: Determines how many frames should be skipped for each frame processed
    :return: list of frames each held in a numpy array
    """
    print("Converting to ASCII")
    # iterating though each frame in the video
    all_frames = []

    for i in range(0,len(vr), frame_skip):
        frame = vr[i].asnumpy()
        grey = frame_to_gs(frame)
        ascii = frame_to_ascii(grey, colourmap)
        all_frames.append("\n".join(ascii)+"\n")
        # Freeing up memory of processed frame data
        del frame, grey, ascii
        print(f"{i}/{len(vr)}", end="\r")
    return all_frames


def draw_video(frames: list, framerate: int):
    """
    Prints every frame in the frames list with a delay decided by framerate
    :param frames: ASCIIfied frames in a list
    :param framerate: How fast the video should play. should be a factor of the initial video framerate
    :return: A good time :D
    """
    timer = fpstimer.FPSTimer(framerate)

    for frame in frames:  # Placed here to allow preparation for the next frame whilst the current one is present.
        print("\033[H\033[3J", end="")
        print(frame, flush = True) # Might enable flush but i found it to cause flickering on some lines.
        timer.sleep()

def frame_to_gs(frame):
    """
    Greyscales a single frame and returns the frame
    :param frame: singlular RGB numpy frame
    :return: singuar Greyscaled numoy frame
    """
    # Vector Calc to convert whole frame in 1 go. Storing frame as unsigned 16 bit int
    return ((frame[:, :, 0] * 0.299) + (frame[:, :, 1] * 0.587) + (frame[:, :, 2] * 0.114)).astype(numpy.uint16)

def frame_to_ascii(frame, colourmap):
    """
    Converts a greyscaled numoy frame into an ASCII frame
    :param frame: Greyscaled numpy frame
    :param colourmap: numpy array of each ascii character allowed
    :return: ASCIIfied frame as a 1D list of strings
    """
    # Formula for calcing ascii value stolen from stackoverflow
    # colourmap length subtracted from 1 due to potential index errors.
    frame = (frame[:] * (len(colourmap)-1)) // 255
    # Maps entire row to corresponding ascii character and adds that row to the string as 1 long string.
    return ["".join(colourmap[row]) for row in frame]

def live_render(video_obj, colourmap, framerate, audio_filepath: str = None):
    """
    Live rendering option of playblack. Renders the video as it is playing.
    :param video_obj: decord VideoReader Object
    :param colourmap: numpy array of each ascii character allowed
    :param framerate: How fast the video should play. should be a factor of the initial video framerate
    :return: A good time :D
    """
    input("Press Enter to start")
    timer = fpstimer.FPSTimer(framerate)
    frame_skip = int(video_obj.get_avg_fps() // framerate)
    if audio_filepath:
        try:
            sound = playsound(audio_filepath, block=False)
        except Exception as err:
            input(f'{err} ')

    for i in range(0,len(video_obj),frame_skip):
        frame_rows = frame_to_ascii(frame_to_gs(video_obj[i].asnumpy()), colourmap)
        frame = "\n".join(frame_rows)+"\n"
        # ANSII escape character. Moves cursor to the top of the terminal and clears everything below cursor
        print("\033[H\033[3J", end="")
        print(frame, flush = True)
        timer.sleep()


def prerender(vider_object, colourmap, framerate, audio_filepath: str = None):
    """
        Renders the video before playing it back. Reccomended for watching at higher resolutions.
        :param video_obj: decord VideoReader Object
        :param colourmap: numpy array of each ascii character allowed
        :param framerate: How fast the video should play. should be a factor of the initial video framerate
        :return: A good time :D
        """
    frame_skip = int(video_obj.get_avg_fps() // framerate)

    frames = video_to_ascii(video_obj, colourmap, frame_skip=frame_skip)

    input("Press enter to start: ")
    os.system('cls' if os.name == 'nt' else 'clear')
    if audio_filepath:
        try:
            sound = playsound(audio_filepath, block=False)
        except Exception as err:
            input(f'{err} ')
    draw_video(frames, requested_framerate)
    os.system('cls' if os.name == 'nt' else 'clear')

just_fix_windows_console()  # Needed as otherwise ANSII Escape codes bug out.
render_mode = input("Live render or Pre render (l/p) (default prerender): ").lower()
quality = input("Enter quality (h/l) (l recomended) (default l): ").lower()
colourmap_reversed = input("Reverse Colourmap(y/n) (default n): ").lower()
enable_audio = input("Enable audio(y/n) (default n): ").lower()

ASCII_COLOURMAP = ""
if enable_audio == "y":
    audio_filepath = input("Enter fill file path of audio file (default no audio): ")
else: audio_filepath = None; enable_audiio = "n"

if quality == "h":
    ASCII_COLOURMAP = list(r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^`'. ")
else:
    ASCII_COLOURMAP = list(r"@%#*+=-:. ")
    quality = "l"

if colourmap_reversed == "y":
    ASCII_COLOURMAP.reverse()
else:
    colourmap_reversed = "n"

# Converting to a numpy array so numpy can do magic mapping stuff
ASCII_COLOURMAP = numpy.array(ASCII_COLOURMAP)

# Means program waits for user to enter a valid video before progressing.
video_obj = None
while video_obj == None:
    try:
        video_file = input("Enter full file path of video (required): ")
        print(f"Current Resolution: {os.get_terminal_size().columns, os.get_terminal_size().lines}")
        input("Adjust Resolution before pressing enter. ")
        os.system('cls' if os.name == 'nt' else 'clear')
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

input(f"Render Mode: {render_mode}\n"
      f"Resolution: {quality}\n"
      f"Reversed Colourmap: {colourmap_reversed}\n"
      f"Enabled Audio: {enable_audio}\n"
      f"Press enter to proceed\n")
if render_mode == "l":
    live_render(video_obj, colourmap=ASCII_COLOURMAP, framerate=requested_framerate, audio_filepath = audio_filepath)
else:
    prerender(video_obj, colourmap=ASCII_COLOURMAP, framerate=requested_framerate, audio_filepath = audio_filepath)

os.system('cls' if os.name == 'nt' else 'clear')