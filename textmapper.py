
#https://www.namecheap.com/support/knowledgebase/article.aspx/9693/29/how-to-install-perl-modules-on-shared-servers/

class Mapper:
  local_files = None
  dist_dir = None
  map = None
  regions = []
  attributes = {}
  defs = []
  path = {}
  lines = []
  things = []
  path_attributes = {}
  text_attributes = ''
  glow_attributes = ''
  label_attributes = ''
  messages = []
  seen = {}
  license = ''
  other = []
  url = ''
  offset = []

  #log = Game.TextMapper.Log.get()
  log = []

  @classmethod
  def example(cls):
      return '''0101 mountain "mountain"
0102 swamp "swamp"
0103 hill "hill"
0104 forest "forest"
0201 empty pyramid "pyramid"
0202 tundra "tundra"
0203 coast "coast"
0204 empty house "house"
0301 woodland "woodland"
0302 wetland "wetland"
0303 plain "plain"
0304 sea "sea"
0401 hill tower "tower"
0402 sand house "house"
0403 jungle "jungle"
0501 mountain cave "cave"
0502 sand "sand"
0503 hill castle "castle"
0205-0103-0202-0303-0402 road
0101-0203 river
0401-0303-0403 border
include default.txt
license <text>Public Domain</text>
'''

  def initialize(self, map):
      map = map.replace("&#45;", "-")
      self.map = map
      self.process(map.split('\n'))

