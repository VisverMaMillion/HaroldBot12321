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

#Bot instance 
class BotInstance:
    def __init__(self, *kwargs):
        self.attribute = kwargs
        self.ydl_opts = {'format': 'bestaudio', 'noplaylist': True, 'quiet': True}
        self.test = True

class Player:
    def __init__(self):
        pass

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


    

    


#bot.run(str(token))
