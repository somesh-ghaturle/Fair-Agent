#!/usr/bin/env python3
"""Add motion to exported archify SVGs: flowing edges, drifting group frames.

Archify exports static SVG; the interactive .html has trace motion but GitHub only
renders the .svg. This injects CSS animation, which runs inside an <img>, so the
diagrams move in the README. Re-run after any `archify deliver` + SVG export.

Edges (`data-edge-from` paths) flow fast, ~14 px/s. Already-dashed group frames drift
slowly, ~4 px/s, so they read as ambient rather than as data movement. Solid frames and
edge-less diagrams are left alone. Durations are per dash period so every loop is
seamless and every stroke of a kind moves at one speed.
"""
import pathlib, re, sys

STYLE = """<style data-archify-motion="1">
@keyframes archify-flow-8{to{stroke-dashoffset:-8}}
@keyframes archify-flow-10{to{stroke-dashoffset:-10}}
@keyframes archify-flow-12{to{stroke-dashoffset:-12}}
@keyframes archify-flow-16{to{stroke-dashoffset:-16}}
path[data-edge-from]{stroke-dasharray:6 10;animation:archify-flow-16 1.1s linear infinite}
path[data-edge-from][stroke-dasharray="4px, 4px"]{stroke-dasharray:4 4;animation-name:archify-flow-8;animation-duration:.55s}
path[data-edge-from][stroke-dasharray="5px, 5px"]{stroke-dasharray:5 5;animation-name:archify-flow-10;animation-duration:.69s}
rect[data-composition-frame-kind]:not([stroke-dasharray="none"]){animation:archify-flow-12 3s linear infinite}
rect[data-composition-frame-kind][stroke-dasharray="4px, 4px"]{animation-name:archify-flow-8;animation-duration:2s}
@media(prefers-reduced-motion:reduce){
path[data-edge-from]{animation:none;stroke-dasharray:none}
rect[data-composition-frame-kind]{animation:none}
}
</style>"""

# strip any style block this script wrote before, so a re-run upgrades instead of stacking
PREVIOUS = re.compile(r'\n?<style(?: data-archify-motion="1")?>\s*@keyframes archify-flow.*?</style>', re.S)
DASHED_FRAME = re.compile(r'data-composition-frame-kind[^>]*?stroke-dasharray="(?!none)')

here = pathlib.Path(__file__).parent
for f in sorted(here.glob("*.svg")):
    original = f.read_text()
    text = PREVIOUS.sub("", original)
    edges = text.count("data-edge-from")
    frames = len(DASHED_FRAME.findall(text))
    if not edges and not frames:
        print(f"{f.name}: nothing to animate, skipped")
        continue
    new, n = re.subn(r"(<svg\b[^>]*>)", lambda m: m.group(1) + "\n" + STYLE, text, count=1)
    if not n:
        print(f"{f.name}: NO <svg> TAG FOUND", file=sys.stderr)
        continue
    if new == original:
        print(f"{f.name}: already current ({edges} edges, {frames} frames)")
        continue
    f.write_text(new)
    print(f"{f.name}: {edges} edges, {frames} frames animated")
