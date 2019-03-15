import discord
from discord.ext import commands

import random

class TicTacToe:
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def ttt(self, ctx):
        board = [[0, 0, 0],
                 [0, 0, 0],
                 [0, 0, 0]]

        output = ''
        for row in board:
            for column in row:
                output += column
            output += '\n'

        await self.client.say(output)

def setup(client):
    client.add_cog(TicTacToe(client))
