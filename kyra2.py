import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import datetime
import subprocess

engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    print("Kyra:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio).lower()
            print("You:", command)
            return command
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            speak("Speech service is unavailable.")
            return ""



def open_website(site):
    urls = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "instagram": "https://www.instagram.com",
        "whatsapp": "https://web.whatsapp.com",
        "snapchat": "https://www.snapchat.com",
        "github": "https://www.github.com",
    }
    if site in urls:
        webbrowser.open(urls[site])
        speak(f"Opening {site}")
    else:
        webbrowser.open(f"https://www.google.com/search?q={site}")
        speak(f"Searching for {site} on Google")

def open_folder(folder_name):
    folders = {
        "downloads": os.path.expanduser("~/Downloads"),
        "documents": os.path.expanduser("~/Documents"),
        "desktop": os.path.expanduser("~/Desktop"),
    }
    if folder_name in folders:
        os.startfile(folders[folder_name])
        speak(f"Opening {folder_name} folder")
    else:
        speak("I couldn't find that folder.")

def process_command(cmd):
    if "open" in cmd:
        if "folder" in cmd or "downloads" in cmd or "documents" in cmd or "desktop" in cmd:
            if "downloads" in cmd:
                open_folder("downloads")
            elif "documents" in cmd:
                open_folder("documents")
            elif "desktop" in cmd:
                open_folder("desktop")
            else:
                speak("Which folder should I open?")
        else:
            for site in ["google", "youtube", "instagram", "whatsapp", "snapchat", "github"]:
                if site in cmd:
                    open_website(site)
                    return
            # open anything else
            words = cmd.split("open", 1)
            if len(words) > 1:
                search_term = words[1].strip()
                open_website(search_term)

    elif "search for" in cmd:
        search_term = cmd.split("search for", 1)[1].strip()
        webbrowser.open(f"https://www.google.com/search?q={search_term}")
        speak(f"Searching Google for {search_term}")

    elif "time" in cmd:
        time_now = datetime.datetime.now().strftime('%I:%M %p')
        speak(f"The time is {time_now}")

    elif "hello" in cmd or "hi" in cmd:
        speak("Hi! I'm Kyra. What can I do for you?")

    elif "exit" in cmd or "stop" in cmd:
        speak("Goodbye!")
        exit()

    else:
        speak("Sorry, I’m still learning. Can you say that again?")

# Start Assistant
speak("Hi, I'm Kyra. Ready to help you.")
while True:
    command = listen()
    if command:
        process_command(command)
