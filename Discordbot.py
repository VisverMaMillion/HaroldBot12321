import discord 
from discord.ext import commands 
from discord.utils import get
import youtube_dl
import random as rd
import numpy as np
import os
import time

token = np.loadtxt('C:/bottoken/haroldtoken.txt', dtype= str)
workdir = os.path.dirname(__file__)
songdir = os.path.join(workdir,'songs')
bot = commands.Bot(command_prefix = '.')

def queclr(x , y ):
    folder = x
    if y == 0:
        for song in os.listdir(folder):
            filepath = os.path.join(x, song)
            os.unlink(filepath)
    else:
        pass

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Hiding on de_dust2"))
    print('Need backup!')    

@bot.command(pass_context=True)
async def backup(ctx):
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
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print('Need backup in %s' %(channel))
        await ctx.send(f'Need backup in %s!' %(channel))
    
    

    songdowndir = os.path.join(workdir,'songs/%(title)s.%(ext)s')
#    song_there = os.path.isfile("song.mp3")
#    try:
#        if song_there:
#            os.remove("song.mp3")
#            print('Removed old song')
#    except PermissionError:
#        print('Trying to delete song but it is being played')
#        await ctx.send('Cannot remove song that is being played')
#        return
    
    await ctx.send("Trying to play your song")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192', 
            }],
        'outtmpl': songdowndir
        }
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('Downloading song\n')
        ydl.download([url])
        info_dict = ydl.extract_info(url, download=False)
        title = info_dict.get('title', None)
        
    songpath = os.path.join(workdir, f'songs/{title}.mp3')
    voice.play(discord.FFmpegPCMAudio(songpath))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.value = 0.07
    
    await ctx.send(f'Playing: {title}')
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
        
@bot.command(pass_context=True, aliases=['s'])  #muokkaa poistamaan que
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    
    if voice and voice.is_playing():
        print('Music stopped')
        voice.stop()
        queclr(songdir, 0)
        await ctx.send('Halted thine noises, sire!')
    else:
        await ctx.send('But sir please!')
        queclr(songdir, 0)
    return

    
@bot.command()
async def delsong(ctx):
    queclr(songdir, 0)
    
@bot.command()
async def lag(ctx):
    await ctx.send(f'{round(bot.latency * 100)} ms ')
        
@bot.command()
async def BombisA(ctx):
    await ctx.send('Getting pounded over here!')
    
@bot.command(aliases = ['drop', 'pls', 'droplz'])
async def dropplz(ctx):
    await ctx.send('But sir please!')
    
exitlist = ["AAAARGH!", "Said no and left.", "Harold fell off the map.", "Harold fucking died.",
            "Harold abandoned the match and received a 7 day competitive matchmaking cooldown."]

deathlist = ["death1", "death2", "death3", "headshot", "olkapää", "aisaatana"]

@bot.command(aliases =  ['KYs','kys','Kys','KyS', "kYS"])
async def KYS(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    try:
        voice.stop()
    except AttributeError:
        pass
    if voice and voice.is_connected():
        deathdir = os.path.join(workdir, f'sfx/deathsounds/{rd.choice(deathlist)}.mp3')
        voice.play(discord.FFmpegPCMAudio(deathdir))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.value = 0.4
        time.sleep(2)
        await voice.disconnect()
        await ctx.send(rd.choice(exitlist))
        exit()
    else:
        await ctx.send(rd.choice(exitlist))
        exit()
        
@bot.command()
async def die(ctx):
    exit()
    

bot.run(str(token))
