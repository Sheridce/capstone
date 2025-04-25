import whisper

try:
    model = whisper.load_model("turbo")
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")
result = model.transcribe("audio.wav")
print(result["text"])