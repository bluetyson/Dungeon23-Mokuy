
#https://www.namecheap.com/support/knowledgebase/article.aspx/9693/29/how-to-install-perl-modules-on-shared-servers/
#TextMapper has
#TextMapper-Mapper-Hex
#TextMapper-Line-Hex #linedir
#TextMapper-Point-Hex #pointdir
#TextMapper-Command-Render #pointdir

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
                    m = re.search(r"\b([a-z]+)=[""]([^""]+)[""]\s*(\d+)", rest)
                    if not m:
                        break
                    tag = m.group(1)
                    label = m.group(2)
                    size = m.group(3)
                    if tag == "name":
                        region = self.make_region(x=x, y=y, z=z, map=self)
                        region.label(label)
                        region.size(size)
                    rest = re.sub(r"\b([a-z]+)=[""]([^""]+)[""]\s*(\d+)?", "", rest)
                while True:
                    m = re.search(r"[""([^""]+)[""]\s*(\d+)?((?:\s*[a-z]+\([^\)]+\))*)", rest)
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
                    rest = re.sub(r"[""([^""]+)[""]\s*(\d+)?((?:\s*[a-z]+\([^\)]+\))*)", "", rest)
                types = rest.split()
                region.type(types)
                self.regions.append(region)
                self.things.append(region)
            elif re.match(r'^(-?\d\d-?\d\d(?:\d\d)?(?:--?\d\d-?\d\d(?:\d\d)?)+)\s+(\S+)\s*(?:["“(.+)["”])?\s*(left|right)?\s*(\d+%)?', line):
                m = re.match(r'^(-?\d\d-?\d\d(?:\d\d)?(?:--?\d\d-?\d\d(?:\d\d)?)+)\s+(\S+)\s*(?:["“(.+)["”])?\s*(left|right)?\s*(\d+%)?',line)

                line = self.make_line(map=self)
                #usestr = re.match(r'^(-?\d\d-?\d\d(?:\d\d)?(?:--?\d\d-?\d\d(?:\d\d)?)+)\s+(\S+)\s*(?:["“(.+)["”])?\s*(left|right)?\s*(\d+%)?', line).group(1)
                usestr = re.match(r'^(-?\d\d-?\d\d(?:\d\d)?(?:--?\d\d-?\d\d(?:\d\d)?)+)\s+(\S+)\s*(?:["“(.+)["”])?\s*(left|right)?\s*(\d+%)?', line).group(1)
                line.type = re.match(r'^(-?\d\d-?\d\d(?:\d\d)?(?:--?\d\d-?\d\d(?:\d\d)?)+)\s+(\S+)\s*(?:["“(.+)["”])?\s*(left|right)?\s*(\d+%)?', line).group(2)
                line.label = re.match(r'^(-?\d\d-?\d\d(?:\d\d)?(?:--?\d\d-?\d\d(?:\d\d)?)+)\s+(\S+)\s*(?:["“(.+)["”])?\s*(left|right)?\s*(\d+%)?', line).group(3)
                line.side = re.match(r'^(-?\d\d-?\d\d(?:\d\d)?(?:--?\d\d-?\d\d(?:\d\d)?)+)\s+(\S+)\s*(?:["“(.+)["”])?\s*(left|right)?\s*(\d+%)?', line).group(4)
                line.start = re.match(r'^(-?\d\d-?\d\d(?:\d\d)?(?:--?\d\d-?\d\d(?:\d\d)?)+)\s+(\S+)\s*(?:["“(.+)["”])?\s*(left|right)?\s*(\d+%)?', line).group(5)
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
            elif re.match(r"^(\S+)\s+attributes\s+(.*)", line):
                self.attributes[re.match("^(\S+)\s+attributes\s+(.*)", line).group(1)] = re.match("^(\S+)\s+attributes\s+(.*)", line).group(2)
            elif re.match("^(\S+)\s+lib\s+(.*)", line):
                self.def1(f"<g id='{re.match(r'^({chr92}S+){chr92}s+lib{chr92}s+(.*)', line).group(1)}'>{re.match(r'^({chr92}S+){chr92}s+lib{chr92}s+(.*)', line).group(2)}</g>")
            elif re.match("^(\S+)\s+xml\s+(.*)", line):
                self.def1(f"<g id='{re.match(r'^({chr92}S+){chr92}s+xml{chr92}s+(.*)', line).group(1)}'>{re.match(r'^({chr92}S+){chr92}s+xml{chr92}s+(.*)', line).group(2)}</g>")
            elif re.match("^(<.*>)", line):
                self.def1(re.match("^(<.*>)", line).group(1))
            elif re.match("^(\S+)\s+path\s+attributes\s+(.*)", line):
                self.path_attributes[re.match(r'(\S+)\s+path\s+attributes\s+(.*)', line).group(1)] = re.match(r'^(\S+)\s+path\s+attributes\s+(.*)', line).group(2)
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
                self.other().append(re.match("^other\s+(.*)", line).group(1))    
            elif re.match(r"^url\s+(\S+)", line):
                self.url = (re.match(r"^url\s+(\S+)", line).group(1))
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

    def def1(self, svg):
        svg = svg.replace(">\s+<", "><")
        self.defs.append(svg)

    def merge_attributes(*args):
        attr = {}
        for a in args:
            if a:
                matches = re.findall(r'(\S+)=((["\']).*?\3)', a)
                for m in matches:
                    attr[m[0]] = m[1]
        return ' '.join([f"{k}={v}" for k, v in sorted(attr.items())])

    def svg_header(self):
        header = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <svg xmlns="http://www.w3.org/2000/svg" version="1.1"
        xmlns:xlink="http://www.w3.org/1999/xlink"
    '''

        if not self.regions:
            return header + "\n"
        
        maxz = 0
        for region in self.regions:
            maxz = region.z if region.z > maxz

        min_x_overall = None
        max_x_overall = None
        min_y_overall = None
        max_y_overall = None
        
        for z in range(maxz + 1):
            minx = None
            miny = None
            maxx = None
            maxy = None
            self.offset[z] = max_y_overall or 0
            for region in self.regions:
                if region.z != z:
                    continue
                minx = region.x if minx is None or minx >= region.x
                maxx = region.x if maxx is None or maxx <= region.x
                miny = region.y if miny is None or miny >= region.y
                maxy = region.y if maxy is None or maxy <= region.y
            
            min_x_overall = minx if min_x_overall is None or minx >= min_x_overall
            max_x_overall = maxx if max_x_overall is None or maxx <= max_x_overall
            if z == 0:
                min_y_overall = miny if min_y_overall is None else min_y_overall
                max_y_overall = miny if max_y_overall is None else max_y_overall
            else:
                max_y_overall += 1
                max_y_overall += 1 + maxy - miny
        
        vx1, vy1, width, height = self.viewbox(min_x_overall, min_y_overall, max_x_overall, max_y_overall)
        header += f"     viewBox='{vx1} {vy1} {width} {height}'>"
        header += f"\n     <!-- min ({min_x_overall}, {min_y_overall}), max ({max_x_overall}, {max_y_overall}) -->\n"
        
        return header

    def svg_defs(self):
        # All the definitions are included by default.
        doc = "  <defs>\n"

        if self.defs:
            doc += "    " + "\n    ".join(self.defs) + "\n"

        # collect region types from attributes and paths in case the sets don't overlap
        types = {}
        for region in self.regions:
            for type in region.type:
                types[type] = 1

        for line in self.lines:
            types[line.type] = 1

        # now go through them all
        for type in sorted(types.keys()):
            path = self.path[type]
            attributes = merge_attributes(self.attributes[type])
            path_attributes = merge_attributes(self.path_attributes['default'], self.path_attributes[type])
            glow_attributes = self.glow_attributes

            if path or attributes:
                doc = doc + f"    <g id='{type}'>\n"

                # just shapes get a glow such, eg. a house (must come first)
                if path and not attributes:
                    doc = doc + f"      <path {glow_attributes} d='{path}' />\n"

                # region with attributes get a shape (square or hex), eg. plains and grass
                if attributes:
                    doc = doc + "      " + self.shape(attributes) + "\n"

                # and now the attributes themselves the shape itself
                if path:
                    doc = doc + f"      <path {path_attributes} d='{path}' />\n"

                # close
                doc = doc + "    </g>\n"
            else:
                pass

        doc = doc + "  </defs>\n"
        return doc

    def svg_backgrounds(self):
        doc = "  <g id='backgrounds'>\n"
        for thing in self.things:
            types = thing.type
            thing.type = [typ for typ in thing.type if typ in self.attributes]
            doc += thing.svg(self.offset)
            thing.type = types
        doc += "  </g>\n"
        return doc

    def svg_things(self):
        doc = "  <g id='things'>\n"
        for thing in self.things:
            thing.type = [typ for typ in thing.type if typ not in self.attributes]
            doc += thing.svg(self.offset)
        doc += "  </g>\n"
        return doc

    def svg_coordinates(self):
        doc = "  <g id='coordinates'>\n"
        for region in self.regions:
            doc += region.svg_coordinates(self.offset)
        doc += "  </g>\n"
        return doc

    def svg_lines(self):
        doc = "  <g id='lines'>\n"
        for line in self.lines:
            doc += line.svg(self.offset)
        doc += "  </g>\n"
        return doc

    def svg_regions(self):
        doc = """  <g id="regions">\n"""
        attributes = self.attributes.get("default", """fill="none"""")
        for region in self.regions:
            doc += region.svg_region(attributes, self.offset)
        doc += """  </g>\n"""
        return doc

    def svg_line_labels(self):
        doc = """  <g id="line_labels">\n"""
        for line in self.lines:
            doc += line.svg_label(self.offset)
        doc += """  </g>\n"""
        return doc

    def svg_labels(self):
        doc = """  <g id="labels">\n"""
        for region in self.regions:
            doc += region.svg_label(self.url, self.offset)
        doc += """  </g>\n"""
        return doc

    def svg(self):
        doc = self.svg_header()
        doc += self.svg_defs()
        doc += self.svg_backgrounds() # opaque backgrounds
        doc += self.svg_lines()
        doc += self.svg_things() # icons, lines
        doc += self.svg_coordinates()
        doc += self.svg_regions()
        doc += self.svg_line_labels()
        doc += self.svg_labels()
        doc += self.license() or ""
        doc += self.svg_other()

        # error messages
        y = 10
        for msg in self.messages:
            doc += f"  <text x='0' y='{y}'>{msg}</text>\n"
            y += 10

        # source code (comments may not include -- for SGML compatibility!)
        source = self.map()
        source = source.replace("--", "&#45;&#45;")
        doc += f"""<!-- Source\n{source}\n-->\n"""
        doc += """</svg>\n"""

        return doc