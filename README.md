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
https://discord.com/oauth2/authorize?client_id=338421932426919936&scope=bot%20applications.commands&permissions=277025442816

Chumlee requires access to the following permissions:
- View Channels
- Send Messages
- Send Messages in Threads
- Embed Links
- Attach Files
- Use Application Commands

## Developing
### Requirements
- Python 3.9
- Firebase Realtime Database
- Docker (optional, can be used for deployment)

### Setup
1. Set up your working directory
2. Create a new Python virtual environment
3. Install the dependencies in `requirements.txt`
4. Obtain your [Firebase service account credentials](https://firebase.google.com/docs/admin/setup#initialize-sdk) and place the JSON file in the project directory
5. Configure the following environment variables
```sh
BOT_TOKEN=<a Discord app bot token>
GOOGLE_APPLICATION_CREDENTIALS=<path to your Firebase credentials JSON file>
DB_ROOT=<the root path of your database, useful for having different paths for dev and prod>
DB_AUTH_UID=<a uid to authorize Firebase requests, set up in your Firebase auth rules>
LOGLEVEL=<logging level>
```
6. Start the bot and invite it to a server for testing

### Setup With Docker
1. Obtain your [Firebase service account credentials](https://firebase.google.com/docs/admin/setup#initialize-sdk) and place the JSON file in the project directory
2. Create a `.env` file with the environment variables listed in the section above
3. Build and tag the image: `docker build -t chumlee-bot:latest .`
4. Run the image, passing in your `.env` file and mounting the directory with the Firebase credentials file to the path you specified in `GOOGLE_APPLICATION_CREDENTIALS`:  
`docker run --env-file .env -v /path/to/creds/dir:${GOOGLE_APPLICATION_CREDENTIALS} chumlee-bot:latest`  
Note: Docker requires absolute paths when mounting volumes

## Contributing
If you for some reason want to contribute to this silly thing feel free to fork it and open a PR!