from gtts import gTTS
import os

text = "빨간색"
tts = gTTS(text=text, lang='ko')
m_mpfile = text + ".mp3"
tts.save(m_mpfile)
os.system("start %s" % m_mpfile)