def process(self):
    line_id = 0
    for line in args:
        if re.match(r"^(-?\d\d)(-?\d\d)(\d\d)?\s+(.*)", line):
            m = re.match(r"^(-?\d\d)(-?\d\d)(\d\d)?\s+(.*)", line)
            x = m.group(1)
            y = m.group(2)
            z = m.group(3) if m.group(3) else "00"
            rest = m.group(4)
            while True:
                m = re.search(r"\b([a-z]+)=["“]([^"”]+)["”]\s*(\d+)", rest)
                if not m:
                    break
                tag = m.group(1)
                label = m.group(2)
                size = m.group(3)
                if tag == "name":
                    region = self.make_region(x=x, y=y, z=z, map=self)
                    region.label(label)
                    region.size(size)
                rest = re.sub(r"\b([a-z]+)=["“]([^"”]+)["”]\s*(\d+)?", "", rest)
            while True:
                m = re.search(r"["“]([^"”]+)["”]\s*(\d+)?((?:\s*[a-z]+\([^\)]+\))*)", rest)
                if not m:
                    break
                label = m.group(1)
                size = m.group(2)
                transform = m.group(3)
                if transform or region.label:
                    self.other().append(lambda: self.other_text(region, label, size, transform))
                else:
                    region.label(label)
                    region.size(size)
                rest = re.sub(r"["“]([^"”]+)["”]\s*(\d+)?((?:\s*[a-z]+\([^\)]+\))*)", "", rest)
            types = rest.split()
            region.type(types)
            self.regions.append(region)
            self.things.append(region)
        elif re.match(r"^(-?\d\d-?\d\d(?:\d\d)?(?:--?\d\d-?\d\d(?:\d\d)?)+)\s+(\S+)\s*(?:["“](.+)["”])?\s*(left|right)?\s*(\d+%)?", line):
            m = re.match(r"^(-?\d\d-?\d\d(?:\d\d)?(?:--?\d\d-?\d\d(?:\d\d)?)+)\s+(\S+)\s*(?:["“](.+)["”])?\s*(left|right)?\s*(\d+%)?",

            line = self.make_line(map=self)
            str = re.match(r"^(-?\d\d-?\d\d(?:\d\d)?(?:--?\d\d-?\d\d(?:\d\d)?)+)\s+(\S+)\s*(?:[“](.+)[”])?\s*(left|right)?\s*(\d+%)?", line).group(1)
            line.type = re.match(r"^(-?\d\d-?\d\d(?:\d\d)?(?:--?\d\d-?\d\d(?:\d\d)?)+)\s+(\S+)\s*(?:[“](.+)[”])?\s*(left|right)?\s*(\d+%)?", line).group(2)
            line.label = re.match(r"^(-?\d\d-?\d\d(?:\d\d)?(?:--?\d\d-?\d\d(?:\d\d)?)+)\s+(\S+)\s*(?:[“](.+)[”])?\s*(left|right)?\s*(\d+%)?", line).group(3)
            line.side = re.match(r"^(-?\d\d-?\d\d(?:\d\d)?(?:--?\d\d-?\d\d(?:\d\d)?)+)\s+(\S+)\s*(?:[“](.+)[”])?\s*(left|right)?\s*(\d+%)?", line).group(4)
            line.start = re.match(r"^(-?\d\d-?\d\d(?:\d\d)?(?:--?\d\d-?\d\d(?:\d\d)?)+)\s+(\S+)\s*(?:[“](.+)[”])?\s*(left|right)?\s*(\d+%)?", line).group(5)
            line.id = "line" + str(line_id)
            line_id += 1
            points = []
            while True:
                match = re.search(r"\G(-?\d\d)(-?\d\d)(\d\d)?-?", str)
                if not match:
                    break
                points.append(Game.TextMapper.Point(x=match.group(1), y=match.group(2), z=match.group(3) or "00"))
            line.points = points
            self.lines.append(line)
        elif re.match(r"^(\S+)\s+attributes\s+(.*)", line
            self.attributes[re.match("^(\S+)\s+attributes\s+(.*)", line).group(1)] = re.match("^(\S+)\s+attributes\s+(.*)", line).group(2)
        elif re.match("^(\S+)\s+lib\s+(.*)", line):
            self.def(f"<g id='{re.match("^(\S+)\s+lib\s+(.*)", line).group(1)}'>{re.match("^(\S+)\s+lib\s+(.*)", line).group(2)}</g>")
        elif re.match("^(\S+)\s+xml\s+(.*)", line):
            self.def(f"<g id='{re.match("^(\S+)\s+xml\s+(.*)", line).group(1)}'>{re.match("^(\S+)\s+xml\s+(.*)", line).group(2)}</g>")
        elif re.match("^(<.*>)", line):
            self.def(re.match("^(<.*>)", line).group(1))
        elif re.match("^(\S+)\s+path\s+attributes\s+(.*)", line):
            self.path_attributes[re.match("^(\S+)\s+path\s+attributes\s+(.*)", line).group(1)] = re.match("^(\S+)\s+path\s+attributes\s+(.*)", line).group(2)
        elif re.match("^(\S+)\s+path\s+(.*)", line):
            self.path[re.match("^(\S+)\s+path\s+(.*)", line).group(1)] = re.match("^(\S+)\s+path\s+(.*)", line).group(2)
        elif re.match("^text\s+(.*)", line):
            self.text_attributes(re.match("^text\s+(.*)", line).group(1))
        elif re.match("^glow\s+(.*)", line):
            self.glow_attributes(re.match("^glow\s+(.*)", line).group(1))
        elif re.match("^label\s+(.*)", line):
            self.label_attributes(re.match("^label\s+(.*)", line).group(1))
        elif re.match("^license\s+(.*)", line):
            self.license(re.match("^license\s+(.*)", line).group(1))
        elif re.match("^other\s+(.*)", line):
            self.other().append(re.match("^other\s+(.*)", line    
        elif re.match(r"^url\s+(\S+)", line):
            self.url(re.match(r"^url\s+(\S+)", line).group(1))
        elif re.match(r"^include\s+(\S*)", line):
            if len(self.seen.keys()) > 5:
                self.messages.append("Includes are limited to five to prevent loops")
            elif not self.seen.get(re.match(r"^include\s+(\S*)", line).group(1)):
                location = re.match(r"^include\s+(\S*)", line).group(1)
                self.seen[location] = 1
                path = None
                if '/' not in location and os.path.isfile(os.path.join(self.dist_dir, location)):
                    path = os.path.join(self.dist_dir, location)
                    print(f"Reading {location}")
                    self.process("\n".join(path.read().decode("utf-8").splitlines()))
                elif self.local_files and os.path.isfile(location):
                    path = location
                    print(f"Reading {location}")
                    self.process("\n".join(path.read().decode("utf-8").splitlines()))
                elif re.match(r"^https?:/", location):
                    print(f"Getting {location}")
                    response = requests.get(location)
                    if response.ok:
                        self.process("\n".join(response.text.splitlines()))
                    else:
                        self.messages.append(f"Getting {location}: {response.status_code} {response.reason}")
                elif re.match(r"^https?:/", self.dist_dir):
                    url = self.dist_dir
                    if not url.endswith("/"):
                        url += "/"
                    url += location
                    print(f"Getting {url}")
                    response = requests.get(url)
                    if response.ok:
                        self.process("\n".join(response.text.splitlines()))
                    else:
                        self.messages.append(f"Getting {url}: {response.status_code} {response.reason}")
                else:
                    print(f"No library '{location}' in {self.dist_dir}")
                    self.messages.append(f"Library '{location}' must be an existing file on the server or a HTTP/HTTPS URL")
        else:
            if line and not line.startswith("#"):
                print(f"Did not parse {line}")                

def svg_other(self):
    data = "\n"
    for other in self.other():
        if callable(other):
            data += other()
        else:
            data += other
        data += "\n"
    return data

def other_text(self, region, label, size=None, transform=None):
    if transform is None:
        transform = "translate({},{})".format(*region.pixels(self.offset))
    else:
        transform = "translate({},{})".format(*region.pixels(self.offset)) + transform
    attributes = "transform=\"{}\" {}".format(transform, self.label_attributes)
    if size and "font-size" not in attributes:
        attributes += " font-size=\"{}\"".format(size)
    data = "    <g><text text-anchor=\"middle\" {} {}>{}</text>".format(attributes, self.glow_attributes or '', label)
    url = self.url
    if url:
        if "%s" in url:
            url = url.replace("%s", url_escape(encode_utf8(label)))
        else:
            url += url_escape(encode_utf8(label))
    data += "<a xlink:href=\"{}\"><text text-anchor=\"middle\" {}>{}</text></a>".format(url, attributes, label) if url else ""
    data += "</g>\n"
    return data
