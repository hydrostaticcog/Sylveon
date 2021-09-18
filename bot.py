#!venv/bin/python3
import asyncio
import base64
import binascii
import os
import pathlib
import random
import re

import aiohttp
import aiomysql
import catapi
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

path = pathlib.Path()
load_dotenv()

sql = asyncio.get_event_loop().run_until_complete(
    aiomysql.create_pool(host=os.getenv('SQLserverhost'),
                         user=os.getenv('SQLusername'),
                         password=os.getenv('SQLpassword'),
                         db=os.getenv('SQLdatabase'),
                         autocommit=True))


async def deping(text) -> str:
    text.replace("@everyone", "Please do not attempt to ping people with this command!")
    text.replace("@here", "Please do not attempt to ping people with this command!")
    text = re.sub("<@(!?)([0-9]*)>", "Please do not attempt to ping people with this command!", text)
    return text


intents = discord.Intents(members=True, guilds=True)
sylveon = commands.Bot(case_insensitive=True, intents=intents,
                       activity=discord.Activity(activity=discord.Game(
                           name=f"with friends!")))
embedcolor = 0xFD6A02


@sylveon.slash_command()
async def hello(ctx,
                member: discord.app.Option(discord.Member, 'Member to say hello to', required=False) = None):
    """o/"""
    if isinstance(member, discord.Member):
        embed = discord.Embed()
        embed.set_image(url='https://c.tenor.com/6us3et_6HDoAAAAC/hello-there-hi-there.gif')
        await ctx.respond(f'Welcome {member.mention}!', embed=embed)
    else:
        await ctx.respond('https://tenor.com/view/hello-there-hi-there-greetings-gif-9442662')


@sylveon.slash_command()
async def ping(ctx):
    """get bot ping"""
    embed = discord.Embed(colour=embedcolor)
    embed.add_field(name="Ping", value=f'🏓 Pong! {round(sylveon.latency * 1000)}ms')
    embed.set_footer(text=f"Request by {ctx.author}")
    await ctx.respond(embed=embed)


@sylveon.slash_command()
async def base64encode(ctx,
                       string: discord.app.Option(str, 'String to convert from base64 to ascii')):
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
async def base64decode(ctx,
                       string: discord.app.Option(str, 'String to convert to ascii from base64')):
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
async def hug(ctx,
              member: discord.app.Option(discord.Member, 'Member you want to hug', required=False) = None,
              reason: discord.app.Option(str, 'Reason for hugs', required=False) = None):
    """Gives someone a hug :D"""
    hugs = ["https://media.tenor.com/images/50c2f13c590fdb27c087d6a6736218e0/tenor.gif",
            "https://media.discordapp.net/attachments/731763704005394523/829133807008743444/image0.gif",
            "https://media1.tenor.com/images/969f0f462e4b7350da543f0231ba94cb/tenor.gif",
            "https://media1.tenor.com/images/b7492c8996b25e613a2ab58a5d801924/tenor.gif?itemid=14227401",
            "https://media1.tenor.com/images/24ac13447f9409d41c1aecb923aedf81/tenor.gif?itemid=5026057",
            "https://media1.tenor.com/images/f720d87668fa1e65b3294eb30fc4ac36/tenor.gif?itemid=19092449",
            "https://c.tenor.com/xIuXbMtA38sAAAAd/toilet-bound-hanakokun.gif"]
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
            await ctx.respond(f"{member.mention}, {ctx.author.mention} gave you a hug, {reason}", embed=embed)
    else:
        await ctx.respond(f":D, {ctx.author.mention} gave you a hug, {reason}", embed=embed)


@sylveon.slash_command()
async def snuggle(ctx,
                  member: discord.app.Option(discord.Member, 'Member you want to snuggle', required=False) = None,
                  reason: discord.app.Option(str, 'Reason for snuggles', required=False) = None):
    """Gives someone a snuggle :D"""
    snuggles = ["https://c.tenor.com/eJkT33i-NcUAAAAC/rosy-cheeks-mochi-peach.gif",
                "https://c.tenor.com/aiC-Lw9RBjkAAAAC/pats-cute.gif",
                "https://c.tenor.com/5VbS6pyBYvsAAAAC/gif-fofinho-heart.gif"]
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
            await ctx.respond(f"{member.mention}, {ctx.author.mention} snuggles you, {reason}", embed=embed)
    else:
        await ctx.respond(f":D, {ctx.author.mention} snuggles you, {reason}", embed=embed)
        await ctx.send(random.choice(snuggles))


@sylveon.slash_command()
async def cuddle(ctx,
                 member: discord.app.Option(discord.Member, 'Member you want to cuddle', required=False) = None,
                 reason: discord.app.Option(str, 'Reason for cuddles', required=False) = None):
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
            await ctx.respond(f"{member.mention}, {ctx.author.mention} cuddles you, {reason}", embed=embed)
    else:
        await ctx.respond(f":D, {ctx.author.mention} cuddles you, {reason}", embed=embed)


