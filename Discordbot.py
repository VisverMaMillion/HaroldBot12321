# #####################Imports#################################################
import discord
from discord.ext import commands, tasks
from discord.utils import get
from itertools import cycle
import youtube_dl
import random as rd
import numpy as np
import os
import time
import urllib.parse
import urllib.request
import re

# ######################Globalvariables########################################
token = np.loadtxt('C:/bottoken/haroldtoken.txt', dtype=str)
workdir = os.path.dirname(__file__)
songdir = os.path.join(workdir, 'songs')
playlistdir = os.path.join(workdir, 'playlists')
songdowndir = os.path.join(workdir, 'songs/%(title)s.%(ext)s')
status = cycle(["Hiding on de_dust2", ".help for help"])
queue = np.array([])
length = np.array([])
urlque = np.array([])
result = np.array([])
kello = 0
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': songdowndir

}

bot = commands.Bot(command_prefix='.')
##############################################################################
# to do
# queue toistaa itseään



def queclr(y, x):  # works
    global queue
    global urlque
    if y == 0:
        try:
            for song in os.listdir(songdir):
                filepath = os.path.join(songdir, song)
                os.unlink(filepath)
        except:
            pass
    elif y == 1:
        try:  # tuhoutuu joskus
            filepath = os.path.join(songdir, queue[0] + '.mp3')
            queue = np.delete(queue, 0)
            urlque = np.delete(urlque, 0)
            os.unlink(filepath)
        except IndexError:
            print('sire, thou art gay')
            pass

    elif y == 2:
        try:
            urlque = np.delete(urlque, x)
        except IndexError:
            print('enemy sighted')
            pass


def get_title(url):
    global ydl_opts
    global length

    #   if title.size == 0:
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        title = info_dict.get('title', None)
    #        lengthval = info_dict.get('duration', None) #turha?
    if title.count(':') >= 1:
        title = title.replace(':', ' -')
    if title.count('|') >= 1:
        title = title.replace('|', '_')
    if title.count('/') >= 1:
        title = title.replace('/', '_')
    if title.count('"') >= 1:
        title = title.replace('"', '\'')

    return title

def firsturl():
    se = urlque[0]
    return se

def urlfromque():  # works deletes too early
    queclr(1, 1)
    try:
        se = urlque[0]
        return se
    except IndexError:
        return None

def songdload(url):  # works , lisää search, mieti saako queen nimet
    global queue
    try:     
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print('Downloading song\n')
            ydl.cache.remove()
            ydl.download([url])
            ntitle = get_title(url)
            queue = np.append(queue, ntitle)
            kello = 0

    except:
        if kello <= 3:
            print('REEE')
            kello += 1
            songdload(url)
        else:
            kello = 0
            return
    return





@bot.event
async def on_ready():  # works
    change_status.start()
    bot.remove_command('help')  # älä koske! Koskin >:)
    for filename in os.listdir(workdir +'\cogs'):   # Lataa laajennukset automaattisesti
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
    print('Need backup!')


@tasks.loop(seconds=10)     # Looppaa statusta
async def change_status():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(next(status)))


@bot.command()
@commands.has_role('Harold Wrangler')   # Tarvitset tämän roolin käyttääksesi tiettyjä komentoja
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.send("Cog reloaded.")


@bot.command()
@commands.has_role('Harold Wrangler')
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.send("Cog loaded.")

@bot.command()
@commands.has_role('Harold Wrangler')
async def clear(ctx, amount=2):
    if amount >= 20 :
        pass
    else:
        await ctx.channel.purge(limit=amount)
        
@bot.command(aliases = ['mtn'])
async def movetonext(ctx):
    last = urlque[:-1]
    np.insert(urlque, 1, last)
    np.delete(urlque,len(urlque)-1)
        


@bot.command()
@commands.has_role('Harold Wrangler')
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send("Cog unloaded.")



