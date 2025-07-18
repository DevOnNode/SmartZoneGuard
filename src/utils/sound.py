import winsound
import os

def play_alert():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sounds', 'alert.wav')
    winsound.PlaySound(path, winsound.SND_FILENAME) 