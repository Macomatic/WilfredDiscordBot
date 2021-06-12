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
import youtube_dl
from pyowm.utils.formatting import timeformat
from discord.ext.commands.cooldowns import BucketType

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
    await bot.change_presence(activity = discord.Game('with Alfred'))

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
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member} has been kicked.")

def perms(ctx):
    return ctx.author.id == 213051396692508673, 498881376917913604

# Command With Permissions
@bot.command(pass_context=True)
@commands.check(perms) # Checks function for who can use the command
@commands.cooldown(1, 10, BucketType.user) # Command Cooldown: 1 use every 10 seconds per user
async def permTest(ctx):
    await ctx.send("This works")

# @permTest.error # Checks for errors for permTest command
# async def permTest_error(ctx, error):
#     if isinstance(error, commands.CheckFailure):
#         await ctx.send("You do not have permissions to use this command.")

@bot.event # Checks for errors for all commands
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You do not have permissions to use this command.")

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
async def forecast(ctx, location):
    # Provides a comprehesive table displaying the hourly forcast 
    
    # Init
    mgr = owm.weather_manager()
    oneCall = mgr.one_call(lat=mgr.weather_at_place(location).location.lat, lon=mgr.weather_at_place(location).location.lon) # Location
    oneCallList = "" 
    oneCallList2 = ""   
    timeTranslate = {"00":"8 PM", "01":"9 PM", "02":"10 PM", "03":"11 PM", "04":"12 AM", "05":"1 AM", "06":"2 AM", "07":"3 AM", "08":"4 AM", "09":"5 AM", "10":"6 AM", "11":"7 AM", "12":"8 AM", "13":"9 AM", "14":"10 AM", "15":"11 AM", "16":"12 PM", "17":"1 PM", "18":"2 PM", "19":"3 PM", "20":"4 PM", "21":"5 PM", "22":"6 PM", "23":"7 PM"} # Dictionary to convert military time to 12 hour time, GMT to EST
    weatherIcons = {"few clouds":"🌤️", "scattered clouds":"⛅", "broken clouds":"🌥️", "overcast clouds":"☁️", "clear sky":"☀️"} # Dictionary to convert weather status into discord emojis
    weatherData = [] 

    # API CALLS
    weatherData.append(str(oneCall.current.reference_time(timeformat='date'))[0:10]) # Current date
    for time in range(1,10): # For loop which calls 9 hours of forcast time (EST)
        # Calls time(Hour), weather status, temperature, feels like temperature, probability of precipitation, humidity, wind speed
        data = [] 
        data.append(timeTranslate[str(oneCall.forecast_hourly[time].reference_time(timeformat='date'))[11:13]]) # Hour of the day
        status = oneCall.forecast_hourly[time].detailed_status 
        if 'thunder' in status: # statments to generalize weather status into icons
            data.append("⛈️")
        elif 'fog' in status or 'mist' in status: 
            data.append("🌫️")
        elif 'snow' in status or 'freezing' in status:
            data.append("🌨️")
        elif 'rain' in status or 'drizzle' in status:
            data.append("🌧️") 
        else:
            data.append(weatherIcons[status]) # for unknown status
        data.append(status.split()) # split detailed multiword status
        data.append(str(round(float(oneCall.forecast_hourly[time].temperature('celsius')['temp']),1)) + "°C") # temperature
        data.append(str(round(float(oneCall.forecast_hourly[time].temperature('celsius')['feels_like']),1)) + "°C") # feels like temperature
        data.append(str(oneCall.forecast_hourly[time].precipitation_probability) + " %") # probability of precipitation
        data.append(str(oneCall.forecast_hourly[time].humidity) + " %") #
        data.append(str(round(oneCall.forecast_hourly[time].wind().get('speed',0)*3.6,1)) + " KM/H") #convert m/s to km/h
        weatherData.append(data)

    # Input
    oneCallList += "```   +-----------------------------------------------------------------------------------------------------------------------------+"
    oneCallList += "\n   |{:^125s}|".format(weatherData[0])
    oneCallList += "\n   |{:^125s}|".format(location)
    oneCallList += "\n   +--------+------------+------------+------------+------------+------------+------------+------------+------------+------------+"
    oneCallList += "\n   |  HOUR  |{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|".format(weatherData[1][0], weatherData[2][0], weatherData[3][0], weatherData[4][0], weatherData[5][0], weatherData[6][0], weatherData[7][0], weatherData[8][0], weatherData[9][0])
    oneCallList += "\n   +--------+------------+------------+------------+------------+------------+------------+------------+------------+------------+"
    oneCallList += "\n   |        |{:^12s}|{:^11s}|{:^12s}|{:^11s}|{:^12s}|{:^11s}|{:^12s}|{:^11s}|{:^12s}|".format(weatherData[1][1], weatherData[2][1], weatherData[3][1], weatherData[4][1], weatherData[5][1], weatherData[6][1], weatherData[7][1], weatherData[8][1], weatherData[9][1])
    oneCallList += "\n   | STATUS |{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|".format(weatherData[1][2][0], weatherData[2][2][0], weatherData[3][2][0], weatherData[4][2][0], weatherData[5][2][0], weatherData[6][2][0], weatherData[7][2][0], weatherData[8][2][0], weatherData[9][2][0])
    oneCallList += "\n   |        |{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|".format(weatherData[1][2][-1], weatherData[2][2][-1], weatherData[3][2][-1], weatherData[4][2][-1], weatherData[5][2][-1], weatherData[6][2][-1], weatherData[7][2][-1], weatherData[8][2][-1], weatherData[9][2][-1])
    oneCallList += "\n   +--------+------------+------------+------------+------------+------------+------------+------------+------------+------------+"
    oneCallList += "\n   |  TEMP  |{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|".format(weatherData[1][3], weatherData[2][3], weatherData[3][3], weatherData[4][3], weatherData[5][3], weatherData[6][3], weatherData[7][3], weatherData[8][3], weatherData[9][3])
    oneCallList += "\n   +--------+------------+------------+------------+------------+------------+------------+------------+------------+------------+```"
    oneCallList2 += "```   +--------+------------+------------+------------+------------+------------+------------+------------+------------+------------+"
    oneCallList2 += "\n   |  FEELS |{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|".format(weatherData[1][4], weatherData[2][4], weatherData[3][4], weatherData[4][4], weatherData[5][4], weatherData[6][4], weatherData[7][4], weatherData[8][4], weatherData[9][4])
    oneCallList2 += "\n   +--------+------------+------------+------------+------------+------------+------------+------------+------------+------------+"
    oneCallList2 += "\n   |  P.O.P |{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|".format(weatherData[1][5], weatherData[2][5], weatherData[3][5], weatherData[4][5], weatherData[5][5], weatherData[6][5], weatherData[7][5], weatherData[8][5], weatherData[9][5])
    oneCallList2 += "\n   +--------+------------+------------+------------+------------+------------+------------+------------+------------+------------+"
    oneCallList2 += "\n   |  HUMID |{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|".format(weatherData[1][6], weatherData[2][6], weatherData[3][6], weatherData[4][6], weatherData[5][6], weatherData[6][6], weatherData[7][6], weatherData[8][6], weatherData[9][6])
    oneCallList2 += "\n   +--------+------------+------------+------------+------------+------------+------------+------------+------------+------------+"
    oneCallList2 += "\n   |  WIND  |{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|{:^12s}|".format(weatherData[1][7], weatherData[2][7], weatherData[3][7], weatherData[4][7], weatherData[5][7], weatherData[6][7], weatherData[7][7], weatherData[8][7], weatherData[9][7])
    oneCallList2 += "\n   +--------+------------+------------+------------+------------+------------+------------+------------+------------+------------+```"
    
    # Output
    #for i in range(len(oneCallList)): # Sends all information stored in weatherData
    await ctx.send(oneCallList)
    await ctx.send(oneCallList2)


