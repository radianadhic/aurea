"""
AUREA App Icon Generator
Generates app icons for Android and iOS in all required sizes.
"""

from PIL import Image, ImageDraw, ImageFilter
import os

# Brand colors
GOLD_PRIMARY = (212, 175, 55)  # #D4AF37
GOLD_LIGHT = (255, 215, 100)   # #FFD764
GOLD_DARK = (184, 134, 11)     # #B8860B
NAVY = (10, 25, 41)            # #0A1929
NAVY_LIGHT = (26, 47, 71)      # #1A2F47


def create_gradient_icon(size):
    """Create AUREA icon with gold gradient on navy."""
    img = Image.new('RGB', (size, size), NAVY)
    draw = ImageDraw.Draw(img)

    # Navy gradient background
    for y in range(size):
        ratio = y / size
        r = int(NAVY[0] + (NAVY_LIGHT[0] - NAVY[0]) * ratio)
        g = int(NAVY[1] + (NAVY_LIGHT[1] - NAVY[1]) * ratio)
        b = int(NAVY[2] + (NAVY_LIGHT[2] - NAVY[2]) * ratio)
        draw.line([(0, y), (size, y)], fill=(r, g, b))

    # Gold A triangle
    margin = int(size * 0.22)
    triangle_width = size - 2 * margin
    triangle_height = int(triangle_width * 1.1)
    apex_x = size // 2
    apex_y = int(size * 0.28)

    for y_offset in range(triangle_height + 1):
        t = y_offset / triangle_height
        color = (
            int(GOLD_LIGHT[0] + (GOLD_DARK[0] - GOLD_LIGHT[0]) * t),
            int(GOLD_LIGHT[1] + (GOLD_DARK[1] - GOLD_LIGHT[1]) * t),
            int(GOLD_LIGHT[2] + (GOLD_DARK[2] - GOLD_LIGHT[2]) * t),
        )
        width_at_y = triangle_width * (1 - y_offset / triangle_height) * 0.7
        if width_at_y > 0:
            y_pos = apex_y + y_offset
            x_start = int(apex_x - width_at_y / 2)
            x_end = int(apex_x + width_at_y / 2)
            draw.line([(x_start, y_pos), (x_end, y_pos)], fill=color)

    # A bottom bar
    bar_y = int(apex_y + triangle_height - triangle_height * 0.13)
    bar_height = max(1, int(triangle_height * 0.08))
    bar_left = apex_x - int(triangle_width * 0.3)
    bar_right = apex_x + int(triangle_width * 0.3)
    for y in range(bar_height):
        t = y / bar_height
        color = (
            int(GOLD_LIGHT[0] + (GOLD_DARK[0] - GOLD_LIGHT[0]) * t),
            int(GOLD_LIGHT[1] + (GOLD_DARK[1] - GOLD_LIGHT[1]) * t),
            int(GOLD_LIGHT[2] + (GOLD_DARK[2] - GOLD_LIGHT[2]) * t),
        )
        draw.line([(bar_left, bar_y + y), (bar_right, bar_y + y)], fill=color)

    # 3 golden dots (MD3G)
    dot_size = max(2, int(size * 0.025))
    dot_y = int(size * 0.78)
    for x_offset in [-0.18, 0, 0.18]:
        cx = int(size * (0.5 + x_offset))
        draw.ellipse(
            [cx - dot_size, dot_y - dot_size, cx + dot_size, dot_y + dot_size],
            fill=GOLD_LIGHT,
        )

    img = img.filter(ImageFilter.SMOOTH)
    return img