@sylveon.slash_command()
async def antisuicide(ctx,
                      person: discord.app.Option(discord.Member, 'Member to send the anti-suicide message to'),
                      message: discord.app.Option(str,
                                                  'Custom message that will be inserted into the default message',
                                                  required=False) = "You are an incredible person who will do incredible things. You deserve the world."):
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


xkcd = sylveon.command_group(
    "xkcd", "xkcd-related commands"
)


@xkcd.command(name="setup")
async def xkcd_setup(ctx,
                     channel: discord.app.Option(discord.abc.GuildChannel,
                                                 'Text channel to send XKCD notifications to'),
                     pingrole: discord.app.Option(discord.Role, 'Role to mention when an XKCD comes out',
                                                  required=False)):
    """Set the channel to receive updates when a new XKCD releases"""
    if ctx.author.guild_permissions.manage_channels:
        if isinstance(channel, discord.TextChannel):
            async with await sql.acquire() as conn:
                async with await conn.cursor() as cur:
                    await cur.execute("""DELETE FROM xkcd WHERE guild = (%s)""", (ctx.guild.id,))
                    if isinstance(pingrole, discord.Role):
                        await cur.execute("""INSERT INTO xkcd VALUES (%s, %s, %s)""",
                                          (ctx.guild.id, channel.id, pingrole.id,))
                    else:
                        await cur.execute("""INSERT INTO xkcd VALUES (%s, %s, NULL)""", (ctx.guild.id, channel.id,))
                    await ctx.respond("XKCD notifier set up successfully!", ephemeral=True)
        else:
            await ctx.respond(
                "Please use a text channel, discord doesn't give a way to specify that your selection must be a text channel.",
                ephemeral=True)
    else:
        await ctx.respond("You must have the `manage channels` permission to use that command.", ephemeral=True)


@xkcd.command(name="disable")
async def xkcd_disable(ctx):
    """Disables the XKCD release notifier."""
    async with await sql.acquire() as conn:
        async with await conn.cursor() as cur:
            await cur.execute("""DELETE FROM xkcd WHERE guild = %s""", (ctx.guild.id,))
    await ctx.respond("Removed this guild from those subscribed to XKCD", ephemeral=True)


@xkcd.command()
async def get(ctx,
              number: discord.app.Option(int, 'XKCD comic number to fetch', required=False) = None):
    """Get an XKCD by number, or the latest xkcd"""
    async with aiohttp.ClientSession() as session:
        if isinstance(number, int):
            async with session.get(f'https://xkcd.com/{number}/info.0.json') as r:
                if r.status == 200:
                    js = await r.json()
                    embed = discord.Embed(description=f"[XKCD #{js['num']}](https://xkcd.com/{js['num']})")
                    embed.set_image(url=js['img'])
                    embed.set_footer(text=js['alt'])
                    await ctx.respond(js['title'], embed=embed)
                else:
                    await ctx.respond(f"XKCD returned error code `{r.status}`")
        else:
            async with session.get('https://xkcd.com/info.0.json') as r:
                if r.status == 200:
                    js = await r.json()
                    embed = discord.Embed(description=f"[XKCD #{js['num']}](https://xkcd.com/{js['num']})")
                    embed.set_image(url=js['img'])
                    embed.set_footer(text=js['alt'])
                    await ctx.respond(js['title'], embed=embed)
                else:
                    await ctx.respond(f"XKCD returned error code `{r.status}`")


@tasks.loop(minutes=1)
async def read_xkcd_com():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://xkcd.com/info.0.json') as r:
            if r.status == 200:
                with open(path / ".sylveoncache/latestxkcd", "r") as cache:
                    if cache.read() == await r.text():
                        return
                js = await r.json()
                embed = discord.Embed(description=f"[XKCD #{js['num']}](https://xkcd.com/{js['num']})")
                embed.set_image(url=js['img'])
                embed.set_footer(text=js['alt'])
                async with await sql.acquire() as conn:
                    async with await conn.cursor() as cur:
                        await cur.execute("""SELECT channel, role_to_ping FROM xkcd""")
                        channels = await cur.fetchall()
                        for channel in channels:
                            send_to = await sylveon.fetch_channel(channel[0])
                            if isinstance(channel[1], int):
                                await send_to.send(f"A new XKCD is out!\n\n <@&{channel[1]}>", embed=embed)
                            else:
                                await send_to.send(f"A new XKCD is out!", embed=embed)
                            await asyncio.sleep(2)
                with open(path / ".sylveoncache/latestxkcd", "w+") as cache:
                    cache.write(await r.text())


read_xkcd_com.start()


@sylveon.slash_command()
async def pussy(ctx):
    """see a pussy"""

    # Initialize the api
    api = catapi.CatApi(api_key=os.getenv('catapikey'))

    results = await api.search_images(limit=1)
    embed = discord.Embed()
    embed.set_image(url=results[0].url)
    await ctx.respond("What did you *think* you were going to see?", embed=embed)


sylveon.run(os.getenv('TOKEN'))
