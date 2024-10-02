from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import pygame
import time

# Load the DialoGPT model and tokenizer
model_name = "microsoft/DialoGPT-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Load GIFs
idle_gif = "D:/AI_Waifu_Project/idle.gif"
talking_gif = "D:/AI_Waifu_Project/talking.gif"

# Function to load and play GIF
def play_gif(gif_path):
    gif = pygame.image.load(gif_path)
    screen.blit(gif, (0, 0))
    pygame.display.update()

# Function to generate response from the model
def generate_response(input_text):
    inputs = tokenizer.encode(input_text + tokenizer.eos_token, return_tensors="pt")
    reply_ids = model.generate(inputs, max_length=1000)
    reply = tokenizer.decode(reply_ids[:, inputs.shape[-1]:][0], skip_special_tokens=True)
    return reply

# Main loop
running = True
user_input = ""
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                play_gif(talking_gif)
                response = generate_response(user_input)
                print("AI:", response)
                user_input = ""
                time.sleep(2)  # Simulate speaking duration
                play_gif(idle_gif)
            else:
                user_input += event.unicode

    play_gif(idle_gif)
    pygame.display.update()

pygame.quit()
