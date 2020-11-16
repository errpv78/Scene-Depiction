print("Loading model from disk")
import cv2
import imutils
import tensorflow as tf
import pathlib
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
from Predict_cap import predict_caption
from gtts import gTTS
import vlc
import pafy
from time import sleep
from imutils.video import FPS


url = 'https://www.youtube.com/watch?v=NX3bSUlv4Ek'
vPafy = pafy.new(url)
play = vPafy.getbest()

def start_video(video='videos/city.mp4'):
    cap = cv2.VideoCapture(video)
    # sound = MediaPlayer(play.url)
    # cap = cv2.VideoCapture(0)
    print("Video stream starting....")
    fps = FPS().start()
    frame_no = 0
    while frame_no<100:

        ret, frame = cap.read()
        # audio_frame, val = sound.get_frame()

        if ret:
            cv2.imshow("Press c to get caption", frame)
            frame_no+=1
            fps.update()


            key = cv2.waitKey(28) & 0xFF
            # if frame_no==0:
            #     key=ord('c')
            # If 'q' key is pressed, break from loop
            if frame_no==100:
                caption = predict_caption(frame)
                print(caption)
                caption = caption.replace('<unknown> ','')
                caption = caption.replace('<unknown>','')
                print(caption)
                # sleep(3)
                file = gTTS(text=caption, lang='en')
                file.save('hello.mp3')
                p = vlc.MediaPlayer('hello.mp3')
                p.play()
                sleep(2)
                frame_no = 0
                # print(caption)
        else:
            break
        if key == ord("q"):
            break
        # if val != 'eof' and audio_frame is not None:
            # audio
            # img, t = audio_frame

    fps.stop()
    print("Elapsed time: {:.2f}".format(fps.elapsed()))
    print("Approx. FPS: {:.2f}".format(fps.fps()))

    cv2.destroyAllWindows()
    cap.release()

start_video(play.url)
# start_video()