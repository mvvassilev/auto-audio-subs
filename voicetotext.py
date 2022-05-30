import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence


class VoiceToTextConverter:

    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()
        self.text_list = []

    def convert_to_text(self, audio_input_path) -> str:
        # handle mp3 conversion
        if audio_input_path.lower().endswith('.mp3'):
            audio = AudioSegment.from_mp3(audio_input_path)
            audio_input_path = audio_input_path[:-3] + 'wav'
            audio.export(audio_input_path, format='wav')

        try:
            # split audio to sentences
            chunks = split_on_silence(
                AudioSegment.from_wav(audio_input_path),
                min_silence_len=400,
                silence_thresh=-55,
                keep_silence=10)
            iterator = 0
            for chunk in chunks:
                audio_file = f'dbg/audio_chunks/chunk_{iterator}.wav'
                chunk.export(audio_file, bitrate='192k', format="wav")
                with sr.AudioFile(audio_file) as audio:
                    self.recognizer.adjust_for_ambient_noise(audio)
                    audiodata = self.recognizer.record(audio)
                    try:
                        self.text_list.append(self.recognizer.recognize_google(
                            audio_data=audiodata, language='en-US'))
                    except Exception as e:
                        print(e)
                iterator += 1
        except Exception as e:
            print(e)
        return self.text_list
