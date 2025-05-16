import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import speech_recognition as sr
from translate import Translator
from pydub import AudioSegment
import os

# List of languages to choose from for translation
language_options = {
    'en': 'English',
    'ta': 'Tamil',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'hi': 'Hindi',
    'ja': 'Japanese',
    'zh-cn': 'Chinese (Simplified)',
    'ar': 'Arabic',
    'it': 'Italian'
}

# Function to handle speech recognition from an audio file
def recognize_from_audio_file(audio_file_path, target_lang):
    recognizer = sr.Recognizer()

    try:
        # Convert MP3 or other audio files to WAV using pydub
        if audio_file_path.endswith(".mp3"):
            audio = AudioSegment.from_mp3(audio_file_path)
            audio_file_path = "temp.wav"
            audio.export(audio_file_path, format="wav")

        with sr.AudioFile(audio_file_path) as source:
            audio = recognizer.record(source)

        # Recognize speech from the audio file
        recognized_text = recognizer.recognize_google(audio).lower()
        print(f"Recognized text: {recognized_text}")

        # Get the correct language code for translation
        language_code = list(language_options.keys())[list(language_options.values()).index(target_lang)]

        # Translate the recognized text to the selected language
        translator = Translator(to_lang=language_code)
        translated_text = translator.translate(recognized_text)

        # Update the result label with the translated text
        result_label.config(text=f"Translation: {translated_text}", fg="#28a745")  # Green for success
        feedback_label.config(text="✔ Translated", fg="#28a745")  # Green check mark for success

        # Clean up temporary file if it was created
        if audio_file_path.endswith("temp.wav"):
            os.remove(audio_file_path)

    except sr.UnknownValueError:
        result_label.config(text="Sorry, I could not understand that.", fg="red")
        feedback_label.config(text="✖ Error", fg="red")
    except sr.RequestError:
        result_label.config(text="Could not connect to the speech service.", fg="red")
        feedback_label.config(text="✖ Error", fg="red")
    except Exception as e:
        result_label.config(text="Error during processing", fg="red")
        feedback_label.config(text="✖ Error", fg="red")
        print(f"Error: {str(e)}")

# Function to open a file dialog and select an audio file
def browse_audio_file():
    audio_file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.flac *.mp3")])
    if audio_file_path:
        target_lang = language_combobox.get()  # Get the selected target language
        if target_lang == 'Select Language':
            messagebox.showerror("Error", "Please select a target language to translate.")
        else:
            recognize_from_audio_file(audio_file_path, target_lang)

# Create the main window
root = tk.Tk()
root.title("Voice Language Translator")

# Set window size and background color
root.geometry("450x350")
root.configure(bg="#F5A8B8")  # Light pink background

# Add a title label with a beautiful font and color
title_label = tk.Label(root, text="Voice Language Translator", font=("Helvetica", 16, "bold"), fg="#D8004E", bg="#F5A8B8")
title_label.pack(pady=20)

# Result label that shows the translation result
result_label = tk.Label(root, text="Upload an audio file for translation.", font=("Helvetica", 14), bg="#F5A8B8", fg="#D8004E")
result_label.pack(pady=20)

# Feedback label to show correct or incorrect symbols
feedback_label = tk.Label(root, text="✔ or ✖", font=("Helvetica", 20), bg="#F5A8B8", fg="green")
feedback_label.pack(pady=10)

# Dropdown for selecting the target language
language_label = tk.Label(root, text="Select target language:", font=("Helvetica", 12), bg="#F5A8B8")
language_label.pack(pady=10)

# ComboBox for language options
language_combobox = ttk.Combobox(root, values=list(language_options.values()), font=("Helvetica", 12))
language_combobox.set('Select Language')
language_combobox.pack(pady=10)

# Button to open the file dialog and select an audio file
browse_button = tk.Button(root, text="Upload Audio File", font=("Helvetica", 14), command=browse_audio_file, fg="white", bg="#D8004E")
browse_button.pack(pady=20)

# Start the tkinter main loop
root.mainloop()
