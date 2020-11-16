import pyautogui
from pynput import keyboard
from pynput.keyboard import Key, Controller, Listener
import speech_recognition as sr
from gtts import gTTS
import vlc
from Visual_Attention_Model import evaluate, plot_attention
import time
import os

r = sr.Recognizer()
# keyboard = Controller()
mic = sr.Microphone()
count = 0


def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

dirpath = os.path.dirname(os.path.abspath(__file__))
command = 'Command not found please speak again'
file = gTTS(text=command, lang='en')
file.save(dirpath + '/cmd.mp3')


# def on_press_play():
#     pass
#
# def on_release_play(key):
#     if key == keyboard.Key.space:
#         return True
#     return False


def on_release(key):
    global count, dirpath
    if key == keyboard.Key.space:
        count += 1
        if count%2==1:
            myScreenshot = pyautogui.screenshot()
            image_path = dirpath + '/temp.png'
            myScreenshot.save(image_path)
            result, attention_plot = evaluate(image_path)
            caption = ' '.join(result[:-1])
            print(caption)
            caption = caption.replace('<unknown> ', '')
            caption = caption.replace('<unknown>', '')
            print(caption)
            file = gTTS(text=caption, lang='en')
            file.save('hello.mp3')
            p = vlc.MediaPlayer('hello.mp3')
            p.play()

            # time.sleep(3)
        # with Listener(
        #         on_press=on_press_play,
        #         on_release=on_release_play) as cmd_listener:
        #     cmd_listener.join()

        # while True:
        #     with mic as source:
        #         audio = r.listen(source)
        #     try:
        #         query = r.recognize_google(audio)
        #         print(query)
        #         if query!='' and query=='play':
        #             keyboard.press(Key.space)
        #             keyboard.release(Key.space)
        #             break
        #     except Exception as e:
        #         p = vlc.MediaPlayer(dirpath+'/cmd.mp3')
        #         p.play()
        #         time.sleep(2)
        #         print('Command not found!!')

while True:
    with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()


