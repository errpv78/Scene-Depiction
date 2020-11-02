# Using SpeechRecognition
import speech_recognition as sr
r = sr.Recognizer()
# r.recognize_google()
mic = sr.Microphone()
with mic as source:
    audio = r.listen(source)
r.recognize_google(audio)
