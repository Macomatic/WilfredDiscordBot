import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot

bot = commands.Bot(command_prefix='!')

print("Initializing Wilfred Bot...")

@bot.event
async def on_ready():
    #Prints to console when the bot is ready/runs
    print(bot.user.name)
    print(bot.user.id)
    print("Online")

@bot.command()
async def test(ctx,*arg):
    await ctx.send('{}'.format(" ".join(arg)))


bot.run("NzY4MTc2MjM5NjkyMjE4NDU5.X48p3w.BmgJCOwqboe8ao7zF1GK3DYSUeo")