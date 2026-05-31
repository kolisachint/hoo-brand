# Hoo Brand System — 2026

> Developer-native identity for an agentic AI ecosystem. Built on node geometry, signal propagation, and system-native typography.

## Overview

This repository contains the **Hoo Brand System 2026** design review — a single-file HTML brand document covering:

- **Symbol** — Abstract owl: two intersecting nodes, diamond spark, bilateral radar arcs
- **Master Wordmark** — Geometric `hoo` letterforms
- **HooCode** — Monospace suffix with live terminal cursor `_`
- **HooWork** — Thin sans-serif suffix with cyan pulse dot

## Files

| File | Description |
|------|-------------|
| `hoo_brand_2026.html` | Full brand review page (single-file HTML) |

## Design System

- **Fonts**: Inter (display) + JetBrains Mono (code)
- **Accent**: Signal Cyan `#00E5F5`
- **Surfaces**: Void `#08080A` → Surface `#101013` → Raised `#1E1E24`
- **Modes**: Dark (default) + Light toggle
- **Type Scale**: Fluid `clamp()` from 12px → 88px
- **Spacing**: 4px base grid system

## Products

| Product | Suffix Style | Signal |
|---------|-------------|--------|
| HooCode | Monospace, muted | Cyan cursor `_` |
| HooWork | Thin sans-serif | Cyan pulse dot |

## Improvements Applied (2026 revision)

- [x] Real font stack — Inter + JetBrains Mono via CDN
- [x] Fluid `clamp()` type scale — no fixed pixel sizes
- [x] Full light + dark mode with nav toggle
- [x] Design token system — spacing, color, radius, shadow
- [x] Semantic HTML + SVG accessibility (`aria-label`, `role="img"`)
- [x] Asymmetric hero layout with animated orbit ring
- [x] Color palette section with semantic naming
- [x] Typography scale showcase

## Suggestions (Open)

- [ ] OhMyOpenAgent brand mark variant
- [ ] Light-background / white-label logo versions for docs
- [ ] Cursor blink animation on HooCode underscore

---

**Author**: Sachin Koli ([@kolisachint](https://github.com/kolisachint))  
**Brand**: Hoo Ecosystem — agentic AI framework
