import argparse


class CLI:
    parser = argparse.ArgumentParser(description='An audio to video converter')
    parser.add_argument('audio_path', help='Path to the audio file')
    parser.add_argument('video_in_path', help='Path to the input video file')
    parser.add_argument(
        '--video_out_path', help='Path to store video output', default='.')
    args = parser.parse_args()