def main():
    base_dir = '/home/user/aurea-mobile'
    icon_dir = os.path.join(base_dir, 'assets', 'icons')

    android_sizes = {
        'mipmap-mdpi': 48,
        'mipmap-hdpi': 72,
        'mipmap-xhdpi': 96,
        'mipmap-xxhdpi': 144,
        'mipmap-xxxhdpi': 192,
    }

    ios_sizes = {
        'Icon-App-20x20@1x': 20,
        'Icon-App-20x20@2x': 40,
        'Icon-App-20x20@3x': 60,
        'Icon-App-29x29@1x': 29,
        'Icon-App-29x29@2x': 58,
        'Icon-App-29x29@3x': 87,
        'Icon-App-40x40@1x': 40,
        'Icon-App-40x40@2x': 80,
        'Icon-App-40x40@3x': 120,
        'Icon-App-60x60@2x': 120,
        'Icon-App-60x60@3x': 180,
        'Icon-App-76x76@1x': 76,
        'Icon-App-76x76@2x': 152,
        'Icon-App-83.5x83.5@2x': 167,
        'Icon-App-1024x1024': 1024,
    }

    print("Generating AUREA app icons...")

    print("\n  Android:")
    for folder, size in android_sizes.items():
        target_dir = os.path.join(base_dir, 'android', 'app', 'src', 'main', 'res', folder)
        os.makedirs(target_dir, exist_ok=True)
        icon = create_gradient_icon(size)
        icon.save(os.path.join(target_dir, 'ic_launcher.png'))
        print(f"    OK  {folder}/ic_launcher.png ({size}x{size})")

    print("\n  iOS:")
    ios_dir = os.path.join(base_dir, 'ios', 'Runner', 'Assets.xcassets', 'AppIcon.appiconset')
    os.makedirs(ios_dir, exist_ok=True)
    for name, size in ios_sizes.items():
        icon = create_gradient_icon(size)
        icon.save(os.path.join(ios_dir, f'{name}.png'))
        print(f"    OK  {name}.png ({size}x{size})")

    print("\n  Master:")
    os.makedirs(icon_dir, exist_ok=True)
    master_icon = create_gradient_icon(1024)
    master_path = os.path.join(icon_dir, 'aurea-icon-1024.png')
    master_icon.save(master_path)
    print(f"    OK  aurea-icon-1024.png (1024x1024)")

    print("\n  Splash:")
    splash = create_gradient_icon(512)
    splash_path = os.path.join(icon_dir, 'aurea-splash-icon.png')
    splash.save(splash_path)
    print(f"    OK  aurea-splash-icon.png (512x512)")

    print("\n  Adaptive (foreground only, transparent):")
    fg = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
    fg_draw = ImageDraw.Draw(fg)
    size = 1024
    margin = int(size * 0.32)
    triangle_width = size - 2 * margin
    triangle_height = int(triangle_width * 1.1)
    apex_x = size // 2
    apex_y = int(size * 0.28)

    for y_offset in range(triangle_height + 1):
        t = y_offset / triangle_height
        color = (
            int(GOLD_LIGHT[0] + (GOLD_DARK[0] - GOLD_LIGHT[0]) * t),
            int(GOLD_LIGHT[1] + (GOLD_DARK[1] - GOLD_LIGHT[1]) * t),
            int(GOLD_LIGHT[2] + (GOLD_DARK[2] - GOLD_LIGHT[2]) * t),
            255,
        )
        width_at_y = triangle_width * (1 - y_offset / triangle_height) * 0.7
        if width_at_y > 0:
            y_pos = apex_y + y_offset
            x_start = int(apex_x - width_at_y / 2)
            x_end = int(apex_x + width_at_y / 2)
            fg_draw.line([(x_start, y_pos), (x_end, y_pos)], fill=color)

    dot_size = int(size * 0.025)
    dot_y = int(size * 0.78)
    for x_offset in [-0.18, 0, 0.18]:
        cx = int(size * (0.5 + x_offset))
        fg_draw.ellipse(
            [cx - dot_size, dot_y - dot_size, cx + dot_size, dot_y + dot_size],
            fill=GOLD_LIGHT + (255,),
        )

    fg_path = os.path.join(base_dir, 'android', 'app', 'src', 'main', 'res', 'drawable', 'ic_launcher_foreground.png')
    fg.save(fg_path)
    print(f"    OK  ic_launcher_foreground.png (1024x1024)")

    print("\nAll AUREA app icons generated!")


if __name__ == '__main__':
    main()
