from gtts import gTTS
import os

try:
    sound_player_name = "wmplayer.exe"
    os.system("taskkill /f /im %s" % sound_player_name)
except:
    pass
os.chdir('voice')
os.chdir('notice')

file_name = "3"
text = "손을 접어 가리켜주세요"

tts = gTTS(text=text, lang='ko')
m_mpfile = file_name + ".mp3"
tts.save(m_mpfile)
os.system("start %s" % m_mpfile)
os.chdir('..')
os.chdir('..')