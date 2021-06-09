import discord
import logging
from datetime import datetime
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_choice, create_option, create_permission
from discord_slash.model import SlashCommandPermissionType
from pyowm.owm import OWM
import os
from pyowm.utils.formatting import timeformat

from pyowm.weatherapi25 import one_call, weather

bot = commands.Bot(command_prefix='!')
owm = OWM('17d978ab62088ebbeab69878b3172d7c')

print("Initializing Wilfred Bot...")

@bot.event
async def on_ready():
    #Prints to console when the bot is ready/runs
    print(bot.user.name)
    print(bot.user.id)
    print("Online")
    await bot.change_presence(activity = discord.Game('with Tea and Biscuits'))

@bot.command()
async def test(ctx,*arg):
    await ctx.send('{}'.format(" ".join(arg)))

slash = SlashCommand(bot, sync_commands=True)

# Server ID
guild_ids = [768176653620215869]

    
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
    confirmDelete = discord.Embed(title='Delete Successful!', description=f'Deleted {len(deleted)} messages in #{ctx.channel}', color=0x4fff4d)
    await ctx.channel.send(embed=confirmDelete, delete_after=3.0)

# @slash.slash(name="clear", description="Delete messages.", guild_ids=guild_ids)
# async def clear(ctx, number:int):
#     deleted = await ctx.channel.purge(limit=number)
#     confirmDelete = discord.Embed(title='Delete Successful', description=f'Deleted {len(deleted)} messages in #{ctx.channel}', color=0x4fffd)
#     await ctx.send(embed=confirmDelete, delete_after=3.0)

@bot.command(pass_context=True)
async def join(ctx):
    # Joins a voice channel

    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You need to be in a voice channel.")

@bot.command(pass_context=True)
async def leave(ctx):
    # Leaves a voice channel

    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send("I'm not in a voice channel.")

#  __          __        _   _                  _____                                          _     
#  \ \        / /       | | | |                / ____|                                        | |    
#   \ \  /\  / /__  __ _| |_| |__   ___ _ __  | |     ___  _ __ ___  _ __ ___   __ _ _ __   __| |___ 
#    \ \/  \/ / _ \/ _` | __| '_ \ / _ \ '__| | |    / _ \| '_ ` _ \| '_ ` _ \ / _` | '_ \ / _` / __|
#     \  /\  /  __/ (_| | |_| | | |  __/ |    | |___| (_) | | | | | | | | | | | (_| | | | | (_| \__ \
#      \/  \/ \___|\__,_|\__|_| |_|\___|_|     \_____\___/|_| |_| |_|_| |_| |_|\__,_|_| |_|\__,_|___/
                                                                                                   
                                                                                                   
@bot.command(pass_context=True, name = 'temperature', help = 'Fetches temperature information')
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

@bot.command(pass_context=True)
async def dForecast(ctx):
    # Provides a comprehesive table displaying the hourly forcast 
    """
    Example Display
    +------------------------------------------------------------------------------------------------------+
    |                                                  DAY                                                 |
    +-------+-------+------+-------+-------+-------+------+------+------+------+------+------+------+------+
    |  HOUR |  8 AM | 9 AM | 10 AM | 11 AM | 12 AM | 1 PM | 2 PM | 3 PM | 4 PM | 5 PM | 6 PM | 7 PM | 8 PM |
    +-------+-------+------+-------+-------+-------+------+------+------+------+------+------+------+------+
    |  STAT |   ""  |      |       |       |       |      |      |      |      |      |      |      |      |
    +-------+-------+------+-------+-------+-------+------+------+------+------+------+------+------+------+
    |  TEMP |   32  |      |       |       |       |      |      |      |      |      |      |      |      |
    +-------+-------+------+-------+-------+-------+------+------+------+------+------+------+------+------+
    | FEELS |   35  |      |       |       |       |      |      |      |      |      |      |      |      |
    +-------+-------+------+-------+-------+-------+------+------+------+------+------+------+------+------+
    | P.O.P |  32%  |      |       |       |       |      |      |      |      |      |      |      |      |
    +-------+-------+------+-------+-------+-------+------+------+------+------+------+------+------+------+
    | HUMID |  120% |      |       |       |       |      |      |      |      |      |      |      |      |
    +-------+-------+------+-------+-------+-------+------+------+------+------+------+------+------+------+
    |  WIND | 9km/h |      |       |       |       |      |      |      |      |      |      |      |      |
    +-------+-------+------+-------+-------+-------+------+------+------+------+------+------+------+------+   
    """
    
    # Init
    mgr = owm.weather_manager()
    oneCall = mgr.one_call(lat=43.845009, lon=-79.561396) # Location
    oneCallList = []
    timeTranslate = {"00":"12 AM", "01":"1 AM", "02":"2 AM", "03":"3 AM", "04":"4 AM", "05":"5 AM", "06":"6 AM", "07":"7 AM", "08":"8 AM", "09":"9 AM", "10":"10 AM", "11":"11 AM", "12":"12 PM", "13":"1 PM", "14":"2 PM", "15":"3 PM", "16":"4 PM", "17":"5 PM", "18":"6 PM", "19":"7 PM", "20":"8 PM", "21":"9 PM", "22":"10 PM", "23":"11 PM"} # Dictionary to convert military time to 12 hour time 
    weatherIcons = {"few clouds":":white_sun_small_cloud:", "scattered clouds":":partly_sunny:", "broken clouds":":white_sun_cloud:", "overcast clouds":":cloud:", "clear sky":":sunny:"} # Dictionary to convert weather status into discord emojis
    weatherData = [] 

    weatherData.append(str(oneCall.current.reference_time(timeformat='date'))[0:10]) # Current date
    for time in range(-4,9): # For loop which calls 12 hours of forcast time (EST)
        # Calls time(Hour), weather status, temperature, feels like temperature, probability of precipitation, humidity, wind speed
        data = [] 
        data.append(timeTranslate[str(oneCall.forecast_hourly[time].reference_time(timeformat='date'))[11:13]]) 
        status = oneCall.forecast_hourly[time].detailed_status 
        data.append(status)
        if 'thunder' in status:
            data.append(":thunder_cloud_rain:")
        elif 'fog' in status or 'mist' in status:
            data.append(":fog:")
        elif 'snow' in status or 'freezing' in status:
            data.append(":cloud_snow:")
        elif 'rain' in status or 'drizzle' in status:
            data.append(":cloud_rain:") 
        else:
            data.append(weatherIcons[status]) # for unknown status

        data.append(oneCall.forecast_hourly[time].temperature('celsius')['temp'])
        data.append(oneCall.forecast_hourly[time].temperature('celsius')['feels_like'])
        data.append(oneCall.forecast_hourly[time].precipitation_probability)
        data.append(oneCall.forecast_hourly[time].humidity)
        data.append(round(oneCall.forecast_hourly[time].wind().get('speed',0)*3.6,2)) #convert m/s to km/h
        weatherData.append(data)
    # Input
    #oneCallList.append("+-------------------------------------------------------------------------------------------------------+")
    #oneCallList.append("|                                                  {:s}                                                                                             |".format(str(oneCall.current.reference_time(timeformat='date'))[:10]))
    #oneCallList.append("+-------------------------------------------------------------------------------------------------------+")
    
    # Output
    for i in range(len(weatherData)): # Sends all information stored in weatherData
        await ctx.send(weatherData[i])

bot.run("NzY4MTc2MjM5NjkyMjE4NDU5.X48p3w.BmgJCOwqboe8ao7zF1GK3DYSUeo")