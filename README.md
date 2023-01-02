# mzbot-v2

MZ Bot v2 for Discord, built with Python!

**This repository is owned and actively maintained by XInTheDark (aka Muzhen Gaming).**

First created on 25 August 2021, the bot now has a huge variety of commands in a number of categories (e.g. utility,
moderation, message processing, entertainment, music, etc.)

*Note: This project has been made open source a while ago. The source code is now openly available to any interested
persons.
We welcome all pull requests and issues.*


### Running the bot:

Hosting MZ Bot is simple. Follow the below steps:

1. In the OS environment, add 2 values: `DISCORD_TOKEN` and `OPENAI_API_KEY`, 
for the [bot token](https://discord.com/developers/applications)
and [OpenAI API Key](https://beta.openai.com/account/api-keys) respectively.
*Note: If there isn't an option to add values to the environment, create a file named `.env` and put the values in that file.
2. Run `main.py`. As of discord.py 2.2.0, Python 3.8 or above is required. A working installation of pip is also required.
It is recommended that you run the code on a Unix-based environment that has npm or apt installed.
3. If you're hosting on [replit](https://www.replit.com), please read [notes_replit.md](notes_replit.md).


### Debugging

The console log should output most of the needed information. 

If you are encountering problems with installation of packages, please run the below commands in order:

```
pip install -U pip setuptools
pip install -r requirements.txt
```

If you are still facing other problems, you can open an Issue on GitHub where you will be assisted.