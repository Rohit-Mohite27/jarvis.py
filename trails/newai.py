# ECHO AI Assistant - Full Version (No API)
import sys
import speech_recognition as sr
import pyttsx3
import wikipedia
import webbrowser
import datetime
import os
import cv2
import psutil
import pywhatkit as kit
from tkinter import *
from tkinter import messagebox
import time
import pyautogui
import random
import subprocess
import platform
import socket
import clipboard
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')
engine = pyttsx3.init()
engine.setProperty("rate", 150)
engine.setProperty("voice", "english")

VOICE_PASSWORD = "open jarvis"
WAKE_WORD = "jarvis"
chatbot_responses = {
    "hello": "Hello Sir! How can I help you?",
    "how are you": "I'm just a virtual assistant, but I'm doing great! How can I assist you?",
    "who are you": "I am Echo, your personal AI assistant.",
    "thank you": "You're welcome Sir!"
}

def speak(text):
    engine.say(text)
    engine.runAndWait()

def welcome():
    speak("Welcome back Sir! How can I assist you?")

def voice_password():
    speak("Please say the password to proceed")
    password = listen()
    if password == VOICE_PASSWORD:
        speak("Access Granted")
        return True
    else:
        speak("Access Denied")
        return False

def face_login():
    cam = cv2.VideoCapture(0)
    result, image = cam.read()
    if result:
        cv2.imshow("Face Recognition", image)
        cv2.imwrite("face.jpg", image)
        cv2.waitKey(2000)
        cv2.destroyAllWindows()
        speak("Face Recognized Successfully")
    else:
        speak("Face Not Detected")

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(audio)
            return query.lower()
        except sr.UnknownValueError:
            return None

def wait_for_wake_word():
    while True:
        print("👂 Waiting for wake word...")
        query = listen()
        if query and WAKE_WORD in query:
            speak("Yes sir, I am listening")
            return

def network_speed():
    interfaces = psutil.net_if_stats()
    for name, stats in interfaces.items():
        if stats.isup:
            speak(f"Your current network interface is {name} with speed {stats.speed} Mbps")
            return
    speak("No active network connection found.")

def bluetooth_on_off(state):
    command = "Start-Service bthserv" if state == "on" else "Stop-Service bthserv"
    os.system(f"powershell.exe {command}")
    speak(f"Bluetooth Turned {state.capitalize()}")

def whatsapp_message(number, message):
    kit.sendwhatmsg_instantly(number, message)
    speak("Message Sent Successfully")

def scroll_window(direction):
    pyautogui.scroll(300 if direction == "up" else -300)
    speak(f"Scrolling {direction.capitalize()}")

def youtube_search(query):
    if query:
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        webbrowser.open(url)
        speak(f"Searching {query} on YouTube")

def youtube_voice_search():
    speak("What do you want to search on YouTube?")
    query = listen()
    youtube_search(query)

def open_new_tab():
    pyautogui.hotkey("ctrl", "t")
    speak("Opening New Tab")

def close_tab():
    pyautogui.hotkey("ctrl", "w")
    speak("Closing Tab")

def previous_tab():
    pyautogui.hotkey("ctrl", "shift", "tab")
    speak("Going to Previous Tab")

def tell_joke():
    jokes = [
        "Why did the computer go to the doctor? Because it had a virus!",
        "Why do programmers prefer dark mode? Because light attracts bugs!"
    ]
    speak(random.choice(jokes))

def battery_status():
    battery = psutil.sensors_battery()
    speak(f"Battery is at {battery.percent} percent")

def take_screenshot():
    path = os.path.join(os.getcwd(), f"screenshot_{int(time.time())}.png")
    pyautogui.screenshot(path)
    speak("Screenshot taken")

def get_ip():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    speak(f"Your IP address is {ip}")

def get_clipboard():
    text = clipboard.paste()
    speak(f"Clipboard says: {text}")

def code_calculator():
    speak("Say the calculation")
    expr = listen()
    try:
        result = eval(expr)
        speak(f"The answer is {result}")
    except:
        speak("Sorry, I couldn't calculate that")

def open_app(name):
    try:
        os.system(f'start {name}')
        speak(f"Opening {name}")
    except:
        speak("App not found")

def shutdown():
    speak("Shutting down")
    os.system("shutdown /s /t 1")

def reminder():
    speak("What should I remind you?")
    task = listen()
    speak("In how many seconds?")
    seconds = listen()
    try:
        seconds = int(seconds)
        speak(f"Reminder set for {task} in {seconds} seconds")
        time.sleep(seconds)
        speak(f"Reminder: {task}")
    except:
        speak("Invalid time")

