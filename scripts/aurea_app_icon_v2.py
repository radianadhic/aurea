"""
AUREA App Icon Generator v2 - Better inner triangle cutout
"""

from PIL import Image, ImageDraw, ImageFilter
import os

GOLD_LIGHT = (255, 215, 100)
GOLD_DARK = (184, 134, 11)
NAVY = (10, 25, 41)
NAVY_LIGHT = (26, 47, 71)


def create_gradient_icon(size):
    """Create AUREA icon - improved version with proper A shape."""
    img = Image.new('RGB', (size, size), NAVY)
    draw = ImageDraw.Draw(img)

    # Navy gradient
    for y in range(size):
        t = y / size
        r = int(NAVY[0] + (NAVY_LIGHT[0] - NAVY[0]) * t)
        g = int(NAVY[1] + (NAVY_LIGHT[1] - NAVY[1]) * t)
        b = int(NAVY[2] + (NAVY_LIGHT[2] - NAVY[2]) * t)
        draw.line([(0, y), (size, y)], fill=(r, g, b))

    # Gold A shape using polygon (more accurate)
    cx = size / 2
    margin = size * 0.24
    top_y = size * 0.30
    bottom_y = size * 0.72
    width = size - 2 * margin

    # A outer polygon points
    half_w = width / 2
    leg_w = width * 0.18  # leg thickness
    # apex
    apex = (cx, top_y)
    # right base
    right_base = (cx + half_w, bottom_y)
    # right inner
    right_inner_top = (cx + half_w * 0.7, top_y + (bottom_y - top_y) * 0.65)
    right_cross = (cx + half_w * 0.4, right_inner_top[1])
    left_cross = (cx - half_w * 0.4, right_inner_top[1])
    left_inner_top = (cx - half_w * 0.7, top_y + (bottom_y - top_y) * 0.65)
    left_base = (cx - half_w, bottom_y)
    right_base_inner = (cx + half_w - leg_w, bottom_y)
    left_base_inner = (cx - half_w + leg_w, bottom_y)

    a_outer = [
        apex,
        (cx + half_w * 0.3, top_y + (bottom_y - top_y) * 0.45),  # right slope top
        right_cross,
        left_cross,
        (cx - half_w * 0.3, top_y + (bottom_y - top_y) * 0.45),  # left slope top
        left_base,
        left_base_inner,
        # bottom flat then up the inside
        (cx - half_w * 0.3, bottom_y),
        (cx - half_w * 0.05, right_inner_top[1]),
        (cx + half_w * 0.05, right_inner_top[1]),
        (cx + half_w * 0.3, bottom_y),
        right_base_inner,
    ]

    # Draw gradient fill by rows
    rows = bottom_y - top_y
    for y_offset in range(int(rows) + 1):
        t = y_offset / rows
        color = (
            int(GOLD_LIGHT[0] + (GOLD_DARK[0] - GOLD_LIGHT[0]) * t),
            int(GOLD_LIGHT[1] + (GOLD_DARK[1] - GOLD_LIGHT[1]) * t),
            int(GOLD_LIGHT[2] + (GOLD_DARK[2] - GOLD_LIGHT[2]) * t),
        )
        # Width of A at this y
        y_pos = top_y + y_offset
        if y_pos < right_cross[1]:
            # Upper triangle part
            frac = y_pos / right_cross[1]
            half_w_at_y = half_w * frac
        else:
            # Lower part with cutout
            frac = (y_pos - right_cross[1]) / (bottom_y - right_cross[1])
            half_w_at_y = half_w * (right_cross[1] / bottom_y) + (half_w * 0.4 - half_w * (right_cross[1] / bottom_y)) * frac

        if half_w_at_y > 1:
            x_start = int(cx - half_w_at_y)
            x_end = int(cx + half_w_at_y)
            # Skip middle for cutout
            cross_frac = 0.15
            inner_left = int(cx - half_w_at_y * cross_frac)
            inner_right = int(cx + half_w_at_y * cross_frac)
            if y_pos > right_cross[1]:
                draw.line([(x_start, y_pos), (inner_left, y_pos)], fill=color)
                draw.line([(inner_right, y_pos), (x_end, y_pos)], fill=color)
            else:
                draw.line([(x_start, y_pos), (x_end, y_pos)], fill=color)

    # 3 golden dots (MD3G) - below the A
    dot_size = max(2, int(size * 0.028))
    dot_y = int(size * 0.83)
    for x_offset in [-0.20, 0, 0.20]:
        dx = int(size * (0.5 + x_offset))
        draw.ellipse(
            [dx - dot_size, dot_y - dot_size, dx + dot_size, dot_y + dot_size],
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

    print("Regenerating AUREA app icons v2...")

    for folder, size in android_sizes.items():
        target_dir = os.path.join(base_dir, 'android', 'app', 'src', 'main', 'res', folder)
        icon = create_gradient_icon(size)
        icon.save(os.path.join(target_dir, 'ic_launcher.png'))

    for name, size in ios_sizes.items():
        ios_dir = os.path.join(base_dir, 'ios', 'Runner', 'Assets.xcassets', 'AppIcon.appiconset')
        icon = create_gradient_icon(size)
        icon.save(os.path.join(ios_dir, f'{name}.png'))

    os.makedirs(icon_dir, exist_ok=True)
    master = create_gradient_icon(1024)
    master.save(os.path.join(icon_dir, 'aurea-icon-1024.png'))

    splash = create_gradient_icon(512)
    splash.save(os.path.join(icon_dir, 'aurea-splash-icon.png'))

    print(f"Done. Master icon: {os.path.join(icon_dir, 'aurea-icon-1024.png')}")


if __name__ == '__main__':
    main()
