import argparse
import os


class CLI:
    parser = argparse.ArgumentParser(description='An audio to video converter')
    parser.add_argument('audio_path', help='Path to the audio file')
    parser.add_argument('--background', help='Path to background image', default='background_default.png')
    parser.add_argument(
        '--video_out_path', help='Path to store video output', default=f'{os.getcwd()}/video.mp4')
    args = parser.parse_args()
