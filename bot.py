import pathlib
import random

import aiosqlite
import discord
from discord.ext import commands

path = pathlib.PurePath()


async def prefixgetter(_, message):
    default_prefix = "%"
    try:
        sid = message.guild.id
    except AttributeError:
        return default_prefix
    db = await aiosqlite.connect(path / 'system/data.db')
    await db.execute('''CREATE TABLE IF NOT EXISTS prefixes
                   (serverid INTEGER, prefix TEXT)''')
    cur = await db.execute(f'''SELECT prefix FROM prefixes WHERE serverid = {sid}''')
    custom_prefix = await cur.fetchone()
    await db.close()
    if custom_prefix:
        return str(custom_prefix[0])
    else:
        return default_prefix


class Help(commands.MinimalHelpCommand):
    def get_command_signature(self, command):
        return '%s%s %s' % (self.clean_prefix, command.qualified_name, command.signature)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help")
        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            command_signatures = [self.get_command_signature(c) for c in filtered]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "System")
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)
        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_error_message(self, error):
        embed = discord.Embed(title="Error", value=error)
        channel = self.get_destination()
        await channel.send(embed=embed)


with open(path / 'system/token.txt', 'r') as file:
    TOKEN = file.read()
intents = discord.Intents().all()
sylveon = commands.Bot(command_prefix=prefixgetter, case_insensitive=True, intents=intents)
crystalball = ["Yes", "No", "Perhaps", "Maybe", "It Is Certain", "Impossible"]
embedcolor = 0xFD6A02

sylveon.help_command = Help()


@sylveon.event
async def on_ready():
    print(f'Logged on as {sylveon.user.name}, prefix: prefixgetter(sylveon, guild)')
    await sylveon.change_presence(
        activity=discord.Game(
            name=f"The Fun Eeveeloutions bot!"))


@sylveon.event
async def on_message(message):
    bot_mention_str = sylveon.user.mention.replace('@', '@!') + ' '
    bot_mention_len = len(bot_mention_str)
    if message.content[:bot_mention_len] == bot_mention_str:
        message.content = await prefixgetter(sylveon, message) + message.content[bot_mention_len:]
        await sylveon.process_commands(message)
    else:
        await sylveon.process_commands(message)


@sylveon.command()
async def hello(ctx):
    await ctx.message.delete()
    await ctx.channel.send('https://tenor.com/view/hello-there-hi-there-greetings-gif-9442662')


@sylveon.command()
async def count(ctx):
    await ctx.channel.send(f"This server has {ctx.guild.member_count} members.")


@sylveon.command()
async def test(ctx):
    embed = discord.Embed(colour=embedcolor)
    embed.add_field(name="TEST", value="Test received!")
    embed.set_footer(text=f"Request by {ctx.author}")
    await ctx.send(embed=embed)


@sylveon.command()
async def ball(ctx):
    await ctx.message.delete()
    send8ball = random.choice(crystalball)
    embed = discord.Embed(colour=embedcolor)
    embed.add_field(name="Result", value=f"{send8ball}")
    embed.set_footer(text=f"Request by {ctx.author}")
    await ctx.send(embed=embed)


@sylveon.command()
async def bruh(ctx):
    await ctx.message.delete()
    await ctx.channel.send("That is quite bruh.")


@sylveon.command()
async def ping(ctx):
    await ctx.message.delete()
    embed = discord.Embed(colour=embedcolor)
    embed.add_field(name="Ping", value=f'🏓 Pong! {round(sylveon.latency * 1000)}ms')
    embed.set_footer(text=f"Request by {ctx.author}")
    await ctx.send(embed=embed)


@sylveon.command()
async def hug(ctx, *, member: discord.Member):
    if member is not None:
        mention = member.mention
    else:
        mention = ":o"
    await ctx.send(f"{mention}, {ctx.author.mention} gave you a hug, aww!")
    await ctx.send("https://media.tenor.com/images/50c2f13c590fdb27c087d6a6736218e0/tenor.gif")


@sylveon.command()
async def huggle(ctx, member: discord.Member = None):
    if member is not None:
        await ctx.send(f"{member.mention}, {ctx.author.mention} gave you a huggle, aww!")
    await ctx.send("https://media.tenor.com/images/16491d8d332f0e231bb084474e66199c/tenor.gif")


@sylveon.command()
async def cuddle(ctx, member: discord.Member = None):
    if member is not None:
        await ctx.send(f"{member.mention}, {ctx.author.mention} gave you a cuddle, aww!")
    await ctx.send("https://media.tenor.com/images/9a8b0edf260a4831271c4a83573a1e12/tenor.gif")


sylveon.run(TOKEN)
