import discord 
from discord.ext import commands 
from discord.utils import get
import youtube_dl
import random as rd
import os

token = str(input('Koodi: '))

bot = commands.Bot(command_prefix = '.')

@bot.event
async def on_ready():
    print('Need backup!')    

@bot.command(pass_context=True)
async def backup(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print('Need backup in %s' %(channel))
        await ctx.send(f'Need backup in %s!' %(channel))
               
@bot.command(pass_context=True, aliases=['enemysighted', 'es'])
async def noob(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"Left {channel}")
        await ctx.send(f"Left {channel}")
    else:
        return
        
@bot.command(pass_context=True, aliases=['p'])
async def play(ctx, url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print('Removed old song')
    except PermissionError:
        print('Trying to delete song but it is being played')
        await ctx.send('Cannot remove song that is being played')
        return
    
    await ctx.send("Trying to play your song")
    
    voice = get(bot.voice_clients, guild=ctx.guild)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',  
            }],
        }
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('Downloading song\n')
        ydl.download([url])
        
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f'Renamed file: {file}\n')
            os.rename(file, "song.mp3")
    
    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print(f'{name} has finished playing'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.value = 0.07
    
    nname = name.rsplit("-", 2)
    await ctx.send(f'Playing: {nname[0]}')
    print('Playing your song')


@bot.command(pass_context=True, aliases=['pau'])
async def pause(ctx):
    
    voice = get(bot.voice_clients, guild=ctx.guild)
    
    if voice and voice.is_playing():
        print('Music paused')
        voice.pause()
        await ctx.send('Music paused, sir!')
    else:
        print('Music not playing')
        await ctx.send('Negative! No music playing, sir!')

@bot.command(pass_context=True, aliases=['r', 'res'])
async def resume(ctx):
    
    voice = get(bot.voice_clients, guild=ctx.guild)
    
    if voice and voice.is_paused():
        print('Music resumed')
        voice.resume()
        await ctx.send('Resumed your music, sir!')
    else:
        await ctx.send('But sir please!')
        
@bot.command(pass_context=True, aliases=['s'])
async def stop(ctx):
    
    voice = get(bot.voice_clients, guild=ctx.guild)
    
    if voice and voice.is_playing():
        print('Music stopped')
        voice.stop()
        await ctx.send('Halted thine noises, sire!')
    else:
        await ctx.send('But sir please!')
        
    song_there = os.path.isfile("song.mp3") # KORJAA TÄMÄ!
    if song_there:
        os.remove("song.mp3")
        print('Removed old song')
    else:
        return
    
@bot.command()
async def delsong(ctx):
    song_there = os.path.isfile("song.mp3")
    if song_there:
        os.remove("song.mp3")
        print('Removed old song')
    else:
        return
    
@bot.command()
async def lag(ctx):
    await ctx.send(f'{round(bot.latency * 100)} ms ')
        
@bot.command()
async def BombisA(ctx):
    await ctx.send('Getting pounded over here!')
    
@bot.command(aliases = ['drop', 'pls', 'droplz'])
async def dropplz(ctx):
    await ctx.send('But sir please!')
    
exitlist = ["AAAARGH!", "Said no and left.", "Harold fell off the map.", "Harold fucking died oh god oh fuck",
            "Harold abandoned the match and received a 7 day competitive matchmaking cooldown."]
    
@bot.command(aliases =  ['KYs','kys','Kys','KyS'])
async def KYS(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    await ctx.send(exitlist[round(rd.random()*4)])
    if voice and voice.is_connected():
        await voice.disconnect()
        exit()
    else:
        exit()
        
@bot.command()
async def die(ctx):
    exit()
    
   
    
bot.run(token)


