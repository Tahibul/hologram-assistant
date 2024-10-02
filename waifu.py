from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import tkinter as tk

# Load the DialoGPT model and tokenizer
model_name = "microsoft/DialoGPT-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

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
    response = generate_response(user_input)
    response_label.config(text="AI: " + response)

# Initialize Tkinter for text input
root = tk.Tk()
root.title("Chat with Himeko Waifu")

# Add the input entry and send button
input_entry = tk.Entry(root, width=50)
input_entry.pack()

send_button = tk.Button(root, text="Send", command=handle_input)
send_button.pack()

# Add the response label
response_label = tk.Label(root, text="", wraplength=400)
response_label.pack()

# Run Tkinter main loop
root.mainloop()
