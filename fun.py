import discord
from discord.ext import commands

import random
import re

class Fun:
    def __init__(self, client):
        self.client = client

    # Say message then delete author message
    @commands.command(pass_context=True, no_pm=True)
    async def say(self, ctx, *, words):
        await self.client.delete_message(ctx.message)
        await self.client.say(words)

    # Random dick size
    @commands.command(pass_context=True)
    async def dick(self, ctx):
        author = ctx.message.author
        size = random.randint(1, 15)

        # Make dick
        output = '8'
        for i in range(size):
            output += '='
        output += 'D'

        # Hard or soft
        flaccidity = ['hard :eggplant:', 'soft :banana:']
        hard_or_soft = random.choice(flaccidity)

        await self.client.say("**{0.mention}** has a ".format(author) + str(size) + " inch dick " + hard_or_soft + " " + output)

    # Rock Paper Scissors       1 == Rock   2 == Paper  3 = Scissors
    @commands.command(pass_context=True)
    async def rps(self, ctx):
        aiChoice = 0
        playerChoice = 0

        author = ctx.message.author
        bot = self.client.user.name

        # Check for emojis
        def check(reaction, author):
            e = str(reaction.emoji)
            return e.startswith(('🗿', '📄', '✂'))

        # AI choice
        aiChoice = random.randint(1, 3)
        choiceList = {1: '🗿', 2: '📄', 3: '✂'}

        # Create embedded message
        embed = discord.Embed(description = "Choose rock 🗿, paper 📄, or scissors ✂!", colour = discord.Colour.gold())
        embed.set_footer(text=bot+' by ian#4359')
        embed.set_author(name="Rock Paper Scissors")

        # Initial message
        msg = await self.client.say(embed=embed)
        for emoji in choiceList:
            await self.client.add_reaction(msg, choiceList[emoji])

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

        # Coin variables
        coins = {1: '🔴', 2:'🔵'}
        aiChoice = random.randint(1, 2)

        # Create embed
        embed = discord.Embed(description = "Heads 🔴 or tails 🔵?", colour = discord.Colour.blue())
        embed.set_footer(text=bot+' by ian#4359')
        embed.set_author(name="Coin Toss")

        # Send initial message
        msg = await self.client.say(embed=embed)
        for emoji in coins:
            await self.client.add_reaction(msg, coins[emoji])

        # Check for emojis
        def check(reaction, author):
            e = str(reaction.emoji)
            return e.startswith(('🔴', '🔵'))

        # Wait for player choice
        choice = await self.client.wait_for_reaction(message=msg, check=check, user=author)

        if ("{0.emoji}".format(choice.reaction)) == "🔴": playerChoice = 1
        if ("{0.emoji}".format(choice.reaction)) == "🔵": playerChoice = 2

        # Guessed right
        if playerChoice is 1 and aiChoice is 1 or playerChoice is 2 and aiChoice is 2:
            embed = discord.Embed(description = "Lucky ass rng, you're right, it's {0}".format(coins[playerChoice]), colour = discord.Colour.green())
            embed.set_footer(text=bot+' by ian#4359')
            embed.set_author(name="You won!")
            await self.client.edit_message(msg, embed=embed)
        # Guessed wrong
        else:
            embed = discord.Embed(description = "lol nice rng idiot, you lost, it's {0}".format(coins[aiChoice]), colour = discord.Colour.red())
            embed.set_footer(text=bot+' by ian#4359')
            embed.set_author(name="You lost..")
            await self.client.edit_message(msg, embed=embed)

    # Random number generator
    @commands.command(pass_context=True)
    async def random(self, ctx, *args):
        try:
            # Get rangeOfNumbers from *args
            rangeOfNumbers = ''
            for word in args:
                rangeOfNumbers += word + ' '

            # Parse rangeOfNumbers into array
            numbers = re.split(r"\s|-|-\s", rangeOfNumbers.strip())

            # Between 2 given numbers (E.g. 50-100)
            if(len(numbers) == 2):
                left = int(numbers[0])
                right = int(numbers[1])
                if left > right:
                    await self.client.say("Number generated from ({0}-{1}): **{2:0{len}d}**".format( right, left, random.randint(right, left), len = len(str(left)) ))
                else:
                    await self.client.say("Number generated from ({0}-{1}): **{2:0{len}d}**".format( left, right, random.randint(left, right), len = len(str(right)) ))

            # Between 0 and rangeOfNumbers (E.g. 0-10)
            elif(len(numbers) == 1):
                await self.client.say("Number generated from (0-{0}): **{1:0{len}d}**".format( rangeOfNumbers.strip(), random.randint(0, int(rangeOfNumbers)), len = len(str(rangeOfNumbers))-1 ))

            # Too much arguments
            else:
                await self.client.say("Too many arguments :confused: ")
        except ValueError:
            await self.client.say("Has to be a number Bobby.")

def setup(client):
    client.add_cog(Fun(client))
