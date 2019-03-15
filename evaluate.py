import discord
from discord.ext import commands

import random

import simpleeval
from simpleeval import simple_eval

import ast
import operator

class Evaluate:
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def math(self, *args):
        try:
            bot = self.client.user.name

            input = ''
            for shit in args:
                input += shit
                input += ' '
            answer = simple_eval(input)

            formula = input.replace("**", " ^ ")
            embed = discord.Embed(
                description = "{} = **{}**".format(formula, answer),
                colour = discord.Colour.green(),
            )
            embed.set_footer(text=bot+' created by ian#4359')
            embed.set_author(name="Math")

            await self.client.say(embed=embed)
        except ValueError:
            await self.client.say("Sorry, those aren't numbers. :japanese_goblin:")
        except SyntaxError:
            await self.client.say("Check that statement again, cutie. :wink:")


def setup(client):
    client.add_cog(Evaluate(client))
