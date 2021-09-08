#!venv/bin/python3
import base64
import binascii
import pathlib
import random
import re
import traceback

import aiohttp
import discord
from discord.ext import commands

path = pathlib.Path()


async def deping(text) -> str:
    text.replace("@everyone", "Please do not attempt to ping people with this command!")
    text.replace("@here", "Please do not attempt to ping people with this command!")
    text = re.sub("<@(!?)([0-9]*)>", "Please do not attempt to ping people with this command!", text)
    return text


with open(path / 'system/token.txt', 'r') as file:
    TOKEN = file.read()
intents = discord.Intents().none()
sylveon = commands.Bot(case_insensitive=True, intents=intents,
                       activity=discord.Activity(activity=discord.Game(
                           name=f"with friends!")))
embedcolor = 0xFD6A02


@sylveon.slash_command()
async def hello(ctx):
    """o/"""
    await ctx.respond('https://tenor.com/view/hello-there-hi-there-greetings-gif-9442662')


@sylveon.slash_command()
async def ping(ctx):
    """get bot ping"""
    embed = discord.Embed(colour=embedcolor)
    embed.add_field(name="Ping", value=f'🏓 Pong! {round(sylveon.latency * 1000)}ms')
    embed.set_footer(text=f"Request by {ctx.author}")
    await ctx.respond(embed=embed)


@sylveon.slash_command()
async def base64encode(ctx, string: str):
    """Encode a string to Base64"""
    try:
        b64_encoded_string = base64.b64encode(string.encode()).decode()
    except binascii.Error:
        await ctx.respond("Something went wrong encoding that string.")
        return
    if len(b64_encoded_string) > 2000:
        await ctx.respond("That string is too long.")
        return
    await ctx.respond(await deping(b64_encoded_string))


@sylveon.slash_command()
async def base64decode(ctx, string: str):
    """Decode a string from Base64"""
    try:
        b64_encoded_string = base64.b64decode(string.encode()).decode()
    except binascii.Error:
        await ctx.respond("Your input doesn't seem to be a base64 string!")
        return
    if len(b64_encoded_string) > 2000:
        await ctx.respond("That string is too long.")
        return
    await ctx.respond(await deping(b64_encoded_string))


@sylveon.slash_command()
async def hug(ctx, member: discord.Member = None, reason: str = None):
    """Gives someone a hug :D"""
    hugs = ["https://media.tenor.com/images/50c2f13c590fdb27c087d6a6736218e0/tenor.gif",
            "https://media.discordapp.net/attachments/731763704005394523/829133807008743444/image0.gif",
            "https://media1.tenor.com/images/969f0f462e4b7350da543f0231ba94cb/tenor.gif",
            "https://media1.tenor.com/images/b7492c8996b25e613a2ab58a5d801924/tenor.gif?itemid=14227401",
            "https://media1.tenor.com/images/24ac13447f9409d41c1aecb923aedf81/tenor.gif?itemid=5026057",
            "https://media1.tenor.com/images/f720d87668fa1e65b3294eb30fc4ac36/tenor.gif?itemid=19092449"]
    embed = discord.Embed()
    embed.set_image(url=random.choice(hugs))
    if reason is None:
        reason = "for being a good friend"
    if member is not None:
        if member.id == 808149899182342145:
            await ctx.respond("But that's Glaceon!")
            await ctx.send("https://tenor.com/view/anime-blush-girl-gif-19459906")
            return
        else:
            await ctx.respond(f"{member.mention}, {ctx.author.mention} gave you a hug {reason}", embed=embed)
    else:
        await ctx.respond(f":D, {ctx.author.mention} gave you a hug {reason}", embed=embed)


@sylveon.slash_command()
async def snuggle(ctx, member: discord.Member = None, reason: str = None):
    """Gives someone a snuggle :D"""
    snuggles = ["https://tenor.com/view/rosy-cheeks-mochi-peach-mochi-cat-cute-kitty-peach-cat-gif-16992602",
                "https://tenor.com/view/pats-cute-cats-love-gif-13979931",
                "https://tenor.com/view/gif-fofinho-heart-love-cuddle-cute-gif-14676815"]
    embed = discord.Embed()
    embed.set_image(url=random.choice(snuggles))
    if reason is None:
        reason = "for being someone awesome"
    if member is not None:
        if member.id == 808149899182342145:
            await ctx.respond("But that's Glaceon!")
            await ctx.send("https://tenor.com/view/anime-blush-girl-gif-19459906")
            return
        else:
            if reason is None:
                reason = "aww!"
            await ctx.respond(f"{member.mention}, {ctx.author.mention} snuggles you {reason}", embed=embed)
    else:
        await ctx.respond(f":D, {ctx.author.mention} snuggles you {reason}", embed=embed)
        await ctx.send(random.choice(snuggles))


