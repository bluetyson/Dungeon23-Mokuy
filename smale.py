import random

world = {}

primary = {
    "water": ["water"],
    "swamp": ["marsh"],
    "desert": ["desert"],
    "plains": ["bush"],
    "forest": ["forest"],
    "hill": ["trees"],
    "mountain": ["mountains"]
}

secondary = {
    "water": ["bush"],
    "swamp": ["bush"],
    "desert": ["trees"],
    "plains": ["trees"],
    "forest": ["trees"],
    "hill": ["mountain"],
    "mountain": ["trees"],
}

tertiary = {
    "water": ["forest","trees"],
    "swamp": ["forest"],
    "desert": ["bush"],
    "plains": ["trees"],
    "forest": ["trees"],
    "hill": ["bush"],
    "mountain": ["forest"],
}

wildcard = {
    "water": [
        "swamp",
        "marsh",
        "desert",
        "desert",
        "bush",
        "bush",
    ],
    "swamp": ["water"],
    "desert": ["water", "mountain"],
    "plains": ["water", "marsh", "desert"],
    "forest": [
        "water",
        "water",
        "water",
        "marsh",
        "marsh",
        "swamp",
        "mountain",
        "mountain",
        "mountains",
    ],
    "hill": [
        "water",
        "water",
        "water",
        "desert",
        "desert",
        "desert",
        "forest",
        "forest",
        "forest",
    ],
    "mountain": ["desert", "desert"],
}


def one(arr):
    if len(arr) == 1 and isinstance(arr[0], list):
        arr = arr[0]
    return arr[random.randint(0, len(arr) - 1)]

def populate_region(hex, primary):
    random_num = random.randint(0, 100)
    encounters = {"water": 10, "swamp": 20, "sand": 20, "grass": 60, "forest": 40, "hill": 40, "mountain": 20}
    if primary in encounters and random_num < encounters[primary]:
        place_major(hex[0], hex[1], random.choice(list(encounters.keys())))