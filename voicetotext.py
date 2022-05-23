import speech_recognition as sr

class VoiceToTextConverter:
    
    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()

    def convert_to_text(self, audio_input_path) -> str:
        try:
            with sr.AudioFile(audio_input_path) as audio:
                self.recognizer.adjust_for_ambient_noise(audio)
                audiodata = self.recognizer.record(audio)
            try:
                text = self.recognizer.recognize_google(  # TODO: use bing
                    audio_data=audiodata, language='en-US')
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)
        return text