@sylveon.slash_command()
async def cuddle(ctx, member: discord.Member = None, reason: str = None):
    """when you want to cuddle with someone, because you love them"""
    cuddles = ["https://c.tenor.com/R4NC0rf5RYAAAAAd/couples-love.gif",
               "https://c.tenor.com/-rW7zgTPkkwAAAAi/hug.gif",
               "https://c.tenor.com/TsL3G4aPH2wAAAAC/milk-and-mocha-milk.gif",
               "https://c.tenor.com/X54vC9bzK6MAAAAC/cute-cuddle.gif",
               "https://c.tenor.com/Aaxuq2evHe8AAAAC/kiss-cute.gif"]
    embed = discord.Embed()
    embed.set_image(url=random.choice(cuddles))
    if reason is None:
        reason = "because they love you"
    if member is not None:
        if member.id == 808149899182342145:
            await ctx.respond("But that's Glaceon!")
            await ctx.send("https://tenor.com/view/anime-blush-girl-gif-19459906")
            return
        else:
            if reason is None:
                reason = "aww!"
            await ctx.respond(f"{member.mention}, {ctx.author.mention} cuddles you {reason}", embed=embed)
    else:
        await ctx.respond(f":D, {ctx.author.mention} cuddles you {reason}", embed=embed)


@sylveon.slash_command()
async def antisuicide(ctx, person: discord.Member,
                  message: str = "You are an incredible person who will do incredible things. You deserve the world."):
    """Sends suicide prevention links to the user selected."""
    try:
        member_direct_message = await person.create_dm()
        await member_direct_message.send(f"""Suicide is never the answer.
Losing a friend or family member to suicide is the worst way to lose them, and there’s no undoing it. Once you die, there is no coming back, there’s no replacing what was lost. Suicide is worse than a car accident, worse than being shot, because everybody feels responsible. Every person who cares about you will blame themselves for it, because they have nobody else to blame. Some of them may take their own lives as well, continuing the domino effect. Life might be bad,  but it will get better. You still have your whole life ahead of you, you can and will accomplish so much with it. Ending it all at your darkest moment will not make it better. 
You matter.
People care about you.
Your life is significant.
{message}
Whoever sent this will do everything in their power stop you from taking your own life, and I know that others will do the same.
Talking to someone- anyone- that you know won't try to hurt you is important. If you don't know or can't find anyone, you can call 1-800-273-8255 or go to https://suicidepreventionlifeline.com/chat
- {ctx.author}, valkyrie_pilot#2707, and smallpepperz#0681.
""")
        await ctx.respond("Successfully sent your friend the message they needed.", ephemeral=True)
    except discord.Forbidden:
        await ctx.respond(
            "Unable to send a message to your friend, they might have DMs off or me blocked. You can have them call "
            "1-800-273-8255 or go to https://suicidepreventionlifeline.com/chat. Please go talk to them yourself.",
            ephemeral=True)
    except discord.HTTPException:
        await ctx.respond(
            "Unable to send a message to the specified user. They are likely a bot.",
            ephemeral=True)


@sylveon.slash_command()
async def xkcd(ctx, id: int = None):
    """Get an XKCD by number, or the latest xkcd"""
    async with aiohttp.ClientSession() as session:
        if isinstance(id, int):
            async with session.get(f'https://xkcd.com/{id}/info.0.json') as r:
                if r.status == 200:
                    js = await r.json()
                    embed = discord.Embed()
                    embed.set_image(url=js['img'])
                    embed.set_footer(text=js['alt'])
                    await ctx.respond(js['title'], embed=embed)
                else:
                    await ctx.respond(f"XKCD returned error code `{r.status}`")
        else:
            async with session.get('https://xkcd.com/info.0.json') as r:
                if r.status == 200:
                    js = await r.json()
                    embed = discord.Embed()
                    embed.set_image(url=js['img'])
                    embed.set_footer(text=js['alt'])
                    await ctx.respond(js['title'], embed=embed)
                else:
                    await ctx.respond(f"XKCD returned error code `{r.status}`")


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

        # format_exception returns a list with line breaks embedded in the lines, so let's just stitch the elements
        # together
        traceback_text = ''.join(lines)

        # now we can send it to the user
        bug_channel = sylveon.get_channel(845453425722261515)
        await bug_channel.send("```\n" + str(traceback_text) + "\n```\n Command being invoked: " + ctx.command.name)
        await ctx.send("Error!\n```" + str(
            error) + "```\nvalkyrie_pilot will be informed.  Most likely this is a bug, but check your syntax.",
                       delete_after=30)


sylveon.run(TOKEN)
