import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import speech_recognition as sr
import pyttsx3
import webbrowser
import threading
from AppOpener import open as open_app

# ---------------- TTS ENGINE -----------------
engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    engine.say(text)
    engine.runAndWait()


# ----------------- COMMANDS -----------------
def process_command(command):
    command = command.lower()

    # ------- Websites -------
    if "youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "whatsapp" in command:
        speak("Opening WhatsApp")
        webbrowser.open("https://web.whatsapp.com")

    elif "instagram" in command:
        speak("Opening Instagram")
        webbrowser.open("https://instagram.com")

    elif "facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")

    elif "chrome" in command:
        speak("Opening Chrome")
        webbrowser.open("https://chrome.com")

    elif "spotify" in command:
        speak("Opening Spotify Web")
        webbrowser.open("https://open.spotify.com")

    elif "telegram" in command:
        speak("Opening Telegram Web")
        webbrowser.open("https://web.telegram.org")

    # ------- Applications -------
    elif "notepad" in command:
        speak("Opening Notepad")
        open_app("notepad")

    elif "vs code" in command:
        speak("Opening Visual Studio Code")
        open_app("visual studio code")

    elif "calculator" in command:
        speak("Opening Calculator")
        open_app("calculator")

    elif "telegram app" in command:
        speak("Opening Telegram")
        open_app("telegram")

    elif "spotify app" in command:
        speak("Opening Spotify App")
        open_app("spotify")

    else:
        speak("Sorry, I cannot understand that.")


# ---------------- LISTENING ------------------
def listen_voice():
    speak("Hello, I am Jarvis. What can I help you with?")
    r = sr.Recognizer()

    with sr.Microphone() as source:
        status_label.config(text="🎤 Listening...")
        r.pause_threshold = 1

        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=6)
            status_label.config(text="🧠 Processing...")
            command = r.recognize_google(audio)
            status_label.config(text=f"You said: {command}")

            process_command(command)

        except:
            status_label.config(text="Say again...")
            speak("Sorry, I did not hear that.")


def start_listening():
    threading.Thread(target=listen_voice).start()


# ---------------- GUI -----------------
root = tk.Tk()
root.title("JARVIS Voice Assistant")
root.geometry("1024x600")
root.config(bg="#000000")

# ---- JARVIS IMAGE ----
try:
    img = Image.open("image.png")
    img = img.resize((380, 380), Image.LANCZOS)
    jarvis_img = ImageTk.PhotoImage(img)
    image_label = Label(root, image=jarvis_img, bg="#000000")
    image_label.pack(pady=10)
except:
    image_label = Label(root, text="[Image Missing: jarvis.png]", fg="red", bg="#000000")
    image_label.pack(pady=10)

# ---- TITLE ----
title = Label(root, text="J A R V I S", font=("Century Gothic", 36, "bold"),
              fg="#00eaff", bg="#000000")
title.pack(pady=5)

# ---- SUBTITLE ----
subtitle = Label(root,
                 text="I'm a Virtual Assistant JARVIS, How may I help you?",
                 font=("Century Gothic", 16),
                 fg="#00a8b5",
                 bg="#000000")
subtitle.pack(pady=5)

# ---- MIC BUTTON ----
speak_btn = Button(root,
                   text="🎤   Click here to speak",
                   font=("Century Gothic", 18, "bold"),
                   bg="#a7b4b9",
                   fg="#000000",
                   activebackground="#00eaff",
                   activeforeground="#000000",
                   padx=40,
                   pady=10,
                   relief="flat",
                   borderwidth=0,
                   command=start_listening)
speak_btn.pack(pady=40)

# ---- STATUS LABEL ----
status_label = Label(root, text="", font=("Century Gothic", 15),
                     fg="#00eaff", bg="#000000")
status_label.pack()

root.mainloop()
