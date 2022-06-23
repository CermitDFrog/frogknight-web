# Importing discord.Webhook and discord.AsyncWebhookAdapter
from discord import Webhook, AsyncWebhookAdapter, utils
from django.conf import settings
from collections import Counter
import aiohttp
import asyncio
import random
import platform

EMOJI = {'sw_p': '<:sw_p:989653989115187200>',
'sw_pa': '<:sw_pa:989653989899522098>',
'sw_c': '<:sw_c:989653869229404160>',
'sw_fzz': '<:sw_fzz:989653988376981557>',
'sw_s': '<:sw_s:989630050456444929>',
'sw_fZZ': '<:sw_fZZ:989653987445837854>',
'sw_bs': '<:sw_bs:989630062909354065>',
'sw_dtt': '<:sw_dtt:989653920496369736>',
'sw_dt': '<:sw_dt:989653918751535147>',
'sw_df': '<:sw_df:989653917086400532>',
'sw_dff': '<:sw_dff:989653917879128064>',
'sw_ps': '<:sw_ps:989653992495804487>',
'sw_baa': '<:sw_baa:989630061802057818>',
'sw_ctf': '<:sw_ctf:989653872182181918>',
'sw_px': '<:sw_px:989653994148352110>',
'sw_bas': '<:sw_bas:989630062468948028>',
'sw_as': '<:sw_as:989630058408849508>',
'sw_cf': '<:sw_cf:989653869975973888>',
'sw_aa': '<:sw_aa:989630055665782864>',
'sw_aaa': '<:sw_aaa:989630056651440128>',
'sw_fZ': '<:sw_fZ:989653985713594368>',
'sw_stf': '<:sw_stf:989630053157597294>',
'sw_a': '<:sw_a:989630054776594452>',
'sw_st': '<:sw_st:989630052360679424>',
'sw_ba': '<:sw_ba:989630061017706576>',
'sw_stt': '<:sw_stt:989630054021627944>',
'sw_sf': '<:sw_sf:989630051614089236>',
'sw_ass': '<:sw_ass:989630059084124231>',
'sw_ct': '<:sw_ct:989653871326527538>',
'sw_pas': '<:sw_pas:989653991828885514>',
'sw_cff': '<:sw_cff:989653870680604752>',
'sw_d': '<:sw_d:989653915836506172>',
'sw_pss': '<:sw_pss:989653993103958047>',
'sw_dtf': '<:sw_dtf:989653919808507995>',
'sw_cy': '<:sw_cy:989653873595666453>',
'sw_paa': '<:sw_paa:989653990683865158>',
'sw_b': '<:sw_b:989630060296298506>',
'sw_aas': '<:sw_aas:989630057418997840>',
'sw_ctt': '<:sw_ctt:989653872937140234>',
'sw_fz': '<:sw_fz:989653986468565052>'}

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
        rolltext = ''.join([EMOJI[face] for face in roll["face"]]) + '\n'
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
