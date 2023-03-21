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
from requests import get as rget

# ######################Globalvariables########################################
token = np.loadtxt('C:/bottoken/haroldtoken.txt', dtype=str)
workdir = os.path.dirname(__file__)
songdir = os.path.join(workdir, 'songs')
playlistdir = os.path.join(workdir, 'playlists')
songdowndir = os.path.join(workdir, 'songs/%(title)s.%(ext)s')
status = cycle(["Hiding on de_dust2", ".help for help","何？"])
queue = np.array([])
length = np.array([])
urlque = np.array([])
result = np.array([])
kello = 0
ydl_opts = {'format': 'bestaudio', 'noplaylist': True, 'quiet': True}

#{
#    'format': 'bestaudio/best',
#    'postprocessors': [{
#        'key': 'FFmpegExtractAudio',
#        'preferredcodec': 'mp3',
#        'preferredquality': '192',
#    }],
#    'outtmpl': songdowndir
#
#
players = {}


bot = commands.Bot(command_prefix='.',intents=discord.Intents.all())


##############################################################################
# to do
# queue toistaa itseään


def getplayer(ctx):
    return players[f'{ctx.guild}']



class Player:
    def __init__(self, ctx):
        self._que = np.array([])
        self.loop = False
        self._playing = False
        self.song = ""
        self.ydl_opts = {'format': 'bestaudio', 'noplaylist': True, 'quiet': True}

    @property
    def playing(self):
        return self._playing

    @playing.setter
    def playing(self, state: bool):
        self._playing = state

    @property
    def que(self):
        return self._que

    @property
    def playlists(self):
        return self.ydl_opts['noplaylist']

    def songsearch(self, arg):
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            try:
                rget(arg)
            except:
                info = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
            else:
                info = ydl.extract_info(arg, download=False)

            if 'entries' in info:
                list = np.asarray([x['webpage_url'] for x in info['entries']])
                self.l2que(list)
                self._que = np.delete(self._que, 0)
                return self.songsearch(self._que[0])

        return info['formats'][0]['url'], info['title']

    def togglepl(self):
        self.ydl_opts['noplaylist'] = not self.ydl_opts['noplaylist']

    def shuffle(self):
        np.random.shuffle(self._que)

    def l2que(self, sangs):
        self._que = np.append(self._que, sangs)
    # make setter for que?

    def rfq(self, index):
        self._que = np.delete(self._que, index)

    def add2que(self, url):
        url = " ".join(url)
        self._que = np.append(self._que, url)

    def _continue_playing(self):
        pass

    def _after_song(self, ctx):
        if not self.loop:
            self._que = np.delete(self._que, 0)
            if len(self._que) != 0:
                self.play(ctx)
            else:
                self.playing = False
                self.song = "No song playing! L"
        else:
            self.play(ctx)

    def play(self, ctx):

        FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        voice = get(bot.voice_clients, guild=ctx.guild)

        try:
            source,self.song = self.songsearch(self._que[0])
            voice.play(discord.FFmpegPCMAudio(source, **FFMPEG_OPTS), after=lambda e: self._after_song(ctx))
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.value = 0.05
        except (IndexError, youtube_dl.DownloadError):
            self._after_song(ctx)


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
            #filepath = os.path.join(songdir, queue[0] + '.mp3')
            #queue = np.delete(queue, 0)
            urlque = np.delete(urlque, 0)
            #os.unlink(filepath)
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


@bot.event
async def on_ready():  # works
    change_status.start()
    bot.remove_command('help')  # älä koske! Koskin >:)
    for filename in os.listdir(os.path.join(workdir, 'cogs')):  # Lataa laajennukset automaattisesti
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
    print('Need backup!')


@tasks.loop(seconds=10)  # Looppaa statusta
async def change_status():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(next(status)))


@bot.command()
@commands.has_role('Harold Wrangler')  # Tarvitset tämän roolin käyttääksesi tiettyjä komentoja
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
    if amount > 20:
        await ctx.send("Max to delete at time 20")
        pass
    else:
        await ctx.channel.purge(limit=amount+1)

