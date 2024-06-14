# superphun-listener v1
# victoria.synthetic
# https://github.com/victoriasynthetic/superphun-listener

import discord
from discord.ext import commands
from discord import TextChannel
import requests
from dotenv import load_dotenv
from PIL import Image
import os
import time
import asyncio

discord_token = "yourtokenhere"

load_dotenv()
client = commands.Bot(command_prefix="*", intents=discord.Intents.all())
directory = os.getcwd()
print(directory)

async def download_image(url, filename, message, input_folder, output_folder):
    response = requests.get(url)
    if response.status_code == 200:

        # Define the input and output folder paths
        input_folder = f"input_{message.channel.name}_{message.channel.id}"
        output_folder = f"output_{message.channel.name}_{message.channel.id}"

        # Check if the input and output folder exists, and create it if necessary
        if not os.path.exists(input_folder):
            os.makedirs(input_folder)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        with open(f"{directory}/{input_folder}/{filename}", "wb") as f:
            f.write(response.content)
            
        print(f"Image downloaded: {filename}")
                
        if "Image #" not in filename:
            file_prefix = os.path.splitext(filename)[0]
            split_image(input_folder, filename, output_folder, file_prefix)
            await message.channel.send("Image processed and saved.")
            
        else:
            os.rename(
                f"{directory}/{input_folder}/{filename}",
                f"{directory}/{output_folder}/{filename}"
            )
        # Delete the input file      
        await message.channel.send("Image moved to output folder.")
        os.remove(f"{directory}/{input_folder}/{filename}")

      
def split_image(input_folder, filename, output_folder, file_prefix):
    with Image.open(f"{directory}/{input_folder}/{filename}") as im:
        # Get the width and height of the original image
        width, height = im.size
        # Calculate the middle points along the horizontal and vertical axes
        mid_x = width // 2
        mid_y = height // 2
        # Split the image into four equal parts
        top_left = im.crop((0, 0, mid_x, mid_y))
        top_right = im.crop((mid_x, 0, width, mid_y))
        bottom_left = im.crop((0, mid_y, mid_x, height))
        bottom_right = im.crop((mid_x, mid_y, width, height))
        
        # Save the output images with dynamic names
        top_left.save(f"{directory}/{output_folder}/{file_prefix}_0.png")
        top_right.save(f"{directory}/{output_folder}/{file_prefix}_1.png")
        bottom_left.save(f"{directory}/{output_folder}/{file_prefix}_2.png")
        bottom_right.save(f"{directory}/{output_folder}/{file_prefix}_3.png")
        
        # return top_left, top_right, bottom_left, bottom_right     

@client.event
async def on_ready():
    print("Bot connected")
    print(f"Logged in as {client.user}")
    
@client.event
async def on_message(message):
    print(message.content)
    
    output_folder = f"output_{message.channel.name}_{message.channel.id}"
    input_folder = f"input_{message.channel.name}_{message.channel.id}"
    text_folder = f"text_{message.channel.name}_{message.channel.id}"
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for attachment in message.attachments:
        if attachment.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".wbem")):
            try:
                response = requests.get(attachment.url)
                if response.status_code == 200:
                    if "Image #" in message.content:
                        with open(f"{directory}/{output_folder}/{attachment.filename}", "wb") as f:
                            f.write(response.content)
                        await message.channel.send("Image moved to output folder.")
                    else:
                        with open(f"{directory}/{input_folder}/{attachment.filename}", "wb") as f:
                            f.write(response.content)
                        print(f"Image downloaded: {attachment.filename}")
                        
                        if "Image #" not in attachment.filename:
                            await download_image(
                                attachment.url, attachment.filename, message, input_folder, output_folder
                            )
                                            
            except Exception as e:
                print(f"Error downloading or processing image: {e}")
                continue
                
            if attachment.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                try:
                    if not os.path.exists(text_folder):
                        os.makedirs(text_folder)
                    
                    message_text = message.content
                    text_filename = f"{attachment.filename}.txt"
                    with open(os.path.join(text_folder, text_filename), "w", encoding="utf-8") as text_file:
                        text_file.write(message_text)
                        
                except Exception as e:
                    print(f"Error saving message text: {e}")
                continue
                
            # Save the message content as a text file
            if attachment.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                try:
                    # Create a folder to store text files if it doesn't exist
                    text_folder = f"text_{message.channel.name}_{message.channel.id}"
                    if not os.path.exists(text_folder):
                        os.makedirs(text_folder)

                    # Save the message content to a text file
                    message_text = message.content
                    text_filename = f"{attachment.filename}.txt"
                    with open(os.path.join(text_folder, text_filename), "w", encoding="utf-8") as text_file:
                        text_file.write(message_text)
                except Exception as e:
                    print(f"Error saving message text: {e}")
                    
client.run(discord_token)
