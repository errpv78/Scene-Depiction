import pyglet
import os

dir = os.path.dirname(os.path.abspath(__file__))
vidPath = dir + '/city.mp4'
print(vidPath)
window = pyglet.window.Window()
player = pyglet.media.Player()
source = pyglet.media.StreamingSource()
MediaLoad = pyglet.media.load(vidPath)

player.queue(MediaLoad)
player.play()


@window.event
def on_draw():
    if player.source and player.source.video_format:
        player.get_texture().blit(50, 50)


pyglet.app.run()