# Terminal Video Player

A Python ASCII Video Player in the Terminal with the ability to play video and audio both live and prerendered.

---

## Features

- Live rendering so you can watch videos without waiting for them to be rendered.
- Pre rendering so you can watch videos at higher resolutions and framerates for better detail.
- Plays audio simultaniously with the video.
- Video resolution scales with terminal size.
- Custom Framerates

## Usage Tutorial
When you run the program you will be prompted to configure a few settings each time you want to watch a video. Here is an explanation of all of them.   
| Setting | Options | Explanation |
|:-------:|:-------:|:-----------:|
| Render Mode | 'l'/'p' | This lets you select how you want to render the <br> video. Whether to render it as you ware watching <br>or to render it all beforehand. |
| Quality | 'h'/'l' | This lets you select how many ASCII characters <br> to use when displaying the video. |
| Reverse Colours | 'y'/'n' | This setting lets you reverse the colourmap where <br> more full characters like "@" and "$" are moved <br> to the back and empty characters like " " and "." <br> are moved to the front. |
| Enabled Audio | 'y'/'n' | Lets you decide whether to play audio with the video. <br> Note the audio has to be a seperate audio file <br>(ideally of the corresponding video). |
| Framerate | A Number | This lets you choose the framerate to play the video back at. |

You will need to have the video you want to watch downloaded seperately from the audio of the video.

### Changing Resolution
To change the video resolution quickly you need to zoom out/in in the terminal and/or change the font
size. To zoom in or out quickly in the Windows terminal hold CRTL+Scroll. You need to adjust this before
decoding the video. The program will warn you to adjust your resolution before continuing. 

### Extra explanations
Some of the options have extra things that should be remembered when using this program.

#### Render Mode
 --- 
   Live rendering lets you skip the wait to watch a video however is not reccomended at higher resolutions due
   to frame drops which if watching with audio can cause the audio to be ahead of the video. To avoid this I 
   reccomend not watching videos at too large resolutions, ensuring the resolution of the video file is not 
   too big (for reference I was able to watch a 480p video at 30fps with no frame drops with a terminal 
   resolution of 470x120). The most important optimisation is reducing the quality of the original video.
   
   Alternatively, you can watch using a pre rendered video which requires you to wait but lets you watch at 
   higher resolution and framerates. However, this does use up more RAM and CPU whilst rendering as it needs
   to remember each frame and I suck at optimising.

#### Quality
 --- 
  The main thing of note is that low quality can represent a pixel as 1 of 10 ASCII characters whilst high 
  can represent a pixel as 1 of 70 ASCII characters. From my testing (mostly with Bad Apple), the anti-aliasing
  is not the greatest. 
 
#### Reverse Colours
 ---
  This setting should be enabled if your terminal font is white/a lighter colour as otherwise it will look 
  like the colours are reversed. Vice versa for people with a darker terminal font.

#### Enabled Audio
 ---
  Enabling this will let you play audio along side the video. It will also prompt you to enter the filepath
  of the audio file you want to listen to but will not check if it is valid. If it is not then it will not
  play audio.

#### Framerate
 ---
  For this if you want the audio to remain synced up with the video you should select a framerate which is a
  factor of the video. Let's say you are watching a 30fps video. The factors of 30 are 1, 2, 3, 5, 6, 10, 15, 
  and 30 so choosing any of those framerates will keep the video synced with the audio (assuming the video is
  able to maintain framerate)
  
## Build & Run
### Prebuilt
Doing later
### Compile from scratch
Doing later


## Troubleshooting & Tips
- Make sure to adjust your terminal zoom before decoding to get desired resolution.
- 99% of the time you will not be able to display a resolution much larger than 480p
  in the terminal anyways from my testing so it is an easy optimisation to ensure the
  video you are rendering is 480p or less.
- If your video and audio are desyncing make sure your selected framerate is a factor
  of the framerate of the original. 

## License

This project is provided as-is, free and open-source. 

## AI Usage
AI was used for this project only to provide assistance with some optimisations such as some of the for loop
optimisations like when converting Greyscale to ASCII as well as introducing me to the del keyword to free up
memory. 
