#!venv/bin/python3
import binascii
import pathlib
import random
import re
import traceback
import typing
import base64
from datetime import datetime, timezone

import aiosqlite
import discord
from discord.ext import commands

path = pathlib.PurePath()


async def deping(text) -> str:
    text.replace("@everyone", "@ everyone")
    text.replace("@here", " @ here")
    text = re.sub("<@(!?)([0-9]*)>", "dont ping people with this", text)
    return text


async def prefixgetter(_, message) -> str:
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


class Help(commands.HelpCommand):
    def get_command_signature(self, command):
        return '%s%s %s' % (self.clean_prefix, command.qualified_name, command.signature)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help")
        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            command_signatures = [self.get_command_signature(c) for c in filtered]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "Commands")
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

            channel = self.get_destination()
            await channel.send(embed=embed)


with open(path / 'system/token.txt', 'r') as file:
    TOKEN = file.read()
intents = discord.Intents().all()
sylveon = commands.Bot(command_prefix=prefixgetter, case_insensitive=True, intents=intents,
                       activity=discord.Activity(activity=discord.Game(
                           name=f"with friends!")), help_command=Help())
embedcolor = 0xFD6A02


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
    """o/"""
    await ctx.message.delete()
    await ctx.channel.send('https://tenor.com/view/hello-there-hi-there-greetings-gif-9442662')


@sylveon.command()
async def ping(ctx):
    """get bot ping"""
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


@sylveon.command(aliases=["b64", "base64", "encode", "encodenick"])
@commands.has_permissions(change_nickname=True)
async def base64_encode(ctx, *, string=None):
    if string is None:
        nickname = base64.b64encode(ctx.author.display_name.encode()).decode()
        if len(nickname) > 32:
            nickname = base64.b64encode(ctx.author.name.encode()).decode()
            if len(nickname) > 32:
                await ctx.reply(
                    "Whoops! base64 encoding of your nickname and name both failed! B64 encoding of your display "
                    "name: ` " + await deping(nickname) + "`")
                return
        try:
            await ctx.author.edit(nick=nickname)
        except discord.Forbidden:
            await ctx.reply(
                "Your nickname could not be changed, probably because you are above me in the role hierarchy or i don't have manage nicknames. "
                "Here is your encoded display name, so you can change it: `" + await deping(base64.b64encode(
                    ctx.author.display_name.encode()).decode()) + "`")
            return
        await ctx.reply("Base64 encoded nickname!")
    else:
        b64_encoded_string = base64.b64encode(string.encode()).decode()
        if len(b64_encoded_string) > 2000:
            await ctx.reply("That string is too long.")
            return
        await ctx.reply(await deping(b64_encoded_string))


@sylveon.command(aliases=["b64_decode", "decode"])
async def base64_decode(ctx, *, string=None):
    if string is None:
        string = ctx.author.display_name
    try:
        b64_encoded_string = base64.b64decode(string.encode()).decode()
    except binascii.Error:
        await ctx.send("Your name or input doesn't seem to be a base64 string!")
        return
    if len(b64_encoded_string) > 2000:
        await ctx.reply("That string is too long.")
        return
    await ctx.reply(deping(b64_encoded_string))


@sylveon.command(aliases=["isotoepoch", "iso2unix", "isotounix"])
async def iso2epoch(ctx):
    await ctx.reply("https://dencode.com/en/date/iso8601")


@sylveon.command()
async def hug(ctx, members: commands.Greedy[discord.Member] = None, *, reason="aww!"):
    """Gives someone- or a lot of someones- a hug :D"""
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
        reason = reason.replace("@everyone", "aww")
    else:
        mentions = " :D"
    if not sent:
        reason = reason.replace("@everyone", "aww")
        reason = reason.replace("@here", "aww")
        await ctx.send(f"{mentions}, {ctx.author.mention} gave you a hug, {reason}")
        hugs = ["https://media.tenor.com/images/50c2f13c590fdb27c087d6a6736218e0/tenor.gif",
                "https://media.discordapp.net/attachments/731763704005394523/829133807008743444/image0.gif",
                "https://media1.tenor.com/images/969f0f462e4b7350da543f0231ba94cb/tenor.gif",
                "https://media1.tenor.com/images/b7492c8996b25e613a2ab58a5d801924/tenor.gif?itemid=14227401",
                "https://media1.tenor.com/images/24ac13447f9409d41c1aecb923aedf81/tenor.gif?itemid=5026057",
                "https://media1.tenor.com/images/f720d87668fa1e65b3294eb30fc4ac36/tenor.gif?itemid=19092449"]
        await ctx.send(random.choice(hugs))


