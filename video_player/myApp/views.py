from django.shortcuts import render
from django.http import HttpResponse,StreamingHttpResponse
import cv2
import time
from django.views.decorators import gzip
import os
from django.views.generic.base import TemplateView

# from .Caption_from_video import start_video
from .models import Video
from .forms import VideoForm
# Create your views here.


class video_with_html(TemplateView):
    template_name = 'video_with_html.html'


def home(request):

    return render(request, 'home.html', {})

def upload_video(request):
    if request.method=='POST':
        form = VideoForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
        lastvideo = Video.objects.last()

        videofile = lastvideo.videofile

        context = {'videofile': videofile,
                   'form': form
                   }
        return render(request, 'video_with_html.html', context)

    else:
        form = VideoForm()
        context = {'form': form
                   }
        return render(request, 'upload_video.html', context)


def live_stream(request):
    return play_video(request)

def play_recorded_video(request):
    return play_video(request, video_name='city.mp4')

# def play_video2(request):
#     return render(request, '')

class VideoCamera(object):
    def __init__(self, video_name=None):
        if video_name==None:
            self.video = cv2.VideoCapture(0)
        else:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            video_path = dir_path + "/" + video_name
            self.video = cv2.VideoCapture(video_path)
    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret,image = self.video.read()
        k = cv2.waitKey(0) &0xFF
        if k==ord('q'):
            del (self)
            return None
        try:
            ret,jpeg = cv2.imencode('.jpg',image)
        except:
            del(self)
            return None
        return jpeg.tobytes()

def gen(camera):
    while True:
        try:
            frame = camera.get_frame()

            yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n'+frame)
            yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        except:
            break

@gzip.gzip_page
def play_video(request, video_name=None):
    try:
        if video_name==None:
            return StreamingHttpResponse(gen(VideoCamera()), content_type="multipart/x-mixed-replace;boundary=frame")
        else:
            return StreamingHttpResponse(gen(VideoCamera(video_name=video_name)), content_type="multipart/x-mixed-replace;boundary=frame")
    except HttpResponseServerError as e:
        print("aborted")