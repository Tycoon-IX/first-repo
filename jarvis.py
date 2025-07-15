import speech_recognition as sr
import pyttsx3
import pywhatkit 
import wikipedia
import pyjokes
import datetime
import webbrowser
import requests
import os
import sys
from typing import Optional

class JARVIS:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.setup_voice()
        
    def setup_voice(self):
        """Configure voice settings"""
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)  # 0 for male, 1 for female
        self.engine.setProperty('rate', 150)  # Speaking rate (words per minute)
        
    def speak(self, text: str) -> None:
        """Convert text to speech with error handling"""
        try:
            print(f"JARVIS: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Speech error: {e}")

    def take_command(self) -> Optional[str]:
        """Take voice input from user with improved error handling"""
        try:
            with sr.Microphone() as source:
                print("Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)
                
            print("Recognizing...")
            query = self.recognizer.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query.lower()
            
        except sr.WaitTimeoutError:
            print("No speech detected")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            self.speak("I didn't catch that. Could you repeat?")
            return None
        except Exception as e:
            print(f"Recognition error: {e}")
            return None

    def play_song(self, song_name: str) -> None:
        """Play song on YouTube with error handling"""
        try:
            self.speak(f"Playing {song_name}")
            pywhatkit.playonyt(song_name)
        except Exception as e:
            self.speak(f"Sorry, I couldn't play {song_name}")
            print(f"Play error: {e}")

    def get_time(self) -> None:
        """Speak current time"""
        time = datetime.datetime.now().strftime('%I:%M %p')
        self.speak(f"The current time is {time}")

    def search_wikipedia(self, query: str) -> None:
        """Search Wikipedia with error handling"""
        try:
            info = wikipedia.summary(query, sentences=2)
            self.speak(info)
        except wikipedia.DisambiguationError as e:
            self.speak("There are multiple matches. Can you be more specific?")
        except wikipedia.PageError:
            self.speak("I couldn't find information about that.")
        except Exception as e:
            self.speak("Sorry, I encountered an error searching Wikipedia.")
            print(f"Wikipedia error: {e}")

    def tell_joke(self) -> None:
        """Tell a random joke"""
        joke = pyjokes.get_joke()
        self.speak(joke)

    def open_application(self, app_name: str) -> None:
        """Open common applications"""
        apps = {
            'chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe'
        }
        
        if app_name in apps:
            try:
                os.startfile(apps[app_name])
                self.speak(f"Opening {app_name}")
            except Exception as e:
                self.speak(f"Couldn't open {app_name}")
                print(f"App error: {e}")
        else:
            self.speak(f"I don't know how to open {app_name}")

    def run(self) -> None:
        """Main execution loop"""
        self.speak("Hello, I am JARVIS. How can I help you today?")
        
        while True:
            query = self.take_command()
            
            if not query:
                continue
                
            if 'play' in query:
                song = query.replace('play', '').strip()
                self.play_song(song)
                
            elif 'time' in query:
                self.get_time()
                
            elif 'who is' in query or 'what is' in query:
                search_term = query.replace('who is', '').replace('what is', '').strip()
                self.search_wikipedia(search_term)
                
            elif 'date' in query:
                date = datetime.datetime.now().strftime('%B %d, %Y')
                self.speak(f"Today's date is {date}")
                
            elif 'joke' in query:
                self.tell_joke()
                
            elif 'open' in query:
                app = query.replace('open', '').strip()
                self.open_application(app)
                
            elif 'search' in query:
                search_query = query.replace('search', '').strip()
                webbrowser.open(f"https://www.google.com/search?q={search_query}")
                self.speak(f"Searching for {search_query}")
                
            elif 'stop' in query or 'exit' in query or 'quit' in query:
                self.speak("Goodbye! Shutting down.")
                sys.exit()
                
            else:
                self.speak("I didn't understand that command. Can you try again?")

if __name__ == "__main__":
    assistant = JARVIS()
    try:
        assistant.run()
    except KeyboardInterrupt:
        assistant.speak("Goodbye!")
    except Exception as e:
        print(f"Fatal error: {e}")
        assistant.speak("I encountered a serious error. Restarting may help.")