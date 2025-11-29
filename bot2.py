import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import datetime
import subprocess
import platform
import sys

# Initialize Engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    """Speaks the provided text."""
    print("Kyra:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listens to microphone input and returns string."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        # Helps filter out background noise
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            command = r.recognize_google(audio).lower()
            print("You:", command)
            return command
        except sr.UnknownValueError:
            # Don't speak here to avoid interrupting the user constantly
            return ""
        except sr.RequestError:
            speak("Speech service is unavailable.")
            return ""
        except sr.WaitTimeoutError:
            return ""

def open_website(site):
    """Opens a website or searches google."""
    urls = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "instagram": "https://www.instagram.com",
        "whatsapp": "https://web.whatsapp.com",
        "snapchat": "https://www.snapchat.com",
        "github": "https://www.github.com",
    }
    
    if site in urls:
        speak(f"Opening {site}")
        webbrowser.open(urls[site])
    else:
        speak(f"Searching for {site} on Google")
        webbrowser.open(f"https://www.google.com/search?q={site}")

def open_folder(folder_name):
    """Opens a directory in the file explorer (Cross-platform)."""
    # Define paths based on OS
    user_home = os.path.expanduser("~")
    folders = {
        "downloads": os.path.join(user_home, "Downloads"),
        "documents": os.path.join(user_home, "Documents"),
        "desktop": os.path.join(user_home, "Desktop"),
    }

    if folder_name not in folders:
        speak("I couldn't find that folder.")
        return

    path = folders[folder_name]

    if os.path.exists(path):
        speak(f"Opening {folder_name} folder")
        # Platform-specific opener
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.Popen(["open", path])
        else:  # Linux
            subprocess.Popen(["xdg-open", path])
    else:
        speak("That folder does not exist.")

def process_command(cmd):
    """Processes the identified command."""
    if not cmd:
        return

    if "open" in cmd:
        # Check for Folder keywords
        if any(x in cmd for x in ["folder", "downloads", "documents", "desktop"]):
            if "downloads" in cmd:
                open_folder("downloads")
            elif "documents" in cmd:
                open_folder("documents")
            elif "desktop" in cmd:
                open_folder("desktop")
            else:
                speak("Which folder should I open?")
        
        # Check for Website keywords
        else:
            # Remove the word 'open' to find the site name
            search_term = cmd.replace("open", "").strip()
            if search_term:
                open_website(search_term)
            else:
                speak("What would you like me to open?")

    elif "search for" in cmd:
        search_term = cmd.split("search for", 1)[1].strip()
        speak(f"Searching Google for {search_term}")
        webbrowser.open(f"https://www.google.com/search?q={search_term}")

    elif "time" in cmd:
        time_now = datetime.datetime.now().strftime('%I:%M %p')
        speak(f"The time is {time_now}")

    elif "hello" in cmd or "hi" in cmd:
        speak("Hi! I'm Kyra. What can I do for you?")

    elif "exit" in cmd or "stop" in cmd or "quit" in cmd:
        speak("Goodbye!")
        sys.exit()

    else:
        speak("Sorry, I didn't understand that command.")

# --- Main Execution ---
if __name__ == "__main__":
    speak("Hi, I'm Kyra. Ready to help you.")
    
    while True:
        command = listen()
        if command:
            process_command(command)
