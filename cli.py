import argparse
import os


class CLI:
    parser = argparse.ArgumentParser(description='An audio to video converter')
    parser.add_argument('audio_path', help='Path to the audio file')
    parser.add_argument(
        '--language', help='Language and accent of speaker. Check README.md for reference', default='en-US')
    parser.add_argument(
        '--video_out_path', help='Path to store video output', default=f'{os.getcwd()}/video.mp4')
    args = parser.parse_args()
