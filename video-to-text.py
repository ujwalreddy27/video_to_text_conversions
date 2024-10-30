import moviepy.editor as mp 
from tkinter.filedialog import *
import speech_recognition as sr 
vid = askopenfilename()
video = mp.VideoFileClip(vid) 
audio_file = video.audio 
audio_file.write_audiofile("demo1.wav") 
r = sr.Recognizer() 
with sr.AudioFile("demo1.wav") as source: 
    data = r.record(source) 
text = r.recognize_google(data)
print("\nThe resultant text from video is: \n") 
print(text) 