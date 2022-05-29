import speech_recognition as sr
from pydub import AudioSegment


class VoiceToTextConverter:

    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()

    def convert_to_text(self, audio_input_path) -> str:
        # handle mp3 conversion
        if audio_input_path.lower().endswith('.mp3'):
            audio = AudioSegment.from_mp3(audio_input_path)
            audio_input_path = audio_input_path[:-3] + 'wav'
            audio.export(audio_input_path, format='wav')

        try:
            with sr.AudioFile(audio_input_path) as audio:
                self.recognizer.adjust_for_ambient_noise(audio)
                audiodata = self.recognizer.record(audio)
            try:
                text = self.recognizer.recognize_google(
                    audio_data=audiodata, language='en-US')
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)
        return text
