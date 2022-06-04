from cli import CLI
from voicetotext import VoiceToTextConverter
from texttovideo import TextToVideoConverter
import json

__author__ = "Momchil Vasilev (mvvassilev)"
__version__ = "1.0.0"

audio_input_path = CLI.args.audio_path
language = CLI.args.language
background = CLI.args.background
video_output_path = CLI.args.video_out_path
json_config = "config.json"

if __name__ == "__main__":
    print(f'Converting file {audio_input_path} to subtitle file...')
    with open(json_config) as config_file:
        config_data = json.load(config_file)
    audio_converter = VoiceToTextConverter(language)
    text_list, audio_len_list, duration = audio_converter.convert_to_text(
        audio_input_path)
    video_converter = TextToVideoConverter(
        background, duration, audio_len_list)
    video_converter.capture(text_list, video_output_path, audio_input_path)
    print(f'Converted to {video_output_path}!')
