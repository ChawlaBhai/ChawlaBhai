import re

with open('README.md', 'r') as f:
    content = f.read()

# Fix 1: Portrait Image to color version
old_portrait = """<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/portrait-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/portrait-light.svg">
  <img src="assets/portrait-dark.svg" width="320" alt="Sahaj Chawla (ChawlaBhai) dot matrix portrait">
</picture>"""
new_portrait = '<img src="assets/portrait.svg" width="320" alt="Sahaj Chawla (ChawlaBhai) dot matrix portrait">'
content = content.replace(old_portrait, new_portrait)

# Fix 2: Github Stats Card using live API
old_stats = """<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/card-stats-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/card-stats-light.svg">
  <img src="assets/card-stats-dark.svg" width="480" alt="github stats card">
</picture>"""
new_stats = """<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api?username=ChawlaBhai&show_icons=true&theme=dark&bg_color=0d1117&hide_border=true&title_color=58a6ff">
  <source media="(prefers-color-scheme: light)" srcset="https://github-readme-stats.vercel.app/api?username=ChawlaBhai&show_icons=true&theme=default&bg_color=ffffff&hide_border=true&title_color=0969da">
  <img src="https://github-readme-stats.vercel.app/api?username=ChawlaBhai&show_icons=true&theme=dark" width="480" alt="github stats card">
</picture>"""
content = content.replace(old_stats, new_stats)

# Fix 3: Snake URLs for correct repo
content = content.replace("ChawlaBhai/ChawlaBhai/output", "ChawlaBhai/ChawlaBhaiGithub/output")

with open('README.md', 'w') as f:
    f.write(content)
