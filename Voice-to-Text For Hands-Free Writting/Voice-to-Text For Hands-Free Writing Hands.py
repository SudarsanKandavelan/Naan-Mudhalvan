import speech_recognition as sr
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk


def recognize_speech_from_file():
   
    result_text.set("")
    progress_bar.start()  

    recognizer = sr.Recognizer()

   
    audio_file_path = file_path.get()

    try:
       
        with sr.AudioFile(audio_file_path) as source:
            print("Processing audio file...")
            audio = recognizer.record(source)  

       
        print("Recognizing speech...")
        text = recognizer.recognize_google(audio)
        result_text.set("You said: " + text)  

    except FileNotFoundError:
        messagebox.showerror("Error", f"Error: The file '{audio_file_path}' was not found.")
    except sr.UnknownValueError:
        messagebox.showerror("Error", "Sorry, I could not understand the audio.")
    except sr.RequestError:
        messagebox.showerror("Error", "Could not request results from Google Speech Recognition service; check your internet connection.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
    finally:
        progress_bar.stop()  


def browse_file():
    file_path.set(filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")]))  

def clear_output():
    file_path.set("") 
    result_text.set("") 
    progress_bar.stop()  
    entry_file.delete(0, tk.END) 


root = tk.Tk()
root.title("Speech Recognition")
root.geometry("500x600")
root.configure(bg="#e6e6fa")  # Set light purple background color


header_frame = tk.Frame(root, bg="#6A0DAD", height=80)
header_frame.pack(fill="x", side="top")


header_label = tk.Label(header_frame, text="Speech Recognition from Audio", font=("Helvetica", 16, "bold"), bg="#6A0DAD", fg="white")
header_label.pack(pady=20)


content_frame = tk.Frame(root, bg="#e6e6fa") 
content_frame.pack(pady=20)


file_path = tk.StringVar()  

entry_file = tk.Entry(content_frame, textvariable=file_path, width=40, font=("Helvetica", 12), bd=2, relief="solid")
entry_file.grid(row=0, column=0, padx=10)

browse_button = tk.Button(content_frame, text="Browse", command=browse_file, font=("Helvetica", 12), bg="#6A0DAD", fg="white", relief="flat", width=10)
browse_button.grid(row=0, column=1)

# Add a button to trigger speech recognition
recognize_button = tk.Button(content_frame, text="Start Recognition", command=recognize_speech_from_file, font=("Helvetica", 12), bg="#6A0DAD", fg="white", relief="flat", width=20, height=2)
recognize_button.grid(row=1, column=0, columnspan=2, pady=20)

# Add a progress bar to show recognition in progress
progress_bar = ttk.Progressbar(content_frame, orient="horizontal", length=200, mode="indeterminate")
progress_bar.grid(row=2, column=0, columnspan=2, pady=10)

# Add a larger text area for the recognized speech
result_text = tk.StringVar()  # Variable to hold the recognized text
result_label = tk.Label(content_frame, textvariable=result_text, font=("Helvetica", 12), bg="#f0f0f0", fg="#333", wraplength=400, height=6, relief="solid", anchor="nw", padx=10, pady=10)
result_label.grid(row=3, column=0, columnspan=2, pady=20, sticky="nsew")

# Add a Clear button to reset the GUI with a different color (blue)
clear_button = tk.Button(content_frame, text="Clear", command=clear_output, font=("Helvetica", 12), bg="#007bff", fg="white", relief="flat", width=20, height=2)
clear_button.grid(row=4, column=0, columnspan=2, pady=10)

# Create a footer with dark purple color
footer_frame = tk.Frame(root, bg="#6A0DAD", height=50)
footer_frame.pack(fill="x", side="bottom")

footer_label = tk.Label(footer_frame, text="Speech Recognition - Powered by Python", font=("Helvetica", 10), bg="#6A0DAD", fg="white")
footer_label.pack(pady=10)

# Run the GUI event loop
root.mainloop()
