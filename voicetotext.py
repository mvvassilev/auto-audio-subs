from numpy import floor_divide
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
from math import floor


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
            audio_segment = AudioSegment.from_wav(audio_input_path)
            # split audio to sentences
            chunks = split_on_silence(
                audio_segment,
                min_silence_len=900,
                silence_thresh=(audio_segment.dBFS)-16,
                keep_silence=200)
            iterator = 0
            text_list = [None] * len(chunks)
            for chunk in chunks:
                audio_file = f'dbg/audio_chunks/chunk_{iterator}.wav'
                chunk.export(audio_file, format="wav")
                with sr.AudioFile(audio_file) as audio:
                    audiodata = self.recognizer.record(audio)
                try:
                    text = self.recognizer.recognize_google(audiodata) + " "
                    text_list[iterator] = text
                except Exception as e:
                    print(e)
                iterator += 1
                # conversion progress
                print(
                    f'converting {floor(iterator*100/len(chunks))}%...')
        except Exception as e:
            print(e)
        return text_list
