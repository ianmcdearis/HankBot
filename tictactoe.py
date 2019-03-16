import discord
from discord.ext import commands

import random

# TODO:
# 1. MAKE WIN METHODS
# 2. MAKE SO PLAYERS CAN ONLY PLAY ON GOING GAME
# 3. FIX SWITCHING BETWEEN PLAYERS

class tictactoe:
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def ttt(self, ctx, member):
        author = ctx.message.author
        bot = self.client.user.name

        if author:
            pass
        # Make embedded message
        def make_embed(player, game_map):
            embed = discord.Embed(
                description = make_board(game_map),
                title = "{0.name} vs {1}".format(author, member),
                colour = discord.Colour.green(),
            )
            embed.set_footer(text=bot+' by ian#4359')
            embed.set_author(name="Tic Tac Toe")
            return embed

        # Make the board
        def make_board(game_map):
            board = [':one:', ':two:', ':three:',
            ':four:', ':five:', ':six:',
            ':seven:', ':eight:', ':nine:']

            count = 0
            output = ''
            for row in range(3):
                for column in range(3):
                    output += str(game_map[count]).replace("0", str(board[count])).replace("1", ":o:").replace("2", ":x:")
                    count += 1
                output += '\n'
            return output

        game_map = [0, 0, 0,
                    0, 0, 0,
                    0, 0, 0]

        # Choose first player
        players = [author, member]
        player = random.choice(players)

        # Send intitial message
        await self.client.say("{0} goes first!".format(player))
        msg = await self.client.say(embed=make_embed(player, game_map))

        game_end = False
        while not game_end:
            for player in (1, 2):
                place = await self.client.wait_for_message(author=author)
                if place.content == "end" or place.content == "stop":
                    game_end = True
                try:
                    game_map[int(place.content)-1] = player
                    await self.client.delete_message(place)
                    await self.client.edit_message(msg, embed=make_embed(player, game_map))
                except IndexError:
                    pass
                except ValueError:
                    pass

def setup(client):
    client.add_cog(tictactoe(client))
