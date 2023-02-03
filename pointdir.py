
#Hex

def pixels(self, offset, add_x=0, add_y=0):
    x = self.x
    y = self.y
    z = self.z
    if offset[z] is not None:
        y += offset[z]
    return x * dy + add_x, y * dy + add_y

def svg_region(self, attributes, offset):
    return '    <rect id="square{}{}{}" x="{:.1f}" y="{:.1f}" width="{:.1f}" height="{:.1f}" {} />\n'.format(
        self.x, self.y, self.z if self.z != 0 else '', # z 0 is not printed at all for the $id
        *self.pixels(offset, -0.5 * dy, -0.5 * dy),
        dy, dy, attributes)

def svg(self, offset):
    data = ''
    for t in self.type:
        data += '    <use x="{:.1f}" y="{:.1f}" xlink:href="#{}" />\n'.format(*self.pixels(offset), t)
    return data

def svg_coordinates(self, offset):
    x = self.x
    y = self.y
    z = self.z
    y += offset[z]
    data = '    <text text-anchor="middle"'
    data += ' x="{:.1f}" y="{:.1f}"'.format(*self.pixels(offset, 0, -0.4 * dy))
    data += ' ' + (self.map.text_attributes or '')
    data += '>'
    data += Game.TextMapper.Point.coord(self.x, self.y, ".") # original
    data += '</text>\n'
    return data

def svg_label(self, url, offset):
    if not self.label:
        return ''

    attributes = self.map.label_attributes
    if self.size:
        if 'font-size="\d+pt"' in attributes:
            attributes = re.sub('\bfont-size="\d+pt"', 'font-size="' + str(self.size) + 'pt"', attributes)
        else:
            attributes += ' font-size="' + str(self.size) + '"'

    if url:
        url = re.sub('%s', urllib.parse.quote_plus(self.label.encode('utf-8')), url) if '%s' in url
        else:
            url += urllib.parse.quote_plus(self.label.encode('utf-8'))

    data = '''    <g><text text-anchor="middle" x="{}" y="{}" {} {}>{}</text>
    '''.format(self.pixels(offset, 0, 0.4 * dy),
                attributes or '',
                self.map.glow_attributes or '',
                self.label)

    if url:
        data += '<a xlink:href="{}">'.format(url)
        data += '''<text text-anchor="middle" x="{}" y="{}" {}>{}</text>
        '''.format(self.pixels(offset, 0, 0.4 * dy),
                    attributes or '',
                    self.label)
        data += '</a>'
    data += '</g>\n'

    return data
