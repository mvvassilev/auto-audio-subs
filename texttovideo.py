from time import sleep
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
        text = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Nam quam nunc, blandit vel, luctus pulvinar, hendrerit id, lorem. Maecenas nec odio et ante tincidunt tempus. Donec vitae sapien ut libero venenatis faucibus. Nullam quis ante. Etiam sit amet orci eget eros faucibus tincidunt. Duis leo. Sed fringilla mauris sit amet nibh. Donec sodales sagittis magna. Sed consequat, leo eget bibendum sodales, augue velit cursus nunc, Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Nam quam nunc, blandit vel, luctus pulvinar, hendrerit id, lorem. Maecenas nec odio et ante tincidunt tempus. Donec vitae sapien ut libero venenatis faucibus. Nullam quis ante. Etiam sit amet orci eget eros faucibus tincidunt. Duis leo. Sed fringilla mauris sit amet nibh. Donec sodales sagittis magna. Sed consequat, leo eget bibendum sodales, augue velit cursus nunc, Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Nam quam nunc, blandit vel, luctus pulvinar, hendrerit id, lorem. Maecenas nec odio et ante tincidunt tempus. Donec vitae sapien ut libero venenatis faucibus. Nullam quis ante. Etiam sit amet orci eget eros faucibus tincidunt. Duis leo. Sed fringilla mauris sit amet nibh. Donec sodales sagittis magna. Sed consequat, leo eget bibendum sodales, augue velit cursus nunc,"

        x, y = 0, 5

        vid_writer = cv2.VideoWriter(
            video_output_path, cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
        text_list = self.text_splitter.split_into_sentences(text)
        sentence_iterator = iter(text_list)
        for sentence in sentence_iterator:
            video_bg = cv2.imread(self.background)
            sentence += next(sentence_iterator, "") + next(sentence_iterator, "") + \
                next(sentence_iterator, "") + \
                next(sentence_iterator, "") + \
                next(sentence_iterator, "")
            # TODO: make width dynamic
            for i, line in enumerate(textwrap.wrap(sentence, width=80)):
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
            for _ in range(70):  # TODO: change frames to corr to audio lenght
                vid_writer.write(cv2.imread(f'dbg/TEMP_{i}.png'))

        vid_writer.release()
        os.system('rm -rf dbg/TEMP_*.png')  # remove temp image
        cv2.destroyAllWindows()
