#!/usr/bin/env python3
import json
import math
from pathlib import Path

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

THEMES = {
    "dark": {"bg": "#0d1117", "border": "#30363d", "grid": "#21262d", "text": "#c9d1d9", "fill": "rgba(57, 211, 83, 0.2)", "stroke": "#39d353", "point": "#39d353"},
    "light": {"bg": "#ffffff", "border": "#d0d7de", "grid": "#ebf0f4", "text": "#24292f", "fill": "rgba(9, 105, 218, 0.2)", "stroke": "#0969da", "point": "#0969da"}
}

def render_radar(data, theme, title):
    c = THEMES[theme]
    W, H = 400, 360
    CX, CY = W / 2, H / 2 + 10
    R = 110
    
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="ui-sans-serif, system-ui, sans-serif">']
    out.append(f'<rect width="{W}" height="{H}" rx="10" fill="{c["bg"]}" stroke="{c["border"]}"/>')
    out.append(f'<text x="{CX}" y="35" font-size="16" font-weight="bold" fill="{c["text"]}" text-anchor="middle">{esc(title)}</text>')
    
    # Grid rings
    levels = 5
    for lvl in range(1, levels + 1):
        r = R * (lvl / levels)
        pts = []
        for i in range(len(data)):
            angle = i * (2 * math.pi / len(data)) - math.pi / 2
            x = CX + r * math.cos(angle)
            y = CY + r * math.sin(angle)
            pts.append(f"{x},{y}")
        out.append(f'<polygon points="{" ".join(pts)}" fill="none" stroke="{c["grid"]}" stroke-width="1"/>')
        
    # Axes
    for i in range(len(data)):
        angle = i * (2 * math.pi / len(data)) - math.pi / 2
        x = CX + R * math.cos(angle)
        y = CY + R * math.sin(angle)
        out.append(f'<line x1="{CX}" y1="{CY}" x2="{x}" y2="{y}" stroke="{c["grid"]}" stroke-width="1"/>')
        
    # Data Polygon
    pts = []
    for i, item in enumerate(data):
        val = max(0.0, min(1.0, item["value"]))
        angle = i * (2 * math.pi / len(data)) - math.pi / 2
        x = CX + R * val * math.cos(angle)
        y = CY + R * val * math.sin(angle)
        pts.append(f"{x},{y}")
    
    out.append(f'<polygon points="{" ".join(pts)}" fill="{c["fill"]}" stroke="{c["stroke"]}" stroke-width="2"/>')
    
    # Data points
    for pt in pts:
        x, y = pt.split(',')
        out.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{c["bg"]}" stroke="{c["point"]}" stroke-width="2"/>')
        
    # Labels
    for i, item in enumerate(data):
        angle = i * (2 * math.pi / len(data)) - math.pi / 2
        pad = 20
        x = CX + (R + pad) * math.cos(angle)
        y = CY + (R + pad) * math.sin(angle)
        anchor = "middle"
        if math.cos(angle) > 0.1: anchor = "start"
        elif math.cos(angle) < -0.1: anchor = "end"
        y_adj = y + 4 if math.sin(angle) > 0.1 else (y if math.sin(angle) > -0.1 else y - 2)
        out.append(f'<text x="{x}" y="{y_adj}" font-size="12" fill="{c["text"]}" text-anchor="{anchor}">{esc(item["axis"])}</text>')
        
    out.append('</svg>')
    return "".join(out)

def main():
    Path("assets").mkdir(exist_ok=True)
    with open("assets/skills.json") as f:
        data = json.load(f)
        
    for theme in ("dark", "light"):
        Path(f"assets/radar-skills-{theme}.svg").write_text(render_radar(data["founder_radar"], theme, "Founder & Operator Capabilities"))
        Path(f"assets/radar-tech-{theme}.svg").write_text(render_radar(data["tech_radar"], theme, "Tech & AI Ecosystem"))
        
if __name__ == "__main__":
    main()
