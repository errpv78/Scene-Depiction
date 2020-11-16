# Using SpeechRecognition
from pynput.keyboard import Key, Controller
import speech_recognition as sr
r = sr.Recognizer()
keyboard = Controller()
# r.recognize_google()
mic = sr.Microphone()
with mic as source:
    audio = r.listen(source)

try:
    query = r.recognize_google(audio)
    print(query)
    keyboard.press(Key.space)
    keyboard.release(Key.space)
except Exception as e:
    print('Nothing')
    pass