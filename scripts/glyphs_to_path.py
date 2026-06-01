#!/usr/bin/env python3
"""Render a text run from a font into an absolute SVG path + ink bbox.

Usage: glyphs_to_path.py <font.ttf> <text> <size> <startX> <baselineY>
Prints JSON: {"d":..., "bbox":[minx,miny,maxx,maxy], "endX":...}
"""
import sys, json
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen

font_path, text, size, startx, baseline = sys.argv[1:6]
size = float(size); startx = float(startx); baseline = float(baseline)

font = TTFont(font_path)
glyphset = font.getGlyphSet()
cmap = font.getBestCmap()
upm = font["head"].unitsPerEm
hmtx = font["hmtx"]
scale = size / upm

svg = SVGPathPen(glyphset)
bounds = BoundsPen(glyphset)
x = startx
for ch in text:
    gname = cmap[ord(ch)]
    matrix = (scale, 0, 0, -scale, x, baseline)
    glyphset[gname].draw(TransformPen(svg, matrix))
    glyphset[gname].draw(TransformPen(bounds, matrix))
    x += hmtx[gname][0] * scale

bb = bounds.bounds  # (minx, miny, maxx, maxy) already transformed
print(json.dumps({
    "d": svg.getCommands(),
    "bbox": [round(v, 2) for v in bb] if bb else None,
    "endX": round(x, 2),
}))
