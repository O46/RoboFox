import random
import discord
import praw
import os
from environs import Env
from discord.ext import commands, tasks
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

for val in ['reddit_client_id', 'reddit_client_secret', 'reddit_user_agent', 'discord_bot_token', 'discord_channel_id', 'subreddit_name']:
    if not os.getenv(val):
        print(f"OS.GetEnv({val}): {os.getenv(val)}")
        os.environ[val] = input(f"Enter value for var {val}: ")
    print(f"OS.GetEnv({val}): {os.getenv(val)}")
    globals()[val] = os.environ[val]

reddit = praw.Reddit(client_id=reddit_client_id, client_secret=reddit_client_secret, user_agent=reddit_user_agent)
bot = commands.Bot(command_prefix='!', intents=intents)
subreddit_name = subreddit_name
env = Env()
env.read_env()
orangeboys = env.list("GITHUB_REPOS", [])
first_run = True


@tasks.loop(seconds=600)
async def check_reddit():
    channel = (bot.get_channel(discord_channel_id) or await bot.fetch_channel(discord_channel_id))
    print(type(channel))
    subreddit = reddit.subreddit(subreddit_name)
    for submission in subreddit.new(limit=5):
        print(f"Submission permalink: {submission.permalink}\nSubmission ID: {submission.id}\nSubmission URL: {submission.url}\nSubmission Title: {submission.title}\nSubmission Stickied: {submission.stickied}\nIs Video: {submission.is_video}\n\n")
        if not submission.stickied:
            if submission.id not in orangeboys:
                title = submission.title
                # if submission.url.endswith(".jpg") or submission.url.endswith(".jpeg"): # https://preview.redd.it/dqlbtyz00iec1.jpg?
                #    image_url = submission.url
                # el
                if submission.is_video:
                    image_url = "https://www.rxddit.com" + submission.permalink
                else:
                    image_url = submission.url
                # else:
                message = f"**{title}**\n{image_url}"
                await channel.send(message)
                orangeboys.append(submission.id)
                break


@tasks.loop(seconds=300)
async def hes_at_it_again(): #(passCheck=True):
    global first_run
    if first_run:
        print("Passing first run")
        first_run = False
        return
    #if not passCheck:
    #    print("Passing first run")
    #    return
    channel = bot.get_channel(discord_channel_id)
    message = f"He’s At it Again!\nhttps://i.redd.it/cm5b0n9jwhec1.jpeg"
    await channel.send(message)
    hes_at_it_again.change_interval(seconds=random.randint(1500, 172800))
    print(f"Changed interval to {hes_at_it_again.change_interval}")


async def on_message(message):
    if message.content.tolower() == "meow":
        await message.add_reaction('🐱')


@bot.event
async def on_ready():
    hes_at_it_again.start()
    check_reddit.start()

bot.run(discord_bot_token)
