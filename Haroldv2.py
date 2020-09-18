# #####################Imports#################################################
from discord.ext import commands, tasks
from discord import utils
from itertools import cycle
import numpy as np
import os
import time
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


@bot.command(pass_context=True)  # works
async def backup(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        await channel.connect()
        print('Need backup in %s' % channel)
        await ctx.send(f'Need backup in %s!' % channel)


@bot.command(aliases=['ping'])  # works
async def lag(ctx):
    await ctx.send(f'{round(bot.latency * 100)} ms ')


@bot.command(aliases=['KYs', 'KYS', 'Kys', 'KyS', "kYS"])  # works mutta optimoi
@commands.has_role('Harold Wrangler')
async def kys(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    try:
        # ##urlque = np.array([])
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
       # await delsong()
        exit()
    else:
        await ctx.send(rd.choice(exitlist))
        exit()


@bot.command()  # works
@commands.has_role('Harold Wrangler')
async def die():
    await bot.close()
    await exit()


bot.run(str(token))
