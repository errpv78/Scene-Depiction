import speech_recognition as sr
# <<<<<<< HEAD
import os
import pyttsx3

# =======
from gtts import gTTS
from googletrans import Translator
import os 
import time
# >>>>>>> c05098483bc596599a48604da6b067d344d738ab

def describe():
    #function to describe scene
    return "Not yet implemented!"

def help_v1():
    #function to help 
    return "Help is coming soon!"

r=sr.Recognizer()
# <<<<<<< HEAD
engine=pyttsx3.init()
# =======
# >>>>>>> c05098483bc596599a48604da6b067d344d738ab

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