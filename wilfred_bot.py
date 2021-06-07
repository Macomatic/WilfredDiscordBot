import discord
import logging
from datetime import datetime
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

    
#    _____ _           _      _____                                          _     
#   / ____| |         | |    / ____|                                        | |    
#  | |    | |__   __ _| |_  | |     ___  _ __ ___  _ __ ___   __ _ _ __   __| |___ 
#  | |    | '_ \ / _` | __| | |    / _ \| '_ ` _ \| '_ ` _ \ / _` | '_ \ / _` / __|
#  | |____| | | | (_| | |_  | |___| (_) | | | | | | | | | | | (_| | | | | (_| \__ \
#   \_____|_| |_|\__,_|\__|  \_____\___/|_| |_| |_|_| |_| |_|\__,_|_| |_|\__,_|___/
                                                                                 
                                                                                 
@bot.command(pass_context=True)
async def clear(ctx, number):
    # Deletes number of messages in the chat

    await ctx.message.delete()
    number = int(number)
    deleted = await ctx.channel.purge(limit=number)
    confirmDelete = discord.Embed(title='Delete Successfull!', description=f'Deleted {len(deleted)} messages in #{ctx.channel}', color=0x4fff4d)
    await ctx.channel.send(embed=confirmDelete, delete_after=3.0)



#  __          __        _   _                  _____                                          _     
#  \ \        / /       | | | |                / ____|                                        | |    
#   \ \  /\  / /__  __ _| |_| |__   ___ _ __  | |     ___  _ __ ___  _ __ ___   __ _ _ __   __| |___ 
#    \ \/  \/ / _ \/ _` | __| '_ \ / _ \ '__| | |    / _ \| '_ ` _ \| '_ ` _ \ / _` | '_ \ / _` / __|
#     \  /\  /  __/ (_| | |_| | | |  __/ |    | |___| (_) | | | | | | | | | | | (_| | | | | (_| \__ \
#      \/  \/ \___|\__,_|\__|_| |_|\___|_|     \_____\___/|_| |_| |_|_| |_| |_|\__,_|_| |_|\__,_|___/
                                                                                                   
                                                                                                   
@bot.command(pass_context=True)
async def temperature(ctx, location):
    # Gives the temperature values, weather status, and humidity in a given area

    # Init
    mgr = owm.weather_manager()
    weatherInfo = mgr.weather_at_place(location).weather # Stores all weather info at that location
    weatherInfoList = [] # Holds all specific weather information
    
    # Temperature
    weatherInfoList.append("__Temperature__")
    weatherInfoList.append("**Average Temperature: **" + str(round(weatherInfo.temperature()['temp'] -273.15,1)) + " °C") 
    weatherInfoList.append("**Minimum Temperature: **" + str(round(weatherInfo.temperature()['temp_min'] -273.15,1)) + " °C")
    weatherInfoList.append("**Maximum Temperature: **" + str(round(weatherInfo.temperature()['temp_max'] -273.15,1)) + " °C")
    weatherInfoList.append("**Current Weather Status: **" + str(weatherInfo.detailed_status).title())
    weatherInfoList.append("**Humidity: **" + str(weatherInfo.humidity)+ "%") # Add current humidity in %


    # Output
    for i in range(len(weatherInfoList)): # Sends all information stored in weatherInfoList
        await ctx.send(weatherInfoList[i])
    
@bot.command(pass_context=True)
async def wind(ctx, location):
    # Gives the wind speed in km/h for a particular location

    # Init
    mgr = owm.weather_manager()
    weatherInfo = mgr.weather_at_place(location).weather # Stores all weather info at that location
    weatherInfoList = [] # Holds all specific weather information

    # Wind
    weatherInfoList.append("__Wind__")
    weatherInfoList.append("**Wind Speed: **" + str(round(weatherInfo.wind()['speed']*3.6,2)) + " km/h")

    # Output
    for i in range(len(weatherInfoList)): # Sends all information stored in weatherInfoList
        await ctx.send(weatherInfoList[i])

@bot.command(pass_context=True)
async def rainfall(ctx,location,timeframe):
    # Gives the previous rainfall in a given timeframe for a particular location. The timeframe is either 1h or 3h ago

    # Init
    mgr = owm.weather_manager()
    weatherInfo = mgr.weather_at_place(location).weather # Stores all weather info at that location
    weatherInfoList = [] # Holds all specific weather information
    lastHour = (timeframe == '1h') # Need to implement rain command to take in param to indicate 1h or 3h

    # Rainfall
    weatherInfoList.append("__Rainfall__")
    rain_dict = mgr.weather_at_place(location).weather.rain
    if lastHour:
        if '1h' in rain_dict:
            weatherInfoList.append("**Rain in the last hour: **" + str(rain_dict['1h']) + " mm")
        
        else:
            weatherInfoList.append("**Rain in the last hour:** 0.0 mm")

    if not lastHour:
        if '3h' in rain_dict:
            weatherInfoList.append("**Rain in the last 3 hours:** " + str(rain_dict['3h']) + " mm")
        
        else:
            weatherInfoList.append("**Rain in the last 3 hours:** 0.0 mm")

    # Output
    for i in range(len(weatherInfoList)): # Sends all information stored in weatherInfoList
        await ctx.send(weatherInfoList[i])

@bot.command(pass_context=True)
async def sun(ctx, location):
    # Gives the sunrise and sunset times for a given location

    # Init
    mgr = owm.weather_manager()
    weatherInfo = mgr.weather_at_place(location).weather # Stores all weather info at that location
    weatherInfoList = [] # Holds all specific weather information

    # Sunrise/Sunset
    weatherInfoList.append("__Sunrise and Sunset__")
    sunrise = weatherInfo.sunrise_time() - 14400 # -14400 for GMT to EST offset; work on a general solution
    sunset = weatherInfo.sunset_time() - 14400

    weatherInfoList.append("**Time of Sunrise: **" + datetime.utcfromtimestamp(sunrise).strftime('%H:%M:%S') + " EST")
    weatherInfoList.append("**Time of Sunset: **" + datetime.utcfromtimestamp(sunset).strftime('%H:%M:%S') + " EST")

    # Output
    for i in range(len(weatherInfoList)): # Sends all information stored in weatherInfoList
        await ctx.send(weatherInfoList[i])

@bot.command(pass_context=True)
async def tennis(ctx, location):
    # Provides key weather-related information related to playing Tennis and gives a recommendation if playing tennis is viable

    # Init
    mgr = owm.weather_manager()
    weatherInfo = mgr.weather_at_place(location).weather # Stores all weather info at that location
    weatherInfoList = [] # Holds all specific weather information

    #Rainfall check
    rain3h = 0.0
    rain_dict = mgr.weather_at_place(location).weather.rain
    if '3h' in rain_dict:
        rain3h = int(rain_dict['3h'])
    



bot.run("NzY4MTc2MjM5NjkyMjE4NDU5.X48p3w.BmgJCOwqboe8ao7zF1GK3DYSUeo")