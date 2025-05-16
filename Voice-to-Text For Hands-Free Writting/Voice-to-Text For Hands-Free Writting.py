import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import speech_recognition as sr
from pydub import AudioSegment
import os


recognizer = sr.Recognizer()


def browse_audio_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav;*.mp3;*.flac")])
    if file_path:
     
        recognize_from_audio_file(file_path)


def recognize_from_audio_file(file_path):
    try:
       
        if file_path.endswith(".mp3"):
            audio = AudioSegment.from_mp3(file_path)
            file_path = "temp.wav"
            audio.export(file_path, format="wav")
        
      
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source) 
            print("Recognizing speech...")

          
            text = recognizer.recognize_google(audio)
            print(f"Recognized Text: {text}")
            
          
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, text)  

       
            if file_path.endswith("temp.wav"):
                os.remove(file_path)

    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        messagebox.showerror("Recognition Error", "Sorry, I could not understand the audio.")
    except sr.RequestError:
        print("Sorry, the speech recognition service is unavailable.")
        messagebox.showerror("Service Error", "Sorry, the speech recognition service is unavailable.")
    except Exception as e:
        print(f"Error: {str(e)}")
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


root = tk.Tk()
root.title("Audio to Text - Convert Audio to Speech")


root.geometry("600x500")
root.configure(bg="#F9F9F9")


title_label = tk.Label(root, text="Convert Audio to Text", font=("Helvetica", 18, "bold"), fg="#6A1B9A", bg="#F9F9F9")
title_label.pack(pady=20)


text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=12, font=("Arial", 12), bg="#F1F1F1", fg="#333333", bd=2, relief="solid")
text_area.pack(padx=20, pady=20)


browse_button = tk.Button(root, text="Browse Audio File", command=browse_audio_file, font=("Helvetica", 14), bg="#FF4081", fg="white", relief="flat", padx=15, pady=10)
browse_button.pack(pady=15)


root.config(bg="#F9F9F9")


def on_enter(e):
    browse_button['bg'] = '#F50057'

def on_leave(e):
    browse_button['bg'] = '#FF4081'

browse_button.bind("<Enter>", on_enter)
browse_button.bind("<Leave>", on_leave)
# Start the Tkinter main loop
root.mainloop()
