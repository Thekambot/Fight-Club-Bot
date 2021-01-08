import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "kurwa"]

starter_encouragments = ["Cheer up!", "Hang in there.", "Walnij se monsterka byczku."]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_encouragments(message):
  if "encouragments" in db.keys():
    encouragments = db["encouragments"]
    encouragments.append(message)
    db["encouragments"] = encouragments
  else:
    db["encouragments"] = [message]

def delete_encouragment(index):
  encouragments = db["encouragments"]
  if len(encouragments) > index:
    del encouragments[index]
  db["encouragments"] = encouragments

@client.event
async def on_ready():
  print('We have logged in as {0.user}' .format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return  
  
  msg = message.content

  if msg.startswith('$hello'):
    await message.channel.send('Hello!')

  if msg.startswith('$quote'):
    quote = get_quote()
    await message.channel.send(quote)

  if db["responding"] == True:
    options = starter_encouragments
    if "encouragments" in db.keys():
      options = options + db["encouragments"]

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    new_message = msg.split("$new ", 1)[1]
    update_encouragments(new_message)
    await message.channel.send("New message added byczku.")

  if msg.startswith("$del"):
    encouragments = []
    if "encouragments" in db.keys():
      index = int(msg.split("$del", 1)[1])
      delete_encouragment(index)
      encouragments = db["encouragments"]
    await message.channel.send(encouragments)

  if msg.startswith("$list"):
    encouragments = []
    if "encouragments" in db.keys():
      encouragments = db["encouragments"]
    await message.channel.send(encouragments)

  if msg.startswith("$ryj"):
    status = msg.split("$ryj ", 1)[1]
    if status.lower() == "true":
      db["responding"] = True
      return_msg = "AAAAAAAAAAAAA!"
    elif status.lower() == "false":
      return_msg = "Dobra już zamykam ryj..."
      db["responding"] = False
    else:
      return_msg = "Co ty pierdolisz?"
    await message.channel.send(return_msg)

keep_alive()
client.run(os.getenv('TOKEN'))