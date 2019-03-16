import discord
from discord.ext import commands

import random

import simpleeval
from simpleeval import simple_eval

import ast
import operator

import traceback

class Evaluate:
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def math(self, *args):
        try:
            bot = self.client.user.name

            # Add every word after #math to input variable
            input = ''
            for word in args:
                input += word
                input += ' '

            # Evaluate using simple_eval python library
            answer = simple_eval(input)

            formula = input.replace("**", " ^ ")
            embed = discord.Embed(
                description = "{} = **{}**".format(formula, answer),
                colour = discord.Colour.blue(),
                title = "Math",
                url = "https://github.com/danthedeckie/simpleeval#operators"
            )
            embed.set_footer(text=bot+' created by ian#4359')

            await self.client.say(embed=embed)
        except Exception as e:
            await self.client.say("what")
            traceback.print_exception(type(e), e, e.__traceback__)


def setup(client):
    client.add_cog(Evaluate(client))
