from progressbar import Progressbar
from cli import CLI
import os
import json
import cv2
from sys import platform
import ffmpeg
from moviepy.editor import VideoFileClip

__author__ = "Momchil Vasilev (mvvassilev)"
__version__ = "1.0.0"

video_input_path = os.path.abspath(f"{CLI.args.video_input}")
json_config = os.path.abspath("../config.json")
final_video_path = "../final_video.mp4"
video_input = "video.mp4"
audio_input = "audio.mp3"


def setup_for_capture():
    # deletes "video_output_path" file if already exists (OS spec)
    if os.path.isfile(final_video_path):
        if platform == "linux" or platform == "linux2":
            os.system(f'rm -rf {final_video_path}')
        elif platform == "win32":
            os.system(f'del /f {final_video_path}')


def cleanup():
    # remove temp files
    if platform == "linux" or platform == "linux2":
        os.system(f'rm -rf {video_input}')
        os.system(f'rm -rf {audio_input}')
    elif platform == "win32":
        os.system(f'del /f {video_input}')
        os.system(f'del /f {audio_input}')
    cv2.destroyAllWindows()


if __name__ == "__main__":
    print(f"Adding Progressbar to {video_input_path}...")

    with open(json_config) as config_file:
        config_data = json.load(config_file)

    height, width, _ = cv2.imread(
        f'../{config_data["background_image"]}').shape

    vid_capture = cv2.VideoCapture(video_input_path)

    vid_writer = cv2.VideoWriter(
        video_input,
        cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),
        15,
        (width, height)
    )

    audio_clipper = VideoFileClip(video_input_path)
    audio_clipper.audio.write_audiofile(audio_input)
    duration = vid_capture.get(cv2.CAP_PROP_FRAME_COUNT)

    progressbar = Progressbar(
        video_input_path,
        config_data,
        cv2.FONT_HERSHEY_COMPLEX,
        (width, height),
        duration
    )

    print("Appending progressbar...")
    setup_for_capture()
    success, frame = vid_capture.read()
    frame_number = 0
    while success:
        progressbar.add_progress_bar(frame, frame_number)
        vid_writer.write(frame)
        success, frame = vid_capture.read()
        frame_number += 1
    vid_writer.release()

    # add audio to video file
    ffmpeg_vid = ffmpeg.input(video_input, vsync=1)
    ffmpeg_aud = ffmpeg.input(audio_input)
    ffmpeg.concat(ffmpeg_vid, ffmpeg_aud, v=1,
                  a=1).output(final_video_path).run()
    cleanup()
