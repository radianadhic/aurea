"""
AUREA Logo Generator
Creates logo variants in SVG + PNG (multiple sizes including favicon).
Brand: AUREA - "The Gold Standard of Data"
"""
from __future__ import annotations

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ============================================================
# Brand Colors
# ============================================================
GOLD_PRIMARY = (212, 175, 55)       # #D4AF37 - primary gold
GOLD_LIGHT = (255, 215, 100)        # #FFD764 - highlight gold
GOLD_DARK = (184, 134, 11)          # #B8860B - deep gold
NAVY_PRIMARY = (10, 25, 41)         # #0A1929 - navy
NAVY_LIGHT = (26, 47, 71)            # #1A2F47 - light navy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

OUTPUT_DIR = Path("/home/user/aurea-brand")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# Helper: Get font
# ============================================================
def get_font(size: int, bold: bool = False):
    """Get system font with fallback."""
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


# ============================================================
# SVG Generator: Logo Mark (icon only)
# ============================================================
def generate_logo_mark_svg() -> str:
    """Generate the AUREA monogram logo mark as SVG.

    Design concept:
    - Stylized "A" letter forming a triangle/mountain shape
    - Gold gradient (representing "golden data")
    - Triangle base represents stability & foundation
    - Apex represents data reaching to the sky
    """
    return '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <!-- Gold gradient -->
    <linearGradient id="goldGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFD764"/>
      <stop offset="50%" stop-color="#D4AF37"/>
      <stop offset="100%" stop-color="#B8860B"/>
    </linearGradient>

    <!-- Inner glow -->
    <radialGradient id="innerGlow" cx="50%" cy="40%" r="60%">
      <stop offset="0%" stop-color="#FFE5A0" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#D4AF37" stop-opacity="0"/>
    </radialGradient>

    <!-- Drop shadow -->
    <filter id="dropShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="3"/>
      <feOffset dx="0" dy="2" result="offsetblur"/>
      <feComponentTransfer>
        <feFuncA type="linear" slope="0.4"/>
      </feComponentTransfer>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Background circle (navy) -->
  <circle cx="100" cy="100" r="95" fill="#0A1929" filter="url(#dropShadow)"/>
  <circle cx="100" cy="100" r="92" fill="url(#innerGlow)"/>

  <!-- Stylized "A" mark - golden triangle/mountain -->
  <!-- Outer A shape -->
  <path d="M 100 35 L 160 165 L 138 165 L 125 138 L 75 138 L 62 165 L 40 165 Z"
        fill="url(#goldGradient)"
        stroke="#B8860B"
        stroke-width="1.5"/>

  <!-- Crossbar of A (creating the "data layers" effect) -->
  <path d="M 84 120 L 116 120 L 110 108 L 90 108 Z"
        fill="#0A1929"
        opacity="0.85"/>

  <!-- Apex highlight (top of A) -->
  <path d="M 100 35 L 108 50 L 92 50 Z"
        fill="#FFE5A0"
        opacity="0.7"/>

  <!-- Small accent - 3 dots representing 3 Golden Data (GC, GA, GP) -->
  <circle cx="70" cy="150" r="3" fill="#FFD764" opacity="0.9"/>
  <circle cx="100" cy="150" r="3" fill="#FFD764" opacity="0.9"/>
  <circle cx="130" cy="150" r="3" fill="#FFD764" opacity="0.9"/>
