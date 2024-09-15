# Chumlee Bot
Inspired by History's _[Pawn Stars](https://en.wikipedia.org/wiki/Pawn_Stars)_ and DaThings's 
_[Prawn Srars](https://www.youtube.com/watch?v=5mEJbX5pio8)_, Chumlee Bot is a Discord bot that your guild members
can "sell" items like text and media attachments to in exchange for Chumcoins. As users earn more Chumcoins, they
can level up and trade in those coins for exclusive Chummedals to be displayed on their profile.

Under the hood Chumlee is really just a random number generator that will make a random offer when asked to. The fun
comes from what your guild's users offer him and how he responds, as well as some other small features and little
easter eggs. The goal isn't a real functioning economy, but rather some good comedy.

## Adding Chumlee Bot to Your Server
I make no guarantees about service quality or uptime, since this is a self-hosted project.

Invite the bot with this link:  
https://discord.com/oauth2/authorize?client_id=338421932426919936

## Development
Chumlee Bot uses Python with Poetry for dependency management, and Google Firebase as a database.

- Clone the project
- Install dependenices with `poetry install`
- Obtain your [Firebase service account credentials](https://firebase.google.com/docs/admin/setup#initialize-sdk). Name the file `db-creds.json` and place it in the `config` directory of the project.
- Set the following environment variables with your development values:
```
BOT_TOKEN=<a Discord app bot token>
GOOGLE_APPLICATION_CREDENTIALS=/app/config/db-creds.json
DB_ROOT=<the root path of your database, useful for having different paths for dev and prod>
DB_AUTH_UID=<a uid to authorize Firebase requests, set up in your Firebase auth rules>
LOGLEVEL=<logging level>
DEBUG_GUILD_IDS=[list of Discord guild IDs to create slash commands in for dev purposes]
```
- Start the bot with `poetry run python src/bot.py`

## Deployment
- Create a `.env` file with the same variables as above set to your production values
- Build and tag the image: `docker build -t chumlee-bot:latest .`
- Run the image, passing in your `.env` file and mounting the directory with the Firebase credentials file to the path you specified in `GOOGLE_APPLICATION_CREDENTIALS`:  
`docker run --env-file .env -v /path/to/creds/dir:${GOOGLE_APPLICATION_CREDENTIALS} chumlee-bot:latest` 

## Contributing
If you for some reason want to contribute to this silly thing feel free to fork it and open a PR!