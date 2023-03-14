import speech_recognition as sr
import webbrowser
import urllib.parse
import random
import os
import shutil

# function to search on Google
def search_google(query):
    query = urllib.parse.quote(query)
    url = "https://www.google.com/search?q=" + query
    webbrowser.open_new_tab(url)

# function to search for a file
def search_file(filename, directory="."):
    for root, dirs, files in os.walk(directory):
        if filename in files:
            return os.path.join(root, filename)
    return None

# function to move a file
def move_file(source_path, target_path):
    try:
        shutil.move(source_path, target_path)
        print(f"File moved from {source_path} to {target_path}")
    except Exception as e:
        print(f"Could not move file: {e}")

# initialize the recognizer
r = sr.Recognizer()

# use the microphone as the audio source
with sr.Microphone() as source:
    # adjust for ambient noise
    r.adjust_for_ambient_noise(source)

    # main loop
    while True:
        # prompt user for input
        print("Say 'Jarvis' to activate the assistant.")
        # capture the audio
        audio = r.listen(source)

        # convert speech to text
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
        except sr.UnknownValueError:
            print("Sorry, I could not understand what you said.")
            continue
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            continue

        # check for wake word
        if "jarvis" in text.lower():
            print("How can I help you?")
            # capture the audio
            audio = r.listen(source)

            # convert speech to text
            try:
                text = r.recognize_google(audio)
                print(f"You said: {text}")
            except sr.UnknownValueError:
                print("Sorry, I could not understand what you said.")
                continue
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                continue

            # check for exit command
            if text.lower() in ["exit", "quit", "bye"]:
                print("Goodbye!")
                break

            # check for joke command
            elif "tell me a joke" in text.lower():
                jokes = [
                    "Why did the tomato turn red? Because it saw the salad dressing!",
                    "Why did the coffee file a police report? It got mugged!",
                    "Why don't scientists trust atoms? Because they make up everything!",
                    "Why did the scarecrow win an award? Because he was outstanding in his field!",
                    "Why was the math book sad? Because it had too many problems!"
                ]
                joke = random.choice(jokes)
                print(joke)
            # check for file search command
            elif "find file" in text.lower():
                filename = text.split("find file ")[-1]
                file_path = search_file(filename)
                if file_path:
                    print(f"File found at {file_path}")
                else:
                    print(f"Could not find file '{filename}'")
            # check for file move command
            elif "move file" in text.lower():
                source_path = text.split("move file ")[-1]
                target_path = input(f"Where would you like to move the file '{source_path}'? ")
                move_file(source_path, target_path
