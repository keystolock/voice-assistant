import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import os
import requests
from dotenv import load_dotenv

recognizer = sr.Recognizer()
engine = pyttsx3.init()
load_dotenv()
chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"


webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(chrome_path))


def speak(text):
    engine.say(text)
    engine.runAndWait()


def getnews():
    news_api = os.getenv("News_API_key")
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={news_api}"
    response = requests.get(url).json()
    articles = response["articles"][:5]
    for article in articles:
        title = article["title"]
        print(title)
        speak(title)


def getWeatherUpdate(city="Ayodhya"):
    weather_api = os.getenv("Weather_API_key")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api}&units=metric"
    response = requests.get(url).json()

    if response.get("cod") != 200:
        speak("Sorry, I couldn't fetch the weather right now.")
        return

    temp = response["main"]["temp"]
    desc = response["weather"][0]["description"]
    report = f"The temperature in {city} is {temp}°C with {desc}."
    print(report)
    speak(report)


def processCommand(c):
    c = c.lower()
    if "open google" in c:
        speak("Opening Google")
        webbrowser.get("chrome").open("https://google.com")
    elif "youtube" in c:
        speak("Opening YouTube")
        webbrowser.get("chrome").open("https://youtube.com")
    elif "facebook" in c:
        speak("Opening Facebook")
        webbrowser.get("chrome").open("https://facebook.com")
    elif "chess" in c:
        speak("Opening Chess")
        webbrowser.get("chrome").open("https://lichess.org/")
    elif "linkedin" in c:
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")
    elif "play" in c:
        song = c.split(" ")[1]
        link = musicLibrary.musicList[song]
        webbrowser.get("chrome").open(link)

    elif "search" in c:
        query = c.replace("search", "").strip()
        speak(f"Searching for {query}")
        webbrowser.get("chrome").open(f"https://www.google.com/search?q={query}")

    elif "open calculator" in c:
        speak("Opening Calculator")
        os.startfile("calc.exe")
    elif "open word" in c:
        speak("Opening Word")
        os.startfile("WINWORD.exe")
    elif "open excel" in c:
        speak("Opening Excel")
        os.startfile("C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE")

    elif "open notepad" in c:
        speak("Opening notepad")
        os.startfile("notepad.exe")
    elif "open paint" in c:
        speak("Opening Paint")
        os.startfile("mspaint.exe")
    elif "news" in c:
        getnews()
    elif "weather" in c:
        getWeatherUpdate()
    
    else:
        speak("Sorry, I don't know that command.")


if __name__ == "__main__":
    speak("Initializing Your Personal Assistance....")

while True:
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening.....")

        try:
            audio = recognizer.listen(source, timeout=7, phrase_time_limit=5)
            print("Recognizing...")
            text = recognizer.recognize_google(audio, language="en-IN")
            print("You said:", text)

            if "google" in text.lower():
                speak("Yeah")
                print("Active")


                # Listen for the actual command
                with sr.Microphone() as source:
                    audio = recognizer.listen(source, timeout=7, phrase_time_limit=5)
                    command = recognizer.recognize_google(audio, language="en-IN")
                    print("Your command:", command)
                    if "stop" in command:
                        break
                    processCommand(command)

            if "exit" in text.lower() or "stop" in text.lower():
                speak("Exiting program. Goodbye!")
                break

        except sr.UnknownValueError:
            print("Assistance could not understand what you have said.")
        except Exception as e:
            print(f"Error : {e}")
            break
        except TimeoutError as e:
            print(f"Error {e}")
            break
