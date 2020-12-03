from .config import db, db_root


def add_allowed_channel(guild_id: str, channel_id: str):
    db.reference(f"{db_root}/guilds/{guild_id}/allowedChannels/{channel_id}").set(True)


def remove_allowed_channel(guild_id: str, channel_id: str):
    db.reference(f"{db_root}/guilds/{guild_id}/allowedChannels/{channel_id}").delete()


def get_allowed_channels(guild_id: str):
    return db.reference(f"{db_root}/guilds/{guild_id}/allowedChannels").get()
