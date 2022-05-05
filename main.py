from secret_handler import parse_secrets
import discord
import os


client = discord.Client()
secrets = parse_secrets()


@client.event
async def on_ready():
    print(f"{client.user} has been enabled.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 971312988848001094 in [role.id for role in message.author.roles]:
        await message.channel.send("Shutup.")
        # await message.delete()
        print(f"Silenced {message.author}")


client.run(secrets["DISCORD_TOKEN"])