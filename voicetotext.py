import azure.cognitiveservices.speech as speechsdk
from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_silence
from math import floor


class VoiceToTextConverter:

    def __init__(self, language) -> None:
        self.speech_config = speechsdk.SpeechConfig(
            subscription="5629aa77fbdd4e85a6c4763ecebf5e58",
            region="eastus")
        self.language = language
        self.audio_duration = 0

    def convert_to_text(self, audio_input_path) -> str:
        # handle mp3 conversion
        if audio_input_path.lower().endswith('.mp3'):
            audio = AudioSegment.from_mp3(audio_input_path)
            audio_input_path = audio_input_path[:-3] + 'wav'
            audio.export(audio_input_path, format='wav')

        try:
            audio_segment = AudioSegment.from_wav(audio_input_path)
            # split audio to sentences
            self.audio_duration = audio_segment.duration_seconds
            silent_chunks = detect_silence(
                audio_segment,
                min_silence_len=900,
                silence_thresh=(audio_segment.dBFS)-16
            )
            chunks = split_on_silence(
                audio_segment,
                min_silence_len=900,
                silence_thresh=(audio_segment.dBFS)-16,
                keep_silence=200
            )
            iterator = 0
            text_list = [None] * len(chunks)
            audio_len_list = [None] * len(chunks)
            for chunk in chunks:
                silent_chunk = \
                    0.001 * (silent_chunks[iterator][1] -
                             silent_chunks[iterator][0])  # milisec to sec
                audio_len_list[iterator] = \
                    chunk.duration_seconds + \
                    silent_chunk
                audio_file = f'dbg/audio_chunks/chunk_{iterator}.wav'
                chunk.export(audio_file, format="wav")
                audio = speechsdk.AudioConfig(filename=audio_file)
                try:
                    recognizer = speechsdk.SpeechRecognizer(
                        self.speech_config, audio_config=audio)
                    output = recognizer.recognize_once_async().get()
                    text = output.text + " "
                    text_list[iterator] = text
                except Exception as e:
                    print(e)
                iterator += 1
                # conversion progress
                print(
                    f'converting audio {floor(iterator*100/len(chunks))}%...')
        except Exception as e:
            print(e)

        return text_list, audio_len_list, self.audio_duration
