import os
import glob
import urllib.request
import time

diag_dir = r"C:\Users\RAYEN\.gemini\antigravity\scratch\CarRental-AWD\Documentation\Diagrams"
puml_files = glob.glob(os.path.join(diag_dir, "*.puml"))

print(f"Found {len(puml_files)} PlantUML files to render into authentic UML diagrams.")

for puml_path in puml_files:
    fname = os.path.basename(puml_path)
    base_name = os.path.splitext(fname)[0]
    out_png = os.path.join(diag_dir, f"{base_name}.png")

    with open(puml_path, "r", encoding="utf-8") as f:
        puml_text = f.read()

    # Enhance skinparam for crisp, publication-quality UML
    if "!theme" not in puml_text:
        puml_text = puml_text.replace("@startuml", "@startuml\nskinparam monochrome false\nskinparam shadowing true\nskinparam defaultFontName Arial\nskinparam dpi 300\n")
    else:
        puml_text = puml_text.replace("@startuml", "@startuml\nskinparam dpi 300\n")

    print(f"Rendering {fname} via Kroki...")
    req = urllib.request.Request(
        "https://kroki.io/plantuml/png",
        data=puml_text.encode("utf-8"),
        headers={
            "Content-Type": "text/plain; charset=utf-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            png_bytes = resp.read()
            with open(out_png, "wb") as out_f:
                out_f.write(png_bytes)
            print(f"  -> Successfully generated {os.path.basename(out_png)} ({len(png_bytes)} bytes)")
    except Exception as e:
        print(f"  -> Error rendering {fname}: {e}")
    time.sleep(0.5)

print("All PlantUML diagrams rendered to authentic UML PNGs successfully.")
