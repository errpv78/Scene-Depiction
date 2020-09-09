import speech_recognition as sr

def describe():
    #function to describe scene
    print("Not yet implemented!")

def help_v1():
    #function to help 
    print("Help is coming soon!")

r=sr.Recognizer()

with sr.Microphone() as source:
    print("Available commands are\ndescribe\nhelp")
    print("Please speak now:")
    audio=r.listen(source)

try:

    tts_str=r.recognize_google(audio)
    print("You spoke: "+tts_str)
    if tts_str=="describe":
        describe()
    elif tts_str=="help":
        help_v1()

except LookupError:
    print("Network Error! Please try again later.")

except sr.UnknownValueError:
    print("Could not hear! Please try again later.")

