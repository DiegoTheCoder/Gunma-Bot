from secret_handler import parse_secrets
import discord
import json
import shlex
import sys
import os


# Will only run on my personal server if this is true.
EXPERIMENTAL = True


client = discord.Client()
# settings, persistant stuff, token, etc defined here.
secrets = parse_secrets()
with open("config.json", "r") as f:
    config = json.load(f)
with open("responses.json", "r") as f:
    try:
        response = json.load(f)
    except json.decoder.JSONDecodeError:
        response = {}

@client.event
async def on_ready():
    print(f"{client.user} has been enabled.")

@client.event
async def on_message(message):
    # to not execute code if message is sent by bot
    if message.author == client.user:
        return
    elif message.guild.id == secrets["SERVER_ID"]:
        return
    
    role_ids = [role.id for role in message.author.roles]
    
    if any([i for i in [secrets["MOD_ID"], secrets["ADMIN_ID"], secrets["OWNER_ID"]] if i in role_ids]) or message.author.id == secrets["DIEGO_ID"]:
        if message.content.startswith(f"{config['prefix']}cprefix"):
            elements = shlex.split(message.content)
            config["prefix"] = elements[1]
            with open("config.json", "w") as f:
                json.dump(config, f)
            await message.channel.send(f"Changed command prefix to: {config['prefix']}")
        elif message.content.startswith(f'{config["prefix"]}nrrole'):
            pass
        elif message.content.startswith(f'{config["prefix"]}nrid'):
            pass
    
            
    # if 971312988848001094 in [role.id for role in message.author.roles]:
    #     await message.channel.send("Shutup.")
    #     print(f"Silenced {message.author}")
    # elif 971670598793179146 in [role.id for role in message.author.roles]:
    #     await message.channel.send("You just got bonded.")
    #     print(f"Bonded {message.author}")


client.run(secrets["DISCORD_TOKEN"])