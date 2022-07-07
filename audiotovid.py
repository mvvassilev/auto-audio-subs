from cli import CLI
from voicetotext import VoiceToTextConverter
from texttovideo import TextToVideoConverter
import json
from pydub import AudioSegment

__author__ = "Momchil Vasilev (mvvassilev)"
__version__ = "1.0.0"

audio_input_path = CLI.args.audio_path
language = CLI.args.language
video_output_path = CLI.args.video_out_path
json_config = "config.json"

if __name__ == "__main__":
    print(f'Converting file {audio_input_path} to subtitle file...')
    with open(json_config) as config_file:
        config_data = json.load(config_file)
    audio_converter = VoiceToTextConverter(language)
    text_list, audio_len_list, duration = audio_converter.convert_to_text(
        audio_input_path)
    audio_len = 0
    audio = AudioSegment.from_file(audio_input_path)
    # audio len in sec
    audio_len = audio.duration_seconds
    video_converter = TextToVideoConverter(
        config_data["background_image"], duration, audio_len_list, config_data, audio_len)
    video_converter.capture(text_list, video_output_path, audio_input_path)
    print(f'Converted to {video_output_path}!')
