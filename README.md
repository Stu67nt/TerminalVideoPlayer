# Terminal Video Player

A Python ASCII Video Player in the Terminal with the ability to play video and audio, both live and prerendered, as well as live-render the camera feed.

---
## Video Demo
[<img width="1893" height="952" alt="Screenshot 2026-01-24 161820" src="https://github.com/user-attachments/assets/9693274b-4adb-4d65-8866-8283cc4a2252" />](https://youtu.be/IqSOCbOGA5Q)
---

## Features
- Can render a live feed of your camera.
- Live rendering so you can watch videos without waiting for them to be rendered.
- Pre-rendering so you can watch videos at higher resolutions and framerates for better detail.
- Plays audio simultaneously with the video.
- No audio-video desync
- Video resolution scales with terminal size.
- Watching a video in colour and ASCII art

## Usage Tutorial
For testing convenience in the github a download of Bad Apple has been provided. You can probably just spam enter through the settings you are prompted for, and it will be fine, if you just want to see it work. For actual use, read below.

When you run the program, you will be prompted to configure a few settings each time you want to watch a video. Here is an explanation of all of them.   
| Setting | Options | Explanation |
|:-------:|:-------:|:-----------:|
| Display Camera | 'y'/'n' | This lets you display your camera feed to <br> the terminal. |
| Render Mode | 'l'/'p' | This lets you select how you want to render the <br> video. Whether to render it as you were watching <br>or to render it all beforehand. |
| Colour | 'y'/'n' | Lets you choose whether to render the video <br> coloured or using ASCII. |
| Quality | 'h'/'l' | This lets you select how many ASCII characters <br> to use when displaying the video. |
| Reverse Colourmap | 'y'/'n' | This setting lets you reverse the colourmap <br> where more full characters like "@" and "$" are <br> moved to the back, and empty characters like " " <br> and "." are moved to the front. Recommend to <br> not reverse on light coloured ones.|

### Changing Resolution
<h4>THIS IS THE MOST IMPORTANT PART, AS OTHERWISE THE OUTPUT MIGHT LOOK SHIT.</h4>
   
To change the video resolution quickly, you need to zoom out/in in the terminal and/or change the font
size. To zoom in or out quickly in the Windows terminal, hold CRTL + - to increase resolution and 
CRTL + + to decrease the resolution. You need to adjust this before decoding the video. The program
will warn you to adjust your resolution before continuing. 

### Extra explanations
Some of the options have extra things that should be remembered when using this program.

#### Render Mode 
   Live rendering lets you skip the wait to watch a video. This is fairly efficient and will probably do
   for a large majority of situations, as it does not take up more memory than it needs to, however, because
   it is both, processing and printing the video can lead to lower framerates.
   
   Alternatively, you can watch using a pre-rendered video, which requires you to wait, but lets you watch at 
   Higher resolution and framerates. However, this does use up a lot more RAM and CPU whilst rendering,   
   as it needs to remember each frame.

#### Colour
   No colour means that the video will be printed using ASCII characters, which is much more efficient, allowing
   for watchable framerates at the max resolution I tested. 

   Colour means that the video will be printed with the RGB colour in the video for that pixel. This is much less
   efficient and means that lower framerates and resolutions can be achieved compared to ASCII, but it looks much better.

#### Quality
  The main thing of note is that low quality can represent a pixel as 1 of 10 ASCII characters, whilst high
  quality can represent a pixel as 1 of 70 ASCII characters. From my testing (mostly with Bad Apple), the
  anti-aliasing is not the greatest.
 
#### Reverse Colours
  This setting should be enabled if your terminal font is white/a lighter colour, as otherwise it will look
  like the colours are reversed. Vice versa for people with a darker terminal font.

  
## Build & Run
This program has only been tested to run on Windows 11, so I cannot guarantee function on other platforms.  
But there is no reason why it should not work.
#### Download Commands
    
    pip install TerminalVideoPlayer
    terminal-video-player

OR FOR FASTER (more broken) UPDATES

    pip install git+https://github.com/Stu67nt/TerminalVideoPlayer
    terminal-video-player

## Troubleshooting & Tips
- Make sure to adjust your terminal zoom before decoding to get the desired resolution.
- If you have a light background terminal, I recommend entering "n" when prompted for reversing the colourmap. IF you are on a lighter terminal background. 

## Optimisations
This project was a continuous battle of optimisations. My first approach was iterative, iterating through each pixel and doing the calculation.
I then learned how to be able to delete things from memory in Python using del, which let me free up memory.
Then I significantly reduced the render times through vectorising the calculations for ASCII conversion and Greyscaling.
I then learned about making LUTs to be able to precalculate everything, which cut my render times by 10x for the ASCII conversion.  
For more details about the optimisations, I talk through them in my flavourtown devlogs.

## AI Usage
ChatGPT was used for this project to introduce me to optimisations, such as some of the for-loop optimisations
like when converting Greyscale to ASCII, the del keyword to free up memory, and doing basic debugging with 
mismatched variable names.
