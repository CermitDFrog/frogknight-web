# Importing discord.Webhook and discord.AsyncWebhookAdapter
from discord import Webhook, AsyncWebhookAdapter
from django.conf import settings
from collections import Counter
import aiohttp
import asyncio
import random
import platform

DICE = {
    "b": (
        {"face": ['sw_b']},
        {"face": ['sw_b']},
        {"advantage": 2, "face": ['sw_baa']},
        {"advantage": 1, "face": ['sw_ba']},
        {"advantage": 1, "success": 1, "face": ['sw_bas']},
        {"success": 1, "face": ['sw_bs']}
    ),
    "s": (
        {"face": ['sw_s']},
        {"face": ['sw_s']},
        {"advantage": -2, "face": ['sw_stt']},
        {"advantage": -1, "face": ['sw_st']},
        {"advantage": -1, "success": -1, "face": ['sw_stf']},
        {"success": -1, "face": ['sw_sf']}
    ),
    "a": (
        {"face": ['sw_a']},
        {"success": 1, "face": ['sw_as']},
        {"success": 1, "face": ['sw_as']},
        {"success": 2, "face": ['sw_ass']},
        {"advantage": 1, "face": ['sw_aa']},
        {"advantage": 1, "face": ['sw_aa']},
        {"advantage": 1, "success": 1, "face": ['sw_aas']},
        {"advantage": 2, "face": ['sw_aaa']}
    ),
    "d": (
        {"face": ['sw_d']},
        {"success": -1, "face": ['sw_df']},
        {"success": -2, "face": ['sw_dff']},
        {"advantage": -1, "face": ['sw_dt']},
        {"advantage": -1, "face": ['sw_dt']},
        {"advantage": -1, "face": ['sw_dt']},
        {"advantage": -2, "face": ['sw_dtt']},
        {"advantage": -1, "success": -1, "face": ['sw_dtf']}
    ),
    "p": (
        {"face": ['sw_p']},
        {"success": 1, "face": ['sw_ps']},
        {"success": 1, "face": ['sw_ps']},
        {"success": 2, "face": ['sw_pss']},
        {"success": 2, "face": ['sw_pss']},
        {"advantage": 1, "face": ['sw_pa']},
        {"advantage": 1, "success": 1, "face": ['sw_pa']},
        {"advantage": 1, "success": 1, "face": ['sw_pas']},
        {"advantage": 1, "success": 1, "face": ['sw_pas']},
        {"advantage": 2, "face": ['sw_paa']},
        {"advantage": 2, "face": ['sw_paa']},
        {"success": 1, "triumph": 1, "face": ['sw_px']}
    ),
    "c": (
        {"face": ['sw_c']},
        {"success": -1, "face": ['sw_cf']},
        {"success": -1, "face": ['sw_cf']},
        {"success": -2, "face": ['sw_cff']},
        {"success": -2, "face": ['sw_cff']},
        {"advantage": -1, "face": ['sw_ct']},
        {"advantage": -1, "face": ['sw_ct']},
        {"advantage": -1, "success": -1, "face": ['sw_ctf']},
        {"advantage": -1, "success": -1, "face": ['sw_ctf']},
        {"advantage": -2, "face": ['sw_ctt']},
        {"advantage": -2, "face": ['sw_ctt']},
        {"success": -1, "despair": 1, "face": ['sw_cy']}
    ),
    "f": (
        {"dark": 1, "face": ['sw_fz']},
        {"dark": 1, "face": ['sw_fz']},
        {"dark": 1, "face": ['sw_fz']},
        {"dark": 1, "face": ['sw_fz']},
        {"dark": 1, "face": ['sw_fz']},
        {"dark": 1, "face": ['sw_fz']},
        {"dark": 2, "face": ['sw_fzz']},
        {"light": 1, "face": ['sw_fZ']},
        {"light": 1, "face": ['sw_Z']},
        {"light": 2, "face": ['sw_fZZ']},
        {"light": 2, "face": ['sw_fZZ']},
        {"light": 2, "face": ['sw_fZZ']}
    )
}

REMAP = {
    "success": "failure",
    "advantage": "threat"
}


def roller(pool, character_name):
    roll = Counter()
    [roll.update(rolled)
     for rolled in [random.choice(DICE[die]) for die in pool]]
    newroll = {}
    for key in roll:
        if key != 'face' and roll[key] < 1:
            if roll[key] == 0:
                continue
            newroll[REMAP[key]] = abs(roll[key])
            continue
        newroll[key] = roll[key]
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(sendToDiscord(newroll, character_name))
    newroll["face"] = [face[4:] for face in newroll["face"][::-1]]
    return newroll


async def sendToDiscord(roll, character_name):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(settings.DISCORD_WEB_HOOK_URL, adapter=AsyncWebhookAdapter(
            session))  # Initializing webhook with AsyncWebhookAdapter
        rolltext = ':'+'::'.join(roll["face"]) + ':\n'
        rolltext += ', '.join([f'{roll[key]} {key}' for key in roll if key !='face'])
        rolltext += f'\n Rolled by {character_name}'
        await webhook.send(content=rolltext)

def uniquelist():
    faces = set()
    for die in DICE:
        for face in DICE[die]:
            faces.add(face['face'][0])
    print(faces)
    print(len(faces))

# uniquelist()
