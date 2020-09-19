import speech_recognition as sr
from gtts import gTTS
from googletrans import Translator
import os 
import time

def describe():
    #function to describe scene
    return "Not yet implemented!"

def help_v1():
    #function to help 
    return "Help is coming soon!"

r=sr.Recognizer()

with sr.Microphone() as source:
    print("Available commands are\ndescribe\nhelp")
    print("Please speak now:")
    audio=r.listen(source)

try:

    tts_str=r.recognize_google(audio)
    print("You spoke: "+tts_str)
    if tts_str=="describe":
        text=describe()
    elif tts_str=="help":
        text=help_v1()
    else:
        text="Please Speak again!"

    myobj=gTTS(text,'en',slow=False)
    myobj.save("first.mp3")
    os.system("mpg321 first.mp3")

    time.sleep(1)
    translator=Translator(service_urls='translate.google.com')
    hi_text=translator.translate(text,dest='hi')
    myobj=gTTS(hi_text.text,'hi',slow=False)
    myobj.save("first.mp3")
    os.system("mpg321 first.mp3")



except LookupError:
    print("Network Error! Please try again later.")

except sr.UnknownValueError:
    print("Could not hear! Please try again later.")