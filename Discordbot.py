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
bot = commands.Bot(command_prefix='.')
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


##############################################################################
# to do
# queue toistaa itseään

bot.remove_command('help')  # älä koske


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


#    else:
#        ans = title[0]
#       return ans


@bot.event
async def on_ready():  # works
    change_status.start()
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
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send("Cog unloaded.")


for filename in os.listdir('./cogs'):   # Lataa laajennukset automaattisesti
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


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
async def play(ctx, url: str):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    def urltoque(url):  # works
        global urlque
        urlque = np.append(urlque, url)

    def firsturl():
        global urlque
        se = urlque[0]
        return se

    def urlfromque():  # works deletes too early
        global urlque
        queclr(1, 1)
        try:
            se = urlque[0]
            print(urlque)
            return se
        except IndexError:
            print('pandas')
            return None

    def songdload(url):  # works , lisää search, mieti saako queen nimet
        global urlque
        global kello
        global ydl_opts
        global queue
        global length
        try:

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                print('Downloading song\n')
                ydl.cache.remove()
                ydl.download([url])
                ntitle = get_title(url)
                queue = np.append(queue, ntitle)
                #                length = np.append(length,lengthval)
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

    def checkque(url):  # it just works
        global urlque
        global queue
        if url == None:
            return
        else:
            if not voice.is_playing():
                songdload(url)
                songpath = os.path.join(workdir, f'songs/{queue[0]}.mp3')
                voice.play(discord.FFmpegPCMAudio(songpath), after=lambda e: checkque(urlfromque()))
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.value = 0.07
            else:
                pass

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        await ctx.send(f'Need backup in %s!' % channel)

    if not voice.is_playing() and urlque.size != 0:
        checkque(firsturl())

    else:
        urltoque(url)
        checkque(url)


@bot.command()
async def playdisk(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    voice = await channel.connect()
    song = 'song'
    songpath = os.path.join(workdir, f'mysongs/{song}.mp3')
    voice.play(discord.FFmpegPCMAudio(songpath))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.value = 0.07


@bot.command(pass_context=True, aliases=['s'])
async def search(ctx, *, search):
    #    async def on_message(message):
    #        message = int(message)
    #        tulos = 'https://www.youtube.com/watch?v=' +search_result[message]
    #        return tulos
    global result

    query_string = urllib.parse.urlencode({'search_query': search})
    htm_content = urllib.request.urlopen(
        'https://www.youtube.com/results?' + query_string)
    search_result = re.findall('href=\"\\/watch\\?v=(.{11})', htm_content.read().decode())
    for i in range(1, 6):
        del search_result[i]

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
    await play(ctx, wanted)


#  await play(ctx, tulos)

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


@bot.command(pass_context=True, aliases=['savepl', 'spl'])  # works
async def saveplaylist(ctx, nimi: str):
    np.save(playlistdir + f'/{nimi}.npy', urlque)


@bot.command(pass_context=True, aliases=['pl', 'loadpl'])  # works
async def loadplaylist(ctx, nimi: str):
    global urlque
    #    voice = get(bot.voice_clients, guild=ctx.guild)
    playlist = np.load(playlistdir + f'/{nimi}.npy')
    urlque = np.append(urlque, playlist)
    print(urlque)
    #    if voice and voice.is_playing(): # ei veden pitävä
    #        pass
    #    else:
    await play(ctx, urlque[0])


@bot.command(pass_context=True, aliases=['atpl'])
async def addtoplaylist(ctx, nimi: str, url):
    playlist = np.load(playlistdir + f'/{nimi}.npy')
    playlist = np.append(playlist, url)
    np.save(playlistdir + f'/{nimi}.npy', playlist)


@bot.command(pass_context=True, aliases=['rmfpl'])  # ei toimi virhe luvussa ?
async def removefromplaylist(ctx, nimi: str, luku: int):
    playlist = np.load(playlistdir + f'/{nimi}.npy')
    if luku > playlist.size:
        await ctx.send('Sire, thou known\'t')
    else:
        playlist = np.delete(playlist, int(luku) - 1)
        np.save(playlistdir + f'/{nimi}.npy', playlist)
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


@bot.command()  # works
@commands.has_role('Harold Wrangler')
async def die(ctx):
    exit()


bot.run(str(token))
