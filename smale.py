import random

class Point:
    def __init__(self):
        self.x = None
        self.y = None
        self.z = None
        self.type = None
        self.label = None
        self.size = None
        self.map = None

    def equal(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z
        
    def cmp(a, b):
        return (a.x - b.x) or (a.y - b.y) or (a.z - b.z)

    def coordinates(self):
        if self.z is not None:
            return self.x, self.y, self.z
        return self.x, self.y

    def coord(x, y, separator=''):
        usex = x
        usey = y
        if x < 0:
            if len(str(x)) == 2:
                usex = "-0" + str(x)[1:]
            else:
                usex = str(x)
        else:
            if len(str(x)) == 1:
                usex = "0" + str(x)
            else:
                usex = str(x)
        
        if y < 0:
            if len(str(y)) == 2:
                usey = "-0" + str(y)[1:]
            else:
                usey = str(y)
        else:
            if len(str(y)) == 1:
                usey = "0" + str(y)
            else:
                usey =  str(y)
            
                
        return usex+usey

dx = 100
dy = 100 * math.sqrt(3)

contrib = ""
#BW stands for "black & white", i.e. a true value skips background colours.
#BW stands for "black & white", i.e. a true value skips background colours.
log = []
contrib = ""

world = {}

primary_dict = {
    "water": ["water"],
    "swamp": ["marsh"],
    "desert": ["desert"],
    "plains": ["bush"],
    "forest": ["forest"],
    "hill": ["trees"],
    "mountain": ["mountain"]
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
        "mountain",
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
    "mountain": ["mountain"]
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
  "swamp": "swamp",    
  
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
    print(arr)
    if len(arr) == 1 and isinstance(arr[0], list):
        arr = arr[0]
    print(arr)
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
    log.append(message)

def place_major(x, y, encounter):
    print("pm:",x,y,encounter)
    print("pm:",encounters[encounter])
    if len(encounters[encounter]) > 0:
        thing = one(encounters[encounter])
    else:
        thing = False
        return
    #if not thing:
        #return
    verbose(f"placing {thing} ({encounter}) at ({x},{y})")
    hex = one(full_hexes(x, y))
    x += hex[0]
    y += hex[1]
    coordinates = Point.coord(x, y)
    print("pm:",world[coordinates])
    primary = reverse_lookup[world[coordinates]]
    print("pm:",primary)
    
    if 1 == 2:
        #bypass don't need?
        color, terrain = world[coordinates].split(' ', 1)
        if encounter == 'settlement':
            if primary == 'plains':
                color = one(['light-soil', 'soil'])
                verbose(f" {world[coordinates]} is {primary} and was changed to {color}")
            if primary != 'plains' or member(thing, ['large-town', 'city']):
                needs_fields.append([x, y])
        world[coordinates] = f"{color} {thing}"

def populate_region(hex, primary):
    random_ = random.randint(1,100)
    if (
        (primary == "water" and random_ < 10)
        or (primary == "swamp" and random_ < 20)
        or (primary == "sand" and random_ < 20)
        or (primary == "grass" and random_ < 60)
        or (primary == "forest" and random_ < 40)
        or (primary == "hill" and random_ < 40)
        or (primary == "mountain" and random_ < 20)
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
        if coord not in world:
            coordinates.append(coord) 
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
  print(x,y,primary)
  print(world)
  print(primary_dict[primary])
  world[Point.coord(x, y)] = one(primary_dict[primary])
  
  region = full_hexes(x, y)
  terrain = None

  for i in range(1, 10):
    coordinates = pick_unassigned(x, y, region)
    terrain = one(primary_dict[primary])
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
    random_ = random.randint(1,6)
    if random_ < 3:
      terrain = one(primary_dict[primary])
      verbose("  halfhex primary   {} => {}".format(coordinates, terrain))
    elif random_ < 5:
      terrain = one(secondary[primary])
      verbose("  halfhex secondary {} => {}".format(coordinates, terrain))
    else:
      terrain = one(tertiary[primary])
      verbose("  halfhex tertiary  {} => {}".format(coordinates, terrain))
    world[coordinates] = terrain

def seed_region(seeds, terrain):
  terrain_above = None
  for hex_ in seeds:
    verbose("seed_region ({}, {}) with {}".format(hex_[0], hex_[1], terrain))
    generate_region(hex_[0], hex_[1], terrain)
    populate_region(hex_, terrain)
    random_ = random.randint(1,12)
    # pick next terrain based on the previous one (to the left); or the one
    # above if in the first column
    next_ = None
    if hex_[0] == 1 and terrain_above:
        terrain = terrain_above  
    else:
        terrain
    if random_ < 6:
      next_ = random.choice(primary[terrain])
      verbose("picked primary {}".format(next_))
    elif random_ < 9:
      next_ = random.choice(secondary[terrain])
      verbose("picked secondary {}".format(next_))
    elif random_ < 11:
      next_ = random.choice(tertiary[terrain])
      verbose("picked tertiary {}".format(next_))
    else:
      next_ = random.choice(wildcard[terrain])
      verbose("picked wildcard {}".format(next_))
    if hex_[0] == 1:
        terrain_above = terrain 
    if next_ not in reverse_lookup:
      raise ValueError("Terrain lacks reverse_lookup: {}".format(next_))
    terrain = reverse_lookup[next_]

def agriculture():
    for hex_ in needs_fields:
        verbose(f"looking to plant fields near {Point.coord(hex_[0], hex_[1])}")
        delta = [[[-1, 0], [0, -1], [1, 0], [1, 1], [0, 1], [-1, 1]],
                [[-1, -1], [0, -1], [1, -1], [1, 0], [0, 1], [-1, 0]]]
        plains = []
        for i in range(6):
            x, y = hex_[0] + delta[hex_[0] % 2][i][0], hex_[1] + delta[hex_[0] % 2][i][1]
            coordinates = Point.coord(x, y)
            if coordinates in world:
                color, terrain = world[coordinates].split(" ", 1)
                verbose(f"  {coordinates} is {world[coordinates]} ie. {reverse_lookup[world[coordinates]]}")
                if reverse_lookup[world[coordinates]] == "plains":
                    verbose(f"   {coordinates} is a candidate")
                    plains.append(coordinates)
        if not plains:
            continue
        target = random.choice(plains)
        world[target] = random.choice(["light-soil fields", "soil fields"])
        verbose(f" {target} planted with {world[target]}")

def generate_map(bw, width=20, height=10):
    seeds = []
    for y in range(1, height + 3, 5):
        for x in range(1, width + 3, 5):
            y0 = y + (x % 10) // 3
            seeds.append([x, y0])
    world.clear()
    seed_terrain = list(primary.keys())
    seed_region(seeds, random.choice(seed_terrain))
    agriculture()
    to_delete = []
    for coordinates in world:
        #print(coordinates)
        ##python version
        usecoord = coordinates.replace("-",'')
        
        #x, y = map(int, [coordinates[0:2], coordinates[2:4]])
        x, y = map(int, [usecoord[0:2], usecoord[2:4]])
        print(usecoord[0:2], usecoord[2:4], coordinates)
        if x < 1 or y < 1 or x > width or y > height or '-' in coordinates:
            print("getridof")
            to_delete.append(coordinates)
    for coordinates in to_delete:
        del world[coordinates]
    if 1 == 2:
        if bw:
            for coordinates in world:
                color, *rest = world[coordinates].split(' ', maxsplit=1)
                if rest:
                    world[coordinates] = rest[0]
                else:
                    del world[coordinates]
    return '\n'.join(f'{coordinates} {world[coordinates]}' for coordinates in sorted(world)) + '\n' + f'include {contrib}/gnomeyland.txt\n'
