import discord
from discord.ext import commands

import random

#
# FIX PROBLEM WITH LOOP GOING THROUGH A SECOND TIME AFTER THINGS ARE DONE
# MAKE SO YOU CAN PLAY ON OTHER SERVER
# DONT TRANSFER DATA ACROSS SERVERS
#

playerList = {}
playerIcon = {}
inProgress = False

class tictactoe:
    def __init__(self, client):
        self.client = client

    @commands.group(pass_context=True, no_pm=True)
    async def ttt(self, ctx):

        # Send message with commands if a subcommand is not called
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                description = "#ttt [start (mention)] | [end]",
                colour = discord.Colour.green(),
            )
            embed.set_footer(text=self.client.user.name+' by ian#4359')
            embed.set_author(name="Tic Tac Toe")
            await self.client.say(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.channel)
    @ttt.command(pass_context=True)
    async def end(self, ctx):
        global inProgress, playerList, playerIcon

        author = ctx.message.author

        # Author in ongoing game
        if inProgress and author in playerList.values():
            # End game if author is playing
            inProgress = False
            await self.client.say("{0.mention} has ended the game.".format(author))
        # Author NOT in ongoing game
        elif inProgress and author not in playerList.values():
            await self.client.say("You can't end someone else's game.")
        # No ongoing game
        else:
            await self.client.say("There isn't a game going on.")

    @commands.cooldown(1, 5, commands.BucketType.channel)
    @ttt.command(pass_context=True)
    async def start(self, ctx, player2: discord.Member):

        # Make the board
        def make_board(game_map):
            board = [':one:',':two:',':three:',
                     ':four:',':five:',':six:',
                     ':seven:',':eight:',':nine:']
            count = 0
            output = ''
            for row in range(3):
                for column in range(3):
                    output += str(game_map[count]).replace("0", str(board[count])).replace("1", ":o:").replace("2", ":x:")
                    count += 1
                output += '\n'
            return output

        # Checks if place is valid
        def check(message):
            global inProgress
            if inProgress:
                onBoard = False
                choice = message.content
                for place in range(1, 9):
                    # Use "==" instead of "is"
                    # Choice is a object
                    if choice == str(place):
                        onBoard = True
                if onBoard and game_map[int(choice)-1] is 0:
                    game_map[int(choice)-1] = player
                    return True
                else:
                    return False

        global inProgress, playerList, playerIcon

        channel = ctx.message.channel

        if inProgress:
            await self.client.send_message(channel, "There is a game in progress between {0.mention} and {1.mention}, wait or go to a new channel.".format(playerList[1], playerList[2]))
        else:
            author = ctx.message.author
            bot = self.client.user.name


            # Checks if player mentioned is bot or himself
            if player2.bot or player2 is author:
                await self.client.send_message(channel, "You can't play with yourself or a bot.")
                inProgress = False

            # Player is valid to play against
            else:
                inProgress = True
                game_map = [0]*9

                # Choose first player
                firstPlayer = random.randint(1, 2)  # Random number between 1 and 2
                if firstPlayer == 2:
                    playerList = {1: player2, 2: author}    # Player 2 goes first
                else:
                    playerList = {1: author, 2: player2}    # Author goes first

                playerIcon = {1: ":o:", 2: ":x:"}

            # Iterates through player 1 and 2 while game is in progress
            while inProgress:
                for player in (1, 2):
                    # Break out of for loop if inProgress is false
                    if inProgress is False:
                        break

                    # Wait for place message, game ends after 30 seconds of no message
                    turn = await self.client.send_message(channel, f"{playerList[player].mention} its your turn ({playerIcon[player]})!")
                    msg = await self.client.send_message(channel, make_board(game_map))
                    place = await self.client.wait_for_message(timeout = 30, check=check, author=playerList[player], channel=ctx.message.channel)

                    if place:
                        # Place
                        game_map[int(place.content)-1] = player
                        await self.client.delete_messages((place, turn, msg))
                    # AFK
                    else:
                        inProgress = False
                        break
                        await self.client.send_message(channel, f"Game ended due to inactivity of {playerList[player].mention}...")

            inProgress = False

def setup(client):
    client.add_cog(tictactoe(client))
