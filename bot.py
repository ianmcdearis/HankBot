import discord
from discord.ext import commands

import operator
from functools import reduce

import datetime
import random

def read_token():
	with open("token.txt", "r") as f:
		lines = f.readlines()
		return lines[0].strip()

TOKEN = read_token()

client = commands.Bot(command_prefix = '#')

extensions = ['fun', 'error_handler']

client.remove_command('help')

@client.event
async def on_ready():
	servers = list(client.servers)
	print("Bot Online!")
	print("Name: {}".format(client.user.name))
	print("ID: {}".format(client.user.id))
	print("Servers:")
	for x in range(len(servers)):
		print(' ' + servers[x-1].name)
	print('---------------------')
	print('')
	await client.change_presence(game=discord.Game(name='with my propane.'))


@client.event
async def on_message(message):
	author = message.author
	content = message.content
	if author.bot:
		return
	if '😂' in content:
		await client.add_reaction(message, '😂')
	await client.process_commands(message)


@client.event
async def on_member_join(member):

	# Random join message
	join_messages = [
	":flushed: Step bro you were gone for so long, welcome {0} to **{1}**",
	"{0} why are you here? The **{1}** doesn't want you.",
	"FUCK YOU {0} AND THIS {1} SERVER".upper(),
	"AMBER ALERT: Missing child ({0}) in **{1}**\nLast seen with 22 year old black male.",
	"{0} leave the **{1}**, please. We fucking hate you.",
	"{0} was just sold! Welcome to slavery in **{1}**",
	"**{1}** BREAKING NEWS:\n{0} just got caught pissing on bitches. Please stay indoors.",
	"Just moonwalked in on {0} getting touched by Michael Jackson in the **{1}**",
	"Woof woof {0}, ruff grrrr **{1}** awoo woof.",
	"{0}! **{1}**!",
	]
	random_join = random.choice(join_messages)

	# Send join message
	for channel in member.server.channels:
		if channel.name == "general" or channel.name == "goodvibes":
			await client.send_message(channel, random_join.format(member.mention, member.server))


@client.event
async def on_member_remove(member):

	# Random leave message
	leave_messages = ['my wife', 'Bobby', 'the dog and a boner', 'a chronic masturbation addiction',
	'Sandra McCormick', 'Rachael McCormick', 'AIDS', 'a coke addiction', 'WOOF WOOF WOOF',
	'Elliott in the 1800s', ':o', ':banana:', '3.141592653589793238462643383279']
	leave = random.choice(leave_messages)

	# Send leave message
	for channel in member.server.channels:
		if channel.name == "general" or channel.name == "goodvibes":
			await client.send_message(channel, '**{0.name}** left with {1}...'.format(member, leave))


@client.event
async def on_message_delete(message):
	author = message.author
	content = message.content
	if author.bot:
		return
	if content.startswith(('#clear', '#ttt', '#say')):
		return
	embed = discord.Embed(
		title = "Message deleted",
		description = "► Content: `" + content + "`\n ► Channel: **" + str(message.channel) + "**",
		colour = author.colour,
	)
	embed.set_author(name=author, icon_url=message.author.avatar_url)
	embed.set_footer(text=client.user.name+' by ian#4359', icon_url=client.user.avatar_url)
	embed.timestamp = datetime.datetime.utcnow()
	channel = discord.utils.get(client.get_all_channels(), name='logs')
	await client.send_message(channel, embed=embed)


# Send private message with help
@client.command(pass_context=True)
async def help(ctx):
	bot = client.user.name
	author = ctx.message.author

	embed = discord.Embed(
		title = "Help",
		description = "Propane and propane accessories for HankBot.",
		colour = discord.Colour.teal(),
	)

	embed.set_author(name=bot, icon_url=client.user.avatar_url)
	embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/kingofthehill/images/c/c4/Hank_Hill.png/revision/latest?cb=20140504043948")

	embed.add_field(name='**#help**', value=":point_left: :eyes:")
	embed.add_field(name='**#clear** [1-100]', value=":no_entry: :1234:")

	embed.add_field(name='**#pfp** [Optional user]', value=":frame_photo: :art:")
	embed.add_field(name='**#userinfo** [Optional user]', value=":thinking: :person_with_blond_hair:")

	embed.add_field(name='**#status** [Anything]', value=":pencil2: :video_game:")
	embed.add_field(name='**#dick**', value=":eggplant: :banana:")

	embed.add_field(name='**#say** [Anything]', value=":open_mouth: :grey_question:")
	embed.add_field(name='**#magicball** [Anything]', value=":8ball: :crystal_ball:")

	embed.add_field(name='**#choose** [List]', value=":thinking: :robot: ")
	embed.add_field(name='**#coin**', value=":large_blue_circle: :red_circle:")

	embed.add_field(name='**#rps**', value="🗿📄✂")
	embed.add_field(name='**#ttt [User]**', value=":o: :x:")

	embed.set_footer(text=client.user.name+' by ian#4359', icon_url=client.user.avatar_url)
	embed.timestamp = datetime.datetime.utcnow()

	await client.say(embed=embed)


