#!/usr/bin/env python3
"""Regenerate the HooCode / HooCowork lockup SVGs with real JetBrains Mono
glyph outlines (vector paths) for the suffix, a baseline-locked 'hoo' mark,
and symmetrically padded tiles."""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen

FONTS = os.path.expanduser("~/Library/Fonts")
MED = f"{FONTS}/JetBrainsMonoNerdFont-Medium.ttf"
BOLD = f"{FONTS}/JetBrainsMonoNerdFont-Bold.ttf"
REG = f"{FONTS}/JetBrainsMonoNerdFont-Regular.ttf"
OUT = os.path.join(os.path.dirname(__file__), "..", "assets")

SIZE, X0, BASE = 36, 140, 56   # suffix < mark for hierarchy (cap 0.73*36≈26 ≈ node size)
DIV_X = 130                    # divider x; ~11px gap from arc and from text
PAD = 28                       # symmetric tile padding


def run(font_path, text, x):
    font = TTFont(font_path)
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    scale = SIZE / font["head"].unitsPerEm
    hmtx = font["hmtx"]
    svg, bounds = SVGPathPen(gs), BoundsPen(gs)
    for ch in text:
        g = cmap[ord(ch)]
        m = (scale, 0, 0, -scale, x, BASE)
        gs[g].draw(TransformPen(svg, m))
        gs[g].draw(TransformPen(bounds, m))
        x += hmtx[g][0] * scale
    return svg.getCommands(), bounds.bounds, x


import math
code_d, code_bb, code_end = run(MED, "code", X0)
us_d, us_bb, _ = run(BOLD, "_", code_end)
cowork_d, cowork_bb, _ = run(REG, "cowork", X0)

# status dot: just after the cowork word, centered on its x-height
DOT_CX = round(cowork_bb[2] + 14, 1)
DOT_CY = round(BASE - (0.55 * SIZE) / 2, 1)   # x-height center
DOT_R = 4


def mark(stroke, divider):
    return f'''  <line x1="30" y1="24" x2="30" y2="56" stroke="{stroke}" stroke-width="4" stroke-linecap="round"/>
  <path d="M 30,42 A 12,12 0 0 1 54,42 L 54,56" fill="none" stroke="{stroke}" stroke-width="4" stroke-linecap="round"/>
  <circle cx="71" cy="44" r="12" fill="none" stroke="{stroke}" stroke-width="4"/>
  <circle cx="95" cy="44" r="12" fill="none" stroke="{stroke}" stroke-width="4"/>
  <polygon points="83,41 86,44 83,47 80,44" fill="#00F0FF"/>
  <path d="M 112,32 A 16,16 0 0 1 112,56" fill="none" stroke="#00F0FF" stroke-width="3" stroke-linecap="round"/>
  <line x1="{DIV_X}" y1="30" x2="{DIV_X}" y2="60" stroke="{divider}" stroke-width="2" stroke-linecap="round"/>'''


BLINK = '''  <style>
    @keyframes hoo-blink { 0%, 49% { opacity: 1; } 50%, 100% { opacity: 0; } }
    .cursor { animation: hoo-blink 1.06s steps(1, end) infinite; }
  </style>
'''

PING = '''  <style>
    @keyframes hoo-ping { 0% { transform: scale(1); opacity: 0.55; } 70%, 100% { transform: scale(2.8); opacity: 0; } }
    .ping { transform-box: fill-box; transform-origin: center; animation: hoo-ping 1.8s ease-out infinite; }
  </style>
'''


def write(name, w, title, tile, stroke, divider, suffix):
    body = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 80" width="{w}" height="80" role="img" aria-labelledby="{name}-title">
  <title id="{name}-title">{title}</title>
{(BLINK if 'hoocode' in name else PING if 'hoocowork' in name else '')}  <rect width="{w}" height="80" rx="16" fill="{tile}"/>
{mark(stroke, divider)}
{suffix}
</svg>
'''
    path = os.path.join(OUT, f"{name}.svg")
    with open(path, "w") as f:
        f.write(body)
    print("wrote", path)


# HooCode tile width: rightmost ink (underscore) + symmetric pad
WC = math.ceil(us_bb[2] + PAD)
code_suffix_dark = f'  <path d="{code_d}" fill="#A1A1AA"/>\n  <path class="cursor" d="{us_d}" fill="#00F0FF"/>'
code_suffix_light = f'  <path d="{code_d}" fill="#71717A"/>\n  <path class="cursor" d="{us_d}" fill="#00F0FF"/>'
write("hoocode", WC, "HooCode lockup", "#09090B", "#FAFAFA", "#27272A", code_suffix_dark)
write("hoocode-light", WC, "HooCode lockup — light", "#FAFAFA", "#09090B", "#E4E4E7", code_suffix_light)

# HooCowork tile width: status dot + symmetric pad
WW = math.ceil(DOT_CX + DOT_R + PAD)
dot = (f'  <circle class="ping" cx="{DOT_CX}" cy="{DOT_CY}" r="{DOT_R}" fill="none" stroke="#00F0FF" stroke-width="1.6"/>\n'
       f'  <circle cx="{DOT_CX}" cy="{DOT_CY}" r="{DOT_R}" fill="#00F0FF"/>')
cowork_suffix_dark = f'  <path d="{cowork_d}" fill="#E4E4E7"/>\n{dot}'
cowork_suffix_light = f'  <path d="{cowork_d}" fill="#27272A"/>\n{dot}'
write("hoocowork", WW, "HooCowork lockup", "#09090B", "#FAFAFA", "#27272A", cowork_suffix_dark)
write("hoocowork-light", WW, "HooCowork lockup — light", "#FAFAFA", "#09090B", "#E4E4E7", cowork_suffix_light)

print(f"hoocode  viewBox 0 0 {WC} 80  -> html img width={round(WC*92/80)} height=92")
print(f"hoocowork viewBox 0 0 {WW} 80  -> html img width={round(WW*92/80)} height=92")
