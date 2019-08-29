from gtts import gTTS
import os

try:
    sound_player_name = "wmplayer.exe"
    os.system("taskkill /f /im %s" % sound_player_name)
except:
    pass
os.chdir('voice')
os.chdir('notices')

file_name = "5"
text = "옷을 넣어주세요"

tts = gTTS(text=text, lang='ko')
m_mpfile = file_name + ".mp3"
tts.save(m_mpfile)
os.system("start %s" % m_mpfile)
os.chdir('..')
os.chdir('..')