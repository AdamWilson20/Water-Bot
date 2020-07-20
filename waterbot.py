import discord
import asyncio
import aiohttp
import random
import datetime
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import Bot

load_dotenv()

TOKEN = os.getenv("TOKEN")
client = commands.Bot(command_prefix = '.')


@client.event
async def on_ready():
	print('Bot is ready.')

@client.event	
async def  on_member_join(member):
	print(f'{member} has joined the server.')
	if member.id == client.id:
		return
	channel = discord.utils.get(bot.guilds[0].channels, name="bot-commands")
	response = f"Welcome to Nerdy Lifting Squad!, {member.name}."
	await channel.send(response)

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	keywords = ["water","thirsty","dry"]
	channel = message.channel
	for keyword in keywords:
		if keyword.lower() in message.content.lower():
			response = f"Did someone say {keyword.lower()}? Drink some water!"
			await channel.send(response)

@client.event
async def water_reminder():
	while(True):
		await client.wait_until_ready()
		online_members = []
		for member in client.get_all_members():
				if member.status != discord.Status.offline and member.id != client.user.id:
					online_members.append(member.id)
	if len(online_members) > 0:
		user = random.choice(online_members)
		current_time= int(datetime.datetime.now().strftime("%I"))
		channel = discord.utils.get(client.guilds[0].channels, name="bot-commands")
		message = f"It's {current_time} o'clock! Time for some water <@{user}>!"
		await channel.send(message)
		await asyncio.sleep(3600)
		
		client.loop.create_task(water_reminder())



@client.event
async def on_member_remove(member):
	print(f'{member} has left the server.')

@client.command(name = 'ping')
async def ping(ctx):
	await ctx.send('Pong!')
  



client.run(TOKEN)

