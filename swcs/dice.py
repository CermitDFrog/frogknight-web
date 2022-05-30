import random
from collections import Counter
import json


DICE = {
    "b": (
        {"face": ['b']},
        {"face": ['b']},
        {"advantage": 2, "face": ['aa']},
        {"advantage": 1, "face": ['a']},
        {"advantage": 1, "success": 1, "face": ['as']},
        {"success": 1, "face": ['s']}
    ),
    "s": (
        {"face": ['b']},
        {"face": ['b']},
        {"advantage": -2, "face": ['tt']},
        {"advantage": -1, "face": ['t']},
        {"advantage": -1, "success": -1, "face": ['tf']},
        {"success": -1, "face": ['f']}
    ),
    "a": (
        {"face": ['b']},
        {"success": 1, "face": ['s']},
        {"success": 1, "face": ['s']},
        {"success": 2, "face": ['ss']},
        {"advantage": 1, "face": ['a']},
        {"advantage": 1, "face": ['a']},
        {"advantage": 1, "success": 1, "face": ['as']},
        {"advantage": 2, "face": ['aa']}
    ),
    "d": (
        {"face": ['b']},
        {"success": -1, "face": ['f']},
        {"success": -2, "face": ['ff']},
        {"advantage": -1, "face": ['t']},
        {"advantage": -1, "face": ['t']},
        {"advantage": -1, "face": ['t']},
        {"advantage": -2, "face": ['tt']},
        {"advantage": -1, "success": -1, "face": ['tf']}
    ),
    "p": (
        {"face": ['b']},
        {"success": 1, "face": ['s']},
        {"success": 1, "face": ['s']},
        {"success": 2, "face": ['ss']},
        {"success": 2, "face": ['ss']},
        {"advantage": 1, "face": ['a']},
        {"advantage": 1, "success": 1, "face": ['a']},
        {"advantage": 1, "success": 1, "face": ['as']},
        {"advantage": 1, "success": 1, "face": ['as']},
        {"advantage": 2, "face": ['aa']},
        {"advantage": 2, "face": ['aa']},
        {"success": 1, "triumph": 1, "face": ['r']}
    ),
    "c": (
        {"face": ['b']},
        {"success": -1, "face": ['f']},
        {"success": -1, "face": ['f']},
        {"success": -2, "face": ['ff']},
        {"success": -2, "face": ['ff']},
        {"advantage": -1, "face": ['t']},
        {"advantage": -1, "face": ['t']},
        {"advantage": -1, "success": -1, "face": ['tf']},
        {"advantage": -1, "success": -1, "face": ['tf']},
        {"advantage": -2, "face": ['tt']},
        {"advantage": -2, "face": ['tt']},
        {"success": -1, "despair": 1, "face": ['e']}
    ),
    "f": (
        {"dark": 1, "face": ['d']},
        {"dark": 1, "face": ['d']},
        {"dark": 1, "face": ['d']},
        {"dark": 1, "face": ['d']},
        {"dark": 1, "face": ['d']},
        {"dark": 1, "face": ['d']},
        {"dark": 2, "face": ['dd']},
        {"light": 1, "face": ['l']},
        {"light": 1, "face": ['l']},
        {"light": 2, "face": ['ll']},
        {"light": 2, "face": ['ll']},
        {"light": 2, "face": ['ll']}
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
    # roll = {key: value for key, value in roll.items() if value != 0}
    return {key: value for key, value in roll.items() if value != 0}
