# superphun-listener
a python bot that listens to a channel and automagically downloads images and splits them in four.

This script builds upon code published here: https://medium.com/@neonforge/how-to-create-a-discord-bot-to-download-midjourney-images-automatically-python-step-by-step-guide-3e76d3282871 Just follow the instructions on how to create your own personal Discord bot, and away you go.

Unfortunately, the original code split all images - whether they were grids or not - and had time-out issues with Discord. Adding to the code is the dumping of Discord message content so that you may reconstruct your prompts. Please remember, images have the job id imbedded in the name.

Images are dropped in a subdirectory off of the one in which the script resides named "output"; prompts share the same name as the images and are located in the directory "message_text." "input" are scratch directories where the initial images are dropped and split.

Contents:
superphun-listener.py -> python script
suprphun-listener.bat -> windows batch file that will execute the python script/ be sure to specify superphun-listener.py location
