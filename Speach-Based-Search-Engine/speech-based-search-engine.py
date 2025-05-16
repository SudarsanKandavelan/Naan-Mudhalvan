import tkinter as tk
from tkinter import filedialog, messagebox
import speech_recognition as sr
import webbrowser
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
            print("Recognizing speech from the audio file...")

            
            query = recognizer.recognize_google(audio)
            print(f"Recognized Query: {query}")
            
          
            search_url = f"https://www.google.com/search?q={query}"
            webbrowser.open(search_url)  
            print(f"Opening search results for: {query}")
            
         
            if file_path.endswith("temp.wav"):
                os.remove(file_path)

    except sr.UnknownValueError:
        print("Sorry, I couldn't understand the audio.")
        messagebox.showerror("Recognition Error", "Sorry, I couldn't understand the audio.")
    except sr.RequestError:
        print("Sorry, the speech recognition service is unavailable.")
        messagebox.showerror("Service Error", "Sorry, the speech recognition service is unavailable.")
    except Exception as e:
        print(f"Error: {str(e)}")
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


root = tk.Tk()
root.title("Speech-Based Search Engine (Audio File)")


root.geometry("500x400")
root.configure(bg="#f0e6f6") 


header_frame = tk.Frame(root, bg="#D77E8E", height=60)
header_frame.pack(fill="x")

header_label = tk.Label(header_frame, text="Speech-Based Search Engine", font=("Helvetica", 16, "bold"), fg="white", bg="#D77E8E")
header_label.pack(pady=10)


browse_button = tk.Button(root, text="Browse Audio File", command=browse_audio_file, font=("Helvetica", 12), bg="#E54D61", fg="white", relief="raised", bd=3)
browse_button.pack(pady=50)


footer_frame = tk.Frame(root, bg="#D77E8E", height=40)
footer_frame.pack(side="bottom", fill="x")

footer_label = tk.Label(footer_frame, text="© 2025 Speech Recognition Inc.", font=("Helvetica", 10), fg="white", bg="#D77E8E")
footer_label.pack(pady=5)


root.mainloop()
