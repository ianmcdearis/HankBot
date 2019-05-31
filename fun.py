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
        list = ['hard :eggplant:', 'soft :banana:']
        flaccidity = random.choice(list)

        await self.client.say("**{0.mention}** has a ".format(author) + str(size) + " inch dick " + flaccidity + " " + output)


    # Where you from? IM THE FROM THE 6IX YOU WASTEYUTE
    @commands.command(pass_context=True)
    async def wasteman(self, ctx):
        author = ctx.message.author
        salutations = ["yo", "ay"]
        people = ["shordy", "wasteyute", "ahlie", "cyattie", "gyal", "mandem", "ting", "mans", "bean", "fam", "sweetermenz", "bucktee", "my g", "kawhi", "danaya", f"{author.mention}"]
        adjectives = ["bare", "mad", "bad", "bored", "cheesed", "dry"]
        phrases = ["nyeahhhh", "don't cheese me", "that's wild", "i like nav", "drake can suck my cock", "scoop me", "copped", "hooooly", "flex", "llow it", "that's beat", "mans are marved"]

        sentences = [f"{random.choice(salutations)} {author.mention}, you're such a {random.choice(adjectives)} {random.choice(people)}",
        f"{random.choice(people)} {random.choice(phrases)} yo",
        f"{random.choice(salutations)}, {random.choice(phrases)} {random.choice(people)}, {random.choice(phrases)}",
        f"{random.choice(phrases)}, why am i such a {random.choice(adjectives)} {random.choice(people)} its crazy {random.choice(people)}",
        f"{random.choice(phrases)} i'm {random.choice(adjectives)} fam",
        f"{random.choice(phrases)} {random.choice(phrases)} {random.choice(salutations)}"]

        await self.client.say(random.choice(sentences))


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
        embed = discord.Embed(description = "Choose rock 🗿, paper 📄, or scissors ✂!", colour = discord.Colour.darker_grey())
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
        embed = discord.Embed(description = "Heads 🔴 or tails 🔵?", colour = discord.Colour.darker_grey())
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
    async def random(self, ctx, *, rangeOfNumbers):
        try:
            rangeOfNumbers = rangeOfNumbers.strip()

            # Parse rangeOfNumbers into array
            numbers = re.split(r"\s|-|-\s", rangeOfNumbers)

            # Between 2 given numbers (E.g. 50-100)
            if(len(numbers) == 2):
                left = int(numbers[0])
                right = int(numbers[1])
                if left > right:
                    await self.client.say(f"Number generated from ({right}-{left}): **{random.randint(right, left):0{len(str(left))}d}**")
                else:
                    await self.client.say(f"Number generated from ({left}-{right}): **{random.randint(left, right):0{len(str(right))}d}**")

            # Between 0 and rangeOfNumbers (E.g. 0-10)
            elif(len(numbers) == 1):
                await self.client.say(f"Number generated from (0-{rangeOfNumbers}): **{random.randint(0, int(rangeOfNumbers)):0{len(str(rangeOfNumbers))}d}**")

            # Too much arguments
            else:
                await self.client.say("Too many arguments :confused: ")
        except ValueError:
            await self.client.say("Has to be a number Bobby.")

def setup(client):
    client.add_cog(Fun(client))
