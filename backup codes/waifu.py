import logging
import os
import tkinter as tk
from PIL import Image, ImageTk
import time
from threading import Thread
from groq import Groq

class HimekoStarRail:
    def __init__(self):
        self.api_key = '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'
        self.client = Groq(api_key=self.api_key)
        print("Starting up systems aboard the Astral Express...")
        print("\n*Adjusts white dress and flips red hair*")
        print("Hey there, Trailblazer! I'm Himeko, your guide aboard the Astral Express.")
        print("As the train's brilliant and beautiful genius, I'm here to help chart our course through the stars!")

    def generate_response(self, user_input):
        try:
            # Create Himeko's personality prompt
            prompt = (
                "Himeko is the brilliant and caring navigator of the Astral Express. "
                "She has flowing red hair, golden eyes, and wears an elegant white dress. "
                "Her responses are warm, enthusiastic, and often reference space travel and exploration.\n"
                f"Trailblazer: {user_input}\n"
                "Himeko:"
            )

            # Use Groq API to generate the response
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
            return response.split("Himeko:")[-1].strip()

        except Exception as e:
            logging.error(f"Error generating response: {e}")
            return "Oh no! I encountered a problem while trying to respond."

# Function to handle user input and AI response
def handle_input():
    user_input = input_entry.get()
    input_entry.delete(0, tk.END)
    switch_gif(talking_gif)
    response = bot.generate_response(user_input)
    response_label.config(text="Himeko: " + response)
    time.sleep(2)  # Simulate speaking duration
    switch_gif(idle_gif)

# Function to switch GIFs
def switch_gif(gif_path):
    gif = Image.open(gif_path)
    frames = []
    try:
        while True:
            frames.append(ImageTk.PhotoImage(gif.copy()))
            gif.seek(len(frames))  # Move to the next frame
    except EOFError:
        pass
    gif_label.config(image=frames[0])
    gif_label.frames = frames
    animate_gif(gif_label)

# Function to animate GIF
def animate_gif(label):
    frames = label.frames
    def update_frame(frame_index):
        label.config(image=frames[frame_index])
        frame_index = (frame_index + 1) % len(frames)
        label.after(100, update_frame, frame_index)
    update_frame(0)

# Initialize Tkinter for text input
root = tk.Tk()
root.title("Chat with Himeko Waifu")

# Load GIFs
idle_gif = "D:/python/AI_Waifu_Project/idle.gif"
talking_gif = "D:/python/AI_Waifu_Project/talking.gif"

# Add the GIF label
gif_label = tk.Label(root)
gif_label.pack()

# Add the input entry and send button
input_entry = tk.Entry(root, width=50)
input_entry.pack()

send_button = tk.Button(root, text="Send", command=handle_input)
send_button.pack()

# Add the response label
response_label = tk.Label(root, text="", wraplength=400)
response_label.pack()

# Start with the idle GIF
switch_gif(idle_gif)

# Create the bot instance
bot = HimekoStarRail()

# Run Tkinter main loop
root.mainloop()
