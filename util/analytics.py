import aiohttp

import logging

import os

ROOT_URL = "https://www.google-analytics.com"
VERSION = 1


class Analytics:
    def __init__(self):
        self.tracking_id = os.environ["GA_TID"]
        self.client_id = os.environ["GA_CID"]
        self.logger = logging.getLogger("chumlee-bot")

    async def send_event(self, category: str, action: str, value: int = None, label: str = None):
        params = {
            "v": VERSION,
            "tid": self.tracking_id,
            "cid": self.client_id,
            "t": "event",
            "ec": category,
            "ea": action
        }

        if value is not None:
            params["ev"] = value

        if label is not None:
            params["el"] = label

        async with aiohttp.ClientSession() as session:
            async with session.post(f"{ROOT_URL}/collect", params=params) as r:
                if r.status != 200:
                    logging.error("Could not send Google Analytics event: %s", r)
