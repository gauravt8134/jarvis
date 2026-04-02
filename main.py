import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
import threading
import speech_recognition as sr
import pyttsx3
import os
import subprocess
import webbrowser
import urllib.parse
import ctypes

# ================== OPENAI ==================
from openai import OpenAI
API_KEY = "YOUR_API_KEY_HERE"   # 🔴 PUT YOUR REAL API KEY

# ================== CHROME PATH ==================
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# ================== TEXT TO SPEECH ==================
def speak(text):
    def _run():
        engine = pyttsx3.init()
        engine.setProperty("rate", 170)
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=_run, daemon=True).start()

# ================== WINDOWS APPS ==================
WINDOWS_APPS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "cmd": "cmd.exe",
    "command prompt": "cmd.exe",
    "task manager": "taskmgr.exe",
    "control panel": "control.exe",
    "settings": "ms-settings:",
    "this pc": "explorer shell:MyComputerFolder",
    "file explorer": "explorer.exe",
    "vs code": r"C:\Users\HP\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "visual studio code": r"C:\Users\HP\AppData\Local\Programs\Microsoft VS Code\Code.exe"
}

# ================== SYSTEM CONTROL ==================
def system_control(command):
    if "shutdown" in command:
        speak("Shutting down system")
        os.system("shutdown /s /t 5")
        return True
    if "restart" in command:
        speak("Restarting system")
        os.system("shutdown /r /t 5")
        return True
    if "lock" in command:
        speak("Locking system")
        ctypes.windll.user32.LockWorkStation()
        return True
    if "sleep" in command:
        speak("Putting system to sleep")
        ctypes.windll.powrprof.SetSuspendState(False, True, False)
        return True
    return False

# ================== OPEN WINDOWS APPS ==================
def open_windows_app(command):
    for app, target in WINDOWS_APPS.items():
        if app in command:
            try:
                if target.startswith("ms-settings"):
                    os.startfile(target)
                else:
                    subprocess.Popen(target)
                speak(f"Opening {app}")
            except:
                speak(f"Cannot open {app}")
            return True
    return False

# ================== PLAY SONG ==================
def play_song(command):
    if not command.startswith("play"):
        return False

    song = command.replace("play", "").replace("song", "").strip()
    if not song:
        return False

    if "spotify" in song:
        song = song.replace("on spotify", "").strip()
        url = f"https://open.spotify.com/search/{urllib.parse.quote(song)}"
        speak(f"Playing {song} on Spotify")
    elif "youtube" in song:
        song = song.replace("on youtube", "").strip()
        url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(song)}"
        speak(f"Playing {song} on YouTube")
    else:
        url = f"https://music.youtube.com/search?q={urllib.parse.quote(song)}"
        speak(f"Playing {song}")

    webbrowser.open(url)
    return True

# ================== GOOGLE APPS ==================
GOOGLE_APPS = {
    "gmail": "mail.google.com",
    "drive": "drive.google.com",
    "docs": "docs.google.com",
    "sheets": "sheets.google.com",
    "slides": "slides.google.com",
    "classroom": "classroom.google.com",
    "maps": "maps.google.com",
    "youtube": "youtube.com",
    "calendar": "calendar.google.com",
    "meet": "meet.google.com",
    "photos": "photos.google.com",
    "translate": "translate.google.com"
}

def open_google_app(command):
    for app, domain in GOOGLE_APPS.items():
        if app in command:
            try:
                if os.path.exists(CHROME_PATH):
                    subprocess.Popen([CHROME_PATH, f"--app=https://{domain}"])
                else:
                    webbrowser.open(f"https://{domain}")
                speak(f"Opening {app}")
            except:
                speak("Unable to open Google service")
            return True
    return False

# ================== SMART SEARCH (CHATGPT FIX) ==================
def smart_search(command):
    if command.startswith("search"):
        query = command.replace("search", "").strip()
        speak(f"Searching for {query}")
        webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote(query)}")
        return True

    question_words = ("who", "what", "when", "where", "why", "how", "define", "calculate")

    if command.startswith(question_words):
        try:
            client = OpenAI(api_key=API_KEY)

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": command}]
            )

            answer = response.choices[0].message.content.strip()

            speak(answer)
            status_label.config(text=answer[:120])

        except:
            speak("Showing Google results")
            webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote(command)}")

        return True

    return False

