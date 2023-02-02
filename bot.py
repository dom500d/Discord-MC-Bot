# bot.py
import os
import asyncio
import discord
from dotenv import load_dotenv
from discord.ext import commands
from mcstatus import JavaServer

server = JavaServer.lookup("10.0.0.213")
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = "Dom's Minecraft Dungeon"
intents1 = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents1)
trigger = bool(1)


@bot.command(name='update')
@commands.has_permissions(administrator=True)
async def update(ctx):
    global trigger
    trigger = bool(1)
    query = server.query()
    embed = discord.Embed(title="Current Server Information",
                          description=f"The server has the following players online: {', '.join(query.players.names)}\n",
                          color=ctx.guild.me.top_role.color
                          )
    msg = await ctx.channel.send(embed=embed)
    while trigger:
        await asyncio.sleep(60)
        query = server.query()
        embed.description = f"The server has the following players online: {', '.join(query.players.names)}\n"
        await msg.edit(embed=embed)


@bot.command(name='stop')
async def stop(ctx):
    global trigger
    trigger = bool(0)


@bot.command(name='ping')
async def server_ping(ctx):
    ping = round(server.ping(), 1)
    response = f"The server ping is {ping} ms!"
    await ctx.send(response)


@bot.command(name='online')
async def server_online(ctx):
    query = server.query()
    response = f"The server has the following players online: {', '.join(query.players.names)}"
    await ctx.send(response)


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to Dom\'s Minecraft Dungeon!'
    )


async def on_command_error(self, exception, context):
    original = exception.original.__class__.__name__
    if original == 'ConnectionRefusedError' or original == 'timeout':
        await self.bot.send_message(
            context.message.channel,
            'The server is not accepting connections at this time.',
        )
    elif original == 'gaierror':
        await self.bot.send_message(
            context.message.channel,
            'The !ip is unreachable; complain to someone in charge.',
        )

bot.run(TOKEN)