@bot.command(pass_context=True)  # works
async def backup(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print('Need backup in %s' % channel)
        await ctx.send(f'Need backup in %s!' % channel)


# @bot.command(pass_context=True, aliases=['enemysighted', 'es'])
# async def noob(ctx):
#    channel = ctx.message.author.voice.channel
#    voice = get(bot.voice_clients, guild=ctx.guild)
#    if voice and voice.is_connected():
#        await voice.disconnect()
#        print(f"Left {channel}")
#        await ctx.send(f"Left {channel}")
#    else:
#        return

@bot.command(pass_context=True, aliases=['p'])
async def play(ctx, * url):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    global urlque
#    
#        def checkque(url):  # it just works
#        global urlque
#        global queue
#        if url == None:
#            return
#        else:
#            if not voice.is_playing():
#                songdload(url)
#                if voice.is_connected():
#                   pass
#                else:
#                channel.connect()
#                songpath = os.path.join(workdir, f'songs/{queue[0]}.mp3')
#                voice.play(discord.FFmpegPCMAudio(songpath), after=lambda e: checkque(urlfromque()))
#                voice.source = discord.PCMVolumeTransformer(voice.source)
#                voice.source.value = 0.05
#            else:
#                pass
    def checkque(url):  # it just works , make test how to make it not disconnect while convert
        if url == None:
            return
        else:
            if not voice.is_playing():
                songdload(url)
                songpath = os.path.join(workdir, f'songs/{queue[0]}.mp3')
                voice.play(discord.FFmpegPCMAudio(songpath), after=lambda e: checkque(urlfromque()))
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.value = 0.05
            else:
                pass



    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        await ctx.send(f'Need backup in %s!' % channel)
        
    url = " ".join(url)
    if not url.startswith(('https://','www.youtube')):
        query_string = urllib.parse.urlencode({'search_query': url})
        htm_content = urllib.request.urlopen('https://www.youtube.com/results?' + query_string)
        song =re.findall('"\\/watch\\?v=(.{11})"', htm_content.read().decode())[:1]
        songlink = 'https://www.youtube.com/watch?v=' + song[0]
        await play(ctx,songlink)
    
    else:
        if not voice.is_playing() and urlque.size != 0:
            checkque(firsturl())
        
        else:
            urlque = np.append(urlque, url)
            checkque(url)

@bot.command()
async def shuffle(ctx):
    global urlque
    np.random.shuffle(urlque[1:])
    
@bot.command(aliases=['np'])
async def nowplaying(ctx):
    global queue
    global urlque
    embed = discord.Embed(title=queue[0], url=urlque[0])
    await ctx.send(embed=embed)

@bot.command(aliases=['que']) #fixdis
async def showqueue(ctx):
    global queue
    await ctx.send(queue[:5])


@bot.command()
async def playdisk(ctx, name):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    voice = await channel.connect()
    song = str(name)
    songpath = os.path.join(workdir, f'mysongs/{song}.mp3')
    voice.play(discord.FFmpegPCMAudio(songpath))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.value = 0.07


@bot.command(pass_context=True, aliases=['s'])
async def search(ctx, * search):
    global result

    query_string = urllib.parse.urlencode({'search_query': search})
    htm_content = urllib.request.urlopen(
        'https://www.youtube.com/results?' + query_string)
    search_result = re.findall('"\\/watch\\?v=(.{11})"',
                    htm_content.read().decode())[:5]
    result = np.array([])
    for i in range(0, 5):
        link = 'https://www.youtube.com/watch?v=' + search_result[i]
        gottitle = get_title(link)
        embed = discord.Embed(title=gottitle, url=link)
        await ctx.send(embed=embed)
        result = np.append(result, link)
        

@bot.command(pass_context=True, aliases=['c'])
async def choose(ctx, number):
    wanted = result[int(number) - 1]
    await play(ctx,wanted)

@bot.command(pass_context=True, aliases=['sk', 'next'])  # works , add message
async def skip(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.stop()
    else:
        pass


@bot.command(pass_context=True, aliases=['rmfq'])  # works
async def removefromque(ctx, x):
    queclr(2, int(x))
    
    
@bot.command()
async def playlists(ctx):
     for filename in os.listdir(playlistdir):
         await ctx.send(f'{filename[:-4]}')
         
         
@bot.command()
async def songs(ctx, plis:str):
    playlist = np.loadtxt(playlistdir + f'/{plis}.dat', dtype=str, usecols=1)
    saad = []
    for s in playlist:
        saad.append(s.replace('_',' '))
    await ctx.send(saad)
   

@bot.command(pass_context=True, aliases=['savepl', 'spl'])  # works
async def saveque(ctx, nimi:str):
    np.savetxt(playlistdir + f'/{nimi}.dat', urlque, fmt='%s')


@bot.command(pass_context=True, aliases=['pl', 'loadpl'])  # works
async def loadplaylist(ctx, nimi:str):
    global urlque
    #    voice = get(bot.voice_clients, guild=ctx.guild)
    playlist = np.loadtxt(playlistdir + f'/{nimi}.dat', dtype=str, usecols=0)
    urlque = np.append(urlque, playlist)
    print(urlque)
    #    if voice and voice.is_playing(): # ei veden pitävä
    #        pass
    #    else:
    await play(ctx, urlque[0])


@bot.command(pass_context=True, aliases=['atpl'])
async def addtoplaylist(ctx, nimi:str, url):
    playlist = np.loadtxt(playlistdir + f'/{nimi}.dat', dtype=str)
    playlist = np.append(playlist, url)
    print(playlist)
    #np.savetxt(playlistdir + f'/{nimi}.dat', playlist)


@bot.command(pass_context=True, aliases=['rmfpl'])  # ei toimi virhe luvussa ?
async def removefromplaylist(ctx, nimi: str, luku: int):
    playlist = np.loadtxt(playlistdir + f'/{nimi}.dat')
    if luku > playlist.size:
        await ctx.send('Sire, thou known\'t')
    else:
        playlist = np.delete(playlist, int(luku) - 1)
        np.savetxt(playlistdir + f'/{nimi}.dat', playlist)
        await ctx.send('Removed')  # lisää sanomaan poistetun kappaleen nimi?
    playlist = np.array([])


@bot.command(pass_context=True, aliases=['pau'])  # works
async def pause(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        print('Music paused')
        voice.pause()
        await ctx.send('Music paused, sir!')
    else:
        print('Music not playing')
        await ctx.send('Negative! No music playing, sir!')


@bot.command()      # sauce just doesn't work :(
async def sauce(ctx):
    def roll(x):
        asdf = round(x * rd.random())
        return asdf

    sauce = str(roll(3)) + str(roll(10)) + str(roll(10)) + str(roll(10)) + str(roll(10)) + str(roll(10))
    await ctx.send(sauce)


@bot.command(pass_context=True, aliases=['r', 'res'])  # works
async def resume(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print('Music resumed')
        voice.resume()
        await ctx.send('Resumed your music, sir!')
    else:
        await ctx.send('But sir please!')


@bot.command(pass_context=True)  # no work
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    global urlque

    if voice and voice.is_playing():
        print('Music stopped')
        urlque = np.array([])
        voice.stop()
        time.sleep(2)
        queclr(0, 1)
        await ctx.send('Halted thine noises, sire!')
        await voice.disconnect()
    else:
        queclr(0, 1)
        await ctx.send('But sir please!')
        await voice.disconnect()
    return


@bot.command()  # works
async def delsong():
    queclr(0, 1)


@bot.command()
async def flip(ctx):
    throw = rd.randint(0, 1)
    if throw == 0:
        await ctx.send('Heads!')
    else:
        await ctx.send('Tails!')


@bot.command(aliases=['ping'])  # works
async def lag(ctx):
    await ctx.send(f'{round(bot.latency * 100)} ms ')


@bot.command()  # works
async def BombisA(ctx):
    await ctx.send('Getting pounded over here!')


@bot.command(aliases=['drop', 'pls', 'droplz'])  # works
async def dropplz(ctx):
    await ctx.send('But sir please!')


exitlist = ["AAAARGH!", "Said no and left.", "Harold fell off the map.", "Harold fucking died.",
            "Harold abandoned the match and received a 7 day competitive matchmaking cooldown."]

deathlist = ["death1", "death2", "death3", "headshot", "olkapaa", "aisaatana"]


@bot.command(aliases=['KYs', 'KYS', 'Kys', 'KyS', "kYS"])  # works mutta optimoi
@commands.has_role('Harold Wrangler')
async def kys(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    global urlque
    try:
        urlque = np.array([])
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
        await delsong()
        exit()
    else:
        await ctx.send(rd.choice(exitlist))
        await delsong()
        exit()
        
@bot.command()
async def hapi(ctx):
    await ctx.send('<:widepeepohappy:656504711880638464>')


@bot.command()  # works
@commands.has_role('Harold Wrangler')
async def die(ctx):
    exit()


bot.run(str(token))
