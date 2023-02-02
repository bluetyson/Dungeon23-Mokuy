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

primary = {
    "water": ["water"],
    "swamp": ["marsh"],
    "desert": ["desert"],
    "plains": ["bush"],
    "forest": ["forest"],
    "hill": ["trees"],
    "mountain": ["mountains"]
}

reverse_lookup = {
  # primary
  "water": "water",
  "marsh": "swamp",
  "desert": "desert",
  "bush": "plains",
  "forest": "forest",
  "trees": "hill",
  "mountain": "mountain",
  
}

encounters = {
    "settlement": ["thorp", "thorp", "thorp", "thorp",
                   "village",
                   "town", "town",
                   "large-town",
                   "city"],
    "fortress": ["keep", "tower", "castle"],
    "religious": ["shrine", "law", "chaos"],
    "ruin": [],
    "monster": [],
    "natural": []
}

needs_fields = []

def one(arr):
    if len(arr) == 1 and isinstance(arr[0], list):
        arr = arr[0]
    return arr[random.randint(0, len(arr) - 1)]

def populate_region(hex, primary):
    random_num = random.randint(0, 100)
    encounters = {"water": 10, "swamp": 20, "sand": 20, "grass": 60, "forest": 40, "hill": 40, "mountain": 20}
    if primary in encounters and random_num < encounters[primary]:
        place_major(hex[0], hex[1], random.choice(list(encounters.keys())))

def member(element, *args):
    for arg in args:
        if element == arg:
            return True
    return False

def verbose(message):
    log.debug(message)

def place_major(x, y, encounter):
    thing = one(encounters[encounter])
    if not thing:
        return
    verbose(f"placing {thing} ({encounter}) at ({x},{y})")
    hex = one(full_hexes(x, y))
    x += hex[0]
    y += hex[1]
    coordinates = Point.coord(x, y)
    primary = reverse_lookup[world[coordinates]]
    color, terrain = world[coordinates].split(' ', 1)
    if encounter == 'settlement':
        if primary == 'plains':
            color = one(['light-soil', 'soil'])
            verbose(f" {world[coordinates]} is {primary} and was changed to {color}")
        if primary != 'plains' or member(thing, ['large-town', 'city']):
            needs_fields.append([x, y])
    world[coordinates] = f"{color} {thing}"

def populate_region(hex, primary):
    random = randint(100)
    if (
        (primary == "water" and random < 10)
        or (primary == "swamp" and random < 20)
        or (primary == "sand" and random < 20)
        or (primary == "grass" and random < 60)
        or (primary == "forest" and random < 40)
        or (primary == "hill" and random < 40)
        or (primary == "mountain" and random < 20)
    ):
        place_major(hex[0], hex[1], random.choice(list(encounters.keys())))


def pick_unassigned(x, y, region):
    hex = random.choice(region)
    coordinates = Point.coord(x + hex[0], y + hex[1])
    while coordinates in world:
        hex = random.choice(region)
        coordinates = Point.coord(x + hex[0], y + hex[1])
    return coordinates


def pick_remaining(x, y, region):
    coordinates = []
    for hex in region:
        coord = Point.coord(x + hex[0], y + hex[1])
        coordinates.append(coord) if coord not in world
    return coordinates

def full_hexes(x, y):
    if x % 2:
        return ([0, -2],
                [-2, -1], [-1, -1], [0, -1], [1, -1], [2, -1],
                [-2,  0], [-1,  0], [0,  0], [1,  0], [2,  0],
                [-2,  1], [-1,  1], [0,  1], [1,  1], [2,  1],
                [-1,  2], [0,  2], [1,  2])
    else:
        return ([-1, -2], [0, -2], [1, -2],
                [-2, -1], [-1, -1], [0, -1], [1, -1], [2, -1],
                [-2,  0], [-1,  0], [0,  0], [1,  0], [2,  0],
                [-2,  1], [-1,  1], [0,  1], [1,  1], [2,  1],
                [0,  2])

def half_hexes(x, y):
    if x % 2:
        return ([-2, -2], [-1, -2], [1, -2], [2, -2],
                [-3,  0], [3,  0],
                [-3,  1], [3,  1],
                [-2,  2], [2,  2],
                [-1,  3], [1,  3])
    else:
        return ([-1, -3], [1, -3],
                [-2, -2], [2, -2],
                [-3, -1], [3, -1],
                [-3,  0], [3,  0],
                [-2,  2], [-1,  2], [1,  2], [2,  2])

def generate_region(x, y, primary):
  world[Point.coord(x, y)] = one(primary[primary])
  
  region = full_hexes(x, y)
  terrain = None

  for i in range(1, 10):
    coordinates = pick_unassigned(x, y, region)
    terrain = one(primary[primary])
    verbose(" primary   {} => {}".format(coordinates, terrain))
    world[coordinates] = terrain
    
  for i in range(1, 7):
    coordinates = pick_unassigned(x, y, region)
    terrain = one(secondary[primary])
    verbose(" secondary {} => {}".format(coordinates, terrain))
    world[coordinates] = terrain

  for coordinates in pick_remaining(x, y, region):
    if random.random() > 0.1:
      terrain = one(tertiary[primary])
      verbose(" tertiary  {} => {}".format(coordinates, terrain))
    else:
      terrain = one(wildcard[primary])
      verbose(" wildcard  {} => {}".format(coordinates, terrain))
    world[coordinates] = terrain

  for coordinates in pick_remaining(x, y, half_hexes(x, y)):
    random = random.randint(6)
    if random < 3:
      terrain = one(primary[primary])
      verbose("  halfhex primary   {} => {}".format(coordinates, terrain))
    elif random < 5:
      terrain = one(secondary[primary])
      verbose("  halfhex secondary {} => {}".format(coordinates, terrain))
    else:
      terrain = one(tertiary[primary])
      verbose("  halfhex tertiary  {} => {}".format(coordinates, terrain))
    world[coordinates] = terrain

