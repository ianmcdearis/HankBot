import discord
from discord.ext import commands

import math
import traceback
import sys

class error_handler:
    def __init__(self, client):
        self.client = client

    async def on_command_error(self, error: Exception, ctx: commands.Context):
        # The event triggered when an error is raised while invoking a command.
        # ctx   : Context
        # error : Exception

        if hasattr(ctx.command, 'on_error'):
            await self.client.send_message(ctx.message.channel, 'Sorry, an error occured.')
            return

        ignored = (commands.UserInputError)
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.CommandNotFound):
            await self.client.send_message(ctx.message.channel, "URG! That command doesn't even exist. :rage:")
            return

        elif isinstance(error, commands.CommandOnCooldown):
            await self.client.send_message(ctx.message.channel, "I'm busy selling propane and propane accessories, please retry in {}s.".format(math.ceil(error.retry_after)))
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
            if ctx.command.qualified_name == 'tag list':
                await self.client.send_message(ctx.message.channel, 'I could not find that member. Please try again.')
                return

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(client):
    client.add_cog(error_handler(client))