#   __  __           _         _____                                          _     
#  |  \/  |         (_)       / ____|                                        | |    
#  | \  / |_   _ ___ _  ___  | |     ___  _ __ ___  _ __ ___   __ _ _ __   __| |___ 
#  | |\/| | | | / __| |/ __| | |    / _ \| '_ ` _ \| '_ ` _ \ / _` | '_ \ / _` / __|
#  | |  | | |_| \__ \ | (__  | |___| (_) | | | | | | | | | | | (_| | | | | (_| \__ \
#  |_|  |_|\__,_|___/_|\___|  \_____\___/|_| |_| |_|_| |_| |_|\__,_|_| |_|\__,_|___/
                                                                                  
                                                   
@bot.command(pass_context=True)
async def play(ctx, url:str):
    song = os.path.isfile("song.mp3")
    try:
        if song:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Music is currently playing! Use the 'stop' command before trying to play another song")
        return

    vc = ctx.author.voice.channel
    await vc.connect()
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


@bot.command(pass_context=True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send("_Wilfred_ is not in a voice channel!")

@bot.command(pass_context=True)
async def pause(ctx):
    voice = voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("There audio is already paused!")

@bot.command(pass_context=True)
async def resume(ctx):
    voice = voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is already playing!")









bot.run("NzY4MTc2MjM5NjkyMjE4NDU5.X48p3w.BmgJCOwqboe8ao7zF1GK3DYSUeo")