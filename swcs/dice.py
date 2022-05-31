from discord import Webhook, AsyncWebhookAdapter # Importing discord.Webhook and discord.AsyncWebhookAdapter
from django.conf import settings
from collections import Counter
import aiohttp
import asyncio 
import random
import platform

DICE = {
    "b": (
        {"face": ['b']},
        {"face": ['b']},
        {"advantage": 2, "face": ['a\na']},
        {"advantage": 1, "face": ['a']},
        {"advantage": 1, "success": 1, "face": ['a\ns']},
        {"success": 1, "face": ['s']}
    ),
    "s": (
        {"face": ['']},
        {"face": ['']},
        {"advantage": -2, "face": ['t\nt']},
        {"advantage": -1, "face": ['t']},
        {"advantage": -1, "success": -1, "face": ['t\nf']},
        {"success": -1, "face": ['f']}
    ),
    "a": (
        {"face": ['']},
        {"success": 1, "face": ['s']},
        {"success": 1, "face": ['s']},
        {"success": 2, "face": ['s\ns']},
        {"advantage": 1, "face": ['a']},
        {"advantage": 1, "face": ['a']},
        {"advantage": 1, "success": 1, "face": ['a\ns']},
        {"advantage": 2, "face": ['a\na']}
    ),
    "d": (
        {"face": ['']},
        {"success": -1, "face": ['f']},
        {"success": -2, "face": ['f\nf']},
        {"advantage": -1, "face": ['t']},
        {"advantage": -1, "face": ['t']},
        {"advantage": -1, "face": ['t']},
        {"advantage": -2, "face": ['t\nt']},
        {"advantage": -1, "success": -1, "face": ['t\nf']}
    ),
    "p": (
        {"face": ['']},
        {"success": 1, "face": ['s']},
        {"success": 1, "face": ['s']},
        {"success": 2, "face": ['s\ns']},
        {"success": 2, "face": ['s\ns']},
        {"advantage": 1, "face": ['a']},
        {"advantage": 1, "success": 1, "face": ['a']},
        {"advantage": 1, "success": 1, "face": ['a\ns']},
        {"advantage": 1, "success": 1, "face": ['a\ns']},
        {"advantage": 2, "face": ['a\na']},
        {"advantage": 2, "face": ['a\na']},
        {"success": 1, "triumph": 1, "face": ['r']}
    ),
    "c": (
        {"face": ['']},
        {"success": -1, "face": ['f']},
        {"success": -1, "face": ['f']},
        {"success": -2, "face": ['f\nf']},
        {"success": -2, "face": ['f\nf']},
        {"advantage": -1, "face": ['t']},
        {"advantage": -1, "face": ['t']},
        {"advantage": -1, "success": -1, "face": ['t\nf']},
        {"advantage": -1, "success": -1, "face": ['t\nf']},
        {"advantage": -2, "face": ['t\nt']},
        {"advantage": -2, "face": ['t\nt']},
        {"success": -1, "despair": 1, "face": ['e']}
    ),
    "f": (
        {"dark": 1, "face": ['z']},
        {"dark": 1, "face": ['z']},
        {"dark": 1, "face": ['z']},
        {"dark": 1, "face": ['z']},
        {"dark": 1, "face": ['z']},
        {"dark": 1, "face": ['z']},
        {"dark": 2, "face": ['z\nz']},
        {"light": 1, "face": ['Z']},
        {"light": 1, "face": ['Z']},
        {"light": 2, "face": ['Z\nZ']},
        {"light": 2, "face": ['Z\nZ']},
        {"light": 2, "face": ['Z\nZ']}
    )
}

REMAP = {
    "success": "failure",
    "advantage": "threat"
}


def roller(pool):
    roll = Counter()
    [roll.update(rolled) for rolled in [random.choice(DICE[die]) for die in pool]]
    roll["face"] = roll["face"][::-1]
    # newroll = {}
    # for key in roll:
    #     if roll[key] > 0 or key == 'face':
    #         newroll[key] = roll[key]
    #         continue
    #     if roll[key]==0:
    #         continue
    #     roll[REMAP[key]] = abs(roll[key])
    roll = {key: value for key, value in roll.items() if value != 0}
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # asyncio.run(sendToDiscord(roll))
    # threading.Thread(target=sendToDiscord, args=(roll)).start()
    return roll

async def sendToDiscord(roll):
  async with aiohttp.ClientSession() as session:  
    webhook = Webhook.from_url(settings.DISCORD_WEB_HOOK_URL, adapter=AsyncWebhookAdapter(session)) # Initializing webhook with AsyncWebhookAdapter
    await webhook.send(content=roll) 

# def sendToDiscord(roll):
#     hook = Webhook.from_url('', adapter=RequestsWebhookAdapter()) # Initializing webhook
#     hook.send(content=json.dumps(roll))