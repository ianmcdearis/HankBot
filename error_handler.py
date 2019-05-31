import discord
from discord.ext import commands

import math
import traceback
import sys
import inspect

class error_handler(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def on_command_error(self, error: Exception, ctx: commands.Context):
        # The event triggered when an error is raised while invoking a command.
        # ctx   : Context
        # error : Exception

        def func(a, b, c):
            pass

        if hasattr(ctx.command, 'on_error'):
            await self.client.send_message(ctx.message.channel, 'Sorry, an error occured.')
            return

        error = getattr(error, 'original', error)

        if isinstance(error, commands.CommandNotFound):
            await self.client.send_message(ctx.message.channel, "URG! That command doesn't even exist. :rage:")
            return

        elif isinstance(error, commands.CommandOnCooldown):
            await self.client.send_message(ctx.message.channel, 'Stop spamming "#{0}", I\'m selling propane. (Wait {1:.2f}s)'.format(ctx.command, error.retry_after))
            return

        elif isinstance(error, commands.DisabledCommand):
            await self.client.send_message(ctx.message.channel, 'The {} command has been disabled, fucking vegetable. :wheelchair:'.format(ctx.command))
            return

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await self.client.send_message(ctx.message.author, ':point_left: Get the {} command out of my DMs...'.format(ctx.command))
                return
            except discord.Forbidden:
                pass

        elif isinstance(error, commands.BadArgument):
            await self.client.send_message(ctx.message.channel, 'Bad argument, try again.')
            return

        elif isinstance(error, commands.MissingRequiredArgument):
            await self.client.send_message(ctx.message.channel, 'Missing required arguments! Try again!')
            return

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(client):
    client.add_cog(error_handler(client))
