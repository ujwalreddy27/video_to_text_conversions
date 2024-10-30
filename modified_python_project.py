from fastapi import FastAPI, UploadFile, File
import moviepy.editor as mp
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
app = FastAPI()

def process_large_audio_file(audio_file_path):
    
    r = sr.Recognizer()
    sound = AudioSegment.from_wav(audio_file_path)
    
    
    chunks = split_on_silence(sound, 
                              min_silence_len=500, 
                              silence_thresh=sound.dBFS-14, 
                              keep_silence=500) 

    recognized_text = []
    
    
    for i, chunk in enumerate(chunks):
        chunk_filename = f"chunk_{i}.wav"
        chunk.export(chunk_filename, format="wav")

        
        with sr.AudioFile(chunk_filename) as source:
            audio_data = r.record(source)
            try:
                text = r.recognize_google(audio_data)
                recognized_text.append(text)
            except sr.UnknownValueError:
                recognized_text.append("[Unintelligible]")
            except sr.RequestError as e:
                recognized_text.append(f"[API error: {e}]")

        
        os.remove(chunk_filename)
    
    return " ".join(recognized_text)


@app.post("/extract_audio_text/")
async def extract_audio_text(file: UploadFile = File(...)):
    
    video_path = f"temp_{file.filename}"
    with open(video_path, "wb") as f:
        f.write(await file.read())

    try:
    
        video = mp.VideoFileClip(video_path)
        audio_file_path = "temp_audio.wav"
        video.audio.write_audiofile(audio_file_path)
        
        
        text = process_large_audio_file(audio_file_path)
        
        
        os.remove(video_path)
        os.remove(audio_file_path)

        return {"text": text}

    except Exception as e:
        return {"error": str(e)}