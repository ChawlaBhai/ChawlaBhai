#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

def run_cmd(cmd):
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

def main():
    print("Building all SVG assets...")
    Path("assets").mkdir(exist_ok=True)
    
    # Generate animated portrait SVGs using dotify
    img_path = "C12CE87C-B389-4CAC-9524-97EB7067D397 copy.PNG"
    
    # 1. Base Portrait (Color)
    run_cmd([sys.executable, "scripts/dotify.py", img_path, "-o", "assets/portrait", 
             "--cols", "110", "--equalize", "--detail", "0.6", "--color", "--animate", "--reveal"])
    
    # 2. Theme Portraits (Dark/Light/Cyber/Ember)
    run_cmd([sys.executable, "scripts/dotify.py", img_path, "-o", "assets/portrait", 
             "--cols", "110", "--equalize", "--detail", "0.6", "--animate", "--reveal"])
             
    # Generate Radar Charts
    run_cmd([sys.executable, "scripts/generate_radar.py"])
    
    # Generate Custom Vector Cards
    run_cmd([sys.executable, "scripts/generate_cards.py"])
    
    print("Build complete!")

if __name__ == "__main__":
    main()
