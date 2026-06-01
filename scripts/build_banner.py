#!/usr/bin/env python3
"""Generate the Hoo terminal mark and boot card.

Outputs:
  assets/tui/owl.txt   — block-glyph owl, plain (single-width, alignment-safe)
  assets/tui/owl.ans   — block-glyph owl, ANSI color (cyan eyes)
  assets/tui/startup.ans — boot card: owl + product info (à la `claude`)
"""
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "tui")
os.makedirs(OUT, exist_ok=True)

CYAN = "\x1b[38;2;0;240;255m"   # Signal Cyan #00F0FF
WHITE = "\x1b[97m"
DIM = "\x1b[38;2;113;113;122m"  # zinc-500
RESET = "\x1b[0m"

# block-glyph owl: flat square blot, dome eyes = the 'oo' nodes
owl = ["▟▀▀▀▀▀▙", "▌▟▙ ▟▙▐", "▜▄▄▄▄▄▛"]
owl_ans = [
    WHITE + owl[0] + RESET,
    WHITE + "▌" + RESET + CYAN + "▟▙ ▟▙" + RESET + WHITE + "▐" + RESET,
    WHITE + owl[2] + RESET,
]
with open(os.path.join(OUT, "owl.txt"), "w") as f:
    f.write("\n".join(owl) + "\n")
with open(os.path.join(OUT, "owl.ans"), "w") as f:
    f.write("\n".join(owl_ans) + "\n")

# startup card: owl mark + product info (mirrors `claude` boot)
info = [
    f"{WHITE}hoo{DIM}│{RESET}{CYAN}code{RESET}",
    f"{DIM}agentic coding agent · v0.1.0{RESET}",
    f"{DIM}~/github/hoocode{RESET}",
]
startup = "".join(owl_ans[i] + "  " + info[i] + "\n" for i in range(3))
with open(os.path.join(OUT, "startup.ans"), "w") as f:
    f.write(startup)

print("owl mark:")
print("\n".join(owl))
print("\nwrote assets/tui/{owl.txt,owl.ans,startup.ans}")
