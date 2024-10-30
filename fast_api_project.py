from fastapi import FastAPI, UploadFile, File
import moviepy.editor as mp
import speech_recognition as sr
import os

app = FastAPI()

@app.post("/extract_audio_text/")
async def extract_audio_text(file: UploadFile = File(...)):
    
    video_path = f"temp_{file.filename}"
    with open(video_path, "wb") as f:
        
        f.write(await file.read())

    try:
        
        video = mp.VideoFileClip(video_path)
        audio_file_path = "temp_audio.wav"
        video.audio.write_audiofile(audio_file_path)
        
        
        r = sr.Recognizer()
        with sr.AudioFile(audio_file_path) as source:
            data = r.record(source)
            text = r.recognize_google(data)
        
        
        os.remove(video_path)
        os.remove(audio_file_path)

        return {"text": text}

    except Exception as e:
        return {"error": str(e)}


