import os
from PIL import Image

char_dir = r"C:\Users\ABC\Desktop\NIA\260625 6회차\6회차 과제\pixel-agents\webview-ui\public\assets\characters"

# Target colors for police theme
NAVY = (15, 23, 42, 255)       # Pants, hat, dark areas of uniform
LIGHT_BLUE = (186, 230, 253, 255) # Shirt
GOLD = (234, 179, 8, 255)       # Badge
BLACK_CAP = (30, 41, 59, 255)  # Cap brim and details
DARK_BLUE = (30, 58, 138, 255)  # Main cap color

def apply_police_theme(img_path, output_path, char_idx):
    img = Image.open(img_path).convert("RGBA")
    w, h = img.size
    pixels = img.load()
    
    # 1. Palette Swap: Detect clothing/features of each character and map to uniform colors
    # We identify original clothing pixels by coordinates or specific color ranges
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue
            
            # Identify shirt & pants colors based on original character palettes
            if char_idx == 0:
                # Original blue shirt/pants: (17, 73, 120), (7, 28, 46) etc.
                if (10 <= r <= 30) and (60 <= g <= 85) and (100 <= b <= 135):
                    pixels[x, y] = LIGHT_BLUE
                elif (3 <= r <= 15) and (15 <= g <= 35) and (35 <= b <= 60):
                    pixels[x, y] = NAVY
                elif (160 <= r <= 190) and (120 <= g <= 150) and (60 <= b <= 90):
                    pixels[x, y] = GOLD  # Golden belt/accents
            elif char_idx == 1:
                # Original orange-brown: (126, 75, 41), (190, 119, 67), (227, 159, 90)
                if (110 <= r <= 140) and (65 <= g <= 90) and (30 <= b <= 55):
                    pixels[x, y] = NAVY
                elif (180 <= r <= 235) and (110 <= g <= 170) and (60 <= b <= 100):
                    pixels[x, y] = LIGHT_BLUE
            elif char_idx == 2:
                # Original dark grey clothes and orange accents: (246, 125, 32)
                if (230 <= r <= 255) and (110 <= g <= 140) and (20 <= b <= 45):
                    pixels[x, y] = LIGHT_BLUE
                elif (20 <= r <= 45) and (15 <= g <= 40) and (15 <= b <= 40):
                    # Dark parts
                    pixels[x, y] = NAVY
            elif char_idx == 3:
                # Original pink/brownish clothes: (182, 115, 82), (176, 166, 163)
                if (170 <= r <= 230) and (100 <= g <= 130) and (70 <= b <= 100):
                    pixels[x, y] = LIGHT_BLUE
                elif (160 <= r <= 200) and (150 <= g <= 190) and (150 <= b <= 190):
                    pixels[x, y] = NAVY

    # 2. Draw Police Cap programmatically on each 16x32 frame
    # We iterate over each 16x32 cell: 7 columns, 3 rows
    for row in range(3):
        for col in range(7):
            cx = col * 16
            cy = row * 32
            
            # Find the top-most non-transparent pixel in this 16x32 frame to locate the head
            head_top_y = -1
            for ly in range(0, 16):
                for lx in range(0, 16):
                    if pixels[cx + lx, cy + ly][3] > 0:
                        head_top_y = ly
                        break
                if head_top_y != -1:
                    break
            
            # If no character detected in this frame, skip
            if head_top_y == -1 or head_top_y > 10:
                continue
            
            # Draw police cap relative to the top of the head
            if row == 0:  # DOWN (Facing front)
                # Cap top (dark blue/navy)
                for lx in range(5, 11):
                    pixels[cx + lx, cy + head_top_y] = DARK_BLUE
                    pixels[cx + lx, cy + head_top_y + 1] = DARK_BLUE
                # Cap brim (black)
                for lx in range(4, 12):
                    pixels[cx + lx, cy + head_top_y + 2] = BLACK_CAP
                # Gold badge in the center
                pixels[cx + 7, cy + head_top_y + 1] = GOLD
                pixels[cx + 8, cy + head_top_y + 1] = GOLD
                
            elif row == 1:  # UP (Facing back)
                # Cap top (dark blue)
                for lx in range(5, 11):
                    pixels[cx + lx, cy + head_top_y] = DARK_BLUE
                    pixels[cx + lx, cy + head_top_y + 1] = DARK_BLUE
                    pixels[cx + lx, cy + head_top_y + 2] = DARK_BLUE
                # Back brim/hair connection
                for lx in range(4, 12):
                    pixels[cx + lx, cy + head_top_y + 3] = BLACK_CAP
                    
            elif row == 2:  # RIGHT (Facing right)
                # Cap top (dark blue)
                for lx in range(5, 10):
                    pixels[cx + lx, cy + head_top_y] = DARK_BLUE
                    pixels[cx + lx, cy + head_top_y + 1] = DARK_BLUE
                # Brim extending right
                for lx in range(5, 12):
                    pixels[cx + lx, cy + head_top_y + 2] = BLACK_CAP
                # Gold badge on side-front
                pixels[cx + 9, cy + head_top_y + 1] = GOLD

    img.save(output_path)
    print(f"Generated police themed sprite: {output_path}")

# Apply to char_0.png through char_3.png
for i in range(4):
    p_path = os.path.join(char_dir, f"char_{i}.png")
    apply_police_theme(p_path, p_path, i)
