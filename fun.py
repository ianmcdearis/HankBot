import discord
from discord.ext import commands

import random

class Fun:
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def echo(self, *args):
        output = ''
        for word in args:
            output += word
            output += ' '
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

    @commands.command(pass_context=True)
    async def ttt(self, ctx, member):

        async def win(current_game):

            # Horizontal winner
            for row in game:
                if row.count(row[0]) == len(row) and row[0] != 0:
                    await self.client.say("Player {0} has won horizontally!".format(row[0]))

            # Vertical winner
            for col in range(len(game)):
                check = []

                for row in game:
                    check.append(row[col])

                if check.count(check[0]) == len(check) and check[0] != 0:
                    await self.client.say("Player {0} has won vertically!".format(check[0]))

            # Diagonal winner
            diags = []
            for col, row in enumerate(reversed(range(len(game)))):
                diags.append(game[row][col])
            if diags.count(diags[0]) == len(diags) and diags[0] != 0:
                await self.client.say("Player {0} has won diagonally (/)!".format(diags[0]))

            diags = []
            for ix in range(len(game)):
                diags.append(game[ix][ix])
            if diags.count(diags[0]) == len(diags) and diags[0] != 0:
                await self.client.say("Player {0} has won diagonally (\\)!".format(diags[0]))

        # Update game board
        async def game_board(game_map, player=0, row=0, column=0, just_display=False):
            emojis = [':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:']
            try:
                if not just_display:
                    game_map[row][column] = player
                output = ''
                count = 0
                for row in game_map:
                    for val in row:
                        output += str(val).replace('0', emojis[count]).replace('1', ':x:').replace('2', ':o:')
                        count += 1
                    output += '\n'
                await self.client.say(output)
                return game_map
            except IndexError as e:
                print(e)
            except Exception as e:
                print(e)

        author = ctx.message.author

        game_won = False
        game_map = [[0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],]

        game = self.client.say(await game_board(game_map, just_display=True))

        while not game_won:

            for player in (1, 2):
                if(player == 1):
                    current_player = author
                else:
                    current_player = author

                # Get row and turn into integer
                row_place = await self.client.wait_for_message(author=current_player)
                row = int(row_place.content)-1
                await self.client.delete_message(row_place)

                # Get column and turn into integer
                col_place = await self.client.wait_for_message(author=current_player)
                col = int(col_place.content)-1
                await self.client.delete_message(col_place)

                # Update game map and display
                await game_board(game_map, player=player, row=row, column=col, just_display=False)
                await self.client.edit_message(game, new_content=await game_board(game_map, just_display=True))

    @commands.command(pass_context=True)
    async def tictactoe(self, ctx, member):

        # Initialize variables
        author = ctx.message.author
        bot = self.client.user.name
        player = author

        # Create board 1-9
        board = [':one:', ':two:', ':three:',
        ':four:', ':five:', ':six:',
        ':seven:', ':eight:', ':nine:']

        # Determine the winner
        def win(board):
            count = 0
            match = False
            for row in range(3):
                for column in range(3):
                    count += 1
                match = True
            return match

        # Make the board look pretty
        def make_board(board):
            output = ''
            count = 0
            for row in range(3):
                for column in range(3):
                    output += board[count]
                    count += 1
                output += '\n'
            return output

        # Randomly choose first player to go
        first = random.randint(1, 2)
        if first == 1:
            player = author
            print("{0.mention} goes first!".format(player))
            await self.client.say("{0.mention} goes first!".format(player))
        else:
            player = member
            print("{0} goes first!".format(player))
            await self.client.say("{0} goes first!".format(player))

        # Make embedded message
        def make_embed(player):
            embed = discord.Embed(
                description = make_board(board),
                colour = discord.Colour.green(),
            )
            embed.set_footer(text=bot+' by ian#4359')
            embed.set_author(name="Tic Tac Toe")
            return embed

        # Send intitial message
        msg = await self.client.say(embed=make_embed(player))

        # Make turn function
        async def turn():
            place = await self.client.wait_for_message(author=player)
            await self.client.delete_message(place)
            try:
                board[int(place.content)-1] = ':x:'
            except IndexError as e:
                await turn()
            except ValueError as e:
                await turn()
            await self.client.edit_message(msg, embed=make_embed(player))

        while not win(board):
            await turn()

        # Announce winner
        await self.client.say("{0} has won the game!".format(player))

def setup(client):
    client.add_cog(Fun(client))
