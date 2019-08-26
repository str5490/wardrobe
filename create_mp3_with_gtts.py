from gtts import gTTS
import os

try:
    sound_player_name = "wmplayer.exe"
    os.system("taskkill /f /im %s" % sound_player_name)
except:
    pass
os.chdir('voice')
os.chdir('colors')

file_name = "dark_blue"
text = "암청색"

tts = gTTS(text=text, lang='ko')
m_mpfile = file_name + ".mp3"
tts.save(m_mpfile)
os.system("start %s" % m_mpfile)
os.chdir('..')
os.chdir('..')