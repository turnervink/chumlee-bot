import re
import time

import dbfunctions

dealcooldown = 900

def is_valid_userid(id):
    return re.match("<@!?[0-9]*>", id)

def in_cooldown_period(id):
    now = int(time.time())
    lastdeal = dbfunctions.last_deal_time(id)

    return (now - lastdeal) >= dealcooldown
