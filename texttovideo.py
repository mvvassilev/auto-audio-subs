import cv2
import os
import numpy as np
from progressbar import ProgressBar
from textsplitter import TextSplitter
import textwrap

heading_weight = 1
title_weight = 1
body_weight = 1

heading_size = 1
title_size = 1
body_size = 1

heading_font = cv2.FONT_HERSHEY_COMPLEX
title_font = cv2.FONT_HERSHEY_TRIPLEX
body_font = cv2.FONT_HERSHEY_COMPLEX


class TextToVideoConverter:

    def __init__(self, background) -> None:
        self.background = background
        self.text_splitter = TextSplitter()

    def capture(self, text, video_output_path):
        video_bg = cv2.imread(self.background)
        height, width, layers = video_bg.shape
        size = (width, height)
        # TEMP TEXT FOR TESTING PURPOSES
        text = """
            Contrary to popular belief, Lorem Ipsum is not simply random text. 
            It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. 
            Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, 
            looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, 
            and going through the cites of the word in classical literature, discovered the 
            undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of 
            "de Finibus Bonorum et Malorum" (The Extremes of Good and Evil) by Cicero, 
            written in 45 BC. This book is a treatise on the theory of ethics, very 
            popular during the Renaissance. The first line of Lorem Ipsum, "Lorem ipsum dolor 
            sit amet..", comes from a line in section 1.10.32.
            Contrary to popular belief, Lorem Ipsum is not simply random text. 
            It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. 
            Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, 
            looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, 
            and going through the cites of the word in classical literature, discovered the 
            undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of 
            "de Finibus Bonorum et Malorum" (The Extremes of Good and Evil) by Cicero, 
            written in 45 BC. This book is a treatise on the theory of ethics, very 
            popular during the Renaissance. The first line of Lorem Ipsum, "Lorem ipsum dolor 
            sit amet..", comes from a line in section 1.10.32.
            Contrary to popular belief, Lorem Ipsum is not simply random text. 
            It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. 
            Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, 
            looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, 
            and going through the cites of the word in classical literature, discovered the 
            undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of 
            "de Finibus Bonorum et Malorum" (The Extremes of Good and Evil) by Cicero, 
            written in 45 BC. This book is a treatise on the theory of ethics, very 
            popular during the Renaissance. The first line of Lorem Ipsum, "Lorem ipsum dolor 
            sit amet..", comes from a line in section 1.10.32.
            Contrary to popular belief, Lorem Ipsum is not simply random text. 
            It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. 
            Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, 
            looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, 
            and going through the cites of the word in classical literature, discovered the 
            undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of 
            "de Finibus Bonorum et Malorum" (The Extremes of Good and Evil) by Cicero, 
            written in 45 BC. This book is a treatise on the theory of ethics, very 
            popular during the Renaissance. The first line of Lorem Ipsum, "Lorem ipsum dolor 
            sit amet..", comes from a line in section 1.10.32.
        """

        x, y = 0, 5

        vid_writer = cv2.VideoWriter(
            video_output_path, cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
        text_list = self.text_splitter.split_into_sentences(text)
        for frame_text in text_list:
            # TODO: make width dynamic
            for i, line in enumerate(textwrap.wrap(frame_text, width=50)):
                video_bg = cv2.imread(self.background)
                textsize = cv2.getTextSize(
                    line, heading_font, heading_size, heading_weight)[0]

                gap = textsize[1] + 10

                y = int((video_bg.shape[0] + textsize[1]) / 2) + i * gap
                x = int((video_bg.shape[1] - textsize[0]) / 2)

                cv2.putText(video_bg,
                            line,
                            (x, y),
                            heading_font, 1,
                            (0, 0, 0),  # rgb
                            heading_weight,
                            cv2.LINE_AA)
                # create a temp image with text
                cv2.imwrite(f'dbg/TEMP_{i}.png', video_bg)
                vid_writer.write(cv2.imread(f'dbg/TEMP_{i}.png'))

        vid_writer.release()
        os.system('rm -rf dbg/TEMP_*.png')  # remove temp image
        cv2.destroyAllWindows()
