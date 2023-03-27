# #####################Imports#################################################
import discord, os, time, youtube_dl, re
from discord.ext import commands, tasks
from discord.utils import get
from itertools import cycle
import numpy as np
# numpy.random 
import urllib.parse ,urllib.request
from requests import get as rget
# ######################Globalvariables########################################
token = np.loadtxt('C:/bottoken/haroldtoken.txt', dtype=str)
workdir = os.path.dirname(__file__)
songdir = os.path.join(workdir, 'songs')
exitlist = ["AAAARGH!", "Said no and left.", "Harold fell off the map.", "Harold fucking died.",
            "Harold abandoned the match and received a 7 day competitive matchmaking cooldown."]
deathlist = ["death1", "death2", "death3", "headshot", "olkapaa", "aisaatana"]
status = cycle(["Hiding on de_dust2", ".help for help","何？"])

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())
# #############################################################################
# Dictionary to hold bot instances with server id as key
instances = {}

#Main class
#maybe all cogs go inside  this
#also cogs have changed in discord py rewrite
#now requires async
# https://discordpy.readthedocs.io/en/stable/migrating.html
class MainClient(commands.Bot):
    def __init__(self) -> None:
        #make help_command=??
        super().__init__(command_prefix='.', help_command=help_command, intents=discord.Intents.all())

        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        for filename in os.listdir(os.path.join(workdir, 'cogs')):  # Lataa laajennukset automaattisesti
            if filename.endswith('.py'):
                self.load_extension(f'cogs.{filename[:-3]}')
        await self.tree.sync()





#Discord Server instance 
class ServerInstance:
    def __init__(self, *kwargs):
        self.attribute = kwargs
        
        self.player = self.bot.get_cog('Player')


#Player class handles music playing
#One player per server
#Shhould also be accessable outside of the class
class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._que = np.array([])
        self.loop = False
        self._playing = False
        self.song = ""
        self.ydl_opts = {'format': 'bestaudio', 'noplaylist': True, 'quiet': True}


    #get the playing state of player
    @property
    def playing(self):
        return self._playing

    #set the playing state of player
    #maybe should be a switch
    @playing.setter
    def playing(self, state: bool):
        self._playing = state

    #get current queue of songs
    @property
    def que(self):
        return self._que


    @property
    def playlists(self):
        return self.ydl_opts['noplaylist']

    
    def toggleplaylists(self):
        self.ydl_opts['noplaylist'] = not self.ydl_opts['noplaylist']  
        return f"No playlists option set to {self.ydl_opts['noplaylist']}"

    
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


# ##################### Block for cogs ############################
#does the looping of status
@tasks.loop(seconds=10) 
async def change_status():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(next(status)))

@bot.event
async def on_ready():  # works
    change_status.start()
    bot.remove_command('help')  # älä koske! Koskin >:)
    for filename in os.listdir(os.path.join(workdir, 'cogs')):  # Lataa laajennukset automaattisesti
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
    print('Need backup!')

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
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send("Cog unloaded.")

# ###################################################################


class UtilityCommands:
    def __init__(self, bot) -> None:
        self.bot = bot

    
#kill switch
@bot.command() 
@commands.has_role('Harold Wrangler')
async def die(ctx):
    #try to make the shutdown graceful
    for x in bot.voice_clients:
        await x.disconnect()
    #await ctx.bot.logout()
    exit() # this aint it

bot.run(str(token))
