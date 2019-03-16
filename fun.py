import discord
from discord.ext import commands

import random

class Fun:
    def __init__(self, client):
        self.client = client

    # Say message then delete author message
    @commands.command(pass_context=True)
    async def say(self, ctx, *args):
        message = ctx.message
        output = ''
        for word in args:
            output += word + ' '
        await self.client.delete_message(message)
        await self.client.say(output)

    # Random dick size
    @commands.command(pass_context=True)
    async def dick(self, ctx):
        author = ctx.message.author

        size = random.randint(1, 15)
        output = '8'
        for i in range(size):
            output += '='
        output += 'D'
        flaccidity = ['hard :eggplant:', 'soft :banana:']
        hard_or_soft = random.choice(flaccidity)
        await self.client.say("**{0.mention}** has a ".format(author) + str(size) + " inch dick " + hard_or_soft + " " + output)

    # Rock paper scissors variables (1 == rock, 2 == paper, 3 == scissors)
    aiChoice = 0
    playerChoice = 0

    # Rock Paper Scissors
    @commands.command(pass_context=True)
    async def rps(self, ctx):
        global playerChoice, aiChoice

        author = ctx.message.author
        bot = self.client.user.name

        # Check for emojis
        def check(reaction, author):
            e = str(reaction.emoji)
            return e.startswith(('🗿', '📄', '✂'))

        # Create embedded message
        embed = discord.Embed(description = "Choose rock 🗿, paper 📄, or scissors ✂!", colour = author.colour,)
        embed.set_footer(text=bot+' by ian#4359')
        embed.set_author(name="Rock Paper Scissors")

        # Initial message
        msg = await self.client.say(embed=embed)
        await self.client.add_reaction(msg, '🗿')
        await self.client.add_reaction(msg, '📄')
        await self.client.add_reaction(msg, '✂')

        # AI choice
        aiChoice = random.randint(1, 3)
        choiceList = {1: '🗿', 2: '📄', 3: '✂'}

        # Wait for choice
        choice = await self.client.wait_for_reaction(message=msg, check=check, user=author)

        #Player choice
        if ("{0.emoji}".format(choice.reaction)) == "🗿": playerChoice = 1
        if ("{0.emoji}".format(choice.reaction)) == "📄": playerChoice = 2
        if ("{0.emoji}".format(choice.reaction)) == "✂": playerChoice = 3

        # Check for win
        if playerChoice is 1 and aiChoice is 3 or playerChoice is 2 and aiChoice is 1 or playerChoice is 3 and aiChoice is 2:
            embed = discord.Embed(description="{0} beats {1}".format(choiceList[playerChoice], choiceList[aiChoice]), colour = discord.Colour.green())
            embed.set_footer(text=bot+' by ian#4359')
            embed.set_author(name="{0.name} Wins".format(author).title())
            await self.client.edit_message(msg, embed=embed)
        # Tie
        elif playerChoice == aiChoice:
            embed = discord.Embed(description="You both chose {0}".format(choiceList[playerChoice]), colour = discord.Colour.blue())
            embed.set_footer(text=bot+' by ian#4359')
            embed.set_author(name="{0.name} Tied".format(author).title())
            await self.client.edit_message(msg, embed=embed)
        # Player loses
        else:
            embed = discord.Embed(description="{0} beats {1}".format(choiceList[aiChoice], choiceList[playerChoice]), colour = discord.Colour.red())
            embed.set_footer(text=bot+' by ian#4359')
            embed.set_author(name="{0.name} Loses".format(author).title())
            await self.client.edit_message(msg, embed=embed)


    # Coin flipper
    @commands.command(pass_context=True)
    async def coin(self, ctx):
    	author = ctx.message.author
    	bot = self.client.user.name
    	coin = random.randint(1, 2)

    	embed = discord.Embed(
    		description = "Heads 🔴, or tails 🔵?",
    		colour = author.colour,
    	)
    	embed.set_footer(text=bot+' by ian#4359')
    	embed.set_author(name="Coin Flip")

        # Send intitial message
    	msg = await self.client.say(embed=embed)
    	await self.client.add_reaction(msg, '🔴')
    	await self.client.add_reaction(msg, '🔵')

    	def check(reaction, author):
    		e = str(reaction.emoji)
    		return e.startswith(('🔴', '🔵'))

    	async def send_coin():
    		if(coin == 1):
    			embed = discord.Embed(
    				description = "**{0.user}** guessed {0.reaction.emoji}, it is 🔴!".format(res),
    				colour = discord.Colour.red(),
    			)
    			embed.set_footer(text=bot+' created by ian#4359')
    			embed.set_author(name="Coin Flip")

    			await self.client.edit_message(msg, embed=embed)
    		else:
    			embed = discord.Embed(
    				description = "**{0.user}** guessed {0.reaction.emoji}, it is 🔵!".format(res),
    				colour = discord.Colour.blue(),
    			)
    			embed.set_footer(text=bot+' created by ian#4359')
    			embed.set_author(name="Coin Flip")

    			await self.client.edit_message(msg, embed=embed)

    	res = await self.client.wait_for_reaction(message=msg, check=check, user=author)
    	await send_coin()

def setup(client):
    client.add_cog(Fun(client))
