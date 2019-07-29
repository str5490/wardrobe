from gtts import gTTS
import os

file_name = "white"
test = "하양색"
tts = gTTS(text=text, lang='ko')
m_mpfile = file_name + ".mp3"
tts.save(m_mpfile)
os.system("start %s" % m_mpfile)