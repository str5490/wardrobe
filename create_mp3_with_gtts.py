from gtts import gTTS
import os

try:
    sound_player_name = "wmplayer.exe"
    os.system("taskkill /f /im %s" % sound_player_name)
except:
    pass
os.chdir('C:/Users/str92/OneDrive/문서/git/wardrobe/voice/colors')

file_name = "black"
text = "검정색"

tts = gTTS(text=text, lang='ko')
m_mpfile = file_name + ".mp3"
tts.save(m_mpfile)
os.system("start %s" % m_mpfile)