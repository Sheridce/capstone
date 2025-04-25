import pyaudio
import time
import whisper
import io
import wave
from keyboard import is_pressed
import tempfile
import os
from pyperclip import copy, paste 
import send_to_bot
from re import sub
from pyautogui import hotkey

CHUNK = 1024 * 8
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

def init():
    global model, p, stream


    try:
        model = whisper.load_model("turbo")
        print("Model loaded successfully")
    except Exception as e:
        print(f"Error loading model: {e}")
        exit()

    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        output=True,
        frames_per_buffer=CHUNK
    )

def transcribe_audio(audio_frames):
    if not audio_frames:
        return "No audio to transcribe"
    
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
        temp_filename = temp_file.name
    
    with wave.open(temp_filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(audio_frames))
    
    try:
        result = model.transcribe(temp_filename)
        transcription = result["text"]
    except Exception as e:
        transcription = f"Transcription error: {e}"
    finally:
        os.unlink(temp_filename)
    
    return transcription

frames = []
current_recording = []

def main(key, lang_model, language):
    init()
    try:
        recording = False
        while True:
            if is_pressed('caps lock'):
                if not recording:
                    print("Recording")
                    recording = True
                    current_recording = [] 
            
                try:
                    data = stream.read(CHUNK, exception_on_overflow=False)
                    current_recording.append(data) 
                except Exception as e:
                    print(f"Error reading audio: {e}")
        
            elif recording:
                print("Transcribing...")
                recording = False
            
                if current_recording:                
                    copy(' ')
                    hotkey('ctrl','c')
                    text = paste()
                    text += transcribe_audio(current_recording)
                    print(f"Transcription: {text}")
                    response = send_to_bot.send_text(text, lang_model, key, language)
                    response = sub(r"```\w*|\w*```", "", response)
                    copy(response)
                    hotkey('ctrl', 'v')
        
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("Stopped recording")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()