</svg>'''


# ============================================================
# SVG Generator: Logo with Text (horizontal)
# ============================================================
def generate_logo_horizontal_svg() -> str:
    """Logo horizontal: mark + AUREA text + tagline."""
    return '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 200" width="800" height="200">
  <defs>
    <linearGradient id="goldGradient2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFD764"/>
      <stop offset="50%" stop-color="#D4AF37"/>
      <stop offset="100%" stop-color="#B8860B"/>
    </linearGradient>
    <radialGradient id="innerGlow2" cx="50%" cy="40%" r="60%">
      <stop offset="0%" stop-color="#FFE5A0" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#D4AF37" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <!-- Logo mark (left side) -->
  <g transform="translate(20, 20)">
    <circle cx="80" cy="80" r="75" fill="#0A1929"/>
    <circle cx="80" cy="80" r="72" fill="url(#innerGlow2)"/>
    <path d="M 80 25 L 130 135 L 112 135 L 100 110 L 60 110 L 48 135 L 30 135 Z"
          fill="url(#goldGradient2)" stroke="#B8860B" stroke-width="1.2"/>
    <path d="M 68 95 L 92 95 L 88 86 L 72 86 Z" fill="#0A1929" opacity="0.85"/>
    <path d="M 80 25 L 86 36 L 74 36 Z" fill="#FFE5A0" opacity="0.7"/>
    <circle cx="56" cy="120" r="2.5" fill="#FFD764" opacity="0.9"/>
    <circle cx="80" cy="120" r="2.5" fill="#FFD764" opacity="0.9"/>
    <circle cx="104" cy="120" r="2.5" fill="#FFD764" opacity="0.9"/>
  </g>

  <!-- Text: AUREA (right side) -->
  <g transform="translate(200, 90)">
    <text x="0" y="0"
          font-family="Georgia, 'Times New Roman', serif"
          font-size="80"
          font-weight="700"
          fill="url(#goldGradient2)"
          letter-spacing="6">AUREA</text>

    <!-- Tagline -->
    <text x="0" y="40"
          font-family="Helvetica, Arial, sans-serif"
          font-size="18"
          font-weight="400"
          fill="#0A1929"
          letter-spacing="3">THE GOLD STANDARD OF DATA</text>
  </g>
</svg>'''


# ============================================================
# SVG Generator: Logo with Text (vertical/stacked)
# ============================================================
def generate_logo_stacked_svg() -> str:
    """Logo stacked: mark on top, AUREA text below."""
    return '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 500" width="400" height="500">
  <defs>
    <linearGradient id="goldGradient3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFD764"/>
      <stop offset="50%" stop-color="#D4AF37"/>
      <stop offset="100%" stop-color="#B8860B"/>
    </linearGradient>
    <radialGradient id="innerGlow3" cx="50%" cy="40%" r="60%">
      <stop offset="0%" stop-color="#FFE5A0" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#D4AF37" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <!-- Logo mark (top) -->
  <g transform="translate(100, 30)">
    <circle cx="100" cy="100" r="95" fill="#0A1929"/>
    <circle cx="100" cy="100" r="92" fill="url(#innerGlow3)"/>
    <path d="M 100 30 L 165 170 L 143 170 L 130 142 L 70 142 L 57 170 L 35 170 Z"
          fill="url(#goldGradient3)" stroke="#B8860B" stroke-width="1.5"/>
    <path d="M 80 122 L 120 122 L 114 108 L 86 108 Z" fill="#0A1929" opacity="0.85"/>
    <path d="M 100 30 L 109 47 L 91 47 Z" fill="#FFE5A0" opacity="0.7"/>
    <circle cx="68" cy="153" r="3" fill="#FFD764" opacity="0.9"/>
    <circle cx="100" cy="153" r="3" fill="#FFD764" opacity="0.9"/>
    <circle cx="132" cy="153" r="3" fill="#FFD764" opacity="0.9"/>
  </g>

  <!-- Text: AUREA (bottom) -->
  <text x="200" y="380"
        font-family="Georgia, 'Times New Roman', serif"
        font-size="90"
        font-weight="700"
        fill="url(#goldGradient3)"
        text-anchor="middle"
        letter-spacing="8">AUREA</text>

  <!-- Tagline -->
  <text x="200" y="425"
        font-family="Helvetica, Arial, sans-serif"
        font-size="18"
        font-weight="400"
        fill="#0A1929"
        text-anchor="middle"
        letter-spacing="4">THE GOLD STANDARD OF DATA</text>

  <!-- Decorative line -->
  <line x1="100" y1="445" x2="300" y2="445" stroke="#D4AF37" stroke-width="2"/>
  <text x="200" y="470"
        font-family="Helvetica, Arial, sans-serif"
        font-size="14"
        font-weight="300"
        fill="#666666"
        text-anchor="middle"
        letter-spacing="2">Master Data Management Platform</text>
