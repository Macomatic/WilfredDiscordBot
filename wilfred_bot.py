import discord

client = discord.Client()

@client.event
async def on_ready():
    print("Bot online")

@client.event
async def on_message(message):
    if message.author != client.user:
        if message.content.startswith("!Hi"):
            await message.channel.send("Hello user!")

client.run("NzY4MTc2MjM5NjkyMjE4NDU5.X48p3w.BmgJCOwqboe8ao7zF1GK3DYSUeo")