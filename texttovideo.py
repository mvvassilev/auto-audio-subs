import cv2
import os
from textsplitter import TextSplitter
import textwrap
from sys import platform
import ffmpeg
import re

heading_weight = 2
title_weight = 2
body_weight = 2

heading_size = 2
title_size = 2
body_size = 2

heading_font = cv2.FONT_HERSHEY_COMPLEX
title_font = cv2.FONT_HERSHEY_TRIPLEX
body_font = cv2.FONT_HERSHEY_COMPLEX
text_width = 50

noaudio_video_filename = "only_video.mp4"


class TextToVideoConverter:

    def __init__(self, background, duration, audio_len_list) -> None:
        self.background = background
        self.text_splitter = TextSplitter()
        self.height, self.width, _ = cv2.imread(self.background).shape
        self.duration = duration * 15  # multiply by the fps
        self.segment_lenght_list = list(audio_len_list)
        self.fullvid_frame = 0

    def add_progress_bar(self, frame) -> None:
        thickness = 20
        start_x = 0
        start_y = self.height - 100
        end_x = int(self.fullvid_frame*(self.width / self.duration))
        end_y = start_y
        cv2.line(frame, (start_x, start_y), (end_x, end_y),
                 (0, 0, 255), thickness)

    def add_next(self, value, iterator, items_count, default_value):
        for _ in range(items_count):
            value += next(iterator, default_value)
        return value

    def display_heading(self):
        pass

    def display_title(self):
        pass

    def display_frames(self, text_list):
        video_bg = cv2.imread(self.background)
        self.height, self.width, _ = video_bg.shape
        size = (self.width, self.height)

        x, y = 0, 5

        vid_writer = cv2.VideoWriter(
            noaudio_video_filename, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 15, size)
        sentence_iterator = iter(text_list)
        for sentence in sentence_iterator:
            video_bg = cv2.imread(self.background)
            sentence = self.add_next(sentence, sentence_iterator, 3, "")
            for i, line in enumerate(textwrap.wrap(sentence, text_width)):
                textsize = cv2.getTextSize(
                    line, body_font, body_size, body_weight)[0]

                gap = textsize[1] + 40

                y = int((video_bg.shape[0] + textsize[1]) / 4) + i * gap
                x = int((video_bg.shape[1] - textsize[0]) / 2)

                cv2.putText(video_bg,
                            line,
                            (x, y),
                            body_font, body_size,
                            (0, 0, 0),  # rgb
                            body_weight,
                            cv2.LINE_AA)
                # create a temp image with text
                cv2.imwrite(f'dbg/TEMP_{i}.png', video_bg)
            segment_iterator = iter(self.segment_lenght_list)
            segment_len = 0
            segment_len = self.add_next(segment_len, segment_iterator, 4, 0)
            for _ in range(int(segment_len*17)):
                current_frame = cv2.imread(f'dbg/TEMP_{i}.png')
                self.add_progress_bar(current_frame)
                vid_writer.write(current_frame)
                self.fullvid_frame += 1  # move to the next frame number
                self.add_next(segment_len, segment_iterator, 4, 0)
        vid_writer.release()

    def setup_for_capture(self, video_output_path):
        # deletes "video_output_path" file if already exists (OS spec)
        if os.path.isfile(video_output_path):
            if platform == "linux" or platform == "linux2":
                os.system(f'rm -rf {video_output_path}')
            elif platform == "win32":
                os.system(f'del /f {video_output_path}')

    def cleanup(self):
        # remove temp images and audio chunks (OS spec)
        if platform == "linux" or platform == "linux2":
            os.system('rm -rf dbg/TEMP_*.png')
            os.system('rm -rf dbg/audio_chunks/*')
            os.system(f'rm -rf {noaudio_video_filename}')
        elif platform == "win32":
            os.system('del /f dbg/TEMP_*.png')
            os.system('del /f dbg/audio_chunks/*')
            os.system(f'del /f {noaudio_video_filename}')
        cv2.destroyAllWindows()

    def capture(self, text_list, video_output_path, audio_input_path):
        # sets up env and files
        self.setup_for_capture(video_output_path)

        # writes the frames to the video
        self.display_frames(text_list)

        # add audio to video file
        ffmpeg_vid = ffmpeg.input(noaudio_video_filename)
        ffmpeg_aud = ffmpeg.input(audio_input_path)
        ffmpeg.concat(ffmpeg_vid, ffmpeg_aud, v=1,
                      a=1).output(video_output_path).run()

        self.cleanup()