</svg>'''


# ============================================================
# SVG Generator: Favicon (16x16, 32x32, 64x64)
# ============================================================
def generate_favicon_svg(size: int = 64) -> str:
    """Favicon - simplified version for small sizes."""
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}">
  <defs>
    <linearGradient id="goldFav" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFD764"/>
      <stop offset="100%" stop-color="#B8860B"/>
    </linearGradient>
  </defs>
  <rect width="{size}" height="{size}" fill="#0A1929" rx="{size // 8}"/>
  <path d="M {size*0.5} {size*0.18} L {size*0.82} {size*0.82} L {size*0.71} {size*0.82} L {size*0.65} {size*0.7} L {size*0.35} {size*0.7} L {size*0.29} {size*0.82} L {size*0.18} {size*0.82} Z"
        fill="url(#goldFav)"/>
  <path d="M {size*0.4} {size*0.6} L {size*0.6} {size*0.6} L {size*0.57} {size*0.54} L {size*0.43} {size*0.54} Z"
        fill="#0A1929"/>
</svg>'''


# ============================================================
# PNG Generator using PIL
# ============================================================
def generate_logo_png(size: int = 512, stacked: bool = False) -> Image.Image:
    """Generate PNG logo using PIL."""
    if stacked:
        # Stacked layout - more vertical space
        w, h = size, int(size * 1.4)
    else:
        # Mark only (square)
        w, h = size, size

    img = Image.new("RGBA", (w, h), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    if stacked:
        # Mark on top
        mark_size = int(size * 0.5)
        mark_x = (w - mark_size) // 2
        mark_y = int(size * 0.05)
        _draw_mark(draw, mark_x, mark_y, mark_size)

        # AUREA text below mark - auto-size to fit
        aurea_text = "AUREA"
        aurea_font_size = int(size * 0.13)
        aurea_font = get_font(aurea_font_size, bold=True)

        # Measure text
        bbox = draw.textbbox((0, 0), aurea_text, font=aurea_font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        # Scale down if too wide
        max_text_w = int(size * 0.85)
        if text_w > max_text_w:
            scale = max_text_w / text_w
            aurea_font_size = int(aurea_font_size * scale)
            aurea_font = get_font(aurea_font_size, bold=True)
            bbox = draw.textbbox((0, 0), aurea_text, font=aurea_font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]

        aurea_y = mark_y + mark_size + int(size * 0.08)
        aurea_x = (w - text_w) // 2
        draw.text((aurea_x, aurea_y), aurea_text, font=aurea_font, fill=GOLD_PRIMARY)

        # Decorative line
        line_y = aurea_y + text_h + int(size * 0.03)
        line_margin = int(size * 0.18)
        draw.line(
            [(line_margin, line_y), (w - line_margin, line_y)],
            fill=GOLD_PRIMARY, width=max(2, size // 120),
        )

        # Tagline below line
        tagline = "THE GOLD STANDARD OF DATA"
        tagline_font_size = int(size * 0.045)
        tagline_font = get_font(tagline_font_size, bold=False)

        # Draw with letter spacing
        total_tagline_w = _measure_text_with_spacing(tagline, tagline_font, tagline_font_size // 6)
        if total_tagline_w > max_text_w:
            tagline_font_size = int(tagline_font_size * (max_text_w / total_tagline_w))
            tagline_font = get_font(tagline_font_size, bold=False)

        spacing = tagline_font_size // 6
        total_w = _measure_text_with_spacing(tagline, tagline_font, spacing)
        tagline_x = (w - total_w) // 2
        tagline_y = line_y + int(size * 0.03)
        _draw_text_with_spacing(draw, tagline, tagline_x, tagline_y,
                                 tagline_font, NAVY_PRIMARY, spacing)
    else:
        _draw_mark(draw, 0, 0, size)

    return img


def _measure_text_with_spacing(text: str, font, spacing: int) -> int:
    """Measure total text width including spacing."""
    img = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(img)
    total = 0
    for i, char in enumerate(text):
        bbox = draw.textbbox((0, 0), char, font=font)
        char_w = bbox[2] - bbox[0]
        total += char_w + (spacing if i < len(text) - 1 else 0)
    return total


def _draw_mark(draw: ImageDraw.Draw, x: int, y: int, size: int) -> None:
    """Draw the AUREA logo mark (the A monogram in circle)."""
    # Background circle (navy)
    circle_radius = int(size * 0.47)
    cx, cy = x + size // 2, y + size // 2
    draw.ellipse(
        [cx - circle_radius, cy - circle_radius,
         cx + circle_radius, cy + circle_radius],
        fill=NAVY_PRIMARY,
    )

    # Draw the A shape (simplified)
    # Vertices for stylized A
    apex = (cx, cy - int(size * 0.32))
    bottom_left = (cx - int(size * 0.30), cy + int(size * 0.32))
    bottom_right = (cx + int(size * 0.30), cy + int(size * 0.32))

    # Outer A (gold)
    a_color = GOLD_PRIMARY
    # Use polygon for the A shape
    a_left = (cx - int(size * 0.18), cy + int(size * 0.32))
    a_right = (cx + int(size * 0.18), cy + int(size * 0.32))
    a_top = apex
    # Draw A as triangle
    draw.polygon(
        [a_top, a_right, a_left],
        fill=a_color,
    )

    # Inner cutout (to make it look like A)
    cutout_top = (cx, cy - int(size * 0.15))
    cutout_bottom_y = cy + int(size * 0.05)
    cutout_left = (cx - int(size * 0.10), cutout_bottom_y)
    cutout_right = (cx + int(size * 0.10), cutout_bottom_y)
    cutout_inner_left = (cx - int(size * 0.06), cy + int(size * 0.05))
    cutout_inner_right = (cx + int(size * 0.06), cy + int(size * 0.05))
    # Crossbar making it look like A
    draw.polygon(
        [cutout_top, cutout_right, cutout_inner_right, cutout_inner_left, cutout_left],
        fill=NAVY_PRIMARY,
    )

    # 3 golden dots (3 Golden Data)
    dot_y = cy + int(size * 0.25)
    dot_r = max(2, int(size * 0.025))
    for dx in [-int(size * 0.13), 0, int(size * 0.13)]:
        draw.ellipse(
            [cx + dx - dot_r, dot_y - dot_r, cx + dx + dot_r, dot_y + dot_r],
            fill=GOLD_LIGHT,
        )


def _draw_text(draw: ImageDraw.Draw, cx: int, y: int, text: str,
               font_size: int, centered: bool = False, navy: bool = False) -> None:
    """Draw text with optional centering."""
    if navy:
        font = get_font(font_size, bold=False)
    else:
        # Use larger font for AUREA and add spacing manually
        font = get_font(font_size, bold=True)

    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    x = cx - text_w // 2 if centered else cx
    color = NAVY_PRIMARY if navy else GOLD_PRIMARY

    # Add letter spacing for tagline
    if navy and " " in text:
        _draw_text_with_spacing(draw, text, x, y, font, color, spacing=font_size // 8)
    else:
        draw.text((x, y), text, font=font, fill=color)


def _draw_text_with_spacing(draw: ImageDraw.Draw, text: str,
                             x: int, y: int, font, color, spacing: int) -> None:
    """Draw text with extra spacing between characters."""
    current_x = x
    for char in text:
        draw.text((current_x, y), char, font=font, fill=color)
        bbox = draw.textbbox((0, 0), char, font=font)
        char_w = bbox[2] - bbox[0]
        current_x += char_w + spacing


# ============================================================
# Main: Generate all assets
# ============================================================
def main() -> None:
    print("=" * 60)
    print("AUREA Logo Generator")
    print("=" * 60)
    print()

    # 1. SVG files
    print("📄 Generating SVG files...")
    files = {
        "logo-mark.svg": generate_logo_mark_svg(),
        "logo-horizontal.svg": generate_logo_horizontal_svg(),
        "logo-stacked.svg": generate_logo_stacked_svg(),
        "favicon-16.svg": generate_favicon_svg(16),
        "favicon-32.svg": generate_favicon_svg(32),
        "favicon-64.svg": generate_favicon_svg(64),
    }
    for filename, content in files.items():
        path = OUTPUT_DIR / filename
        path.write_text(content)
        size_kb = path.stat().st_size / 1024
        print(f"  ✅ {filename} ({size_kb:.1f} KB)")

    # 2. PNG files
    print()
    print("🖼️  Generating PNG files...")
    png_files = {
        "logo-mark-512.png": (512, False),
        "logo-mark-256.png": (256, False),
        "logo-mark-128.png": (128, False),
        "logo-mark-64.png": (64, False),
        "logo-stacked-512.png": (512, True),
        "logo-stacked-256.png": (256, True),
    }
    for filename, (size, stacked) in png_files.items():
        img = generate_logo_png(size, stacked=stacked)
        path = OUTPUT_DIR / filename
        img.save(path, "PNG", optimize=True)
        size_kb = path.stat().st_size / 1024
        print(f"  ✅ {filename} ({size_kb:.1f} KB, {img.size[0]}x{img.size[1]})")

    # 3. Favicon variants (32x32 and 16x16)
    print()
    print("🎨 Generating favicons...")
    for size in [16, 32, 48, 64, 128]:
        img = generate_logo_png(size, stacked=False)
        path = OUTPUT_DIR / f"favicon-{size}x{size}.png"
        img.save(path, "PNG", optimize=True)
        size_kb = path.stat().st_size / 1024
        print(f"  ✅ favicon-{size}x{size}.png ({size_kb:.1f} KB)")

    # 4. ICO file (multi-size)
    print()
    print("💎 Generating favicon.ico...")
    favicon_16 = generate_logo_png(16)
    favicon_32 = generate_logo_png(32)
    favicon_48 = generate_logo_png(48)
    favicon_64 = generate_logo_png(64)
    favicon_128 = generate_logo_png(128)
    favicon_256 = generate_logo_png(256)
    ico_path = OUTPUT_DIR / "favicon.ico"
    favicon_256.save(
        ico_path,
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
    )
    print(f"  ✅ favicon.ico (multi-size: 16, 32, 48, 64, 128, 256)")

    # 5. Summary
    print()
    print("=" * 60)
    print(f"✅ Done! All assets saved to: {OUTPUT_DIR}")
    print("=" * 60)
    print()
    print("📁 Generated files:")
    for f in sorted(OUTPUT_DIR.iterdir()):
        size_kb = f.stat().st_size / 1024
        print(f"  - {f.name:35s} {size_kb:>6.1f} KB")
    print()
    print("🎨 Brand colors used:")
    print(f"  - Gold Primary:  #D4AF37 (RGB {GOLD_PRIMARY})")
    print(f"  - Gold Light:    #FFD764 (RGB {GOLD_LIGHT})")
    print(f"  - Gold Dark:     #B8860B (RGB {GOLD_DARK})")
    print(f"  - Navy Primary:  #0A1929 (RGB {NAVY_PRIMARY})")
    print(f"  - White:         #FFFFFF")
    print()
    print("📖 Usage:")
    print("  - favicon.ico         → web favicon (drop in /public)")
    print("  - logo-mark.svg       → icon-only logo (sidebar, app icon)")
    print("  - logo-horizontal.svg → header/email signature")
    print("  - logo-stacked.svg    → presentation cover, splash screen")


if __name__ == "__main__":
    main()
