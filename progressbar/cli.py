import argparse


class CLI:
    parser = argparse.ArgumentParser(
        description='Generates a progress bar for a provided video file')
    parser.add_argument('video_input', help='Path to the input video file')
    args = parser.parse_args()
