import vlc
import pafy
import time

url = 'https://www.youtube.com/watch?v=NX3bSUlv4Ek'
video = pafy.new(url)
best = video.getbest()
playurl = best.url

Instance = vlc.Instance()
player = Instance.media_player_new()
media = Instance.media_new(playurl)
media.get_mrl()
player.set_media(media)
player.play()
time.sleep(60)
