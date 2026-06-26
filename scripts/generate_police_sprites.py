import os
from PIL import Image

def generate_police_sprites():
    # Target directory for character sprites
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    public_char_dir = os.path.join(base_dir, "webview-ui", "public", "assets", "characters")
    dist_char_dir = os.path.join(base_dir, "dist", "assets", "characters")
    
    # Police theme color palette
    NAVY = (15, 23, 42, 255)         # Police trousers / dark accents
    LIGHT_BLUE = (186, 230, 253, 255)# Police uniform shirt
    LIGHT_BLUE_SHADE = (125, 211, 252, 255) # Shirt shadow
    GOLD = (234, 179, 8, 255)        # Gold police badge / belt buckle / buttons
    BLACK_CAP = (30, 41, 59, 255)    # Police cap brim / visor
    DARK_BLUE = (30, 58, 138, 255)   # Police cap crown

    # Exact known shirt color palettes for char_0 ~ char_5
    shirt_palettes = [
        # char_0
        {(17, 100, 169), (17, 73, 120), (15, 64, 106)},
        # char_1
        {(190, 119, 67), (126, 75, 41), (227, 159, 90)},
        # char_2
        {(246, 125, 32), (232, 114, 24), (232, 116, 27), (169, 29, 24), (139, 26, 22), (86, 17, 14)},
        # char_3
        {(255, 241, 239), (240, 225, 222), (218, 204, 201), (233, 215, 212), (255, 167, 124), (224, 141, 100), (172, 104, 71), (140, 88, 63)},
        # char_4
        {(189, 189, 189), (212, 212, 212), (238, 238, 238)},
        # char_5
        {(178, 71, 55), (225, 100, 81), (159, 63, 49), (100, 0, 38)}
    ]

    pants_palettes = [
        # char_0
        {(7, 28, 46), (15, 64, 106)},
        # char_1
        {(43, 43, 43), (16, 16, 16), (37, 37, 37)},
        # char_2
        {(35, 30, 29), (24, 22, 22), (40, 36, 35), (43, 40, 39)},
        # char_3
        {(121, 96, 100), (60, 49, 79), (76, 76, 76)},
        # char_4
        {(7, 28, 46), (15, 64, 106), (53, 53, 53)},
        # char_5
        {(51, 44, 35), (42, 35, 32), (29, 23, 24), (40, 40, 40), (48, 48, 48)}
    ]

    for char_idx in range(6):
        src_path = os.path.join(public_char_dir, f"char_{char_idx}.png")
        if not os.path.exists(src_path):
            continue

        img = Image.open(src_path).convert("RGBA")
        pixels = img.load()
        width, height = img.size # 112 x 96 (7 cols x 3 rows of 16x32)

        shirt_set = shirt_palettes[char_idx]
        pants_set = pants_palettes[char_idx]

        # Process each 16x32 frame
        for row in range(3):
            for col in range(7):
                cx = col * 16
                cy = row * 32

                # 1. Color swap clothes
                for ly in range(32):
                    for lx in range(16):
                        x = cx + lx
                        y = cy + ly
                        r, g, b, a = pixels[x, y]
                        if a == 0:
                            continue
                        
                        rgb = (r, g, b)
                        if rgb in shirt_set:
                            # Add subtle shading based on original brightness
                            if r + g + b < 350:
                                pixels[x, y] = LIGHT_BLUE_SHADE
                            else:
                                pixels[x, y] = LIGHT_BLUE
                        elif rgb in pants_set:
                            pixels[x, y] = NAVY

                # 2. Draw Korean police officer cap on head
                # Find top of head
                head_top_y = -1
                for ly in range(15):
                    for lx in range(16):
                        if pixels[cx + lx, cy + ly][3] > 0:
                            head_top_y = ly
                            break
                    if head_top_y != -1:
                        break

                if head_top_y != -1:
                    ty = head_top_y
                    
                    if row == 0:  # DOWN (facing front)
                        # Crown top
                        for lx in range(4, 12):
                            if pixels[cx + lx, cy + ty + 1][3] > 0 or lx in range(5, 11):
                                pixels[cx + lx, cy + ty] = DARK_BLUE
                                pixels[cx + lx, cy + ty + 1] = DARK_BLUE
                        # Crown band
                        for lx in range(4, 12):
                            pixels[cx + lx, cy + ty + 2] = DARK_BLUE
                        # Black Visor / Brim
                        for lx in range(4, 12):
                            pixels[cx + lx, cy + ty + 3] = BLACK_CAP
                        # Gold police emblem in center
                        pixels[cx + 7, cy + ty + 1] = GOLD
                        pixels[cx + 8, cy + ty + 1] = GOLD
                        pixels[cx + 7, cy + ty + 2] = GOLD
                        pixels[cx + 8, cy + ty + 2] = GOLD

                    elif row == 1:  # UP (facing back)
                        for lx in range(4, 12):
                            pixels[cx + lx, cy + ty] = DARK_BLUE
                            pixels[cx + lx, cy + ty + 1] = DARK_BLUE
                            pixels[cx + lx, cy + ty + 2] = DARK_BLUE
                            pixels[cx + lx, cy + ty + 3] = NAVY

                    elif row == 2:  # RIGHT (facing right)
                        for lx in range(5, 11):
                            pixels[cx + lx, cy + ty] = DARK_BLUE
                            pixels[cx + lx, cy + ty + 1] = DARK_BLUE
                        for lx in range(5, 12):
                            pixels[cx + lx, cy + ty + 2] = DARK_BLUE
                        # Visor pointing right
                        for lx in range(7, 13):
                            pixels[cx + lx, cy + ty + 3] = BLACK_CAP
                        # Gold emblem on side
                        pixels[cx + 10, cy + ty + 1] = GOLD
                        pixels[cx + 10, cy + ty + 2] = GOLD

        # Save back to public and dist
        img.save(src_path)
        dist_path = os.path.join(dist_char_dir, f"char_{char_idx}.png")
        if os.path.exists(os.path.dirname(dist_path)):
            img.save(dist_path)
        print(f"[OK] Successfully generated police uniform for char_{char_idx}.png")

if __name__ == "__main__":
    generate_police_sprites()
