#!/usr/bin/env python3
"""
Convert an image into an animated SVG dot/binary matrix portrait.
Enhanced for ChawlaBhai profile.
"""
import argparse
import sys
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance

# --------------------------------------------------------------------------- #
# Palettes & Themes
# --------------------------------------------------------------------------- #

THEMES = {
    # theme: (foreground, background, shimmer_color)
    "dark": ("#39d353", "#161b22", "#00ff41"), # Hacker green
    "light": ("#0969da", "#ffffff", "#0040ff"), # Clean blue
    "cyber": ("#0ff", "#000", "#f0f"), # Cyan/Magenta
    "ember": ("#ff6600", "#111", "#ffcc00") # Fire orange
}

# --------------------------------------------------------------------------- #
# Image processing
# --------------------------------------------------------------------------- #

def circle_falloff(x, y, w, h):
    nx, ny = (x / w) * 2 - 1, (y / h) * 2 - 1
    d = nx*nx + ny*ny
    if d > 1: return 0.0
    return 1.0 - (d ** 2)

def load_grid(img_path, target_cols, contrast, gamma, cell_aspect, square, focus, equalize, detail):
    img = Image.open(img_path).convert("RGBA")
    
    # Fill transparent background with black (so it becomes empty in dot matrix)
    bg = Image.new("RGBA", img.size, (0, 0, 0, 255))
    img = Image.alpha_composite(bg, img).convert("RGB")
    
    w, h = img.size
    if square:
        size = min(w, h)
        left = int((w - size) * focus[0])
        top = int((h - size) * focus[1])
        img = img.crop((left, top, left + size, top + size))
        w, h = size, size

    target_rows = int(target_cols * (h / w) * cell_aspect)
    
    if equalize:
        img = ImageOps.autocontrast(img)
    if detail > 0:
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.0 + detail)
        
    img = img.resize((target_cols, target_rows), Image.Resampling.LANCZOS)
    
    # Adjust contrast and gamma
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(contrast)
    
    # Convert to luminance
    lum_img = img.convert("L")
    lum_data = lum_img.load()
    rgb_data = img.load()
    
    lum = []
    rgb = []
    for y in range(target_rows):
        row_lum = []
        row_rgb = []
        for x in range(target_cols):
            val = lum_data[x, y] / 255.0
            if gamma != 1.0:
                val = val ** gamma
            row_lum.append(val)
            row_rgb.append(rgb_data[x, y])
        lum.append(row_lum)
        rgb.append(row_rgb)
        
    return target_cols, target_rows, lum, rgb

# --------------------------------------------------------------------------- #
# SVG generation
# --------------------------------------------------------------------------- #

def svg_header(w, h, rows, opts):
    lanes = opts.lanes
    dur = opts.duration
    fade = opts.reveal_fade
    rt = opts.reveal_time
    
    css = ["svg { background: transparent; }"]
    if opts.animate:
        css.append(f"@keyframes shimmer {{ 0% {{ opacity: 0.15; }} 50% {{ opacity: 1.0; filter: drop-shadow(0 0 2px currentColor); }} 100% {{ opacity: 0.15; }} }}")
        for i in range(lanes):
            delay = (i / lanes) * dur
            css.append(f".l{i} {{ animation: shimmer {dur}s infinite {delay}s; }}")
            
    if opts.reveal:
        css.append(f"@keyframes reveal {{ from {{ opacity: 0; transform: translateY(-5px); }} to {{ opacity: 1; transform: translateY(0); }} }}")
        for y in range(rows):
            delay = (y / rows) * rt if opts.reveal_dir == "down" else ((rows - 1 - y) / rows) * rt
            css.append(f".r{y} {{ opacity: 0; animation: reveal {fade}s forwards {delay}s ease-out; }}")

    bg_rect = f'<rect width="{w}" height="{h}" fill="{opts.bg}"/>' if opts.bg else ""

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}">'
        f'<defs><style>{" ".join(css)}</style></defs>'
        f'{bg_rect}<g>'
    )

def build_dots(cols, rows, lum, rgb, theme, opts):
    fg, dim, shimmer = THEMES[theme]
    cell = opts.cell
    lanes = opts.lanes
    out = []
    for y in range(rows):
        row = []
        for x in range(cols):
            v = lum[y][x]
            if opts.invert: v = 1 - v
            if opts.circle: v *= circle_falloff(x, y, cols, rows)
            if v < opts.floor: continue
            
            r = (cell / 2) * opts.dot_scale * (0.4 + 0.6 * v)
            
            if opts.color:
                cr, cg, cb = rgb[y][x]
                fill = f"#{cr:02x}{cg:02x}{cb:02x}"
            else:
                fill = fg if v > 0.4 else dim
                
            cls = f' class="l{x % lanes}"' if opts.animate else ""
            op = f' opacity="{0.2 + 0.8 * v:.2f}"'
            row.append(f'<circle cx="{x * cell + cell/2:.1f}" cy="{y * cell + cell/2:.1f}" r="{r:.2f}" fill="{fill}"{op}{cls}/>')
            
        if not row: continue
        if opts.reveal:
            out.append(f'<g class="r{y}">{"".join(row)}</g>')
        else:
            out += row
            
    return "".join(out), cols * cell, rows * cell

def main():
    p = argparse.ArgumentParser()
    p.add_argument("image", type=Path)
    p.add_argument("-o", "--out", type=Path, default=Path("assets/portrait"))
    p.add_argument("--cols", type=int, default=100)
    p.add_argument("--cell", type=float, default=8.0)
    p.add_argument("--dot-scale", type=float, default=0.9)
    p.add_argument("--gamma", type=float, default=1.1)
    p.add_argument("--contrast", type=float, default=1.3)
    p.add_argument("--equalize", action="store_true")
    p.add_argument("--detail", type=float, default=0.5)
    p.add_argument("--floor", type=float, default=0.08)
    p.add_argument("--cell-aspect", type=float, default=1.0)
    p.add_argument("--square", action="store_true")
    p.add_argument("--focus", default="0.5,0.5")
    p.add_argument("--invert", action="store_true")
    p.add_argument("--circle", action="store_true")
    p.add_argument("--color", action="store_true")
    p.add_argument("--animate", action="store_true")
    p.add_argument("--lanes", type=int, default=20)
    p.add_argument("--duration", type=float, default=3.0)
    p.add_argument("--reveal", action="store_true")
    p.add_argument("--reveal-time", type=float, default=1.5)
    p.add_argument("--reveal-fade", type=float, default=0.5)
    p.add_argument("--reveal-dir", default="down")
    p.add_argument("--bg", default="")
    args = p.parse_args()

    fx, fy = (float(v) for v in args.focus.split(","))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    
    cols, rows, lum, rgb = load_grid(args.image, args.cols, args.contrast,
                                     args.gamma, args.cell_aspect,
                                     args.square, (fx, fy),
                                     args.equalize, args.detail)

    themes = ("dark",) if args.color else ("dark", "light", "cyber", "ember")
    for theme in themes:
        body, w, h = build_dots(cols, rows, lum, rgb, theme, args)
        svg = svg_header(w, h, rows, args) + body + "</g></svg>"
        stem = args.out.name if args.color else f"{args.out.name}-{theme}"
        dest = args.out.with_name(f"{stem}.svg")
        dest.write_text(svg, encoding="utf-8")
        print(f"wrote {dest}")

if __name__ == "__main__":
    main()
