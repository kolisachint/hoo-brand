#!/usr/bin/env python3
"""Generate the Hoo product-lockup SVGs (dark + light).

Every lockup is the same recipe:

    [ hoo mark ] | [ product word ] [ cyan signal glyph ]

The word is rendered from real JetBrains Mono glyph outlines (vector paths —
no runtime font dependency) and each product carries one cyan "signal" that
encodes its behaviour:

    code     blinking cursor   _     terminal / coding
    cowork   pulsing dot       ●     a single live presence
    teams    fan-out nodes     ⤜     one planner dispatching to many agents

Add a product by appending one `Product(...)` to PRODUCTS. Run:

    python3 scripts/build_lockups.py
"""
import math
import os
from dataclasses import dataclass
from typing import Callable

from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen

# --- geometry / palette -----------------------------------------------------
FONTS = os.path.expanduser("~/Library/Fonts")
WEIGHTS = {
    "regular": f"{FONTS}/JetBrainsMonoNerdFont-Regular.ttf",
    "medium": f"{FONTS}/JetBrainsMonoNerdFont-Medium.ttf",
    "bold": f"{FONTS}/JetBrainsMonoNerdFont-Bold.ttf",
}
OUT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "assets"))

CYAN = "#00F0FF"
SIZE, X0, BASE = 36, 140, 56     # suffix size, pen start x, baseline
DIV_X = 130                      # divider x; ~11px gap from arc and from text
PAD = 28                         # symmetric tile padding
MID_Y = round(BASE - 0.55 * SIZE / 2, 1)   # suffix x-height centre (46.1)

# theme = (tile, mark stroke, divider)
DARK = ("#09090B", "#FAFAFA", "#27272A")
LIGHT = ("#FAFAFA", "#09090B", "#E4E4E7")

_FONTS: dict[str, TTFont] = {}


def _font(weight: str) -> TTFont:
    if weight not in _FONTS:
        _FONTS[weight] = TTFont(WEIGHTS[weight])
    return _FONTS[weight]


def run(weight: str, text: str, x: float):
    """Render `text` at pen position `x`; return (path_d, bbox, end_x)."""
    font = _font(weight)
    gs, cmap, hmtx = font.getGlyphSet(), font.getBestCmap(), font["hmtx"]
    scale = SIZE / font["head"].unitsPerEm
    svg, bounds = SVGPathPen(gs), BoundsPen(gs)
    for ch in text:
        g = cmap[ord(ch)]
        m = (scale, 0, 0, -scale, x, BASE)
        gs[g].draw(TransformPen(svg, m))
        gs[g].draw(TransformPen(bounds, m))
        x += hmtx[g][0] * scale
    return svg.getCommands(), bounds.bounds, x


# --- shared chrome ----------------------------------------------------------
def mark(stroke: str, divider: str) -> str:
    return f'''  <line x1="30" y1="24" x2="30" y2="56" stroke="{stroke}" stroke-width="4" stroke-linecap="round"/>
  <path d="M 30,42 A 12,12 0 0 1 54,42 L 54,56" fill="none" stroke="{stroke}" stroke-width="4" stroke-linecap="round"/>
  <circle cx="71" cy="44" r="12" fill="none" stroke="{stroke}" stroke-width="4"/>
  <circle cx="95" cy="44" r="12" fill="none" stroke="{stroke}" stroke-width="4"/>
  <polygon points="83,41 86,44 83,47 80,44" fill="{CYAN}"/>
  <path d="M 112,32 A 16,16 0 0 1 112,56" fill="none" stroke="{CYAN}" stroke-width="3" stroke-linecap="round"/>
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

DISPATCH = '''  <style>
    @keyframes hoo-dispatch { 0%, 100% { opacity: 0.28; } 45% { opacity: 1; } }
    .arm { animation: hoo-dispatch 2s ease-in-out infinite; }
    .arm-2 { animation-delay: 0.18s; }
    .arm-3 { animation-delay: 0.36s; }
  </style>
'''


# --- signals: (end_x, word_right) -> (svg, css, right_edge) -----------------
def cursor(end_x: float, _word_right: float):
    d, bb, _ = run("bold", "_", end_x)
    return f'<path class="cursor" d="{d}" fill="{CYAN}"/>', BLINK, bb[2]


def presence(_end_x: float, word_right: float):
    cx = round(word_right + 14, 1)
    svg = (f'<circle class="ping" cx="{cx}" cy="{MID_Y}" r="4" fill="none" stroke="{CYAN}" stroke-width="1.6"/>\n'
           f'  <circle cx="{cx}" cy="{MID_Y}" r="4" fill="{CYAN}"/>')
    return svg, PING, cx + 4


def fanout(_end_x: float, word_right: float):
    """One hub node fanning a signal out to three agent nodes (top→bottom wave)."""
    hx = round(word_right + 16, 1)          # hub
    wx = round(hx + 17, 1)                   # worker column
    ys = [round(MID_Y - 12, 1), MID_Y, round(MID_Y + 12, 1)]
    parts = [
        f'<circle cx="{hx}" cy="{MID_Y}" r="3.4" fill="{CYAN}"/>',
    ]
    for i, y in enumerate(ys):
        cls = "arm" + (f" arm-{i + 1}" if i else "")
        parts.append(f'<line class="{cls}" x1="{hx}" y1="{MID_Y}" x2="{wx}" y2="{y}" '
                     f'stroke="{CYAN}" stroke-width="1.5" stroke-linecap="round"/>')
        parts.append(f'<circle class="{cls}" cx="{wx}" cy="{y}" r="2.4" fill="{CYAN}"/>')
    return '\n  '.join(parts), DISPATCH, wx + 2.4


# --- product catalogue ------------------------------------------------------
@dataclass
class Product:
    slug: str                 # hoocode
    title: str                # HooCode
    word: str                 # code
    weight: str               # medium | regular | bold
    ink: tuple[str, str]      # suffix fill: (dark, light)
    signal: Callable          # cursor | presence | fanout


PRODUCTS = [
    Product("hoocode", "HooCode", "code", "medium", ("#A1A1AA", "#71717A"), cursor),
    Product("hoocowork", "HooCowork", "cowork", "regular", ("#E4E4E7", "#27272A"), presence),
    Product("hooteams", "HooTeams", "teams", "medium", ("#E4E4E7", "#27272A"), fanout),
]


def build(p: Product):
    # geometry is theme-independent — compute the word + signal once
    word_d, word_bb, end_x = run(p.weight, p.word, X0)
    sig, css, right = p.signal(end_x, word_bb[2])
    w = math.ceil(right + PAD)

    for tag, (tile, stroke, divider), ink in (("", DARK, p.ink[0]), ("-light", LIGHT, p.ink[1])):
        name = p.slug + tag
        title = p.title + (" lockup" if not tag else " lockup — light")
        body = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 80" width="{w}" height="80" role="img" aria-labelledby="{name}-title">
  <title id="{name}-title">{title}</title>
{css}  <rect width="{w}" height="80" rx="16" fill="{tile}"/>
{mark(stroke, divider)}
  <path d="{word_d}" fill="{ink}"/>
  {sig}
</svg>
'''
        with open(os.path.join(OUT, f"{name}.svg"), "w") as f:
            f.write(body)
        print("wrote", os.path.join(OUT, f"{name}.svg"))
    return w


if __name__ == "__main__":
    for p in PRODUCTS:
        w = build(p)
        print(f"  {p.slug:10} viewBox 0 0 {w} 80  ->  img height=60 width={round(w * 60 / 80)}")
