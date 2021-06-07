import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from pyowm.owm import OWM
import os

bot = commands.Bot(command_prefix='!')
owm = OWM('17d978ab62088ebbeab69878b3172d7c')

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

@bot.command(pass_context=True)
async def weather(ctx, location):
    mgr = owm.weather_manager()
    weatherInfo = mgr.weather_at_place(location).weather # Stores all weather info at that location
    weatherInfoList = [] # Holds all specific weather information
    weatherInfoList.append("Temperature: " + str(weatherInfo.temperature()['temp'] -273.15) + " °C") # Add current temperature in °C
    #weatherInfoList.append("Humidity: " + str(weatherInfo.get_humidity())+ " %") # Add current humidity in %
    #weatherInfoList.append(str(weatherInfo.get_detailed_status()))
    
    for i in range(len(weatherInfoList)): # Sends all information stored in weatherInfoList
        await ctx.send(weatherInfoList[i])



bot.run("NzY4MTc2MjM5NjkyMjE4NDU5.X48p3w.BmgJCOwqboe8ao7zF1GK3DYSUeo")