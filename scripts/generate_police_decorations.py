import os
from PIL import Image, ImageDraw

base_dir = r"C:\Users\ABC\Desktop\NIA\260625 6회차\6회차 과제\pixel-agents\webview-ui\public\assets\furniture"

def create_large_painting():
    # 32x32 pixels
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    pixels = img.load()
    
    # Colors
    FRAME = (51, 65, 85, 255) # Steel-blue frame
    BG = (30, 41, 59, 255)    # Dark background
    GOLD = (250, 204, 21, 255) # Gold shield
    GOLD_DARK = (202, 138, 4, 255)
    WHITE = (255, 255, 255, 255)
    BLUE = (29, 78, 216, 255)
    
    # Draw frame
    for y in range(32):
        for x in range(32):
            if x < 2 or x > 29 or y < 2 or y > 29:
                pixels[x, y] = FRAME
            else:
                pixels[x, y] = BG
                
    # Draw a shield shape (police emblem)
    # Shield points: top flat, curved sides to a bottom tip
    shield_pixels = [
        # (x, y)
        (15, 8), (16, 8),
        (12, 9), (13, 9), (14, 9), (15, 9), (16, 9), (17, 9), (18, 9), (19, 9),
        (11, 10), (12, 10), (13, 10), (14, 10), (15, 10), (16, 10), (17, 10), (18, 10), (19, 10), (20, 10),
    ]
    # Let's programmatically draw a shield with ImageDraw
    draw = ImageDraw.Draw(img)
    # Gold Shield Polygon
    draw.polygon([
        (10, 11), (21, 11), (22, 15), (20, 21), (16, 25), (15, 25), (11, 21), (9, 15)
    ], fill=GOLD, outline=GOLD_DARK)
    
    # Draw a blue star in the center
    # Center is at (15, 16)
    star_points = [
        (15, 13), (16, 13),
        (15, 14), (16, 14),
        (13, 15), (14, 15), (15, 15), (16, 15), (17, 15), (18, 15),
        (14, 16), (15, 16), (16, 16), (17, 16),
        (13, 17), (14, 17), (15, 17), (16, 17), (17, 17), (18, 17),
        (14, 18), (17, 18),
        (13, 19), (18, 19)
    ]
    for px, py in star_points:
        pixels[px, py] = BLUE
        
    # Add gold badge wings or highlights
    pixels[15, 15] = WHITE
    pixels[16, 15] = WHITE
    
    out_path = os.path.join(base_dir, "LARGE_PAINTING", "LARGE_PAINTING.png")
    img.save(out_path)
    print(f"Generated large police painting: {out_path}")

def create_small_painting_1():
    # 16x32 pixels
    # A police poster showing a red & blue siren light on top
    img = Image.new("RGBA", (16, 32), (0, 0, 0, 0))
    pixels = img.load()
    
    FRAME = (71, 85, 105, 255)
    BG = (15, 23, 42, 255)
    RED = (239, 68, 68, 255)
    BLUE = (59, 130, 246, 255)
    GOLD = (234, 179, 8, 255)
    WHITE = (248, 250, 252, 255)
    
    for y in range(32):
        for x in range(16):
            if x == 0 or x == 15 or y == 0 or y == 31:
                pixels[x, y] = FRAME
            else:
                pixels[x, y] = BG
                
    # Draw Siren (y: 4 to 12)
    # Siren stand
    for x in range(5, 11):
        pixels[x, 11] = (100, 116, 139, 255)
    # Siren light Left (Red)
    for y in range(6, 11):
        for x in range(4, 8):
            pixels[x, y] = RED
    # Siren light Right (Blue)
    for y in range(6, 11):
        for x in range(8, 12):
            pixels[x, y] = BLUE
            
    # Hangers/reflectors
    pixels[5, 5] = WHITE
    pixels[10, 5] = WHITE
    
    # Bottom text representation "POLICE"
    # P
    pixels[3, 18] = WHITE; pixels[4, 18] = WHITE
    pixels[3, 19] = WHITE; pixels[5, 19] = WHITE
    pixels[3, 20] = WHITE; pixels[4, 20] = WHITE
    pixels[3, 21] = WHITE
    pixels[3, 22] = WHITE
    
    # O
    pixels[7, 18] = WHITE; pixels[8, 18] = WHITE
    pixels[6, 19] = WHITE; pixels[9, 19] = WHITE
    pixels[6, 20] = WHITE; pixels[9, 20] = WHITE
    pixels[6, 21] = WHITE; pixels[9, 21] = WHITE
    pixels[7, 22] = WHITE; pixels[8, 22] = WHITE
    
    # L
    pixels[11, 18] = WHITE
    pixels[11, 19] = WHITE
    pixels[11, 20] = WHITE
    pixels[11, 21] = WHITE
    pixels[11, 22] = WHITE; pixels[12, 22] = WHITE; pixels[13, 22] = WHITE

    out_path = os.path.join(base_dir, "SMALL_PAINTING", "SMALL_PAINTING.png")
    img.save(out_path)
    print(f"Generated small police painting 1: {out_path}")

def create_small_painting_2():
    # 16x32 pixels
    # A police poster showing the police mascot/badge and Korean flag symbol
    img = Image.new("RGBA", (16, 32), (0, 0, 0, 0))
    pixels = img.load()
    
    FRAME = (71, 85, 105, 255)
    BG = (30, 41, 59, 255)
    RED = (239, 68, 68, 255)
    BLUE = (59, 130, 246, 255)
    GOLD = (234, 179, 8, 255)
    WHITE = (255, 255, 255, 255)
    
    for y in range(32):
        for x in range(16):
            if x == 0 or x == 15 or y == 0 or y == 31:
                pixels[x, y] = FRAME
            else:
                pixels[x, y] = BG
                
    # Draw Police Eagle symbol (simplified)
    # Eagle wings
    for y in range(6, 10):
        pixels[3, y] = WHITE
        pixels[12, y] = WHITE
    for y in range(7, 11):
        pixels[4, y] = WHITE
        pixels[11, y] = WHITE
    # Eagle head
    pixels[7, 5] = GOLD
    pixels[8, 5] = GOLD
    pixels[7, 6] = WHITE
    pixels[8, 6] = WHITE
    # Eagle body/emblem
    for y in range(7, 12):
        for x in range(5, 11):
            pixels[x, y] = GOLD
            
    # Taegeuk symbol (Red/Blue center) in emblem
    pixels[7, 8] = RED
    pixels[8, 8] = BLUE
    pixels[7, 9] = RED
    pixels[8, 9] = BLUE

    # Bottom letters "112"
    # 1
    pixels[4, 18] = WHITE
    pixels[4, 19] = WHITE
    pixels[4, 20] = WHITE
    # 1
    pixels[7, 18] = WHITE
    pixels[7, 19] = WHITE
    pixels[7, 20] = WHITE
    # 2
    pixels[10, 18] = WHITE; pixels[11, 18] = WHITE
    pixels[11, 19] = WHITE
    pixels[10, 20] = WHITE; pixels[11, 20] = WHITE

    out_path = os.path.join(base_dir, "SMALL_PAINTING_2", "SMALL_PAINTING_2.png")
    img.save(out_path)
    print(f"Generated small police painting 2: {out_path}")

create_large_painting()
create_small_painting_1()
create_small_painting_2()
