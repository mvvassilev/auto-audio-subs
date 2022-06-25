import cv2


class Progressbar:
    def __init__(self, video, json_config, font, background_size, duration) -> None:
        self.video = video
        self.font = font
        self.size = json_config["progressbar_size"]
        self.weight = json_config["progressbar_weight"]
        self.background_size = background_size
        self.json_config = json_config
        self.fps = 15
        self.duration = duration * self.fps

    def display_progress(self, frame, fullvid_frame, thickness, start_x, start_y) -> None:
        line_color = self.json_config["progress-bar-color:"]
        start_y -= int(thickness/2)
        end_x = int(fullvid_frame *
                    (self.background_size[0] / self.duration)) + 1
        end_y = int(start_y + thickness)
        cv2.rectangle(frame, (start_x, start_y), (end_x, end_y),
                      line_color, -1)

    def timestamp_to_sec(self, timestamp_string):
        hours, minutes, seconds = timestamp_string.split(':')
        return int(hours) * 3600 + int(minutes) * 60 + int(seconds)

    def get_progressbar_sections_len(self) -> list:
        ch_timestamps = self.json_config["chapter-timestamps"]
        sections = []
        for i in range(1, len(ch_timestamps) + 1):
            ch_time = self.timestamp_to_sec(ch_timestamps[f"{i}"])
            video_lenght = self.duration / self.fps  # divide by fps to get len in sec
            sections.append(
                int(self.background_size[0]*(ch_time/video_lenght)))
        return sections

    def display_pbar_sections(self, sections_len_list, frame):
        thickness = 10
        line_color = (255, 255, 255)  # white
        for start_x in sections_len_list:
            start_x += 5
            end_x = start_x
            start_y = self.background_size[1] - 150
            end_y = self.background_size[1] - 50
            cv2.line(frame, (start_x, start_y), (end_x, end_y),
                     line_color, thickness)

    def add_progress_bar(self, frame, fullvid_frame) -> None:
        thickness = 50
        start_x = 0
        start_y = self.background_size[1] - 100
        end_x = self.background_size[0]
        end_y = start_y
        line_color = (210, 210, 210)  # basic light grey
        cv2.line(frame, (start_x, start_y), (end_x, end_y),
                 line_color, thickness)

        # shows current progress on bar
        self.display_progress(frame, fullvid_frame,
                              thickness, start_x, start_y)

        progressbar_sections = self.get_progressbar_sections_len()
        self.display_pbar_sections(progressbar_sections, frame)

        chapter_number = 1
        for progressbar_section in progressbar_sections:
            ch_title = self.json_config["chapter-titles"][f"{chapter_number}"]
            cv2.putText(frame,
                        ch_title,
                        (progressbar_section + 60,
                         int(start_y + thickness/2 - 15)),
                        self.font,
                        self.size,
                        (0, 0, 0),  # rgb
                        self.weight,
                        cv2.LINE_AA)
            chapter_number += 1
