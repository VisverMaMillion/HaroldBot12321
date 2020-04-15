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
queue = np.array([])
length = np.array([])
urlque = np.array([])

def queclr(y):
    global queue
    if y == 0:
        for song in os.listdir(songdir):
            filepath = os.path.join(songdir, song)
            os.unlink(filepath)
    elif y == 1:   
        filepath = os.path.join(songdir,queue[0] +'.mp3')
        queue = np.delete(queue,0)
        os.unlink(filepath)
        print(filepath)
        
        
    
 

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
    
    def urltoque(url):
        global urlque
        urlque = np.append(urlque,url)
        
    def urlfromque():
        global urlque
        queclr(1)
        try:
            se = urlque[0]
            return se
        except IndexError:
            return None


        
    def songdload(url):
        global queue
        global length
        global urlque
        songdowndir = os.path.join(workdir,'songs/%(title)s.%(ext)s')
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
            lengthval = info_dict.get('duration', None)
            if title.count(':') >= 1:
                title = title.replace(':', ' -')
        ntitle = np.array([title])
        queue = np.append(queue,ntitle)
        length = np.append(length,lengthval)
        try:
            urlque = np.delete(urlque,0)
            print(urlque)
        except IndexError:
            pass

        
        
    def checkque(url):
        global urlque
        global queue
        if url == None:
            return
        else:
            if voice.is_playing() == False:
                songdload(url)
                songpath = os.path.join(workdir, f'songs/{queue[0]}.mp3')
                voice.play(discord.FFmpegPCMAudio(songpath), after=lambda e: checkque(urlfromque()))
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.value = 0.07
            
            else:
                urltoque(url)        

        
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print('Need backup in %s' %(channel))
        await ctx.send(f'Need backup in %s!' %(channel))
    
    

    
#    song_there = os.path.isfile("song.mp3")
#    try:
#        if song_there:
#            os.remove("song.mp3")
#            print('Removed old song')
#    except PermissionError:
#        print('Trying to delete song but it is being played')
#        await ctx.send('Cannot remove song that is being played')
#        return
    checkque(url)
    
#    await ctx.send("Trying to play your song")
    
    
    print('Playing your song', urlque)
        
        
        
        
        
        
        
        
        



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
        urlque = np.array([])
        voice.stop()
        time.sleep(2)
        queclr(songdir, 0)
        await ctx.send('Halted thine noises, sire!')
    else:
        await ctx.send('But sir please!')
        queclr(songdir, 0)
    return

    
@bot.command()
async def delsong(ctx):
    queclr(0)
    
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

deathlist = ["death1", "death2", "death3", "headshot", "olkapaa", "aisaatana"]

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
