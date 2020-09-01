import cv2
import imutils
from Predict_cap import predict_caption
from gtts import gTTS
import vlc
import pafy
from ffpyplayer.player import MediaPlayer

# import gi

print("Loading model from disk")

print("Video stream starting....")
url = 'https://www.youtube.com/watch?v=NX3bSUlv4Ek'
vPafy = pafy.new(url)
play = vPafy.getbest()

cap = cv2.VideoCapture('Project-demo.mp4')
# sound = MediaPlayer(play.url)
# cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()
    # audio_frame, val = sound.get_frame()
    cv2.imshow("Press c to get caption", frame)

    key = cv2.waitKey(28) & 0xFF

    # If 'q' key is pressed, break from loop
    if key == ord("c"):
        caption = predict_caption(frame)
        print(caption)
        file = gTTS(text=caption, lang='en')
        file.save('hello.mp3')
        p = vlc.MediaPlayer('hello.mp3')
        p.play()

    if key == ord("q"):
        break
    # if val != 'eof' and audio_frame is not None:
    #     # audio
    #     img, t = audio_frame

cv2.destroyAllWindows()
cap.release()

