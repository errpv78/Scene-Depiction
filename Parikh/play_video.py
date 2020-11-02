import cv2
import numpy as np
from ffpyplayer.player import MediaPlayer
import pafy
from time import sleep
from imutils.video import FPS


def getVideoSource(source, width, height):
    cap = cv2.VideoCapture(source)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    return cap


def main():
    url = 'https://www.youtube.com/watch?v=NX3bSUlv4Ek'
    vPafy = pafy.new(url)
    play = vPafy.getbest()

    # sourcePath = "/home/err_pv/Desktop/Parikh/Projects/Minor/Scene-Depiction/Image Captioning/Visual Attention Model/city.mp4"
    sourcePath = play.url
    fps = FPS().start()

    camera = getVideoSource(sourcePath, 720, 480)
    player = MediaPlayer(sourcePath)
    fr = 0
    while True:
        ret, frame = camera.read()
        audio_frame, val = player.get_frame()

        if (ret == 0):
            print("End of video")
            break

        frame = cv2.resize(frame, (720, 480))
        cv2.imshow('Camera', frame)
        # fr+=1
        # if fr<100:
        sleep(0.0305)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # if val != 'eof' and audio_frame is not None:
        #     frame, t = audio_frame
            # print("Frame:" + str(frame) + " T: " + str(t))
        fps.update()

        # Stopping timer and displaying FPS information
    fps.stop()
    print("Elapsed time: {:.2f}".format(fps.elapsed()))
    print("Approx. FPS: {:.2f}".format(fps.fps()))

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()