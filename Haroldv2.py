# #####################Imports#################################################
import discord, os, time
from discord.ext import commands, tasks
from discord import utils
from itertools import cycle
import numpy as np
import random as rd
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

class BotInstance:
    def __init__(*kwargs):
        pass
# teen näitä töiksi kohta btw



bot.run(str(token))
