from secret_handler import parse_secrets
import discord
import json
import shlex
import sys
import os


# Will only run on my personal server if this is true.
EXPERIMENTAL = False


client = discord.Client()
# settings, persistant stuff, token, etc defined here.
secrets = parse_secrets()
with open("config.json", "r") as f:
    config = json.load(f)
with open("response.json", "r") as f:
    response = json.load(f)


@client.event
async def on_ready():
    print(f"{client.user} has been enabled.")


@client.event
async def on_message(message):
    
    # to not execute code if message is sent by bot
    if message.author == client.user:
        return
    elif message.guild.id != secrets["SERVER_ID"] and not EXPERIMENTAL:
        return
    
    
    role_ids = [role.id for role in message.author.roles]
    common_roles = [i for i in role_ids if i in response]
    
    
    if any([i for i in [secrets["MOD_ID"], secrets["ADMIN_ID"], secrets["OWNER_ID"]] if i in role_ids]) or message.author.id == secrets["DIEGO_ID"]:
        if message.content == "prefix?":
            await message.channel.send(f"Current prefix: {config['prefix']}")
        
        if message.content.startswith(f"{config['prefix']}newprefix"):
            elements = shlex.split(message.content)
            config["prefix"] = elements[1]
            with open("config.json", "w") as f:
                json.dump(config, f)
            await message.channel.send(f"Changed command prefix to: {config['prefix']}")
            
        elif message.content.startswith(f'{config["prefix"]}newrole'):
            elements = shlex.split(message.content)
            response[int(elements[1])] = elements[2]
            with open("response.json", "w") as f:
                json.dump(response, f)
            await message.channel.send(f"Added Response to role: {message.guild.get_role(int(elements[1])).name}")
        
        elif message.content.startswith(f'{config["prefix"]}delrole'):
            elements = shlex.split(message.content)
            response.pop(int(elements[1]))
            with open("response.json", "w") as f:
                json.dump(response, f)
            await message.channel.send(f"Removed response for role: {message.guild.get_role(int(elements[1])).name}")
        
        elif message.content.startswith(f'{config["prefix"]}newid'):
            elements = shlex.split(message.content)
        
        elif message.content.startswith(f'{config["prefix"]}delid'):
            elements = shlex.split(message.content)
    
    
    if any(common_roles):
        for role in common_roles:
            await message.channel.send(response[role])
    


client.run(secrets["DISCORD_TOKEN"])