# Clear messages with permissions
@commands.cooldown(1, 5, commands.BucketType.user)
@client.command(pass_context = True, no_pm = True)
async def clear(ctx, amount: int):
	channel = ctx.message.channel
	messages = []
	if ctx.message.author.server_permissions.administrator:
		async for message in client.logs_from(channel, limit = int(amount) + 1):
			messages.append(message)
		await client.delete_messages(messages)
		await client.say(str(amount) + ' messages deleted.')


# Get avatar of user
@client.command(pass_context=True)
async def pfp(ctx, member: discord.Member = None):
	member = ctx.message.author if not member else member

	# Make pfp embed message
	def make_embed(profile, avatar_url, color):
		embed = discord.Embed(title = profile.name + " Avatar URL", colour = color, url = avatar_url)
		embed.set_image(url=avatar_url)
		embed.set_footer(text=client.user.name+' by ian#4359', icon_url=client.user.avatar_url)
		embed.timestamp = datetime.datetime.utcnow()
		return embed

	# If no avatar, return default avatar
	if len(member.avatar_url) == 0:
		embed = make_embed(member, member.default_avatar_url, discord.Colour.blue())
	# Return avatar
	else:
		embed = make_embed(member, member.avatar_url, discord.Colour.blue())

	await client.say(embed=embed)

# Get user information
@client.command(pass_context=True, no_pm=True)
async def userinfo(ctx, member: discord.Member = None):
	member = ctx.message.author if not member else member

	roles = [role for role in member.roles]

	embed = discord.Embed(colour = member.colour)
	embed.timestamp = datetime.datetime.utcnow()

	embed.set_author(name = "User Info - {0}".format(member))
	embed.set_thumbnail(url = member.avatar_url)
	embed.set_footer(text = "Requested by {0}".format(ctx.message.author), icon_url = ctx.message.author.avatar_url)

	embed.add_field(name = "ID: ", value = member.id, inline = True)
	embed.add_field(name = "Guild Name: ", value = member.name, inline = True)

	embed.add_field(name = "Created at: ", value = member.created_at.strftime("%a, %#d, %B %Y, %I:%M %p UTC"), inline = False)
	embed.add_field(name = "Joined at: ", value = member.joined_at.strftime("%a, %#d, %B %Y, %I:%M %p UTC"), inline = False)

	embed.add_field(name = "Roles ({0})".format(len(roles)), value = " ".join([role.mention for role in roles]), inline = False)
	embed.add_field(name = "Top role: ", value = member.top_role.mention, inline = True)
	embed.add_field(name = "Bot? ", value = member.bot, inline = True)

	embed.set_footer(text=client.user.name+' by ian#4359', icon_url=client.user.avatar_url)
	embed.timestamp = datetime.datetime.utcnow()

	await client.say(embed=embed)

# Change the status message of bot
@commands.cooldown(1, 5, commands.BucketType.user)
@client.command(pass_context=True)
async def status(ctx, *, gameStatus):
	await client.change_presence(game=discord.Game(name=gameStatus))
	await client.say("Bobby updated game status to '{}'".format(gameStatus))

# When you wanna settle something
@client.command(pass_context=True)
async def choose(ctx, *choices : str):
	# Choose between choices
	await client.say(random.choice(choices))

# Rank a list of things
@client.command(pass_context=True)
async def rank(ctx, *, items : str):
	# Rank a list of items
	list = items.split(",")
	random.shuffle(list)

	for i in range(len(list)):
		await client.say(f"{i+1}. {list[i]}")

# Add cogs (extensions)
if __name__ == '__main__':
	for extension in extensions:
		try:
			client.load_extension(extension)
		except Exception as error:
			print('{} cannot be loaded. [{}]'.format(extension, error))

client.run(TOKEN)
