"""
Remove white background from ARPAN logo using only Pillow.
"""
from PIL import Image

def remove_white_bg(input_path, output_path, threshold=225):
    img = Image.open(input_path).convert('RGBA')
    pixels = img.load()
    w, h = img.size
    
    count = 0
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            # If pixel is white or near-white, make transparent
            if r > threshold and g > threshold and b > threshold:
                pixels[x, y] = (r, g, b, 0)
                count += 1
            elif r > (threshold - 30) and g > (threshold - 30) and b > (threshold - 30):
                # Transition zone: partially transparent for smoother edges
                min_val = min(r, g, b)
                alpha_ratio = max(0, (threshold - min_val)) / 30.0
                new_alpha = int(min(a, alpha_ratio * 255))
                pixels[x, y] = (r, g, b, new_alpha)
    
    img.save(output_path, 'PNG')
    print(f"Done! Removed {count:,} white pixels.")
    print(f"Saved to: {output_path}")

if __name__ == '__main__':
    remove_white_bg('LOGO_ARPAN.png', 'images/logo_transparent.png')
