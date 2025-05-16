import tkinter as tk
from tkinter import filedialog, messagebox
from pydub import AudioSegment
import speech_recognition as sr
import os

# Initialize the recognizer
recognizer = sr.Recognizer()

# Function to browse and load the audio file
def browse_audio_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav;*.mp3;*.flac")])
    if file_path:
        # Call the function to process the audio file
        recognize_from_audio_file(file_path)

# Function to recognize speech from the audio file
def recognize_from_audio_file(file_path):
    try:
        # Convert audio to WAV format if it's in MP3 or other formats
        if file_path.endswith(".mp3"):
            audio = AudioSegment.from_mp3(file_path)
            file_path = "temp.wav"
            audio.export(file_path, format="wav")
        
        # Use speech recognition to convert audio to text
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)  # Read the entire audio file
            print("Recognizing speech...")

            # Recognize speech using Google Web Speech API
            text = recognizer.recognize_google(audio)
            print(f"Recognized Text: {text}")
            
            # Insert the recognized text into the GUI's text box
            text_area.delete(1.0, tk.END)  # Clear any previous text
            text_area.insert(tk.END, text)  # Insert new recognized text

            # Enable the submit button after recognizing text
            submit_button.config(state=tk.NORMAL)

            # Clean up temporary files if created
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

# Function to submit the recognized text
def submit_data():
    data = text_area.get(1.0, tk.END).strip()
    if data:
        # Here, you can save the recognized text to a file or a database
        with open("data_entry.txt", "a") as f:
            f.write(f"{data}\n")
        print(f"Data saved: {data}")
        messagebox.showinfo("Success", "Data has been saved successfully!")
        text_area.delete(1.0, tk.END)  # Clear the text area after submission
        submit_button.config(state=tk.DISABLED)

# Create the main window
root = tk.Tk()
root.title("Speech-Based Data Entry System")

# Set window size
root.geometry("600x500")
root.configure(bg="white")  # No background color

# Header container
header_container = tk.Frame(root, bg="#9B4D97", pady=20)
header_container.pack(fill=tk.X)

# Title Label inside the header container
title_label = tk.Label(header_container, text="Speech-Based Data Entry", font=("Helvetica", 16, "bold"), fg="white", bg="#9B4D97")
title_label.pack()

# Main content container (for the text area and buttons)
content_container = tk.Frame(root, bg="white", pady=20)
content_container.pack(fill=tk.BOTH, expand=True)

# Create a scrollable text area to display the recognized text
text_area = tk.Text(content_container, wrap=tk.WORD, width=50, height=10, font=("Helvetica", 12), bg="#F2E6FF", fg="#4B0082", bd=2, relief="solid", padx=10, pady=10)
text_area.pack(padx=20, pady=20)

# Create a button to browse for the audio file
browse_button = tk.Button(content_container, text="Browse Audio File", command=browse_audio_file, font=("Helvetica", 12), bg="#9B4D97", fg="white", relief="raised", bd=3)
browse_button.pack(pady=10)

# Create a submit button to save the data with green color for visibility
submit_button = tk.Button(content_container, text="Submit Data", command=submit_data, font=("Helvetica", 12), bg="#4CAF50", fg="white", relief="raised", bd=3, state=tk.DISABLED)
submit_button.pack(pady=10)

# Footer container
footer_container = tk.Frame(root, bg="#9B4D97", pady=10)
footer_container.pack(fill=tk.X, side="bottom")

# Footer text
footer_label = tk.Label(footer_container, text="Data Entry System | Powered by AI", font=("Helvetica", 10), fg="white", bg="#9B4D97")
footer_label.pack()

# Start the Tkinter main loop
root.mainloop()
