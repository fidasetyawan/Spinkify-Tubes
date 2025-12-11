from PIL import Image, ImageDraw
import os

ASSETS_DIR = "assets"
if not os.path.exists(ASSETS_DIR):
    os.makedirs(ASSETS_DIR)

COLOR = "#ff69b4" # Hot Pink
BG_COLOR = (46, 46, 46) 
SIZE = (64, 64)
PADDING = 12

def create_image(name, size=SIZE):
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    return img, draw

def save_image(img, name):
    img.save(os.path.join(ASSETS_DIR, name))
    print(f"Saved {name}")

def create_icons():
    # 1. Play
    img, draw = create_image("play.png")
    points = [(PADDING + 10, PADDING), (PADDING + 10, SIZE[1] - PADDING), (SIZE[0] - PADDING, SIZE[1] // 2)]
    draw.polygon(points, fill=COLOR)
    save_image(img, "play.png")

    # 2. Pause
    img, draw = create_image("pause.png")
    bar_width = 12
    draw.rectangle([PADDING + 8, PADDING, PADDING + 8 + bar_width, SIZE[1] - PADDING], fill=COLOR)
    draw.rectangle([SIZE[0] - PADDING - 8 - bar_width, PADDING, SIZE[0] - PADDING - 8, SIZE[1] - PADDING], fill=COLOR)
    save_image(img, "pause.png")

    # 3. Next
    img, draw = create_image("next.png", (48, 48))
    draw.polygon([(10, 10), (30, 24), (10, 38)], fill=COLOR)
    draw.rectangle([30, 10, 35, 38], fill=COLOR)
    save_image(img, "next.png")

    # 4. Prev
    img, draw = create_image("prev.png", (48, 48))
    draw.polygon([(38, 10), (18, 24), (38, 38)], fill=COLOR)
    draw.rectangle([13, 10, 18, 38], fill=COLOR)
    save_image(img, "prev.png")

    # 5. Search
    img, draw = create_image("search.png", (32, 32))
    draw.ellipse([8, 8, 22, 22], outline=COLOR, width=2)
    draw.line([20, 20, 26, 26], fill=COLOR, width=2)
    save_image(img, "search.png")

    # 6. Plus (Add)
    img, draw = create_image("plus.png", (32, 32))
    draw.line([16, 8, 16, 24], fill=COLOR, width=2)
    draw.line([8, 16, 24, 16], fill=COLOR, width=2)
    save_image(img, "plus.png")

    # 7. Default Art
    img = Image.new('RGB', (100, 100), color=(50, 50, 50))
    draw = ImageDraw.Draw(img)
    draw.rectangle([20, 20, 80, 80], outline="white", width=2)
    draw.text((35, 40), "No Image", fill="white")
    save_image(img, "default_art.png")
    
    # 8. Heart Outline
    img, draw = create_image("heart_outline.png", (32, 32))
    draw.polygon([(16, 28), (4, 14), (4, 8), (10, 4), (16, 10), (22, 4), (28, 8), (28, 14)], outline="white", fill=None)
    save_image(img, "heart_outline.png")

    # 9. Heart Filled
    img, draw = create_image("heart_filled.png", (32, 32))
    draw.polygon([(16, 28), (4, 14), (4, 8), (10, 4), (16, 10), (22, 4), (28, 8), (28, 14)], fill=COLOR, outline=COLOR)
    save_image(img, "heart_filled.png")
    
    # 10. Play Small
    img, draw = create_image("play_small.png", (32, 32))
    draw.ellipse([0, 0, 31, 31], fill=COLOR)
    draw.polygon([(12, 8), (22, 16), (12, 24)], fill="white")
    save_image(img, "play_small.png")
    
    # 11. Plus Small
    img, draw = create_image("plus_small.png", (32, 32))
    draw.ellipse([0, 0, 31, 31], fill="#333333")
    draw.line([16, 8, 16, 24], fill="white", width=2)
    draw.line([8, 16, 24, 16], fill="white", width=2)
    save_image(img, "plus_small.png")
    
    # 12. Music Icon (for All Songs button)
    img, draw = create_image("music_icon.png", (24, 24))
    # Musical note
    draw.ellipse([8, 14, 16, 22], fill=COLOR)  # Note head
    draw.rectangle([15, 6, 17, 16], fill=COLOR)  # Stem
    draw.ellipse([4, 4, 10, 10], fill=COLOR)  # Top decoration
    save_image(img, "music_icon.png")

if __name__ == "__main__":
    create_icons()
