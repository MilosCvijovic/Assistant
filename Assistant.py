import datetime
from datetime import date
import speech_recognition as sr
import pyttsx3
import wikipedia
import webbrowser
import sys
import time
import pywhatkit
import subprocess
from functools import wraps

print('I am your assistant, how can I help you')

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def call_once(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    return wrapper()


def speak(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            statement = r.recognize_google(audio, language='en')
            print(f"user said:{statement}\n")

        except Exception as e:
            speak("Pardon me, please say that again")
            return "None"
        return statement


def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])


wake_up = "alexa"

if __name__ == '__main__':
    while True:
        statement = take_command().lower()
        while statement.count(wake_up) == 1:
            @call_once
            def wish_me():
                hour = datetime.datetime.now().hour
                if 0 <= hour < 12:
                    speak("Hello,Good Morning")
                    print("Hello,Good Morning")
                elif 12 <= hour < 18:
                    speak("Hello,Good Afternoon")
                    print("Hello,Good Afternoon")
                else:
                    speak("Hello,Good Evening")
                    print("Hello,Good Evening")
            speak("I am ready...")
            speak("How can I help you?")

            statement = take_command().lower()
            if statement == 0:
                continue

        if ("goodbye" or "shut down") in statement:
            speak('Good bye.')
            print('Your personal assistant is shutting down.')
            sys.exit()

        if 'play' in statement:
            song = take_command()
            speak("playing " + song + " on YouTube")
            pywhatkit.playonyt(song)

        if 'wikipedia' in statement:
            speak('Searching Wikipedia...')
            statement = statement.replace("wikipedia", "")
            results = wikipedia.summary(statement, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in statement:
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("Opening YouTube")
            time.sleep(5)

        elif 'open google' in statement:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Opening Google Chrome")
            time.sleep(5)

        elif 'open gmail' in statement:
            webbrowser.open_new_tab("gmail.com")
            speak("Opening Google Mail")
            time.sleep(5)

        elif 'time' in statement:
            strTime = datetime.datetime.now().strftime("%H:%M")
            speak(f"the time is {strTime}")
            print(f"the time is {strTime}")

        elif 'date' in statement:
            today = date.today()
            speak(f"Today is {today}")
            print(f"Today is {today}")

        elif 'search' in statement:
            statement = statement.replace("search", "")
            webbrowser.open_new_tab(statement)
            speak("What do you want to find?")
            print("What do you want to find?")
            time.sleep(5)

        elif "log off" in statement:
            speak("Ok, your pc will log off in 10 seconds")
            subprocess.call(["shutdown", "/l"])

        elif "make a note" in statement:
            speak("What do you want to write down?")
            note_text = take_command()
            note(note_text)
            speak("I've made note of that.")

time.sleep(3)
