from cli import CLI
from voicetotext import VoiceToTextConverter
from texttovideo import TextToVideoConverter

__author__ = "Momchil Vasilev (mvvassilev)"
__version__ = "1.0.0"

audio_input_path = CLI.args.audio_path
video_input_path = CLI.args.video_in_path
video_output_path = CLI.args.video_out_path

if __name__ == "__main__":
    print(f'Converting file {audio_input_path} to subtitle file...')
    audio_converter = VoiceToTextConverter()
    text = audio_converter.convert_to_text(audio_input_path=audio_input_path)
    print(text)