# ================== SMART WEBSITE (WHATSAPP FIX) ==================
def smart_open_website(command):
    if "open" not in command:
        return False

    site = command.replace("open", "").replace("website", "").replace("app", "").strip()

    if not site:
        return False

    # 🔥 FIX FOR WHATSAPP
    if "whatsapp" in command or "whats app" in command or "whatsap" in command:
        try:
            subprocess.Popen("C:\\Users\\HP\\AppData\\Local\\WhatsApp\\WhatsApp.exe")
            speak("Opening WhatsApp")
        except:
            webbrowser.open("https://web.whatsapp.com")
            speak("Opening WhatsApp Web")
        return True

    known_sites = {
        "instagram": "https://www.instagram.com",
        "youtube": "https://www.youtube.com",
        "gmail": "https://mail.google.com",
        "whatsapp": "https://web.whatsapp.com",
        "telegram": "https://web.telegram.org",
        "instagram": "https://www.instagram.com",
        "facebook": "https://www.facebook.com",
        "twitter": "https://twitter.com",
        "x": "https://twitter.com",
        "reddit": "https://www.reddit.com",
        "linkedin": "https://www.linkedin.com",
        "discord": "https://discord.com",
        "snapchat": "https://www.snapchat.com",
        "pinterest": "https://www.pinterest.com",
        "amazon": "https://www.amazon.in",
        "flipkart": "https://www.flipkart.com",
        "youtube": "https://www.youtube.com",
        "netflix": "https://www.netflix.com",
        "gmail": "https://mail.google.com",
        "drive": "https://drive.google.com",
        "github": "https://github.com",
        "chatgpt": "https://chat.openai.com",
        "google": "https://www.google.com",
        "maps": "https://maps.google.com",
        "zomato": "https://www.zomato.com",
        "swiggy": "https://www.swiggy.com"
    }

    if site in known_sites:
        webbrowser.open(known_sites[site])
        speak(f"Opening {site}")
        return True

    return False

# ================== COMMAND EXECUTION ==================
def execute_command(command):
    command = command.lower().strip()
    for word in ["jarvis", "please"]:
        command = command.replace(word, "")

    if not command:
        speak("Please say a command")
        return

    if system_control(command): return
    if play_song(command): return
    if open_google_app(command): return
    if open_windows_app(command): return
    if smart_open_website(command): return
    if smart_search(command): return

    speak("Searching on Google")
    webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote(command)}")

# ================== VOICE LISTENER ==================
def listen_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="🎤 LISTENING...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=11, phrase_time_limit=12)
            status_label.config(text="🧠 PROCESSING...")
            command = r.recognize_google(audio)
            status_label.config(text=f"YOU SAID: {command}")
            execute_command(command)
        except:
            status_label.config(text="❌ COMMAND NOT RECOGNIZED")
            speak("Sorry, I did not understand")

def start_listening():
    speak("Hello I'm JARVIS your Virtual Assistant. How may I help you?")
    threading.Thread(target=listen_voice, daemon=True).start()

# ================== GUI ==================
root = tk.Tk()
root.title("JARVIS Voice Assistant")
root.geometry("1024x600")
root.config(bg="#000000")

try:
    img = Image.open("image.png").resize((420, 420), Image.LANCZOS)
    jarvis_img = ImageTk.PhotoImage(img)
    Label(root, image=jarvis_img, bg="#000000").pack(pady=10)
except:
    Label(root, text="[IMAGE MISSING]", fg="red", bg="#000000").pack(pady=10)

Label(root, text="J A R V I S",
      font=("Century Gothic", 45, "bold"),
      fg="#00eaff", bg="#000000").pack()

Label(root,
      text="Hello I'm JARVIS your Virtual Assistant. How may I help you?",
      font=("Century Gothic", 18),
      fg="#00a8b5", bg="#000000").pack(pady=5)

def on_enter(e):
    speak_btn.config(bg="#00eaff", fg="#000000")

def on_leave(e):
    speak_btn.config(bg="#0a2a2f", fg="#00eaff")

speak_btn = Button(
    root,
    text="🎤 CLICK HERE TO ACTIVATE JARVIS",
    font=("Century Gothic", 18, "bold"),
    bg="#0a2a2f",
    fg="#00eaff",
    bd=0,
    padx=50,
    pady=12,
    cursor="hand2",
    command=start_listening
)
speak_btn.pack(pady=35)
speak_btn.bind("<Enter>", on_enter)
speak_btn.bind("<Leave>", on_leave)

status_label = Label(root,
                     text="SYSTEM READY",
                     font=("Consolas", 14),
                     fg="#00ffcc",
                     bg="#000000")
status_label.pack(pady=10)

Label(root,
      text="JARVIS v1.0 | Developed by Gaurav Thakare",
      font=("Consolas", 10),
      fg="#555555",
      bg="#000000").pack(side="bottom", pady=10)

root.mainloop()