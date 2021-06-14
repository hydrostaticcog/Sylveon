#!/home/gxhut/Sylveon/venv/bin/python3
import pathlib
import random
import traceback

import aiosqlite
import discord
from discord.ext import commands

path = pathlib.PurePath()


async def prefixgetter(_, message):
    default_prefix = "&"
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
sylveon = commands.Bot(command_prefix=prefixgetter, case_insensitive=True, intents=intents,
                       activity=discord.Activity(activity=discord.Game(
                           name=f"with friends!")))
crystalball = ["Yes", "No", "Perhaps", "Maybe", "It Is Certain", "Impossible"]
embedcolor = 0xFD6A02

sylveon.help_command = Help()


@sylveon.event
async def on_ready():
    print(f'Logged on as {sylveon.user.name}, prefix: prefixgetter(sylveon, guild)')
    await sylveon.change_presence(
        activity=discord.Game(
            name=f"with friends!"))


@sylveon.event
async def on_message(message):
    bot_mention_str = sylveon.user.mention.replace('@', '@!') + ' '
    bot_mention_len = len(bot_mention_str)
    if message.content[:bot_mention_len] == bot_mention_str:
        message.content = await prefixgetter(sylveon, message) + message.content[bot_mention_len:]
        ctx = await sylveon.get_context(message)
        await sylveon.invoke(ctx)
    else:
        ctx = await sylveon.get_context(message)
        await sylveon.invoke(ctx)


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
@commands.has_permissions(administrator=True)  # requires that the person issuing the command has administrator perms
async def prefix(ctx, newprefix):  # context and what we should set the new prefix to
    """Sets the bot prefix for this server"""
    serverid = ctx.guild.id  # gets serverid for convinience
    db = await aiosqlite.connect(path / 'system/data.db')  # connect to our server data db
    dataline = await db.execute(
        f'''SELECT prefix FROM prefixes WHERE serverid = {serverid}''')  # get the current prefix for that server,
    # if it exists
    if await dataline.fetchone() is not None:  # actually check if it exists
        await db.execute("""UPDATE prefixes SET prefix = ? WHERE serverid = ?""",
                         (newprefix, serverid))  # update prefix
    else:
        await db.execute("INSERT INTO prefixes(serverid, prefix) VALUES (?,?)",
                         (serverid, newprefix))  # set new prefix
    await db.commit()  # say "yes i want to do this for sure"
    await db.close()  # close connection
    await ctx.send(f"Prefix set to {newprefix}")  # tell admin what happened


@sylveon.command()
async def hug(ctx, members: commands.Greedy[discord.Member] = None, *, reason="aww!"):
    sent = False
    mentions = []
    if members:
        for person in members:
            if person.id == 808149899182342145:
                await ctx.send("But that's Glaceon!")
                await ctx.send("https://tenor.com/view/anime-blush-girl-gif-19459906")
                sent = True
        for person in members:
            mentions.append(person.mention)
        mentions = " ".join(mentions)
    elif ctx.message.mention_everyone:
        mentions = "@everyone"
        reason = reason.replace("@everyone", "")
    else:
        mentions = " :D"
    if not sent:
        await ctx.send(f"{mentions}, {ctx.author.mention} gave you a hug, {reason}")
        hugs = ["https://media.tenor.com/images/50c2f13c590fdb27c087d6a6736218e0/tenor.gif",
                "https://media.discordapp.net/attachments/731763704005394523/829133807008743444/image0.gif",
                "https://media1.tenor.com/images/969f0f462e4b7350da543f0231ba94cb/tenor.gif",
                "https://media1.tenor.com/images/b7492c8996b25e613a2ab58a5d801924/tenor.gif?itemid=14227401",
                "https://media1.tenor.com/images/24ac13447f9409d41c1aecb923aedf81/tenor.gif?itemid=5026057",
                "https://media1.tenor.com/images/f720d87668fa1e65b3294eb30fc4ac36/tenor.gif?itemid=19092449"]
        await ctx.send(random.choice(hugs))


@sylveon.event
async def on_command_error(ctx, error):
    if hasattr(ctx.command, 'on_error'):
        # await ctx.message.add_reaction('<:CommandError:804193351758381086>')
        return

    elif isinstance(error, discord.ext.commands.errors.CommandNotFound) or ctx.command.hidden:
        return

    elif isinstance(error, discord.ext.commands.errors.NotOwner):
        await ctx.reply("lol only valk can do that")
        return

    elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.reply("You are not allowed to do that!")
        return

    elif isinstance(error, discord.ext.commands.errors.BotMissingPermissions):
        await ctx.reply("I do not have the requisite permissions to do that!")
        return

    elif isinstance(error, discord.ext.commands.errors.MissingRole):
        await ctx.send("I am missing the role to do that!")
        return

    elif isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
        if str(error.cooldown.type.name) != "default":
            cooldowntype = f'per {error.cooldown.type.name}'

        else:
            cooldowntype = 'global'
        await ctx.reply(
            f"This command is on a {round(error.cooldown.per, 0)} second {cooldowntype} cooldown.\n"
            f"Wait {round(error.retry_after, 1)} seconds, and try again.",
            delete_after=min(10, error.retry_after))
        return

    elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.reply(f"Missing required argument!\nUsage:`{ctx.command.signature}`", delete_after=30)
        return

    elif isinstance(error, discord.ext.commands.errors.BadArgument):
        await ctx.reply(f"Invalid argument!\nUsage:`{ctx.command.signature}`", delete_after=30)
        return

    elif isinstance(error, discord.ext.commands.errors.NoPrivateMessage):
        await ctx.reply("That can only be used in servers, not DMs!")
        return

    else:
        # Send user a message
        # get data from exception
        etype = type(error)
        trace = error.__traceback__

        # 'traceback' is the stdlib module, `import traceback`.
        lines = traceback.format_exception(etype, error, trace)

        # format_exception returns a list with line breaks embedded in the lines, so let's just stitch the elements together
        traceback_text = ''.join(lines)

        # now we can send it to the user
        bug_channel = sylveon.get_channel(845453425722261515)
        await bug_channel.send("```\n" + str(traceback_text) + "\n```\n Command being invoked: " + ctx.command.name)
        await ctx.send("Error!\n```" + str(
            error) + "```\nvalkyrie_pilot will be informed.  Most likely this is a bug, but check your syntax.",
                       delete_after=30)


sylveon.run(TOKEN)
