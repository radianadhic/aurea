"""
AUREA Animated Splash Screen - GIF Generator
Generates an animated GIF version of the AUREA splash screen for use in:
- README files
- Social media posts
- PowerPoint slides
- Any platform that doesn't support CSS/SVG animation
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Configuration
WIDTH, HEIGHT = 600, 600
FPS = 30
DURATION = 4.0  # seconds
TOTAL_FRAMES = int(FPS * DURATION)

# Brand colors
GOLD_PRIMARY = (212, 175, 55)  # #D4AF37
GOLD_LIGHT = (255, 215, 100)   # #FFD764
GOLD_DARK = (184, 134, 11)     # #B8860B
NAVY_PRIMARY = (10, 25, 41)    # #0A1929
NAVY_LIGHT = (26, 47, 71)      # #1A2F47
WHITE = (255, 255, 255)
GRAY = (143, 165, 189)         # #8FA5BD

# Easing function
def ease_out_cubic(t):
    return 1 - (1 - t) ** 3

def ease_out_back(t):
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2

def lerp(a, b, t):
    return a + (b - a) * t

def lerp_color(c1, c2, t):
    return tuple(int(lerp(c1[i], c2[i], t)) for i in range(3))


def draw_aurea_frame(frame_num, total_frames):
    """Draw a single frame of the AUREA animation."""
    img = Image.new('RGB', (WIDTH, HEIGHT), NAVY_PRIMARY)
    draw = ImageDraw.Draw(img, 'RGBA')

    # Calculate timing
    t = frame_num / total_frames  # 0 to 1
    current_time = t * DURATION   # 0 to 4 seconds

    # ===== Background gradient =====
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        color = lerp_color(NAVY_PRIMARY, NAVY_LIGHT, ratio)
        draw.line([(0, y), (WIDTH, y)], fill=color)

    # ===== Floating particles =====
    for i, x_pos in enumerate([100, 180, 300, 420, 500]):
        particle_time = (current_time * 0.7 + i * 0.4) % 3
        if particle_time < 2.5:
            y_pos = int(HEIGHT - (particle_time / 2.5) * HEIGHT)
            opacity = 0.6 if 0.2 < particle_time < 2.3 else 0
            color = GOLD_PRIMARY if i % 2 == 0 else GOLD_LIGHT
            size = 3 if i % 2 == 0 else 2
            draw.ellipse(
                [x_pos - size, y_pos - size, x_pos + size, y_pos + size],
                fill=color + (int(255 * opacity),)
            )

    # ===== Pulse rings =====
    if current_time > 0.5:
        pulse_t = (current_time - 0.5) % 1.5
        if pulse_t < 1.2:
            progress = pulse_t / 1.2
            radius = int(120 + 60 * ease_out_cubic(progress))
            opacity = int(255 * (1 - progress) * 0.6)
            for r in [radius, radius + 20]:
                draw.ellipse(
                    [300 - r, 280 - r, 300 + r, 280 + r],
                    outline=GOLD_PRIMARY + (opacity,),
                    width=2
                )

    # ===== Main circle (expands from 0) =====
    if current_time < 0.8:
        circle_progress = current_time / 0.8
        radius = int(120 * ease_out_back(circle_progress))
        # Outer dark circle
        draw.ellipse(
            [300 - radius, 280 - radius, 300 + radius, 280 + radius],
            fill=NAVY_PRIMARY,
            outline=NAVY_LIGHT,
            width=2
        )
    else:
        # Full circle
        draw.ellipse(
            [180, 160, 420, 400],
            fill=NAVY_PRIMARY,
            outline=NAVY_LIGHT,
            width=2
        )

    # ===== A triangle (drops in at t=0.5s) =====
    if 0.5 < current_time < 1.3:
        a_progress = (current_time - 0.5) / 0.8
        drop_offset = int(50 * (1 - ease_out_back(a_progress)))

        # Main A shape
        a_points = [
            (300, 195 + drop_offset),
            (365, 350 + drop_offset),
            (340, 350 + drop_offset),
            (322, 315 + drop_offset),
            (278, 315 + drop_offset),
            (260, 350 + drop_offset),
            (235, 350 + drop_offset),
        ]
        # Draw with gradient effect
        draw.polygon(a_points, fill=GOLD_PRIMARY)

        # A cutout
        if current_time > 1.1:
            cutout_points = [
                (285, 295 + drop_offset),
                (315, 295 + drop_offset),
                (308, 280 + drop_offset),
                (292, 280 + drop_offset),
            ]
            draw.polygon(cutout_points, fill=NAVY_PRIMARY)

        # Bottom bar
        if current_time > 1.2:
            bar_y = 305 + drop_offset
            draw.rectangle(
                [268, bar_y, 332, bar_y + 10],
                fill=GOLD_PRIMARY
            )
    elif current_time >= 1.3:
        # Final A position
        a_points = [(300, 195), (365, 350), (340, 350), (322, 315), (278, 315), (260, 350), (235, 350)]
        draw.polygon(a_points, fill=GOLD_PRIMARY)

        cutout_points = [(285, 295), (315, 295), (308, 280), (292, 280)]
        draw.polygon(cutout_points, fill=NAVY_PRIMARY)

        draw.rectangle([268, 305, 332, 315], fill=GOLD_PRIMARY)

    # ===== 3 Golden Dots (pulse) =====
    if current_time > 1.3:
        for i, x in enumerate([270, 300, 330]):
            delay = 1.6 + i * 0.2
            if current_time > delay:
                pulse_t = (current_time - delay) % 2.0
                if pulse_t < 2.0:
                    pulse_progress = pulse_t / 2.0
                    radius = int(4 + 2 * abs(0.5 - pulse_progress) * 2)
                    draw.ellipse(
                        [x - radius, 335 - radius, x + radius, 335 + radius],
                        fill=GOLD_LIGHT
                    )

    # ===== AUREA Text (letter by letter) =====
    try:
        font_large = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf', 68)
        font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
        font_version = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 11)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_version = ImageFont.load_default()

    letters = ['A', 'U', 'R', 'E', 'A']
    for i, letter in enumerate(letters):
        appear_time = 1.6 + i * 0.15
        if current_time > appear_time:
            # Letter position
            x_pos = 140 + i * 80
            y_pos = 470
            # Draw with slight shadow for gold effect
            for offset in [(0, 0), (1, 1)]:
                draw.text(
                    (x_pos + offset[0], y_pos + offset[1]),
                    letter,
                    font=font_large,
                    fill=GOLD_PRIMARY
                )

    # ===== Divider line (expands from center) =====
    if 2.5 < current_time < 3.1:
        div_progress = (current_time - 2.5) / 0.6
        line_half = int(200 * ease_out_cubic(div_progress))
        draw.line(
            [(300 - line_half, 490), (300 + line_half, 490)],
            fill=GOLD_PRIMARY,
            width=2
        )
    elif current_time >= 3.1:
        draw.line([(100, 490), (500, 490)], fill=GOLD_PRIMARY, width=2)

    # ===== Tagline =====
    if current_time > 2.9:
        tagline_progress = min(1.0, (current_time - 2.9) / 0.5)
        if tagline_progress > 0:
            # Fade in
            text_color = tuple(int(GRAY[i] * tagline_progress) for i in range(3))
            tagline = "THE GOLD STANDARD OF DATA"

            # Calculate text width for centering
            bbox = draw.textbbox((0, 0), tagline, font=font_small)
            text_width = bbox[2] - bbox[0]
            x_center = (WIDTH - text_width) // 2

            draw.text(
                (x_center, 510),
                tagline,
                font=font_small,
                fill=text_color
            )

    # ===== Loading bar =====
    if current_time > 3.2:
        # Background bar
        draw.rectangle([200, 555, 400, 558], fill=GOLD_PRIMARY + (60,))

        # Progress bar
        if current_time > 3.4:
            progress = min(1.0, (current_time - 3.4) / 2.0)
            bar_width = int(200 * ease_out_cubic(progress))
            draw.rectangle([200, 555, 200 + bar_width, 558], fill=GOLD_PRIMARY)

    return img


def main():
    output_dir = '/home/user/aurea-brand'
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 60)
    print("  AUREA Animated Splash - GIF Generator")
    print("=" * 60)
    print(f"  Resolution: {WIDTH}x{HEIGHT}")
    print(f"  Duration:   {DURATION}s @ {FPS}fps")
    print(f"  Frames:     {TOTAL_FRAMES}")
    print("=" * 60)
    print()

    frames = []
    for i in range(TOTAL_FRAMES):
        if i % 10 == 0:
            print(f"  Rendering frame {i+1}/{TOTAL_FRAMES}...")
        frame = draw_aurea_frame(i, TOTAL_FRAMES)
        frames.append(frame)

    print()
    print("  Saving GIF...")
    output_path = os.path.join(output_dir, 'aurea-animated-splash.gif')
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=int(1000 / FPS),  # ms per frame
        loop=0,  # infinite loop
        optimize=True
    )

    file_size = os.path.getsize(output_path) / 1024
    print(f"  ✅ Saved: {output_path}")
    print(f"  File size: {file_size:.1f} KB")
    print()
    print("  🎉 Done! Use the GIF in:")
    print("     - README.md")
    print("     - Twitter/X posts")
    print("     - LinkedIn")
    print("     - PowerPoint slides")
    print("     - Documentation")
    print()

    # Also create a smaller "preview" GIF for README
    print("  Creating smaller preview GIF (300x300)...")
    small_frames = [f.resize((300, 300), Image.LANCZOS) for f in frames]
    preview_path = os.path.join(output_dir, 'aurea-splash-preview.gif')
    small_frames[0].save(
        preview_path,
        save_all=True,
        append_images=small_frames[1:],
        duration=int(1000 / FPS),
        loop=0,
        optimize=True
    )
    preview_size = os.path.getsize(preview_path) / 1024
    print(f"  ✅ Saved: {preview_path} ({preview_size:.1f} KB)")


if __name__ == '__main__':
    main()
