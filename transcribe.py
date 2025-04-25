import pyaudio
import time
import whisper
import io
import wave
import tempfile
import os
from pyperclip import copy, paste 
import send_to_bot
from re import sub
from pyautogui import hotkey
import threading

CHUNK = 1024 * 8
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

model = None
p = None
stream = None

def init():
    global model, p, stream

    try:
        model = whisper.load_model("turbo")
        print("Model loaded successfully")
    except Exception as e:
        print(f"Error loading model: {e}")
        return False

    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        output=True,
        frames_per_buffer=CHUNK
    )
    return True

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

def cleanup():
    global stream, p
    if stream:
        stream.stop_stream()
        stream.close()
    if p:
        p.terminate()

def record_and_transcribe(code, key, lang_model, language, stop_event):
    """
    Record audio until stop_event is set, then transcribe the audio
    """
    if not init():
        return "Failed to initialize audio and model"
    
    try:
        current_recording = []
        print("Recording started...")
        
        while not stop_event.is_set():
            try:
                data = stream.read(CHUNK, exception_on_overflow=False)
                current_recording.append(data)
            except Exception as e:
                print(f"Error reading audio: {e}")
                break
            time.sleep(0.01)
        
        print("Recording stopped, transcribing...")
        
        if current_recording:
            text = code
            text += transcribe_audio(current_recording)
            print(f"Transcription: {text}")
            
            response = send_to_bot.send_text(text, lang_model, key, language)
            response = sub(r"```\w*|\w*```", "", response)
            copy(response)
            
            return response
        else:
            return "No audio was recorded"
    
    finally:
        cleanup()

def main(key, lang_model, language):
    """
    Legacy function maintained for compatibility
    """
    stop_event = threading.Event()
    result = record_and_transcribe(key, lang_model, language, stop_event)
    return result