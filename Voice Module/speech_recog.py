import speech_recognition as sr
import os
import pyttsx3


def describe():
    #function to describe scene
    tts_string="Not yet implemented!"
    print(tts_string)
    return tts_string

def help_v1():
    #function to help 
    tts_string="Help is coming soon!"
    print(tts_string)
    return tts_string

r=sr.Recognizer()
engine=pyttsx3.init()

with sr.Microphone() as source:
    print("Available commands are\ndescribe\nhelp")
    print("Please speak now:")
    audio=r.listen(source)

try:

    stt_str=r.recognize_google(audio)
    print("You spoke: "+stt_str)
    if stt_str=="describe":
        engine.say(describe())
        engine.runAndWait()
    elif stt_str=="help":
        engine.say(help_v1())
        engine.runAndWait()
    

except LookupError:
    print("Network Error! Please try again later.")

except sr.UnknownValueError:
    print("Could not hear! Please try again later.")

