import numpy
from decord import VideoReader
from decord import cpu
import os
import fpstimer
from playsound3 import playsound
from colorama import just_fix_windows_console  # Fixes Issue with ANSII codes not working

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

def video_to_ascii(vr, colourmap, frame_skip: int=4):
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
        grey = frame_to_gs(frame)
        ascii = frame_to_ascii(grey, colourmap)
        all_frames.append(ascii)
        del frame, grey, ascii
        print(f"{i}/{len(vr)}", end="\r")
    return all_frames


"""
def convert_video_to_GS(frames: list):
    
    Returns list of greyscaled frames in the video
    :param frames: list of RBG numpy frames
    :return: list of greyscaled numpy frames
    
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

def video_to_ascii(frames, colourmap):
    
    :param frames: List of greyscaled numpy frames
    :param colourmap: determines the ascii characters avaliable for pixels to be mapped to
    :return: list of ascii frames in a 2d list. List structure as follows. Video consists of frames which consists
     of rows.

    print("Converting to ascii")
    frame_count = 0
    total = len(frames)
    all_ascii_frames = []

    for current_frame in frames:
        frame = ((current_frame[:] * (len(colourmap) - 1)) // 255).astype(numpy.uint8)
        # Fancy numpy shit happens here
        all_ascii_frames.append(["".join(colourmap[row]) for row in frame])
         
        ascii_frame = []
        # Formula for calcing ascii value stolen from stackoverflow
        # colourmap length subtracted from 1 due to potential index errors.
        indexed_frame = (current_frame[:] * (len(ASCII_COLOURMAP)-1)) // 255

        for row in indexed_frame:
            # generates list of each char in the row then adds it to the string at once.
            row_string = "".join(ASCII_COLOURMAP[int(p)] for p in row)
            ascii_frame.append(row_string)
        
        frame_count += 1
        print(f"{frame_count}/{total}", end="\r")

    return all_ascii_frames
"""


def draw_video(frames, framerate: int):
    """
    :param frames: ASCIIfied frames in a 2D list
    :param framerate: How fast the video should play. ideally a factor of the initial video framerate
    :return: A good time :D
    """
    timer = fpstimer.FPSTimer(framerate)

    for frame_number in range(len(frames)):
        frame = ""
        for row in frames[frame_number]:
            frame += "\n"+row
        timer.sleep()
        print("\033[H\033[3J", end="")
        print(frame)

def frame_to_gs(frame):
    """
    Greyscales a single frame and returns the frame
    :param frame: singlular RGB numpy frame
    :return: singuar Greyscaled numoy frame
    """
    return ((frame[:, :, 0] * 0.299) + (frame[:, :, 1] * 0.587) + (frame[:, :, 2] * 0.114)).astype('int64')

def frame_to_ascii(frame, colourmap):
    """
    Converts a greyscaled numoy frame into an ASCII frame
    :param frame: Greyscaled numpy frame
    :param colourmap: list of characters
    :return: ASCIIfied frame as a 1D list of strings
    """
    # Formula for calcing ascii value stolen from stackoverflow
    # colourmap length subtracted from 1 due to potential index errors.
    frame = (frame[:] * (len(colourmap)-1)) // 255
    return ["".join(colourmap[row]) for row in frame]
    """for row in frame:
        # generates list of each char in the row then adds it to the string at once.
        row_string = "".join(colourmap[int(p)] for p in row)
        ascii_frame.append("\n"+row_string)
    return ascii_frame"""

"""
def structure_frame(frame: list):
    Converts ASCIIfied frame into a printable string
    :param frame: ASCIIfied frame in a 1D list of strings. Each string should represent 1 row.
    :return: String of full printable row
    return "".join(row for row in frame)
"""

def live_render(video_obj, colourmap, framerate, audio_filepath: str = None):
    """
    Live rendering option of playblack. Renders the video as it is playing.
    :param video_obj:
    :param colourmap:
    :param framerate:
    :return:
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
        frame = "".join(frame_rows)+"\n"
        timer.sleep()
        print("\033[H\033[3J", end="")
        print(frame)


def prerender(vider_object, colourmap, framerate, audio_filepath: str = None):
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

just_fix_windows_console()
print("Any entries marked with a (*) are required. Rest can be left blank for default")
render_mode = input("Live render or Pre render (l/p): ").lower()
resolution_mode = input("Enter resolution mode (h/l) (l recomended): ").lower()
colourmap_reversed = input("Reverse Colourmap(y/n): ").lower()
enable_audio = input("Enable audio(y/n): ").lower()

ASCII_COLOURMAP = ""
if enable_audio == "y":
    audio_filepath = input("Enter fill file path of audio file (default no audio): ")
else: audio_filepath = None

if resolution_mode == "h":
    ASCII_COLOURMAP = list(r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^`'. ")
else:
    ASCII_COLOURMAP = list(r"@%#*+=-:. ")

if colourmap_reversed == "y":
    ASCII_COLOURMAP.reverse()
ASCII_COLOURMAP = numpy.array(ASCII_COLOURMAP)

# Means program waits for user to enter a valid video before progressing.
video_obj = None
while video_obj == None:
    try:
        video_file = input("Enter full file path of video (*): ")
        #print(os.get_terminal_size().columns, os.get_terminal_size().lines)
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


if render_mode == "p":
    prerender(video_obj, colourmap=ASCII_COLOURMAP, framerate=requested_framerate, audio_filepath = audio_filepath)
else:
    live_render(video_obj, colourmap=ASCII_COLOURMAP, framerate=requested_framerate, audio_filepath = audio_filepath)

os.system('cls' if os.name == 'nt' else 'clear')