@sylveon.command()
async def snuggle(ctx, members: commands.Greedy[discord.Member] = None, *, reason="aww!"):
    """Snuggles someone or multiple people. When you want closeness but not romance"""
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
        reason = reason.replace("@everyone", "aww")
    else:
        mentions = " :D"
    if not sent:
        reason = reason.replace("@everyone", "aww")
        reason = reason.replace("@here", "aww")
        await ctx.send(f"{mentions}, {ctx.author.mention} wants to snuggle, {reason}")
        snuggles = ["https://tenor.com/view/rosy-cheeks-mochi-peach-mochi-cat-cute-kitty-peach-cat-gif-16992602",
                    "https://tenor.com/view/pats-cute-cats-love-gif-13979931",
                    "https://tenor.com/view/gif-fofinho-heart-love-cuddle-cute-gif-14676815"]
        await ctx.send(random.choice(snuggles))


@sylveon.command()
async def cuddle(ctx, members: commands.Greedy[discord.Member] = None, *, reason="❤️"):
    """when you want to cuddle with someone, because you love them"""
    mentions = []
    if members:
        for person in members:
            if person.id == 808149899182342145:
                await ctx.send("But that's Glaceon!")
                await ctx.send("https://tenor.com/view/anime-blush-girl-gif-19459906")
                return
        for person in members:
            mentions.append(person.mention)
        mentions = " ".join(mentions)
    elif ctx.message.mention_everyone:
        mentions = "@everyone"
        reason = reason.replace("@everyone", "❤️")
    else:
        mentions = " :D"
    reason = reason.replace("@everyone", "❤️")
    reason = reason.replace("@here", "❤️")
    await ctx.send(f"{mentions}, {ctx.author.mention} cuddles you, {reason}")
    cuddles = ["https://tenor.com/bgaNg.gif",
               "https://tenor.com/WdJI.gif"]
    await ctx.send(random.choice(cuddles))


@sylveon.command(aliases=['safe', 'lifeline', 'prevention', 'suicideprevention', 'suicidepreventionhotline'])
async def suicide(ctx, members: commands.Greedy[discord.Member] = None, *, custom_message: typing.Optional[
    str] = "You are an incredible person who will do incredible things. You deserve the world."):
    """if someone is in danger of hurting themselves, this sends them a link to the Suicide Prevention Hotline."""
    await ctx.message.delete()
    if members is None:
        members = [ctx.author]
    for member in members:
        try:
            member_direct_message = await member.create_dm()
            await member_direct_message.send(f"""Suicide is never the answer.
Losing a friend or family member to suicide is the worst way to lose them, and there’s no undoing it. Once you die, there is no coming back, there’s no replacing what was lost. Suicide is worse than a car accident, worse than being shot, because everybody feels responsible. Every person who cares about you will blame themselves for it, because they have nobody else to blame. Some of them may take their own lives as well, continuing the domino effect. Life might be bad,  but it will get better. You still have your whole life ahead of you, you can and will accomplish so much with it. Ending it all at your darkest moment will not make it better. 
You matter.
People care about you.
Your life is significant.
{custom_message}
Whoever sent this will do everything in their power stop you from taking your own life, and I know that others will do the same.
Talking to someone- anyone- that you know won't try to hurt you is important. If you don't know or can't find anyone, you can call 1-800-273-8255 or go to https://suicidepreventionlifeline.com/chat
- {ctx.author}, valkyrie_pilot#2707, and smallpepperz#0681.
""")
        except discord.Forbidden or discord.HTTPException:
            try:
                author_dm = await ctx.author.create_dm()
                await author_dm.send("Unable to send a message to your friend. Links: `You can call 1-800-273-8255 or "
                                     "go to https://suicidepreventionlifeline.com/chat`. Please go talk to them yourself.")
            except discord.Forbidden or discord.HTTPException:
                pass


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
