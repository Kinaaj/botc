import os
import subprocess
import glob

# === CONFIGURATION ===
# Path to Inkscape (Update this path!)
# Windows Example: r"C:\Program Files\Inkscape\bin\inkscape.exe"
# Mac/Linux Example: "inkscape"
INKSCAPE_PATH = r"C:\Program Files\Inkscape\bin\inkscape.exe"

# Output Dimensions (Pixels)
WIDTH = 400
HEIGHT = 400

# Output folder
OUTPUT_DIR = "icons_400px"

def export_svgs():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    svg_files = glob.glob("*.svg")

    if not svg_files:
        print("No .svg files found!")
        return

    print(f"Found {len(svg_files)} SVGs. Exporting to {WIDTH}x{HEIGHT}px PNGs...")

    for i, filename in enumerate(svg_files):
        name_no_ext = os.path.splitext(filename)[0]
        output_path = os.path.join(OUTPUT_DIR, f"{name_no_ext}.png")

        print(f"[{i+1}/{len(svg_files)}] Exporting {filename}...")

        cmd = [
            INKSCAPE_PATH,
            filename,
            "--export-type=png",
            f"--export-filename={output_path}",
            f"-w={WIDTH}",   # Width in pixels
            f"-h={HEIGHT}",  # Height in pixels
            
            # OPTION A: Use this if your SVG page size is already set to 400x400 (Recommended)
            "--export-area-page"
            
            # OPTION B: Use this if your SVG is A4 but the drawing is small
            # "--export-area-drawing" 
        ]

        try:
            # shell=True is often needed on Windows
            subprocess.run(cmd, check=True, shell=(os.name == 'nt'))
        except subprocess.CalledProcessError as e:
            print(f"Error exporting {filename}: {e}")

    print("Done!")

if __name__ == "__main__":
    export_svgs()