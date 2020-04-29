import discord
from discord.ext import commands
bot = commands.Bot(command_prefix='.')


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    bot.remove_command('help')  # älä koske

    @bot.command(pass_context=True, aliases=["apu"])
    async def help(self, ctx):
        msg = ctx.message.content
        prefix_used = ctx.prefix
        alias_used = ctx.invoked_with
        text = msg[len(prefix_used) + len(alias_used):]

        embed1 = discord.Embed()

        embed1.set_author(name="Help commands")
        embed1.add_field(name="help general", value="General commands.", inline=False)
        embed1.add_field(name="help music", value="Music commands.", inline=False)
        embed1.add_field(name="help memes", value="Garbage.", inline=False)
        embed1.add_field(name="help dev", value="*Plays Hacknet once.*", inline=False)

        embed2 = discord.Embed(
            colour=discord.Colour.teal(),
        )

        embed2.set_author(name="Music commands")
        embed2.add_field(name="play [p] (youtube link)", value="Play from link.", inline=False)
        embed2.add_field(name="search [s]", value="Search from youtube, then choose from list.", inline=False)
        embed2.add_field(name="choose [c] (number)", value="Choose from search list.", inline=False)
        embed2.add_field(name="pause, resume, skip", value="It do what it say yes", inline=False)
        embed2.add_field(name="stop", value="Stops song and deletes it from que.", inline=False)

        embed3 = discord.Embed(
            colour=discord.Colour.dark_green(),
        )

        embed3.set_author(name="Cringe ass memes")
        embed3.add_field(name="sauce", value="If you know, you know.", inline=False)
        embed3.add_field(name="BombisA", value="Demonstrates Harold's retake skills.", inline=False)
        embed3.add_field(name="dropplz", value="Cmon man you have 16k money ёбаный урод.", inline=False)

        embed4 = discord.Embed(
            colour=discord.Colour.light_grey(),
        )

        embed4.set_author(name="General commands")
        embed4.add_field(name="backup", value="Summons bot to voice channel.", inline=False)
        embed4.add_field(name="lag [ping]", value="Shows latency.", inline=False)
        embed4.add_field(name="flip", value="Flip a coin.", inline=False)

        embed5 = discord.Embed()

        embed5.set_author(name="Dev commands (you need a role for these)")
        embed5.add_field(name="reload (cogname)", value="Reloads cog.", inline=False)
        embed5.add_field(name="load (cogname)", value="Loads cog.", inline=False)
        embed5.add_field(name="unload (cogname)", value="Unloads cog.", inline=False)
        embed5.add_field(name="kys", value="Shuts down the bot.", inline=False)
        embed5.add_field(name="die", value="This kills the bot.", inline=False)

        if text == '':
            await ctx.send(embed=embed1)


        elif text == " music":
            await ctx.send(embed=embed2)

        elif text == " memes":
            await ctx.send(embed=embed3)


        elif text == " general":
            await ctx.send(embed=embed4)


        elif text == " dev":
            await ctx.send(embed=embed5)

        else:
            pass


def setup(bot):
    bot.add_cog(Help(bot))
