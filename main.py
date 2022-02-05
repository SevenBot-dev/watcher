import asyncio
import discord
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print("SevenBot Wathcer is ready!")

@client.event
async def on_presence_update(before, after):
    if after.id != 718760319207473152 or not before:
        return
    if after.status == discord.Status.offline:
        print("Offline detected, watching...")
        try:
            await client.wait_for("presence_update", check=lambda member, _: member.id == 718760319207473152, timeout=60)
        except asyncio.TimeoutError:
            print("Not restarting in 60s, starting...")
            subprocess.Popen("bash -l start.sh".split())
        else:
            print("Restarted, ignoring...")

@client.event
async def on_message(message):
    if message.channel.id != 934611880146780200:
        return
    if message.content == "em:shutdown":
        print("Shutdown signal received, shutting down...")
        open("../sevenbot/shutdown", "w").close()

client.run(os.getenv("TOKEN"))
