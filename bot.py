import discord
from discord.ext import commands

import operator
from functools import reduce

import datetime
import random
import SECRETS

client = commands.Bot(command_prefix = '#')

extensions = ['evaluate', 'fun', 'tictactoe', 'error_handler']

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
	if author == client.user:
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
	if author == client.user:
		return
	if (content.startswith('#clear')):
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
		description = "[Don't include brackets in commands.]",
		colour = discord.Colour.green(),
	)
	embed.set_author(name=bot, icon_url=client.user.avatar_url)
	embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/kingofthehill/images/c/c4/Hank_Hill.png/revision/latest?cb=20140504043948")
	embed.add_field(name='**#help**', value=":eyes:", inline=False)
	embed.add_field(name='**#clear** [1-100]', value="GET THAT OUT OF HERE :middle_finger: ", inline=False)
	embed.add_field(name='**#pfp** [Optional user]', value="WHAT IS THAT :art:", inline=False)
	embed.add_field(name='**#status**', value="PLAYING WITH MY BALLS :video_game:", inline=False)
	embed.add_field(name='**#dick**', value="BOBBY GET THE PROPENE :eggplant:", inline=False)
	embed.add_field(name='**#say** [Anything]', value="THE FUCK YOU SAY? :open_mouth:", inline=False)
	embed.add_field(name='**#coin**', value="FLIP A COIN :red_circle: ", inline=False)
	embed.add_field(name='**#rps**', value="🗿📄✂", inline=False)

	math = discord.Embed(
		title = "Math",
		description = "Information for the math class",
		colour = discord.Colour.blue(),
	)
	math.set_author(name=bot, icon_url=client.user.avatar_url)
	math.set_thumbnail(url="https://78.media.tumblr.com/79ba6a68e9e4bbe978e808d5990005b4/tumblr_n1y3j6UZxq1rn02guo1_250.png")
	math.add_field(name="Library", value="The SimpleEval library: https://github.com/danthedeckie/simpleeval#operators", inline=False)
	math.add_field(name="**Operators**", value="``+`` Add two or more things. ``x + y`` ``1 + 1`` -> ``2``\n``-`` Subtract two or more things. ``x - y`` ``2 - 1`` -> ``1``\n``*`` Multiply two or more things. ``x * y`` ``2 * 2`` -> ``4``\n``/`` Divide two or more things. ``x / y`` ``2 / 1`` -> ``2``\n``**`` To the power of ``x ** y`` ``2 ** 2`` -> ``4``\n``%`` Modulus (remainder). ``x % y`` ``3 % 2`` -> ``1``\n``==`` Equals. ``x == y`` ``15 == 4`` -> ``False``\n``>`` Greater than. ``x > y`` ``6 > 1`` -> ``True``\n``<`` Less than. ``x < y`` ``22 < 2`` -> ``False``\n``=>`` Greater than or equal to. ``x => y`` ``3 => 3`` -> ``True``\n``<=`` Less than or equal to. ``x <= y`` ``4 <= 100`` -> ``False``\n``in`` Is something contained within something else. ``'spam' in 'dog'`` -> ``False``", inline=False)
	math.set_footer(text=bot+' created by ian#4359')
	await client.say(embed=embed)
	await client.say(embed=math)

# Clear messages with permissions
@commands.cooldown(1, 5, commands.BucketType.user)
@client.command(pass_context = True, no_pm = True)
async def clear(ctx, amount = 5):
    channel = ctx.message.channel
    messages = []
    try:
        if ctx.message.author.server_permissions.administrator:
	        async for message in client.logs_from(channel, limit = int(amount) + 1):
	            messages.append(message)
	        await client.delete_messages(messages)
	        await client.say(str(amount) + ' messages deleted.')
    except ValueError:
        await client.say('Please enter a whole number 1-100.')
    except BadArgument:
        await client.say('Please enter a whole number 1-100.')

# Get avatar of user
@client.command(pass_context=True)
async def pfp(ctx):
	author = ctx.message.author

	# Make pfp embed message1
	def make_embed(profile, avatar_url, color):
		embed = discord.Embed(title = profile.name + " Avatar URL", colour = color, url = avatar_url)
		embed.set_image(url=avatar_url)
		embed.set_footer(text=client.user.name+' by ian#4359', icon_url=client.user.avatar_url)
		embed.timestamp = datetime.datetime.utcnow()
		return embed

	# Check for mentions in message
	if(ctx.message.mentions.__len__() > 0):
		for user in ctx.message.mentions:
			# If no avatar, return default avatar
			if user.avatar_url.__len__() == 0:
				embed = make_embed(user, user.default_avatar_url, discord.Colour.green())
			# Return avatar
			else:
				embed = make_embed(user, user.avatar_url, discord.Colour.green())

	# Else return author avatar
	else:
		# If no avatar, return default avatar
		if author.avatar_url.__len__() == 0:
			embed = make_embed(author, author.default_avatar_url, discord.Colour.blue())
		# Return avatar
		else:
			embed = make_embed(author, author.avatar_url, discord.Colour.blue())

	await client.say(embed=embed)

# Test command for logging messages
# @client.command(pass_context = True)
# async def logme(ctx, amount = 10):
#     channel = ctx.message.channel
#     messages = []
# 	  async for message in client.logs_from(channel, limit = int(amount)):
#         messages.append(message)
#         print("{}: {}".format(message.author, message.content))
#     await client.say("Messages logged.")

# Change the status message of bot
@commands.cooldown(1, 5, commands.BucketType.user)
@client.command(pass_context=True)
async def status(ctx, *args):
	game_status = ''
	for word in args:
		game_status += word
		game_status += ' '
	await client.change_presence(game=discord.Game(name=game_status))
	await client.say("Bobby updated game status to '{}'".format(game_status))

# Add cogs (extensions)
if __name__ == '__main__':
	for extension in extensions:
		try:
			client.load_extension(extension)
		except Exception as error:
			print('{} cannot be loaded. [{}]'.format(extension, error))

client.run(SECRETS.TOKEN)
