from cli import CLI
from voicetotext import VoiceToTextConverter
from texttovideo import TextToVideoConverter

__author__ = "Momchil Vasilev (mvvassilev)"
__version__ = "1.0.0"

audio_input_path = CLI.args.audio_path
background = CLI.args.background
video_output_path = CLI.args.video_out_path

if __name__ == "__main__":
    print(f'Converting file {audio_input_path} to subtitle file...')
    audio_converter = VoiceToTextConverter()
    text_list = audio_converter.convert_to_text(audio_input_path=audio_input_path)
    video_converter = TextToVideoConverter(background)
    video_converter.capture(text_list, video_output_path)
