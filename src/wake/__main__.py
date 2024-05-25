"""
TO INSTALL:

pip install py-cord
pip install translate

"""
import os, sys, discord, logging
from discord.ext import commands
# from cogs.core.server_settings import Settings

COGS_ROOT_PATH = os.path.join(os.path.dirname(__file__), "cogs")

logger = logging.getLogger(__name__)
prefix = '~'
intents = discord.Intents.all()

# This sets the prefix to use for commands. 
bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix),
                   intents=intents)

# async def traceback(ctx, e):
#     print(f'{e}')
#     embed = discord.Embed(
#         title='Traceback (most recent call):',
#         description=f'```{e}```',
#         color=0xea623b)
#     embed.set_image(url='https://media.tenor.com/zpvRLlcI5mEAAAAC/anime_blush_error_moan.gif')
#     await ctx.send(embed=embed, delete_after=10)

@bot.event
async def on_ready():
    print(f'{bot.user} [{bot.user.id}] is connected to the following guilds:')
    for guild in bot.guilds:
        print(f'\t- {guild.name}(id: {guild.id})')

# In this function, we load all the files from the Cogs folder.
# Cogs are just files that hold our commands.
def load_cogs():
    """
    Loads the directories under the /cogs/ folder,
    then digs through those directories and loads the cogs.
    """
    print("Loading Cogs...")
    failed_to_load = []
    # for directory in os.listdir(COGS_ROOT_PATH):
    #     if directory.startswith("_"):
    #         print(f"Skipping {directory} as it is a hidden directory.")
    #         continue
    #     if directory.startswith("debug") and not logger.level == logging.DEBUG:
    #         print(f"Skipping {directory} as it is not the debug cog.")
    #         continue

    # cog_subdir_path = os.path.join(COGS_ROOT_PATH, directory)
    for file in os.listdir(COGS_ROOT_PATH):
        if file.endswith(".py") and not file.startswith("_"):
            # try:
            cog_path = os.path.join(COGS_ROOT_PATH, file)
            # print(f"Loading Cog: {cog_path}")
            try:
                if len(sys.argv) > 1:
                    bot.load_extension(f"cogs.{file[:-3]}")
                else:
                    bot.load_extension(f"wake.cogs.{file[:-3]}")
                print(f"Loaded Cog: {cog_path}")
            except Exception as e:
                logger.warning("Failed to load: {%s}.{%s}, {%s}", COGS_ROOT_PATH, file, e)
                failed_to_load.append(f"{file[:-3]}")
    if failed_to_load:
        logger.warning(f"Cog loading finished. Failed to load the following cogs: {', '.join(failed_to_load)}")
    else:
        print("Loaded all cogs successfully.")

# In this function, we use an argument or env file to load the Bot-Token.
def load_token_and_run():
    # server_settings_path = './resources'
    # if server_settings_path:
    #     bot.server_settings = Settings(server_settings_path)  # type: ignore
    if len(sys.argv) > 1:
        TOKEN = sys.argv[1]
        bot.run(TOKEN)
    else:
        bot.run(os.getenv("DISCORD_TOKEN"))

def main():
    load_cogs()
    load_token_and_run()

if __name__ == '__main__':
    main()
