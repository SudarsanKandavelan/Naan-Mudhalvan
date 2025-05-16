import tkinter as tk
from tkinter import filedialog, messagebox
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


def save_note():
    note_text = text_area.get("1.0", "end-1c") 
    if note_text.strip() == "":
        messagebox.showwarning("Empty Note", "Please load an audio file first.")
    else:
        with open("notes.txt", "a") as file:
            file.write(note_text + "\n\n") 
        messagebox.showinfo("Success", "Note saved successfully!")
        text_area.delete("1.0", "end")  


def clear_note():
    text_area.delete("1.0", "end")  


root = tk.Tk()
root.title("Voice Notes and Memo System (Audio File Input)")


root.geometry("600x450")
root.configure(bg="#FFEEF1")  


title_label = tk.Label(root, text="Voice Notes and Memo", font=("Arial", 18, "bold"), fg="#D32F2F", bg="#FFEEF1")
title_label.pack(pady=20)


text_area = tk.Text(root, wrap=tk.WORD, width=50, height=10, font=("Arial", 12), bg="#FFFFFF", fg="#333333", bd=2, relief="solid", padx=10, pady=10)
text_area.pack(padx=20, pady=20)


def create_button(text, command, bg_color, fg_color):
    button = tk.Button(root, text=text, command=command, font=("Arial", 14), width=20, height=2, bd=0, fg=fg_color, bg=bg_color, relief="flat", activebackground="#D32F2F", activeforeground="white")
    button.pack(pady=10)


browse_button = create_button("Browse Audio File", browse_audio_file, "#FF6F61", "white")  # Reddish-pink
save_button = create_button("Save Note", save_note, "#D32F2F", "white")  # Darker reddish-pink
clear_button = create_button("Clear Note", clear_note, "#FF4081", "white")  # Light pink


root.mainloop()
