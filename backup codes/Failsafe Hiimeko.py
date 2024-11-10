from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import tkinter as tk
from PIL import Image, ImageTk
import time
from threading import Thread

# Load the DialoGPT model and tokenizer
model_name = "microsoft/DialoGPT-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Himeko's persona
himeko_persona = (
    "You are Himeko from Honkai Star Rail. You are the head navigator of the astral express and a skilled warrior. "
    "You are kind, wise, and always ready to help others. You have a calm and composed demeanor."
    "You speak with a gentle and reassuring tone."
    "You are a young woman with a fair complexion, bright red hair, and golden eyes. You wear a white toga gown."
    "You are also 5 foot 7 inches"
)

# Function to generate response from the model
def generate_response(input_text):
    prompt = himeko_persona + "\nUser: " + input_text + "\nHimeko:"
    inputs = tokenizer.encode(prompt + tokenizer.eos_token, return_tensors="pt")
    reply_ids = model.generate(inputs, max_length=1000)
    reply = tokenizer.decode(reply_ids[:, inputs.shape[-1]:][0], skip_special_tokens=True)
    return reply

# Function to handle user input and AI response
def handle_input():
    user_input = input_entry.get()
    input_entry.delete(0, tk.END)
    switch_gif(talking_gif)
    response = generate_response(user_input)
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

# Run Tkinter main loop
root.mainloop()
