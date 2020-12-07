# Chumlee Bot
Inspired by History's _[Pawn Stars](https://en.wikipedia.org/wiki/Pawn_Stars)_ and dathings1's 
_[Prawn Srars](https://www.youtube.com/watch?v=5mEJbX5pio8)_, Chumlee Bot is a Discord bot that your guild members
can "sell" items like text and media attachments to in exchange for Chumcoins. As users earn more Chumcoins, they
can level up and trade in those coins for exclusive Chummedals to be displayed on their profile.

Under the hood Chumlee is really just a random number generator that will make a random offer when asked to. The fun
comes from what your guild's users offer him and how he responds, as well as some other small features and little
easter eggs. The goal isn't a real functioning economy, but rather some good comedy.

## Adding Chumlee Bot to Your Server
Chumlee Bot isn't currently publicly available. Keep an eye on this repo for updates, or go ahead and deploy your own fork!

## Developing
### Requirements
- Python 3.9
- Firebase Realtime Database
- Docker (optional, can be used for deployment)

### Setup
1. Set up your working directory
2. Create a new Python virtual environment
3. Install the dependencies in `requirements.txt`
4. Configure the following environment variables
```sh
GOOGLE_APPLICATION_CREDENTIALS=<path to a JSON file containing your Firebase service account credentials>
DB_ROOT=<the root path of your database, useful for having different paths for dev and prod>
DB_AUTH_UID=<a uid to authorize Firebase requests, set up in your Firebase auth rules>
BOT_TOKEN=<a Discord app bot token>
LOGLEVEL=<logging level>
```
5. Start the bot and invite it to a server for testing

## Contributing
If you for some reason want to contribute to this silly thing feel free to fork it and open a PR!