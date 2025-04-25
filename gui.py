import tkinter as tk
from tkinter import scrolledtext
import transcribe
import threading

class LineNumberedText(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        
        self.text = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=60, height=20)
        self.text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.line_numbers = tk.Text(self, width=4, padx=4, pady=4, takefocus=0,
                                    border=0, background='lightgrey', state='disabled')
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        self.text.bind('<KeyRelease>', self.update_line_numbers)
        self.text.bind('<MouseWheel>', self.update_line_numbers)
        self.text.bind("<<Modified>>", self.update_line_numbers)
        self.text.bind("<Configure>", self.update_line_numbers)
        
        self.update_line_numbers()
    
    def update_line_numbers(self, event=None):
        self.line_numbers.config(state='normal')
        
        self.line_numbers.delete('1.0', tk.END)
        
        num_lines = self.text.get('1.0', tk.END).count('\n')
        
        line_numbers_str = '\n'.join(str(i) for i in range(0, num_lines))
        self.line_numbers.insert('1.0', line_numbers_str)
        
        self.line_numbers.config(state='disabled')
        
        if event is not None:
            self.line_numbers.yview_moveto(self.text.yview()[0])
        
        self.text.edit_modified(False)
    
    def get_text(self):
        return self.text.get('1.0', 'end-1c')
    
    def set_text(self, text):
        self.text.delete('1.0', tk.END)
        self.text.insert('1.0', text)
        self.update_line_numbers()

class SpeechToCodeApp:
    def __init__(self, root):
        self.window = root
        self.window.title("Speech-to-Code")
        self.window.geometry("800x600")
        
        self.selected_option = tk.StringVar()
        self.selected_option.set("Claude")
        self.model = self.selected_option.get()
        self.options = ["Claude", "Gemini", "local"]
        self.api_key = ""
        self.language = ""
        
        self.transcription_text = ""
        
        self.is_recording = False
        self.transcription_thread = None
        self.stop_event = threading.Event()
        
        self.create_control_panel()
        self.create_text_area()
        
        self.text_area.text.bind('<<Modified>>', self.on_text_change)
    
    def on_text_change(self, event=None):
        self.transcription_text = self.text_area.get_text()
        self.text_area.text.edit_modified(False)
        
    def create_control_panel(self):
        control_frame = tk.Frame(self.window)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        model_frame = tk.Frame(control_frame)
        model_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(model_frame, text="Model:").pack(side=tk.LEFT)
        dropdown = tk.OptionMenu(model_frame, self.selected_option, *self.options, 
                                command=self.option_changed)
        dropdown.pack(side=tk.LEFT, padx=5)
        button = tk.Button(model_frame, text="Confirm Model", command=self.show_model)
        button.pack(side=tk.LEFT, padx=5)
        self.model_label = tk.Label(model_frame, text="")
        self.model_label.pack(side=tk.LEFT, padx=10)
        
        key_frame = tk.Frame(control_frame)
        key_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(key_frame, text="API Key:").pack(side=tk.LEFT)
        self.key_textbox = tk.Entry(key_frame, width=40)
        self.key_textbox.pack(side=tk.LEFT, padx=5)
        key_button = tk.Button(key_frame, text="Confirm Key", command=self.save_key)
        key_button.pack(side=tk.LEFT, padx=5)
        self.key_label = tk.Label(key_frame, text="")
        self.key_label.pack(side=tk.LEFT, padx=10)
        
        lang_frame = tk.Frame(control_frame)
        lang_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(lang_frame, text="Language:").pack(side=tk.LEFT)
        self.lang_textbox = tk.Entry(lang_frame, width=40)
        self.lang_textbox.pack(side=tk.LEFT, padx=5)
        lang_button = tk.Button(lang_frame, text="Confirm Language", command=self.save_language)
        lang_button.pack(side=tk.LEFT, padx=5)
        self.lang_label = tk.Label(lang_frame, text="")
        self.lang_label.pack(side=tk.LEFT, padx=10)
        
        button_frame = tk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.record_button = tk.Button(button_frame, text="Start Recording", 
                                     command=self.start_recording, bg="#4CAF50", fg="white", 
                                     padx=10, pady=5)
        self.record_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(button_frame, text="Stop Recording", 
                                   command=self.stop_recording, bg="#F44336", fg="white", 
                                   padx=10, pady=5, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.save_text_button = tk.Button(button_frame, text="Save Text", 
                                        command=self.save_text_content, bg="#2196F3", fg="white",
                                        padx=10, pady=5)
        self.save_text_button.pack(side=tk.LEFT, padx=5)
        
        self.status_label = tk.Label(button_frame, text="Not Recording", fg="red")
        self.status_label.pack(side=tk.LEFT, padx=10)
    
    def create_text_area(self):
        text_frame = tk.Frame(self.window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(text_frame, text="Transcription Results:").pack(anchor=tk.W)
        
        self.text_area = LineNumberedText(text_frame)
        self.text_area.pack(fill=tk.BOTH, expand=True)
    
    def option_changed(self, event):
        self.model = self.selected_option.get()
    
    def show_model(self):
        self.model_label.config(text=f"Selected: {self.model}")
    
    def save_key(self):
        self.api_key = self.key_textbox.get()
        self.key_label.config(text=f"API Key: {self.api_key[:5]}..." if self.api_key else "")
    
    def save_language(self):
        self.language = self.lang_textbox.get()
        self.lang_label.config(text=f"Language: {self.language}")
    
    def save_text_content(self):
        self.transcription_text = self.text_area.get_text()
        print(f"Text saved to variable: {self.transcription_text[:50]}...")
        
        self.status_label.config(text="Text Saved!", fg="blue")
        self.window.after(2000, lambda: self.status_label.config(
            text="Not Recording" if not self.is_recording else "Recording...",
            fg="red" if not self.is_recording else "green"
        ))
    
    def start_recording(self):
        self.is_recording = True
        
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Recording...", fg="green")
        
        self.stop_event.clear()
        
        self.transcription_thread = threading.Thread(
            target=self.run_transcription,
            daemon=True
        )
        self.transcription_thread.start()
    
    def stop_recording(self):
        self.is_recording = False
        
        if self.transcription_thread and self.transcription_thread.is_alive():
            self.stop_event.set()
            
            self.record_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.status_label.config(text="Not Recording", fg="red")
    
    def run_transcription(self):
        result = transcribe.record_and_transcribe(
            self.transcription_text, self.api_key, self.model, self.language, self.stop_event
        )
        
        if not result:
            result = "No transcription result received."
        
        self.window.after(0, lambda: self.text_area.set_text(result))
        
        self.transcription_text = result
        
        self.window.after(0, lambda: self.record_button.config(state=tk.NORMAL))
        self.window.after(0, lambda: self.stop_button.config(state=tk.DISABLED))
        self.window.after(0, lambda: self.status_label.config(text="Not Recording", fg="red"))
        self.is_recording = False

if __name__ == "__main__":
    window = tk.Tk()
    app = SpeechToCodeApp(window)
    window.mainloop()