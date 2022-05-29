# Automatic Video Subtitles from Audio
Outputs a video file that acts as subtitles from the audio input

# Description
Takes an audio file as an input and provides a video file that consits of the speach from the audio converted into subtitled text. The conversion is done into small parts around 1-2 sentences, formatted and showing a progress bar underneath indicating how far into the audio it is.

# Usage
First make sure your python enviroment is setup properly
Install all packages in "pip_requirements.txt"
> pip install -r pip_requirements.txt

Run command:
> python audiotovid.py SAMPLE_AUDIO.mp3

The command outputs a "video.mp4" file in the working directory

# Note
Running the following displays the help menu
> python audiotovid.py --help
