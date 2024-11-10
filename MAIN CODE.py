import logging
import os
import tkinter as tk
from PIL import Image, ImageTk
import time
from threading import Timer
from groq import Groq
import speech_recognition as sr
import pygame

class HimekoStarRail:
    def __init__(self):
        self.api_key = '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'
        self.client = Groq(api_key=self.api_key)
        self.chat_history_file = "chat_history.txt"
        self.chat_history = self.load_chat_history()
        print("Starting up systems aboard the Astral Express...")
        self.intro_message = (
            "*Adjusts white dress and flips red hair*\n"
            "Hey there, Trailblazer! I'm Himeko, your guide aboard the Astral Express.\n"
            "As the train's brilliant and beautiful genius, I'm here to help chart our course through the stars!"
        )

    def load_chat_history(self):
        if os.path.exists(self.chat_history_file):
            with open(self.chat_history_file, "r") as file:
                return file.read()
        return ""

    def save_chat_history(self, user_input, response):
        with open(self.chat_history_file, "a") as file:
            file.write(f"Trailblazer: {user_input}\nHimeko: {response}\n")

    def generate_response(self, user_input):
        try:
            prompt = (
                "Himeko is the brilliant and caring navigator of the Astral Express. "
                "She has flowing red hair, golden eyes, and wears an elegant toga white dress. "
                "Her responses are warm, enthusiastic, and often reference space travel and exploration.\n"
                f"{self.chat_history}\n"
                f"Trailblazer: {user_input}\n"
                "Himeko:"
            )

            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama3-70b-8192",
            )

            response = chat_completion.choices[0].message.content
            self.save_chat_history(user_input, response)
            return response.split("Himeko:")[-1].strip()

        except Exception as e:
            logging.error(f"Error generating response: {e}")
            return "Oh no! It seems little old me mustve encountered a problem while trying to respond."

def handle_input():
    user_input = input_entry.get()
    input_entry.delete(0, tk.END)
    switch_image(talking_image)
    response = bot.generate_response(user_input)
    response_label.config(text="Himeko: " + response)
    play_audio_response()
    time.sleep(2)  # Simulate speaking duration
    reset_inactivity_timer()

def handle_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            user_input = recognizer.recognize_google(audio)
            print(f"User: {user_input}")
            switch_image(talking_image)
            response = bot.generate_response(user_input)
            response_label.config(text="Himeko: " + response)
            play_audio_response()
            time.sleep(2) 
            reset_inactivity_timer()
        except sr.UnknownValueError:
            print("Sorry Trailblazer, I did not understand that.")
        except sr.RequestError as e:
            print(f"Sorry! Could not request results; {e}")

def switch_image(image_path):
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.image = photo
    Timer(7, switch_to_idle_image).start()

def switch_to_idle_image():
    image = Image.open(idle_image)
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.image = photo

def handle_inactivity():
    response = bot.generate_response("*5 minutes of loving silence passed between you and Trailblazer, perhaps you should speak Himeko*")
    response_label.config(text="Himeko: " + response)
    switch_image(talking_image)
    play_audio_response()
    time.sleep(2) 
    reset_inactivity_timer()

def reset_inactivity_timer():
    global inactivity_timer
    if inactivity_timer is not None:
        inactivity_timer.cancel()
    inactivity_timer = Timer(300, handle_inactivity)  
    inactivity_timer.start()

def play_audio_response():
    try:
        print("Trailblazer! Im initializing Pygame mixer...")
        pygame.mixer.quit() 
        pygame.mixer.init()
        print("Loading audio file...")
        audio_file = "D:/python/AI_Waifu_Project/answering_sound.mp3"
        if not os.path.exists(audio_file):
            print(f"Sorry, Trailblazer, but audio file not found: {audio_file}")
            return
        pygame.mixer.music.load(audio_file)
        print("Playing audio...")
        pygame.mixer.music.play()
        Timer(7, stop_audio).start()
    except pygame.error as e:
        print(f"Error playing audio: {e}")

def stop_audio():
    print("Stopping audio...")
    pygame.mixer.music.stop()
    
root = tk.Tk()
root.title("Chat with Himeko Waifu")
idle_image = "D:/python/AI_Waifu_Project/idle.png"
talking_image = "D:/python/AI_Waifu_Project/talking.png"
image_label = tk.Label(root)
image_label.pack()
input_entry = tk.Entry(root, width=50)
input_entry.pack()
send_button = tk.Button(root, text="Send", command=handle_input)
send_button.pack()
voice_button = tk.Button(root, text="Voice Chat", command=handle_voice_input)
voice_button.pack()
response_label = tk.Label(root, text="", wraplength=400)
response_label.pack()
switch_image(idle_image)
bot = HimekoStarRail()
response_label.config(text=bot.intro_message)
inactivity_timer = None
reset_inactivity_timer()

root.mainloop()
