import discord
import os
import requests
import json
import random

client = discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {0.user}' .format(client))

@client.event
async def on_message(message):
	print('Test')

client.run(os.getenv('TOKEN'))