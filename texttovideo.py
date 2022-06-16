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
progressbar_weight = 1
heading_size = 2
title_size = 2
body_size = 2
progressbar_size = 1

heading_font = cv2.FONT_HERSHEY_COMPLEX
title_font = cv2.FONT_HERSHEY_TRIPLEX
body_font = cv2.FONT_HERSHEY_COMPLEX
progressbar_font = cv2.FONT_HERSHEY_COMPLEX

text_width = 50
heading_offset_y = 200
title_offset = 100
heading_height = 450

noaudio_video_filename = "only_video.mp4"


class TextToVideoConverter:

    def __init__(self, background, duration, audio_len_list, json_config) -> None:
        self.background = background
        self.json_config = json_config
        self.text_splitter = TextSplitter()
        self.height, self.width, _ = cv2.imread(self.background).shape
        self.duration = duration * 15  # multiply by the fps
        self.segment_lenght_list = list(audio_len_list)
        self.fullvid_frame = 0
        self.last_x = 0

    def timestamp_to_sec(self, timestamp_string):
        hours, minutes, seconds = timestamp_string.split(':')
        return int(hours) * 3600 + int(minutes) * 60 + int(seconds)

    def get_progressbar_sections_len(self) -> list:
        ch_timestamps = self.json_config["chapter-timestamps"]
        sections = []
        for i in range(1, len(ch_timestamps) + 1):
            ch_time = self.timestamp_to_sec(ch_timestamps[f"{i}"])
            video_lenght = self.duration / 15  # divide by fps to get len in sec
            sections.append(int(self.width*(ch_time/video_lenght)))
        return sections

    def display_progress(self, frame, thickness, start_x, start_y) -> None:
        line_color = self.json_config["progress-bar-color:"]
        start_y -= int(thickness/2)
        end_x = int(self.fullvid_frame*(self.width / self.duration))
        end_y = int(start_y + thickness)
        cv2.rectangle(frame, (start_x, start_y), (end_x, end_y),
                      line_color, -1)

    def display_pbar_sections(self, sections_len_list, frame):
        thickness = 10
        line_color = (255, 255, 255)  # white
        for start_x in sections_len_list:
            start_x += 5
            end_x = start_x
            start_y = self.height - 150
            end_y = self.height - 50
            cv2.line(frame, (start_x, start_y), (end_x, end_y),
                     line_color, thickness)

    def add_progress_bar(self, frame) -> None:
        thickness = 50
        start_x = 0
        start_y = self.height - 100
        end_x = self.width
        end_y = start_y
        line_color = (210, 210, 210)  # basic light grey
        cv2.line(frame, (start_x, start_y), (end_x, end_y),
                 line_color, thickness)

        # shows current progress on bar
        self.display_progress(frame, thickness, start_x, start_y)

        progressbar_sections = self.get_progressbar_sections_len()
        self.display_pbar_sections(progressbar_sections, frame)

        chapter_number = 1
        for progressbar_section in progressbar_sections:
            ch_title = self.json_config["chapter-titles"][f"{chapter_number}"]
            cv2.putText(frame,
                        ch_title,
                        (progressbar_section + 60,
                         int(start_y + thickness/2 - 15)),
                        progressbar_font,
                        progressbar_size,
                        (0, 0, 0),  # rgb
                        progressbar_weight,
                        cv2.LINE_AA)
            chapter_number += 1

    def add_next(self, value, iterator, items_count, default_value):
        for _ in range(items_count):
            value += next(iterator, default_value)
        return value

    def get_chapter_num(self, frame):
        chapter = 1
        total_len = int(frame / 15)
        ch_timestamps = self.json_config["chapter-timestamps"]
        for i in range(1, len(ch_timestamps) + 1):
            ch_time = self.timestamp_to_sec(ch_timestamps[f"{i}"])
            if ch_time < total_len:
                chapter = i
        return chapter

    def display_heading(self, tmp_image, video_bg, chapter_number):
        heading_number = chapter_number
        heading_name = f"CHAPTER {heading_number}"
        textsize = cv2.getTextSize(
            heading_name, heading_font, heading_size, heading_weight)[0]
        y = heading_offset_y
        x = int((self.width - textsize[0]) / 2)
        video_bg = cv2.imread(video_bg)
        cv2.putText(video_bg,
                    heading_name,
                    (x, y),
                    heading_font, heading_size,
                    (0, 0, 0),  # rgb
                    heading_weight,
                    cv2.LINE_AA)
        cv2.imwrite(tmp_image, video_bg)

    def display_title(self, tmp_image, video_bg, chapter_number):
        titles = self.json_config["chapter-titles"]
        title_name = titles[f"{chapter_number}"]
        textsize = cv2.getTextSize(
            title_name, title_font, title_size, title_weight)[0]
        y = heading_offset_y + title_offset
        x = int((self.width - textsize[0]) / 2)
        video_bg = cv2.imread(video_bg)
        cv2.putText(video_bg,
                    title_name,
                    (x, y),
                    title_font, title_size,
                    (0, 0, 0),  # rgb
                    title_weight,
                    cv2.LINE_AA)
        cv2.imwrite(tmp_image, video_bg)

    def draw_text(self, count, line, width, video_bg, is_last):
        tmp_image = f'dbg/TEMP_{count}.png'

        previous_line = line
        if not is_last:
            while((l := width-len(line)) > 0):
                line = re.sub(r"(\s+)", r"\1 ", line, count=l)
                if(line == previous_line):
                    break

        textsize = cv2.getTextSize(
            line, body_font, body_size, body_weight)[0]

        gap = textsize[1] + 40

        y = heading_height + count * gap
        x = int((self.width - textsize[0]) / 2.3)
        if not is_last:
            self.last_x = x
        x = self.last_x

        cv2.putText(video_bg,
                    line,
                    (x, y),
                    body_font, body_size,
                    (0, 0, 0),  # rgb
                    body_weight,
                    cv2.LINE_AA)
        # create a temp image with text
        cv2.imwrite(tmp_image, video_bg)

    def display_frames(self, text_list):
        video_bg = cv2.imread(self.background)
        self.height, self.width, _ = video_bg.shape
        size = (self.width, self.height)

        vid_writer = cv2.VideoWriter(
            noaudio_video_filename, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 15, size)
        sentence_iterator = iter(text_list)
        for sentence in sentence_iterator:
            video_bg = cv2.imread(self.background)
            sentence = self.add_next(sentence, sentence_iterator, 2, "")

            wrapper = textwrap.TextWrapper(width=text_width)
            dedented_text = textwrap.dedent(text=sentence)

            text = wrapper.fill(text=dedented_text)

            i = 0
            lines = text.splitlines()
            for count, line in enumerate(lines):
                is_line_last = True if count == len(lines) - 1 else False
                self.draw_text(count, line, text_width, video_bg, is_line_last)
                i += 1

            segment_iterator = iter(self.segment_lenght_list)
            segment_len = 0
            segment_len = self.add_next(segment_len, segment_iterator, 3, 0)
            for _ in range(int(segment_len*17)):
                chapter_number = self.get_chapter_num(self.fullvid_frame)
                tmp_image_no_heading = f'dbg/TEMP_{count}.png'
                tmp_image = f'dbg/TEMP_{chapter_number}_{count}.png'
                self.display_heading(
                    tmp_image, tmp_image_no_heading, chapter_number)
                self.display_title(tmp_image, tmp_image, chapter_number)
                current_frame = cv2.imread(tmp_image)
                if self.json_config["progress-bar-enabled"] == "on":
                    self.add_progress_bar(current_frame)
                vid_writer.write(current_frame)
                self.fullvid_frame += 1  # move to the next frame number
                segment_len = self.add_next(
                    segment_len, segment_iterator, 3, 0)
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
            os.system('rm -rf dbg/TEMP_*')
            os.system('rm -rf dbg/audio_chunks/*')
            os.system(f'rm -rf {noaudio_video_filename}')
        elif platform == "win32":
            os.system('del /f dbg/TEMP_*')
            os.system('del /f dbg/audio_chunks/*')
            os.system(f'del /f {noaudio_video_filename}')
        cv2.destroyAllWindows()

    def capture(self, text_list, video_output_path, audio_input_path):
        # sets up env and files
        print("Generating video file ...")
        self.setup_for_capture(video_output_path)

        # writes the frames to the video
        self.display_frames(text_list)

        # add audio to video file
        ffmpeg_vid = ffmpeg.input(noaudio_video_filename)
        ffmpeg_aud = ffmpeg.input(audio_input_path)
        ffmpeg.concat(ffmpeg_vid, ffmpeg_aud, v=1,
                      a=1).output(video_output_path).run()

        self.cleanup()
