import numpy
from decord import VideoReader, AudioReader
from decord import cpu
import os
from colorama import just_fix_windows_console  # Fixes Issue with ANSII codes not working
import time
import cv2 as cv
import sounddevice

def create_video_obj(video_file: str):
	"""
	Converts a video file in a processable video object
	:param video_file: File path for video file either relevative or exact.
	:return: decord VideoReader Object
	"""
	with open(video_file, 'rb') as f:
		try:
			vr = VideoReader(f, width=os.get_terminal_size().columns, height=os.get_terminal_size().lines-2)
			print(os.get_terminal_size().columns, os.get_terminal_size().lines-2)
		except OSError:  # Caused when running program in an IDE
			print("Could not get terminal size defaulting to 144p resolution")
			vr = VideoReader(f, width=256, height=144)
		f.close()
	return vr

def extract_audio(video_file: str):
	"""
	Converts a video file in numpy array for play
	:param video_file: File path for video file either relevative or exact.
	:return: decord AudioReader Object in numpy array format
	"""
	ar = AudioReader(video_file, ctx=cpu(0), sample_rate=44100, mono=True)
	samples = ar[:].asnumpy()
	return samples

def video_to_ascii(vr, colourmap, frame_skip: int=4, is_coloured = False):
	"""
	Converts Video Object into a list of RGB frames which are each numpy arrays.
	:param vr: decord VideoReader Object
	:param colourmap: numpy array of each ascii character allowed
	:param frame_skip: Determines how many frames should be skipped for each frame processed
	:param is_coloured: Determines whether to render the video in colour or not.
	:return: list of frames each held in a numpy array
	"""
	print("Converting Video")
	# iterating though each frame in the video
	all_frames = []
	if not is_coloured:
		for i in range(0,len(vr), frame_skip):
			try:
				frame = vr[i].asnumpy()
				grey = frame_to_gs(frame)
				ascii_frame = frame_to_ascii(grey, colourmap)
				all_frames.append(ascii_frame)
				# Freeing up memory of processed frame data
				del frame, grey, ascii_frame
				print(f"{i}/{len(vr)}", end="\r")
			except Exception as err:
				print()
				print(f"{err}", end="\r")
	else:
		for i in range(0,len(vr), frame_skip):
			try:
				frame = vr[i].asnumpy()
				coloured_frame = colour_frame(frame, colourmap)
				all_frames.append(coloured_frame)
				# Freeing up memory of processed frame data
				del frame, coloured_frame
				print(f"{i}/{len(vr)}", end="\r")
			except Exception as err:
				print()
				print(f"{err}", end="\r")

	return all_frames

