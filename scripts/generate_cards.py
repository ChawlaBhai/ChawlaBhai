#!/usr/bin/env python3
import json
import textwrap
from pathlib import Path

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

THEMES = {
    "dark": {"bg": "#0d1117", "border": "#30363d", "title": "#58a6ff", "text": "#c9d1d9", "muted": "#8b949e", "tag_bg": "#21262d", "tag_text": "#58a6ff"},
    "light": {"bg": "#ffffff", "border": "#d0d7de", "title": "#0969da", "text": "#24292f", "muted": "#57606a", "tag_bg": "#ddf4ff", "tag_text": "#0969da"}
}

LANG_COLORS = {
    "TypeScript": "#3178c6", "React": "#61dafb", "Python": "#3572A5", "JavaScript": "#f1e05a"
}

def render_founder_card(theme):
    c = THEMES[theme]
    W, H = 480, 200
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="ui-sans-serif, system-ui, sans-serif">']
    out.append(f'<rect width="{W-1}" height="{H-1}" x="0.5" y="0.5" rx="10" fill="{c["bg"]}" stroke="{c["border"]}"/>')
    
    out.append(f'<text x="25" y="35" font-size="16" font-weight="700" fill="{c["title"]}">0-to-1 Founder Scale Metrics</text>')
    out.append(f'<line x1="25" y1="50" x2="{W-25}" y2="50" stroke="{c["border"]}" stroke-width="1"/>')
    
    metrics = [
        {"val": "₹30L+ MRR", "lbl": "Peak Bootstrapped Run Rate", "x": 25, "y": 90},
        {"val": "26,000+", "lbl": "Active Community Built", "x": 240, "y": 90},
        {"val": "100+", "lbl": "Live Offline Events Executed", "x": 25, "y": 150},
        {"val": "₹0", "lbl": "Paid Ad Spend", "x": 240, "y": 150},
    ]
    
    for m in metrics:
        out.append(f'<text x="{m["x"]}" y="{m["y"]}" font-size="22" font-weight="800" fill="{c["text"]}">{m["val"]}</text>')
        out.append(f'<text x="{m["x"]}" y="{m["y"]+18}" font-size="11" font-weight="500" fill="{c["muted"]}">{m["lbl"]}</text>')
        
    out.append('</svg>')
    return "".join(out)

def render_project_card(proj, theme):
    c = THEMES[theme]
    W, H = 420, 150
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="ui-sans-serif, system-ui, sans-serif">']
    out.append(f'<rect width="{W-1}" height="{H-1}" x="0.5" y="0.5" rx="10" fill="{c["bg"]}" stroke="{c["border"]}"/>')
    
    # Title
    out.append(f'<text x="20" y="35" font-size="16" font-weight="700" fill="{c["title"]}">{esc(proj["name"])}</text>')
    
    # Description
    lines = textwrap.wrap(proj["description"], width=55)
    y_offset = 60
    for line in lines[:3]:
        out.append(f'<text x="20" y="{y_offset}" font-size="13" fill="{c["text"]}">{esc(line)}</text>')
        y_offset += 18
        
    # Bottom Row: Language + Tags only (Removed fake stars/forks to fix overlap)
    bottom_y = H - 20
    lang = proj.get("language", "TypeScript")
    lcolor = LANG_COLORS.get(lang, "#8b949e")
    
    out.append(f'<circle cx="25" cy="{bottom_y - 4}" r="6" fill="{lcolor}"/>')
    out.append(f'<text x="38" y="{bottom_y}" font-size="12" fill="{c["text"]}">{esc(lang)}</text>')
    
    # Tags
    tag_x = 120
    for tag in proj.get("tags", [])[:3]:
        # Approximate tag width
        tag_w = len(tag) * 7.5 + 16
        out.append(f'<rect x="{tag_x}" y="{bottom_y - 14}" width="{tag_w}" height="20" rx="10" fill="{c["tag_bg"]}"/>')
        out.append(f'<text x="{tag_x + tag_w/2}" y="{bottom_y + 1}" font-size="11" font-weight="600" fill="{c["tag_text"]}" text-anchor="middle">{esc(tag)}</text>')
        tag_x += tag_w + 8
        
    out.append('</svg>')
    return "".join(out)

def main():
    Path("assets").mkdir(exist_ok=True)
    
    # Founder cards
    for t in ("dark", "light"):
        Path(f"assets/card-founder-{t}.svg").write_text(render_founder_card(t))
        
    # Project cards
    with open("assets/projects.json") as f:
        data = json.load(f)
        
    for proj in data.get("projects", []):
        for t in ("dark", "light"):
            fname = f"assets/card-{proj['repo']}-{t}.svg"
            Path(fname).write_text(render_project_card(proj, t))

if __name__ == "__main__":
    main()
