import os
import glob
import zlib
import urllib.request
import time

def plantuml_encode(text):
    zlib_bytes = zlib.compress(text.encode('utf-8'))
    compressed = zlib_bytes[2:-4] # strip zlib header and checksum
    
    mapping = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
    
    def encode_3bytes(b1, b2, b3):
        c1 = b1 >> 2
        c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
        c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
        c4 = b3 & 0x3F
        return mapping[c1] + mapping[c2] + mapping[c3] + mapping[c4]
        
    def encode_2bytes(b1, b2):
        c1 = b1 >> 2
        c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
        c3 = (b2 & 0xF) << 2
        return mapping[c1] + mapping[c2] + mapping[c3]
        
    def encode_1byte(b1):
        c1 = b1 >> 2
        c2 = (b1 & 0x3) << 4
        return mapping[c1] + mapping[c2]

    res = []
    i = 0
    n = len(compressed)
    while i < n:
        if i + 2 < n:
            res.append(encode_3bytes(compressed[i], compressed[i+1], compressed[i+2]))
            i += 3
        elif i + 1 < n:
            res.append(encode_2bytes(compressed[i], compressed[i+1]))
            i += 2
        else:
            res.append(encode_1byte(compressed[i]))
            i += 1
            
    return "".join(res)

diag_dir = r"C:\Users\RAYEN\.gemini\antigravity\scratch\CarRental-AWD\Documentation\Diagrams"
puml_files = glob.glob(os.path.join(diag_dir, "*.puml"))

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/png,image/*;q=0.8'
}

print(f"Total PUML files to process: {len(puml_files)}")

for puml_path in puml_files:
    fname = os.path.basename(puml_path)
    base_name = os.path.splitext(fname)[0]
    out_png = os.path.join(diag_dir, f"{base_name}.png")
    
    with open(puml_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Ensure standard clean UML styling
    if "skinparam" not in content:
        content = content.replace("@startuml", "@startuml\nskinparam monochrome false\nskinparam shadowing true\nskinparam defaultFontName Arial\n")
        
    encoded = plantuml_encode(content)
    url = f"https://www.plantuml.com/plantuml/png/{encoded}"
    
    req = urllib.request.Request(url, headers=headers)
    try:
        print(f"Fetching official UML diagram for {fname}...")
        with urllib.request.urlopen(req, timeout=25) as resp:
            png_data = resp.read()
            with open(out_png, "wb") as out_f:
                out_f.write(png_data)
            print(f"  [OK] Saved {base_name}.png ({len(png_data)} bytes)")
    except Exception as e:
        print(f"  [FAIL] Error for {fname}: {e}")
        
    time.sleep(0.8)

print("Done rendering official PlantUML diagrams.")
