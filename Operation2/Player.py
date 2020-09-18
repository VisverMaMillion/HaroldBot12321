import discord, re, os, youtube_dl
from discord.ext import commands, tasks
from discord.utils import get
import urllib.parse
import urllib.request
import random as rd
import numpy as np
# ##################################################
workdir = os.path.dirname(__file__)
songdir = os.path.join(workdir, 'songs')
playlistdir = os.path.join(workdir, 'playlists')
songdowndir = os.path.join(workdir, 'songs/%(title)s.%(ext)s')
queue = np.array([])
length = np.array([])
urlque = np.array([])
result = np.array([])
kello = 0
bot = commands.Bot(command_prefix='.')
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': songdowndir
}


def queclr(y, x):  # works
    global queue
    global urlque
    if y == 0:
        try:
            for song in os.listdir(songdir):
                filepath = os.path.join(songdir, song)
                os.unlink(filepath)
        except error:
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
    global kello
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print('Downloading song\n')
            ydl.cache.remove()
            ydl.download([url])
            ntitle = get_title(url)
            queue = np.append(queue, ntitle)
            kello = 0

    except error:
        if kello <= 3:
            print('REEE')
            kello += 1
            songdload(url)
        else:
            kello = 0
            return
    return


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.player={
            "songfiles":[]
        }

    @commands.Cog.listener('on_voice_state_update')
    async def queclear(self,user,after):
        if after.channel is None and user.id == self.bot.user.id:
            try:
                # laita clearaamaan que per server ??
            except KeyError: # tarkistele tomiiko tämä
                pass

    async def ytplaylist(self,data,msg): #kemali bag löater
        for i in data['queue']:
            self.player[msg.guild.id]['queue'].append({'title':i, 'author':msg})



#@bot.command(aliases=['KYs', 'KYS', 'Kys', 'KyS', "kYS"])  # works mutta optimoi
#@commands.has_role('Harold Wrangler')
#async def kys(ctx):
#    voice = utils.get(bot.voice_clients, guild=ctx.guild)
#    try:
#        # ##urlque = np.array([])
#        voice.stop()
#    except AttributeError:
#        pass
#    if voice and voice.is_connected():
#        deathdir = os.path.join(workdir, f'sfx/deathsounds/{rd.choice(deathlist)}.mp3')
#        voice.play(discord.FFmpegPCMAudio(deathdir))
#        voice.source = discord.PCMVolumeTransformer(voice.source)
#        voice.source.value = 0.4
#        time.sleep(2)
#        await voice.disconnect()
#        await ctx.send(rd.choice(exitlist))
#       # await delsong()
#        exit()
#    else:
#        await ctx.send(rd.choice(exitlist))
#        exit()


#@bot.command(pass_context=True)  # works
#async def backup(ctx):
#    channel = ctx.message.author.voice.channel
#    voice = utils.get(bot.voice_clients, guild=ctx.guild)
#    if voice and voice.is_connected():
#        await voice.move_to(channel)
#    else:
#        await channel.connect()
#        print('Need backup in %s' % channel)
#        await ctx.send(f'Need backup in %s!' % channel)

