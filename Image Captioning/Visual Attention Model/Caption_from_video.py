print("Loading model from disk")
import cv2
import imutils
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
from Predict_cap import predict_caption
from gtts import gTTS
import vlc
import pafy
from ffpyplayer.player import MediaPlayer


url = 'https://www.youtube.com/watch?v=NX3bSUlv4Ek'
vPafy = pafy.new(url)
play = vPafy.getbest()

def start_video(video='videos/city.mp4'):
    cap = cv2.VideoCapture(video)
    sound = MediaPlayer(play.url)
    # cap = cv2.VideoCapture(0)
    print("Video stream starting....")

    while True:

        ret, frame = cap.read()
        audio_frame, val = sound.get_frame()
        if ret:
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
        else:
            break
        if key == ord("q"):
            break
        if val != 'eof' and audio_frame is not None:
            # audio
            img, t = audio_frame

    cv2.destroyAllWindows()
    cap.release()

# start_video(play.url)
start_video()