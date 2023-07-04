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

#Main class
#maybe all cogs go inside  this
#also cogs have changed in discord py rewrite
#now requires async
# https://discordpy.readthedocs.io/en/stable/migrating.html

class MainClient(commands.Bot):
    def __init__(self) -> None:
        #make help_command=??
        # help_command=help_command, to below
        super().__init__(command_prefix='.',  intents=discord.Intents.all())

        #self.tree = discord.app_commands.CommandTree(self)
        # Dictionary to hold bot instances with server id as key
        self.instances = {}

    async def setup_hook(self) -> None:
        #for filename in os.listdir(os.path.join(workdir, 'cogs')):  # Lataa laajennukset automaattisesti
         #   if filename.endswith('.py'):
                #await self.load_extension(f'cogs.{filename[:-3]}')
        await self.load_extension("cogs.DND")

    @commands.command()
    async def create_instance(self, ctx):
        pass
        #self.instances.update({f'{ctx.guild}': Player(ctx)})
        

    async def play(self, ctx, *url):
        pass



#Discord Server instance 
#at this point not used but allows the project to expand in the future
class ServerInstance:
    def __init__(self, *kwargs):
        self.attribute = kwargs
        
        self.ydl_opts = {'format': 'bestaudio', 'noplaylist': True, 'quiet': True}
        self.player = Player()


#Player class handles music playing
#One player per server
#Shhould also be accessable outside of the class
class Player:
    """Player class.
    
    Most music player functions should be here, but have accessability
    for outside. One Player class should be assigned for one server. 
    When bot leaves the voice channel the player gets deleted, so if que 
    is to be saved for later usage it needs to be saved on server instance.
    
    Parameters
    ----------
    voice : discord.VoiceClient
        Discord voice client of the current server
    ydl_opts : dict
        Options for youtubeDL
    que : ndarray, optinal
        Queue can be set on init, default is empty
        

    Attributes
    ----------
    Add them here
    """
    def __init__(self, voice: discord.VoiceClient, ydl_opts: dict, que: np.ndarray=np.array([])):
        #holds the discord voice client
        self.voice = voice
        #if que set in init make the code play it
        self._que = que #make option to add into que pos n ?
        self.loop = False
        self._playing = False
        #a way to return current song now str -> embed?
        self.song = ""
        self.ydl_opts = ydl_opts
        self.FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        
    # If bugs make some way to prevent que access at the same time


    #get the playing state of player
    @property
    def playing(self) -> bool:
        return self._playing

    #set the playing state of player
    #maybe should be a switch
    #is setter really necessary? -> do automatically
    @playing.setter
    def playing(self, state: bool) -> None:
        self._playing = state

    #get current queue of songs
    @property
    def que(self) -> np.ndarray:
        """Returns current queue as ndarray"""
        return self._que
    
    #change ytdl opts to allow playing youtube playlists, dissallowed by default
    def allowplaylists(self) -> str:
        """
        Switches the boolean state of ytdl_opts['noplaylist'] to opposite

        Returns
        -------
        return: str
            Feedback of the setting change
        """
        self.ydl_opts['noplaylist'] = not self.ydl_opts['noplaylist']  
        return f"Noplaylists option set to {self.ydl_opts['noplaylist']}"

    def shuffle(self) -> None:
        """Shuffles the current que"""
        #now works only on current que, is it necesasry to suffle again after 
        # every song? Maybe new added songs should also be shuffled?
        np.random.shuffle(self._que)

    def add2que(self, arg:str) -> None:
        """If voice is occupied add the new query to que"""
        self._que = np.append(self._que, arg)

    def removefromque(self, index: int) -> None:
        """Removes the n+1 th elemnt from que"""
        #this should be checked to feel natural for non coders start sifted 0->1
        #also if changes in que remember to fix here
        self._que = np.delete(self._que, index)
    
    def songsearch(self, arg):
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            #just works
            try:
                rget(arg)
            except:
                info = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
            #url ?
            else:
                info = ydl.extract_info(arg, download=False)
            
            #probably for playlists, but done poorly -> fix it
            if 'entries' in info:
                list = np.asarray([x['webpage_url'] for x in info['entries']])
                #l2que will not be added -> add to que here
                self.l2que(list)
                #if que system change to del first after song played change here also
                self._que = np.delete(self._que, 0)
                return self.songsearch(self._que[0])

        #make the return be consistent? -> why url + title?
        return info['formats'][0]['url'], info['title']

    #is it stuck in play(aftersong(play(...)))
    #maybe test it lule
    def play(self) -> int:
        """Plays the songs.
        
        Takes first one of the que and plays it. After song is done 
        plays all songs from que.

        Returns
        -------
        int : 0 for success

        int : 1 for error
        """
        try:
            source, self.song = self.songsearch(self._que[0])
            self.voice.play(discord.FFmpegPCMAudio(source, **self.FFMPEG_OPTS), after=lambda e: self._aftersong())
            #wtf is this line black magic? look it up man -> it's 6:05 man
            self.voice.source = discord.PCMVolumeTransformer(self.voice.source)
            self.voice.source.value = 0.05
        except (IndexError, youtube_dl.DownloadError):
            self._aftersong()
            return 1
        return 0


# ##################### Block for cogs ############################
#does the looping of status
intents = discord.Intents.default()
#bot.run(str(token))
client = MainClient()

@tasks.loop(seconds=10) 
async def change_status():
    await client.change_presence(status=discord.Status.online, activity=discord.Game(next(status)))

#@client.event
#async def on_ready():  # works
#    change_status.start()
#    bot.remove_command('help')  # älä koske! Koskin >:)
#    for filename in os.listdir(os.path.join(workdir, 'cogs')):  # Lataa laajennukset automaattisesti
#        if filename.endswith('.py'):
#            bot.load_extension(f'cogs.{filename[:-3]}')
#    print('Need backup!')


@client.command()
@commands.has_role('Harold Wrangler')  # Tarvitset tämän roolin käyttääksesi tiettyjä komentoja
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.send("Cog reloaded.")

@client.command()
@commands.has_role('Harold Wrangler')
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.send("Cog loaded.")

@client.command()
@commands.has_role('Harold Wrangler')
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send("Cog unloaded.")

@client.hybrid_command(description="Kill the bot")
async def die(ctx):
    exit()

@client.command()
async def synch(ctx):
    await client.tree.sync(guild=discord.Object(id=602544427528880147))


# ###################################################################


class UtilityCommands:
    def __init__(self, bot) -> None:
        self.bot = bot

    
#kill switch
#@bot.command() 
#@commands.has_role('Harold Wrangler')
#async def die(ctx):
    #try to make the shutdown graceful
#    for x in bot.voice_clients:
#        await x.disconnect()
    #await ctx.bot.logout()
#    exit() # this aint it



client.run(str(token))