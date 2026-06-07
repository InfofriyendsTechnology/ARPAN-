"""
Create a light/white version of the ARPAN logo for dark backgrounds.
- Dark green pixels → White
- Gold pixels → Brighter gold / light gold
"""
from PIL import Image

def create_light_logo(input_path, output_path):
    img = Image.open(input_path).convert('RGBA')
    pixels = img.load()
    w, h = img.size

    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            
            if a < 30:
                # Already transparent, skip
                continue
            
            # Detect dark green pixels (the ARPAN text and decorative elements)
            # Dark green: low R, medium G, low B
            is_dark = (r < 100 and g < 100 and b < 100)
            is_green = (g > r and g > b and r < 120 and b < 100)
            is_dark_green = is_dark or is_green
            
            # Detect gold pixels
            # Gold: high R, medium-high G, low B
            is_gold = (r > 150 and g > 120 and b < 120 and r > b * 1.5)
            
            # Detect near-white/light gray (background remnants)
            is_light = (r > 200 and g > 200 and b > 200)
            
            if is_light:
                # Make remaining light pixels transparent
                pixels[x, y] = (r, g, b, 0)
            elif is_gold:
                # Keep gold but make it slightly brighter/lighter
                new_r = min(255, int(r * 1.15))
                new_g = min(255, int(g * 1.15))
                new_b = min(255, int(b * 1.05))
                pixels[x, y] = (new_r, new_g, new_b, a)
            elif is_dark_green:
                # Convert dark green to white
                pixels[x, y] = (255, 255, 255, a)
            else:
                # Other colors - make them lighter
                # Shift toward white
                factor = 0.3
                new_r = min(255, int(r + (255 - r) * 0.75))
                new_g = min(255, int(g + (255 - g) * 0.75))
                new_b = min(255, int(b + (255 - b) * 0.75))
                pixels[x, y] = (new_r, new_g, new_b, a)

    img.save(output_path, 'PNG')
    print(f"Light logo saved to: {output_path}")

if __name__ == '__main__':
    create_light_logo('images/logo_transparent.png', 'images/logo_light.png')
