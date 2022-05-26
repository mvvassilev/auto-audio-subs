import cv2
from progressbar import ProgressBar

heading_weight = 1
title_weight = 2
body_weight = 1

heading_font = cv2.FONT_HERSHEY_COMPLEX
title_font = cv2.FONT_HERSHEY_TRIPLEX
body_font = cv2.FONT_HERSHEY_COMPLEX


class TextToVideoConverter:

    def __init__(self, video_input_path) -> None:
        self.video_input_path = video_input_path
        self.cap = cv2.VideoCapture(self.video_input_path)

    def capture(self, text):
        progress_bar = ProgressBar(self.cap)
        (fps, frame_count, durationSec) = progress_bar.getStats()

        while(True):
            # Capture frames in the video
            ret, currentframe = self.cap.read()

            # Use putText() method for
            # inserting text on video
            cv2.putText(currentframe,
                        text,
                        (50, 50),
                        heading_font, 1,
                        (0, 0, 0),  # rgb
                        heading_weight,
                        cv2.LINE_4)

            cv2.putText(currentframe,
                        text,
                        (50, 90),
                        title_font, 1,
                        (0, 0, 0),  # rgb
                        title_weight,
                        cv2.LINE_4)

            cv2.putText(currentframe,
                        text,
                        (50, 130),
                        body_font, 1,
                        (0, 0, 0),  # rgb
                        body_weight,
                        cv2.LINE_4)

            if currentframe is not None:

                # display progress bar after saving video so that it does not ge saved with
                # current frame
                currentframe = progress_bar.displayProgressBar(currentframe)
                # display video stream
                cv2.imshow('video', currentframe)
            else:
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # release the cap object
        self.cap.release()
        # close all windows
        cv2.destroyAllWindows()