def draw_video(frames: list, framerate: int):
	"""
	Prints every frame in the frames list with a delay decided by framerate
	:param frames: ASCIIfied frames in a list
	:param framerate: How fast the video should play. should be a factor of the initial video framerate
	:return: A good time :D
	"""

	target_secs = 1.0 / framerate  # Target amount of time spent rendering frame
	i = 0
	vid_len = len(frames)
	start_time = time.perf_counter()  # Inital time to compare against

	while i < vid_len:  # Stops when end of video reached
		print("\033[H", end="")
		print(frames[i], flush=True)
		elapsed_time = time.perf_counter() - start_time
		expected_frame = int(elapsed_time / target_secs)  # Calculates frame we should be on
		i = max(i + 1, expected_frame)
		# translates to start time of the video + seconds of video passed
		next_frame_time = start_time + (i * target_secs)

		sleep_dur = next_frame_time - time.perf_counter()

		# Sleep due can be negative
		if sleep_dur > 0:
			time.sleep(sleep_dur)

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
	# Once frame is converted the colourmap is applied to whole frame
	frame = colourmap[((frame[:] * (len(colourmap)-1)) // 255).astype(numpy.uint8)]
	# Maps entire row to corresponding ascii character and adds that row to the string as 1 long string.
	# frame is stiill in raw bytes so we need to decode it
	return frame.tobytes().decode()

def colour_frame(frame, colourmap):
	"""
	Assigns each pixel in the frame a colour and returns that pixel as 1 long string
	:param frame:
	:param colourmap:
	:return:
	"""
	r = colourmap[0][frame[:, :, 0]]
	g = colourmap[1][frame[:, :, 1]]
	b = colourmap[2][frame[:, :, 2]]

	return "".join((r+g+b).ravel())

def live_render(video_obj, colourmap, audio, is_coloured = False):
	"""
	Live rendering option of playblack. Renders the video as it is playing.
	:param video_obj: decord VideoReader Object
	:param colourmap: numpy array of each ascii/colours character allowed
	:param audio: decord AudioReader Object in numpy array
	:param is_coloured: Determines whether to render the fideo in colour or using ASCII
	:return: A good time :D
	"""
	fps = video_obj.get_avg_fps()
	target_secs = 1.0 / fps
	i = 0
	delay = 0
	vid_len = len(video_obj)

	start_time = time.perf_counter()
	try:
		sounddevice.play(audio.T)
	except:
		pass

	if not is_coloured:
		while i < vid_len:
			t1 = time.perf_counter()
			frame = frame_to_ascii(frame_to_gs(video_obj[i].asnumpy()), colourmap)
			# ANSII escape character. Moves cursor to the top of the terminal and clears everything below cursor
			print("\033[H", end="")
			print(frame)

			elapsed_time = time.perf_counter()-start_time
			expected_frame = int(elapsed_time / target_secs)
			i = max(i + 1, expected_frame)
			next_frame_time = start_time + (i*target_secs)

			sleep_dur = next_frame_time - time.perf_counter()

			if sleep_dur > 0:
				time.sleep(sleep_dur)
	else:
		while i < vid_len:
			t1 = time.perf_counter()
			frame = colour_frame(video_obj[i].asnumpy(), colourmap)
			# ANSII escape character. Moves cursor to the top of the terminal and clears everything below cursor
			print("\033[H", end="")
			print(frame)
			elapsed_time = time.perf_counter() - start_time
			expected_frame = int(elapsed_time / target_secs)
			i = max(i + 1, expected_frame)
			next_frame_time = start_time + (i * target_secs)

			sleep_dur = next_frame_time - time.perf_counter()

			if sleep_dur > 0:
				time.sleep(sleep_dur)
	os.system('cls' if os.name == 'nt' else 'clear')

def prerender(video_obj, colourmap, framerate, audio, is_coloured = False):
	"""
		Renders the video before playing it back. Reccomended for watching at higher resolutions.
		:param video_obj: decord VideoReader Object
		:param colourmap: numpy array of each ascii character allowed
		:param audio: decord AudioReader Object in numpy array
		:param is_coloured: Determines whether to render the fideo in colour or using ASCII
		:return: A good time :D
		"""
	frame_skip = int(video_obj.get_avg_fps() // framerate)
	frames = video_to_ascii(video_obj, colourmap, frame_skip=frame_skip, is_coloured=is_coloured)

	input("Press enter to start: ")
	os.system('cls' if os.name == 'nt' else 'clear')
	try:
		sounddevice.play(audio.T)
	except:
		pass
	draw_video(frames, framerate)
	os.system('cls' if os.name == 'nt' else 'clear')

def terminal_camera(colourmap, is_coloured):
	cap = cv.VideoCapture(0)
	if not cap.isOpened():
		print("Cannot open camera")
	while True:
		ret, frame = cap.read()
		frame = cv.resize(frame, (os.get_terminal_size().columns, os.get_terminal_size().lines-2))
		frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

		if not ret:
			print("Can't receive frame (stream end?). Exiting ...")
			break

		if not is_coloured:
			frame = frame_to_ascii(frame_to_gs(frame), colourmap)
			# ANSII escape character. Moves cursor to the top of the terminal and clears everything below cursor
			print("\033[H", end="")
			print(frame)
		else:
			frame = colour_frame(frame, colourmap)
			# ANSII escape character. Moves cursor to the top of the terminal and clears everything below cursor
			print("\033[H", end="")
			print(frame)

	cap.release()
	cv.destroyAllWindows()

def main():
	quality = "N/A"
	colourmap_reversed = "N/A"
	render_mode = "N/A"
	video_fps = "N/A"
	video_obj = None
	audio_obj = None

	just_fix_windows_console()  # Needed as otherwise ANSII Escape codes bug out.
	camera = input("Display camera? (y/n) (default n): ").lower()
	if camera != "y":
		camera = "n"
		render_mode = input("Live render or Pre render (l/p) (default live (l)): ").lower()

	colour = input("Use colour (y/n) (default n): ").lower()
	if colour != "y":
		quality = input("Enter quality (h/l) (l recomended) (default l): ").lower()
		colourmap_reversed = input("Reverse Colourmap(y/n) (default y): ").lower()

	ASCII_COLOURMAP = ""

	if colour != "y":
		if quality == "h":
			ASCII_COLOURMAP = r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^`'. "
		else:
			ASCII_COLOURMAP = r"@%#*+=-:. "
			quality = "l"

		if colourmap_reversed == "n":
			pass
		else:
			ASCII_COLOURMAP = ASCII_COLOURMAP[::-1]
			colourmap_reversed = "y"

	if camera != "y":
		if render_mode != "p":
			render_mode = "l"

	# Converting colourmap to a lookup table of raw bytes
	if colour == "y":
		R_STR = numpy.array([f"\033[38;2;{i};" for i in range(256)], dtype=object)
		G_STR = numpy.array([f"{i};" for i in range(256)], dtype=object)
		B_STR = numpy.array([f"{i}m█" for i in range(256)], dtype=object)
		lut = [R_STR, G_STR, B_STR]
		print_colours = True
	else:
		lut = numpy.frombuffer(ASCII_COLOURMAP.encode(), dtype=numpy.uint8)
		print_colours = False
		colour = "n"

	if camera == "n":
		# Means program waits for user to enter a valid video before progressing.
		while video_obj is None:
			try:
				video_file = input("Enter full file path of video (required): ").strip(r"\"").strip()
				print(f"Current Resolution: {os.get_terminal_size().columns, os.get_terminal_size().lines}")
				input("Adjust Resolution before pressing enter. \n"
					  "(Use CRTL + +/- to decrease/increase resolution)")
				os.system('cls' if os.name == 'nt' else 'clear')
				print("Extracting video")
				video_obj = create_video_obj(video_file)
			except Exception as err:
				print(f"Ran into an error whilst trying to process the video. Please try a different one.\n {err}")
			try:
				print("Extracting Audio")
				audio_obj = extract_audio(video_file)
			except Exception as err:
				print(f"Failed to extract audio from video (possibly video has no audio embedded).\n"
					  f"Playing without audio. ")
		video_fps = video_obj.get_avg_fps()

	input(f"Original video framerate: {round(video_fps)}\n"
		  f"Render Mode: {render_mode}\n"
		  f"Resolution: {quality}\n"
		  f"Reversed Colourmap: {colourmap_reversed}\n"
		  f"Colour: {colour}\n"
		  f"Press enter to proceed\n")

	if render_mode == "l":
		live_render(video_obj,
					colourmap=lut,
					audio = audio_obj,
					is_coloured=print_colours)
	elif render_mode == "p":
		prerender(video_obj,
				  colourmap=lut,
				  framerate=video_fps,
				  audio = audio_obj,
				  is_coloured=print_colours)
	elif camera == "y":
		terminal_camera(lut, print_colours)

	print("\033[0m")
	os.system('cls' if os.name == 'nt' else 'clear')

def run():
	while True:
		main()
		should_exit = input("Exit? (y/n) ").lower()
		if should_exit == "y":
			break
		os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
	run()