#!/usr/bin/env python3
import json
from pathlib import Path

def esc(s): return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

THEMES = {
    "dark": {"bg": "#0d1117", "border": "#30363d", "title": "#58a6ff", "text": "#c9d1d9", "muted": "#8b949e", "tag_bg": "#1f2428", "tag_text": "#58a6ff", "star": "#e3b341", "fork": "#8b949e"},
    "light": {"bg": "#ffffff", "border": "#d0d7de", "title": "#0969da", "text": "#24292f", "muted": "#57606a", "tag_bg": "#f6f8fa", "tag_text": "#0969da", "star": "#bf8700", "fork": "#57606a"}
}

LANG_COLORS = {
    "TypeScript": "#3178c6", "JavaScript": "#f1e05a", "Python": "#3572A5", "React": "#61dafb", "HTML": "#e34c26"
}

def render_project_card(proj, theme):
    c = THEMES[theme]
    W, H = 420, 150
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="ui-sans-serif, system-ui, sans-serif">']
    out.append(f'<rect width="{W-1}" height="{H-1}" x="0.5" y="0.5" rx="6" fill="{c["bg"]}" stroke="{c["border"]}"/>')
    
    # Title
    out.append(f'<text x="20" y="32" font-size="16" font-weight="600" fill="{c["title"]}">{esc(proj["name"])}</text>')
    
    # Description
    words = proj["description"].split()
    lines, current = [], ""
    for w in words:
        if len(current + " " + w) * 7.5 > W - 40:
            lines.append(current)
            current = w
        else:
            current = (current + " " + w).strip()
    if current: lines.append(current)
    
    for i, line in enumerate(lines[:3]):
        out.append(f'<text x="20" y="{58 + i*18}" font-size="13" fill="{c["text"]}">{esc(line)}</text>')
        
    # Footer (Language, Stars, Forks, Tags)
    fy = H - 20
    x = 20
    
    if "language" in proj:
        lcol = LANG_COLORS.get(proj["language"], c["muted"])
        out.append(f'<circle cx="{x+6}" cy="{fy-4}" r="6" fill="{lcol}"/>')
        out.append(f'<text x="{x+18}" y="{fy}" font-size="12" fill="{c["text"]}">{esc(proj["language"])}</text>')
        x += 20 + len(proj["language"]) * 7.5 + 15
        
    out.append(f'<text x="{x}" y="{fy}" font-size="12" fill="{c["text"]}"><tspan fill="{c["star"]}">★</tspan> {proj["stars"]}</text>')
    x += 25 + len(str(proj["stars"])) * 7.5 + 15
    out.append(f'<text x="{x}" y="{fy}" font-size="12" fill="{c["text"]}"><tspan fill="{c["fork"]}">⑂</tspan> {proj["forks"]}</text>')
    
    # Tags right aligned
    tx = W - 20
    for tag in reversed(proj.get("tags", [])):
        tw = len(tag) * 7.5 + 16
        tx -= tw
        out.append(f'<rect x="{tx}" y="{fy-12}" width="{tw-6}" height="20" rx="10" fill="{c["tag_bg"]}"/>')
        out.append(f'<text x="{tx + (tw-6)/2}" y="{fy+2}" font-size="11" font-weight="500" fill="{c["tag_text"]}" text-anchor="middle">{esc(tag)}</text>')
        tx -= 10
        
    out.append('</svg>')
    return "".join(out)

def render_founder_card(theme):
    c = THEMES[theme]
    W, H = 480, 200
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="ui-sans-serif, system-ui, sans-serif">']
    out.append(f'<rect width="{W-1}" height="{H-1}" x="0.5" y="0.5" rx="10" fill="{c["bg"]}" stroke="{c["border"]}"/>')
    out.append(f'<text x="25" y="35" font-size="18" font-weight="700" fill="{c["title"]}">0-to-1 Founder Scale Metrics</text>')
    out.append(f'<line x1="25" y1="50" x2="{W-25}" y2="50" stroke="{c["border"]}" stroke-width="1"/>')
    
    metrics = [
        ("₹30L+ MRR", "Peak Bootstrapped Run Rate"),
        ("26,000+", "Active Community Built"),
        ("100+", "Live Offline Events Executed"),
        ("₹0", "Paid Ad Spend"),
    ]
    
    for i, (val, label) in enumerate(metrics):
        cx = 25 + (i % 2) * (W/2 - 10)
        cy = 85 + (i // 2) * 55
        out.append(f'<text x="{cx}" y="{cy}" font-size="24" font-weight="800" fill="{c["text"]}">{esc(val)}</text>')
        out.append(f'<text x="{cx}" y="{cy+18}" font-size="12" fill="{c["muted"]}">{esc(label)}</text>')
        
    out.append('</svg>')
    return "".join(out)

def main():
    Path("assets").mkdir(exist_ok=True)
    with open("assets/projects.json") as f:
        data = json.load(f)
        
    for theme in ("dark", "light"):
        Path(f"assets/card-founder-{theme}.svg").write_text(render_founder_card(theme))
        for proj in data["projects"]:
            Path(f"assets/card-{proj['repo']}-{theme}.svg").write_text(render_project_card(proj, theme))
            
if __name__ == "__main__":
    main()
