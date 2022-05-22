from cli import CLI
import speech_recognition as sr

__author__ = "Momchil Vasilev (mvvassilev)"
__version__ = "1.0.0"

audio_input_path = CLI.args.audio_path
video_output_path = CLI.args.video_path

if __name__ == "__main__":

    print(f'Converting file {audio_input_path} to subtitle file...')
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_input_path) as audio:
            recognizer.adjust_for_ambient_noise(audio)
            audiodata = recognizer.record(audio)
            try:
                text = recognizer.recognize_google(  # TODO: use bing
                    audio_data=audiodata, language='en-US')
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
