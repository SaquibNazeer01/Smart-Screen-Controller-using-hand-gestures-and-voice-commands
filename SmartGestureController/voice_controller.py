import speech_recognition as sr
import pyttsx3
import pyautogui
import time

r = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

speak("🎤 Voice controller ready. Say your command...")

while True:
    with sr.Microphone() as source:
        try:
            print("🎤 Listening...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=5, phrase_time_limit=4)
            command = r.recognize_google(audio).lower()
            print(f"🗣️ Command: {command}")

            if "next slide" in command:
                pyautogui.press('right')
                speak("Next slide")

            elif "previous slide" in command:
                pyautogui.press('left')
                speak("Previous slide")

            elif "zoom in" in command:
                pyautogui.hotkey('ctrl', '+')
                speak("Zooming in")

            elif "zoom out" in command:
                pyautogui.hotkey('ctrl', '-')
                speak("Zooming out")

            elif "scroll down" in command:
                pyautogui.press('down')
                speak("Scrolling down")

            elif "scroll up" in command:
                pyautogui.press('up')
                speak("Scrolling up")

            elif "exit" in command:
                speak("Exiting voice controller")
                break

            else:
                speak("Command not recognized")

        except Exception as e:
            print("⚠️ Error:", e)