def play_guessing_game():
    speak("Let's play a number guessing game. Guess a number between 1 and 10")
    number = random.randint(1, 10)
    guess = listen()
    try:
        if int(guess) == number:
            speak("Congratulations! You guessed right.")
        else:
            speak(f"Sorry, the correct number was {number}")
    except:
        speak("That was not a number")

def chatbot(query):
    for key in chatbot_responses:
        if key in query:
            speak(chatbot_responses[key])
            return
    speak("Sorry, I couldn't find an answer to that question!")

def generate_text(prompt):
    # Placeholder text generation
    responses = [
        f"Here's a paragraph on {prompt}...",
        f"Writing a letter about {prompt}...",
        f"Generating story on {prompt}..."
    ]
    speak(random.choice(responses))

def run_script():
    scripts = [f for f in os.listdir() if f.endswith(".py") and f != os.path.basename(__file__)]
    if scripts:
        speak("Running the first script I found")
        os.system(f"python {scripts[0]}")
    else:
        speak("No Python script found")

def wikipedia_summary():
    speak("What topic should I look up?")
    topic = listen()
    if topic:
        try:
            summary = wikipedia.summary(topic, sentences=2)
            speak(summary)
        except:
            speak("Couldn't find anything")

def convert_jpg_to_png(image_path):
    try:
        img = Image.open(image_path)
        new_path = image_path.replace(".jpg", ".png")
        img.save(new_path, "PNG")
        return new_path
    except:
        return image_path

def gui():
    def on_listen():
        wait_for_wake_word()
        jarvis()

    root = Tk()
    root.title("ECHO")
    root.geometry("600x400")
    try:
        converted_image = convert_jpg_to_png("goku.jpg")
        bg_image = PhotoImage(file=converted_image)
        bg_label = Label(root, image=bg_image)
        bg_label.image = bg_image
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except:
        print("Background image not found")
    Label(root, text="Welcome to ECHO", font=("Arial", 18)).pack(pady=20)
    Button(root, text="🎙️ Start Listening", command=on_listen).pack(pady=10)
    Button(root, text="📷 Screenshot", command=take_screenshot).pack(pady=5)
    Button(root, text="🔋 Battery", command=battery_status).pack(pady=5)
    Button(root, text="🎲 Play Game", command=play_guessing_game).pack(pady=5)
    Button(root, text="📝 Reminder", command=reminder).pack(pady=5)
    Button(root, text="📜 Run Script", command=run_script).pack(pady=5)
    Button(root, text="❌ Exit", command=root.destroy).pack(pady=10)
    root.mainloop()

def jarvis():
    welcome()
    if voice_password():
        face_login()
        while True:
            query = listen()
            if query:
                if "exit" in query or "bye" in query:
                    speak("Goodbye Sir! Have a nice day.")
                    break
                elif "open youtube" in query:
                    webbrowser.open("https://www.youtube.com")
                elif "search youtube" in query:
                    youtube_voice_search()
                elif "new tab" in query:
                    open_new_tab()
                elif "close tab" in query:
                    close_tab()
                elif "previous tab" in query:
                    previous_tab()
                elif "scroll up" in query:
                    scroll_window("up")
                elif "scroll down" in query:
                    scroll_window("down")
                elif "time" in query:
                    speak(datetime.datetime.now().strftime("%H:%M:%S"))
                elif "network speed" in query:
                    network_speed()
                elif "bluetooth on" in query:
                    bluetooth_on_off("on")
                elif "bluetooth off" in query:
                    bluetooth_on_off("off")
                elif "send whatsapp message" in query:
                    speak("Tell the number")
                    number = listen()
                    speak("Your message")
                    message = listen()
                    whatsapp_message(number, message)
                elif "joke" in query:
                    tell_joke()
                elif "battery" in query:
                    battery_status()
                elif "screenshot" in query:
                    take_screenshot()
                elif "ip address" in query:
                    get_ip()
                elif "clipboard" in query:
                    get_clipboard()
                elif "calculate" in query:
                    code_calculator()
                elif "shutdown" in query:
                    shutdown()
                elif "reminder" in query:
                    reminder()
                elif "play game" in query:
                    play_guessing_game()
                elif "run script" in query:
                    run_script()
                elif "search wikipedia" in query:
                    wikipedia_summary()
                elif "generate text" in query:
                    speak("What topic?")
                    topic = listen()
                    generate_text(topic)
                elif "open app" in query:
                    speak("App name?")
                    open_app(listen())
                else:
                    chatbot(query)

if __name__ == "__main__":
    gui()