#ei toimi
@bot.command(aliases=['mtn'])
async def movetonext(ctx):
    player = getplayer(ctx)
    last = urlque[:-1]
    np.insert(urlque, 1, last)
    np.delete(urlque, len(urlque) - 1)


@bot.command()
@commands.has_role('Harold Wrangler')
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send("Cog unloaded.")


@bot.command(pass_context=True)  # works
async def backup(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    #check if already on dictionary and if not add it
    if f'{ctx.guild}' in players:
        pass
    else:
        players.update({f'{ctx.guild}': Player(ctx)})

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        await channel.connect()
        print('Need backup in %s' % channel)
        await ctx.send(f'Need backup in %s!' % channel)


@bot.command(pass_context=True, aliases=['p'])
async def play(ctx, *url):
    #lazy way to ensure the bot has player object
    await backup(ctx)
    time.sleep(1)

    player = getplayer(ctx)

    player.add2que(url)
    if not player.playing:
        player.playing = True
        player.play(ctx)




@bot.command()
async def loop(ctx):
    player = getplayer(ctx)
    player.loop = not player.loop

@bot.command()
async def shuffle(ctx):
    try:
        player = getplayer(ctx)
    except KeyError:
        await ctx.send("Harold ei ole edes paikalla vitun pälli?")
        return
    player.shuffle()
    await ctx.send("Sekoitettu kieh köh röh")


@bot.command(aliases=['np'])
async def nowplaying(ctx):
    player = getplayer(ctx)
    await ctx.send(player.song)


@bot.command(aliases=['que'])  # fixdis, maybe embed
async def showqueue(ctx):
    try:
        player = getplayer(ctx)
    except KeyError:
        await ctx.send("Nothing playing")
    pque = player.que
    await ctx.send(pque)


@bot.command()
async def playdisk(ctx, name):
    await backup(ctx)
    voice = get(bot.voice_clients, guild=ctx.guild)
    song = str(name)
    songpath = os.path.join(workdir, f'mysongs/{song}.mp3')
    voice.play(discord.FFmpegPCMAudio(songpath))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.value = 0.05


#meme sound file commands
@bot.command()
async def jonin(ctx):
    while True:
        await playdisk(ctx, "Dream_Mask")


@bot.command()
async def sus(ctx):
    await playdisk(ctx, "SUS")

@bot.command()
async def aha(ctx):
    await backup(ctx)
    voice = get(bot.voice_clients, guild=ctx.guild)
    songpath = os.path.join(workdir, f'mysongs/AHA.mp3')
    voice.play(discord.FFmpegPCMAudio(songpath))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.value = 0.5


@bot.command(pass_context=True, aliases=['s'])
async def search(ctx, *search):
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
    await play(ctx, wanted)


#skip doesn't work
@bot.command(pass_context=True, aliases=['sk', 'next'])  # works , add message
async def skip(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected() and voice.is_playing():
        voice.stop()
        await ctx.send("Starting next song, sire")
    else:
        await ctx.send("Nothing to skip")



@bot.command(pass_context=True, aliases=['rmfq'])  # doesn't works
async def removefromque(ctx, x):
    if x < 1:
        await ctx.send("What the hell?")
    try:
        player = getplayer(ctx)
    except KeyError:
        await ctx.send("I'm holding here, sire!")
    r = player.rfq(x)
    await ctx.send(f'Removed from que')



@bot.command()
async def savedplaylists(ctx):
    for filename in os.listdir(playlistdir):
        await ctx.send(f'{filename[:-4]}')


@bot.command()
async def songs(ctx, plis: str):
    playlist = np.loadtxt(playlistdir + f'/{plis}.dat', dtype=str)
    saad = []
    for s in playlist:
        saad.append(s.replace('_', ' ')[1:-1])
    await ctx.send(saad)


@bot.command(pass_context=True, aliases=['savepl', 'spl'])  # works
async def saveque(ctx, nimi: str):
    np.savetxt(playlistdir + f'/{nimi}.dat', urlque, fmt='%s')


@bot.command(pass_context=True, aliases=['pl', 'loadpl'])  # works
async def loadplaylist(ctx, nimi: str):
    #    voice = get(bot.voice_clients, guild=ctx.guild)
    await backup(ctx)
    player = getplayer(ctx)
    playlist = np.loadtxt(playlistdir + f'/{nimi}.dat', dtype=str, usecols=0)
    player.l2que(playlist)
    if not player.playing:
        player.playing = True
        player.play(ctx)


@bot.command(pass_context=True, aliases=['atpl'])
async def addtoplaylist(ctx, nimi: str, url):
    playlist = np.loadtxt(playlistdir + f'/{nimi}.dat', dtype=str)
    playlist = np.append(playlist, url)
    print(playlist)
    # np.savetxt(playlistdir + f'/{nimi}.dat', playlist)


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
        voice.pause()
        await ctx.send('Halted thine noises, sire!')
    else:
        await ctx.send('Negative! No music playing, sir!')


@bot.command()  # sauce just doesn't work :(
async def sauce(ctx):
    def roll(x):
        asdf = round(x * rd.random())
        return asdf

    dum = str(roll(3)) + str(roll(10)) + str(roll(10)) + str(roll(10)) + str(roll(10)) + str(roll(10))
    await ctx.send(dum)


@bot.command(aliases=['ping'])  # works
async def lag(ctx):
    await ctx.send(f'{round(bot.latency * 100)} ms ')


@bot.command(pass_context=True, aliases=['r', 'res'])  # works
async def resume(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        voice.resume()
        await ctx.send('Resumed your music, sir!')
    else:
        await ctx.send('But sir please!')


@bot.command(pass_context=True)  # no work
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        del players[f'{ctx.guild}']
        await ctx.send('Halted thine noises, sire!')
        await voice.disconnect()
    else:
        await ctx.send('But sir please!')
        await voice.disconnect()


exitlist = ["AAAARGH!", "Said no and left.", "Harold fell off the map.", "Harold fucking died.",
            "Harold abandoned the match and received a 7 day competitive matchmaking cooldown.", "Uwu"]

deathlist = ["death1", "death2", "death3", "headshot", "olkapaa", "aisaatana"]


# Disconnects bot from server
@bot.command(aliases=['KYs', 'KYS', 'Kys', 'KyS', "kYS"])  # works mutta optimoi
@commands.has_role('Harold Wrangler')
async def kys(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    players.pop(f"{ctx.guild}")
    # stop playing music for death sound
    if voice.is_playing():
        voice.stop()
    # if on voice channel plays sound before diconnecting
    if voice.is_connected():
        deathdir = os.path.join(workdir, f'sfx/deathsounds/{rd.choice(deathlist)}.mp3')
        voice.play(discord.FFmpegPCMAudio(deathdir))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.value = 0.4
        time.sleep(2)
        await voice.disconnect()
        await ctx.send(rd.choice(exitlist))

    else:
        await ctx.send('But sir please!')
    # removes player object from list



# Toggles playlist, on default they are off
@bot.command(aliases=['tpl'])
async def playlists(ctx):
    try:
        player = getplayer(ctx)
    except KeyError:
        await ctx.send("I'm not even there xd")
        return
    player.togglepl()
    await ctx.send(f'Allowing playlists: {player.playlists} ')
    

@bot.command()
async def hapi(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.send('<:widepeepohappy:656504711880638464>')


@bot.command()
@commands.has_permissions(administrator=True)
async def goodbot(ctx):
    await ctx.send(file=discord.File(workdir + '/sfx/pat.jpg'))


@bot.command()  # works
@commands.has_role('Harold Wrangler')
async def die(ctx):
    for x in bot.voice_clients:
        await x.disconnect()
    #await ctx.bot.logout()
    exit()

#Token
bot.run(token)
