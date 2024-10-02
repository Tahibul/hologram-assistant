from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import pygame
import time
import tkinter as tk
from threading import Thread

# Load the DialoGPT model and tokenizer
model_name = "microsoft/DialoGPT-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Initialize Pygame
pygame.init()

# Load GIFs
idle_gif = "D:/AI_Waifu_Project/idle.gif"
talking_gif = "D:/AI_Waifu_Project/talking.gif"

# Function to load and play GIF
def play_gif(gif_path):
    gif = pygame.image.load(gif_path)
    screen = pygame.display.set_mode(gif.get_size())
    screen.blit(gif, (0, 0))
    pygame.display.update()

# Function to generate response from the model
def generate_response(input_text):
    inputs = tokenizer.encode(input_text + tokenizer.eos_token, return_tensors="pt")
    reply_ids = model.generate(inputs, max_length=1000)
    reply = tokenizer.decode(reply_ids[:, inputs.shape[-1]:][0], skip_special_tokens=True)
    return reply

# Function to handle user input and AI response
def handle_input():
    user_input = input_entry.get()
    input_entry.delete(0, tk.END)
    play_gif(talking_gif)
    response = generate_response(user_input)
    response_label.config(text="AI: " + response)
    time.sleep(2)  # Simulate speaking duration
    play_gif(idle_gif)

# Initialize Tkinter for text input
root = tk.Tk()
root.title("Chat with Himeko Waifu")

# Create a canvas for embedding Pygame
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack()

# Add the input entry and send button below the canvas
input_entry = tk.Entry(root, width=50)
input_entry.pack()

send_button = tk.Button(root, text="Send", command=handle_input)
send_button.pack()

# Add the response label below the send button
response_label = tk.Label(root, text="", wraplength=400)
response_label.pack()

# Function to run the Pygame loop
def run_pygame():
    screen = pygame.display.set_mode((800, 600))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        play_gif(idle_gif)
        pygame.display.update()
        time.sleep(0.1)  # Reduce update frequency to lessen load

    pygame.quit()

# Run Pygame in a separate thread
pygame_thread = Thread(target=run_pygame)
pygame_thread.start()

# Run Tkinter main loop
root.mainloop()
