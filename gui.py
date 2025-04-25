import tkinter as tk
import transcribe

window = tk.Tk()
window.title("Speech-to-Code")

selected_option = tk.StringVar()
selected_option.set("Claude")
model = selected_option.get()
options = ["Claude", "Gemini", "local"]

api_key = ""
language = ""

def option_changed(event):
    global model
    model = selected_option.get()

def show_model():
    label.config(text=f"Selected: {model}")

def save_key():
    global api_key
    api_key = key_textbox.get("1.0", "end-1c")
    key_label.config(text=f"API Key: {api_key}")

def save_language():
    global language
    language = lang_textbox.get("1.0", "end-1c")
    lang_label.config(text=f"Language: {language}")

def start_transcription():
    transcribe.main(api_key, model, language)

model_frame = tk.Frame(window)
model_frame.pack(pady=20)

dropdown = tk.OptionMenu(model_frame, selected_option, *options, command=option_changed)
dropdown.pack(side=tk.LEFT)

button = tk.Button(model_frame, text="confirm model", command=show_model)
button.pack(side=tk.LEFT, padx=5)

label = tk.Label(window, text="")
label.pack(padx=10, pady=20)

key_frame = tk.Frame(window)
key_frame.pack(fill=tk.X, padx=10, pady=5)

key_textbox = tk.Text(key_frame, width=40, height=1)
key_textbox.pack(side=tk.LEFT)

key_button = tk.Button(key_frame, text="confirm key", command=save_key)
key_button.pack(side=tk.LEFT, padx=10)

key_label = tk.Label(window, text="")
key_label.pack(padx=10, pady=5)

lang_frame = tk.Frame(window)
lang_frame.pack(fill=tk.X, padx=10, pady=5)

lang_textbox = tk.Text(lang_frame, width=40, height=1)
lang_textbox.pack(side=tk.LEFT)

lang_button = tk.Button(lang_frame, text="confirm language", command=save_language)
lang_button.pack(side=tk.LEFT, padx=10)

lang_label = tk.Label(window, text="")
lang_label.pack(padx=10, pady=5)

button = tk.Button(window, text="start transcription", command=start_transcription)
button.pack(pady=5)

window.mainloop()
