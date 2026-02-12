import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
from google import genai


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Please set your API key.")

client = genai.Client(api_key=api_key)


engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()


def take_command():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        print("User:", command)
        return command.lower()

    except Exception as e:
        print("Speech Recognition Error:", e)
        speak("Sorry, I did not understand that.")
        return ""


def ask_ai(question):
    try:
        response = client.models.generate_content(
            model="models/gemini-2.0-flash",
            contents=question
        )

        if response.text:
            return response.text
        else:
            return "I couldn't generate a response."

    except Exception as e:
        print("FULL GEMINI ERROR:", e)
        return "AI connection failed."

def main():
    speak("Hello Manish.")

    while True:
        command = take_command()

        if not command:
            continue

        elif "time" in command:
            now = datetime.datetime.now().strftime("%H:%M")
            speak(f"The current time is {now}")

        elif "date" in command:
            today = datetime.date.today()
            speak(f"Today's date is {today}")

        elif "open google" in command:
            webbrowser.open("https://www.google.com")
            speak("Opening Google")

        elif "open youtube" in command:
            webbrowser.open("https://www.youtube.com")
            speak("Opening YouTube")

        elif "open file manager" in command:
            os.startfile("C:\\")
            speak("Opening File Manager")

        elif "search" in command:
            query = command.replace("search", "").strip()
            webbrowser.open(f"https://www.google.com/search?q={query}")
            speak("Here are the search results")

        elif "exit" in command or "stop" in command or "quit" in command:
            speak("Goodbye Manish. Have a great day.")
            break

        else:
            response = ask_ai(command)
            speak(response[:400])


if __name__ == "__main__":
    main()
