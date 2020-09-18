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
status = cycle(["Hiding on de_dust2", ".help for help"])

bot = commands.Bot(command_prefix='.')
# #############################################################################


@bot.event
async def on_ready():  # works
    change_status.start()
    bot.remove_command('help')  # älä koske! Koskin >:)
#    for filename in os.listdir(workdir + '/Operation2'):  # Lataa laajennukset automaattisesti
#        if filename.endswith('.py'):
#            bot.load_extension(f'cogs.{filename[:-3]}')
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
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send("Cog unloaded.")


@bot.command(aliases=['ping'])  # works
async def lag(ctx):
    await ctx.send(f'{round(bot.latency * 100)} ms ')


@bot.command()  # works
@commands.has_role('Harold Wrangler')
async def die(ctx):
    for song in os.listdir(songdir):
        filepath = os.path.join(songdir, song)
        os.unlink(filepath)
    await bot.close()

bot.run(str(token))
