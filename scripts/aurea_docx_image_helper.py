"""
AUREA DOCX Image Generator
Creates composite images for the DOCX deliverable:
- Brand identity card
- Logo system overview
- Color palette swatches
- App mockups (text-based)
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Brand colors
GOLD_LIGHT = (255, 215, 100)
GOLD_PRIMARY = (212, 175, 55)
GOLD_DARK = (184, 134, 11)
NAVY_PRIMARY = (10, 25, 41)
NAVY_LIGHT = (26, 47, 71)
WHITE = (255, 255, 255)
GRAY_50 = (249, 250, 251)
GRAY_100 = (243, 244, 246)
GRAY_300 = (209, 213, 219)
GRAY_500 = (107, 114, 128)
GRAY_700 = (55, 65, 81)
GRAY_900 = (17, 24, 39)


def get_font(size, bold=False):
    paths = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                pass
    return ImageFont.load_default()


def create_brand_identity_card():
    """Create a brand identity overview card."""
    W, H = 1200, 800
    img = Image.new('RGB', (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    # Navy background left half
    draw.rectangle([0, 0, W // 2, H], fill=NAVY_PRIMARY)
    # Subtle gradient overlay
    for y in range(H):
        alpha = y / H
        r = int(NAVY_PRIMARY[0] + (NAVY_LIGHT[0] - NAVY_PRIMARY[0]) * alpha * 0.4)
        g = int(NAVY_PRIMARY[1] + (NAVY_LIGHT[1] - NAVY_PRIMARY[1]) * alpha * 0.4)
        b = int(NAVY_PRIMARY[2] + (NAVY_LIGHT[2] - NAVY_PRIMARY[2]) * alpha * 0.4)
        draw.line([(0, y), (W // 2, y)], fill=(r, g, b))

    # === LEFT SIDE: Logo + AUREA wordmark ===
    # Gold A triangle
    cx, cy = W // 4, H // 2 - 80
    a_w = 160
    a_h = 180
    a_points = [
        (cx, cy - a_h // 2),
        (cx + a_w // 2, cy + a_h // 2),
        (cx + a_w // 2 - 30, cy + a_h // 2),
        (cx + 12, cy - 10),
        (cx - 12, cy - 10),
        (cx - a_w // 2 + 30, cy + a_h // 2),
        (cx - a_w // 2, cy + a_h // 2),
    ]
    draw.polygon(a_points, fill=GOLD_PRIMARY)
    # Inner cutout
    inner = [
        (cx, cy - 30),
        (cx + 25, cy + 30),
        (cx + 18, cy + 30),
        (cx + 8, cy + 5),
        (cx - 8, cy + 5),
        (cx - 18, cy + 30),
        (cx - 25, cy + 30),
    ]
    draw.polygon(inner, fill=NAVY_PRIMARY)
    # A bottom bar
    draw.rectangle([cx - 50, cy + 35, cx + 50, cy + 50], fill=GOLD_PRIMARY)
    # 3 golden dots
    for x_off in [-30, 0, 30]:
        draw.ellipse([cx + x_off - 5, cy + 75, cx + x_off + 5, cy + 85], fill=GOLD_LIGHT)

    # AUREA wordmark
    f_big = get_font(72, bold=True)
    # Gold gradient effect (overlay multiple tones)
    for offset, color in [(0, GOLD_DARK), (0, GOLD_PRIMARY), (0, GOLD_LIGHT)]:
        draw.text((W // 4 - 100, H // 2 + 80), 'AUREA', font=f_big, fill=color)
    # Re-render with gradient
    aurea_text = 'AUREA'
    bbox = draw.textbbox((W // 4 - 100, H // 2 + 80), aurea_text, font=f_big)
    text_w = bbox[2] - bbox[0]
    for i, ch in enumerate(aurea_text):
        ratio = i / max(len(aurea_text) - 1, 1)
        color = tuple(int(GOLD_LIGHT[c] + (GOLD_DARK[c] - GOLD_LIGHT[c]) * ratio) for c in range(3))
        x = bbox[0] + i * 40 + 5
        draw.text((x, bbox[1]), ch, font=f_big, fill=color)

    # Tagline
    f_tag = get_font(14, bold=True)
    draw.text((W // 4 - 100, H // 2 + 180), 'THE GOLD STANDARD OF DATA', font=f_tag, fill=GOLD_LIGHT)

    # === RIGHT SIDE: Brand details ===
    f_title = get_font(36, bold=True)
    f_h = get_font(20, bold=True)
    f_body = get_font(16)
    f_small = get_font(13, bold=True)

    x_right = W // 2 + 60
    y = 80

    # Title
    draw.text((x_right, y), 'Brand Identity', font=f_title, fill=NAVY_PRIMARY)
    y += 50
    # Gold underline
    draw.rectangle([x_right, y, x_right + 120, y + 3], fill=GOLD_PRIMARY)
    y += 30

    # Name section
    draw.text((x_right, y), 'PRODUCT NAME', font=f_small, fill=GRAY_500)
    y += 22
    draw.text((x_right, y), 'AUREA', font=f_h, fill=NAVY_PRIMARY)
    y += 30
    draw.text((x_right + 80, y), '(Latin: "Golden")', font=f_body, fill=GRAY_500)
    y += 40

    # Tagline
    draw.text((x_right, y), 'TAGLINE', font=f_small, fill=GRAY_500)
    y += 22
    draw.text((x_right, y), 'The Gold Standard of Data', font=f_h, fill=NAVY_PRIMARY)
    y += 50

    # Colors section
    draw.text((x_right, y), 'COLOR PALETTE', font=f_small, fill=GRAY_500)
    y += 22
    colors = [
        ('Gold Primary', '#D4AF37', GOLD_PRIMARY),
        ('Gold Light', '#FFD764', GOLD_LIGHT),
        ('Gold Dark', '#B8860B', GOLD_DARK),
        ('Navy', '#0A1929', NAVY_PRIMARY),
    ]
    for name, hex_code, color in colors:
        # Swatch
        draw.rectangle([x_right, y, x_right + 36, y + 36], fill=color, outline=GRAY_300, width=1)
        # Label
        draw.text((x_right + 50, y + 4), name, font=f_body, fill=NAVY_PRIMARY)
        draw.text((x_right + 50, y + 22), hex_code, font=f_small, fill=GRAY_500)
        y += 50

    y += 10
    # Symbolism
    draw.text((x_right, y), 'SYMBOLISM', font=f_small, fill=GRAY_500)
    y += 22
    symbols = [
        ('Letter A', 'Aurea = first letter of brand'),
        ('Triangle', 'Stability & trust'),
        ('3 Gold Dots', 'MD3G (GC, GA, GP)'),
    ]
    for label, desc in symbols:
        draw.text((x_right, y), f'•  {label}', font=f_body, fill=NAVY_PRIMARY)
        draw.text((x_right + 110, y), f'— {desc}', font=f_body, fill=GRAY_500)
        y += 26

    return img


def create_color_palette():
    """Detailed color palette swatch sheet."""
    W, H = 1200, 700
    img = Image.new('RGB', (W, H), GRAY_50)
    draw = ImageDraw.Draw(img)

    f_title = get_font(32, bold=True)
    f_h = get_font(18, bold=True)
    f_body = get_font(14)
    f_small = get_font(12, bold=True)

    # Title
    draw.text((60, 50), 'AUREA Color System', font=f_title, fill=NAVY_PRIMARY)
    draw.text((60, 95), 'Brand colors for digital and print', font=f_body, fill=GRAY_500)

    # Primary section
    y = 160
    draw.text((60, y), 'PRIMARY', font=f_small, fill=GRAY_500)
    y += 25

    primary = [
        ('Gold 500', '#D4AF37', (212, 175, 55), WHITE),
        ('Gold 300', '#FFD764', GOLD_LIGHT, NAVY_PRIMARY),
        ('Gold 700', '#B8860B', GOLD_DARK, WHITE),
        ('Navy 600', '#0A1929', NAVY_PRIMARY, GOLD_PRIMARY),
        ('Navy 500', '#1A2F47', NAVY_LIGHT, GOLD_PRIMARY),
    ]
    x = 60
    for name, hex_c, color, text_color in primary:
        # Big swatch
        draw.rectangle([x, y, x + 200, y + 160], fill=color)
        # Border
        draw.rectangle([x, y, x + 200, y + 160], outline=GRAY_300, width=1)
        # Hex code on swatch
        draw.text((x + 16, y + 120), hex_c, font=get_font(16, bold=True), fill=text_color)
        # Name below
        draw.text((x, y + 175), name, font=f_h, fill=NAVY_PRIMARY)
        draw.text((x, y + 198), hex_c, font=f_body, fill=GRAY_500)
        x += 220

    # Semantic section
    y = 410
    draw.text((60, y), 'SEMANTIC', font=f_small, fill=GRAY_500)
    y += 25

    semantic = [
        ('Success', '#16A34A', (22, 163, 74)),
        ('Warning', '#EA580C', (234, 88, 12)),
        ('Error', '#DC2626', (220, 38, 38)),
        ('Info', '#0284C7', (2, 132, 199)),
    ]
    x = 60
    for name, hex_c, color in semantic:
        draw.rectangle([x, y, x + 200, y + 100], fill=color)
        draw.rectangle([x, y, x + 200, y + 100], outline=GRAY_300, width=1)
        draw.text((x + 16, y + 65), hex_c, font=get_font(14, bold=True), fill=WHITE)
        draw.text((x, y + 115), name, font=f_h, fill=NAVY_PRIMARY)
        draw.text((x, y + 138), hex_c, font=f_body, fill=GRAY_500)
        x += 220

    # Gradient strip
    y = 600
    draw.text((60, y), 'GOLD GRADIENT', font=f_small, fill=GRAY_500)
    grad_y = y + 25
    for x_off in range(W - 120):
        ratio = x_off / (W - 120)
        color = tuple(int(GOLD_LIGHT[c] + (GOLD_DARK[c] - GOLD_LIGHT[c]) * ratio) for c in range(3))
        draw.line([(60 + x_off, grad_y), (60 + x_off, grad_y + 30)], fill=color)
    draw.text((60, grad_y + 45), '#FFD764 → #D4AF37 → #B8860B', font=f_body, fill=GRAY_500)

    return img


def create_app_mockup_admin():
    """Mockup of AUREA Console admin dashboard."""
    W, H = 1400, 900
    img = Image.new('RGB', (W, H), GRAY_50)
    draw = ImageDraw.Draw(img)

    f_title = get_font(20, bold=True)
    f_h = get_font(16, bold=True)
    f_body = get_font(13)
    f_small = get_font(11, bold=True)
    f_tiny = get_font(10)

    # Sidebar (navy)
    draw.rectangle([0, 0, 240, H], fill=NAVY_PRIMARY)
    # Gold accent
    draw.rectangle([0, 0, 240, 4], fill=GOLD_PRIMARY)

    # Logo in sidebar
    cx, cy = 50, 50
    a_w = 24
    a_h = 28
    draw.polygon([
        (cx, cy - a_h // 2), (cx + a_w // 2, cy + a_h // 2),
        (cx + a_w // 2 - 5, cy + a_h // 2), (cx + 2, cy - 1),
        (cx - 2, cy - 1), (cx - a_w // 2 + 5, cy + a_h // 2), (cx - a_w // 2, cy + a_h // 2)
    ], fill=GOLD_PRIMARY)
    for i, x_off in enumerate([-12, 0, 12]):
        draw.ellipse([cx + x_off - 2, cy + 18, cx + x_off + 2, cy + 22], fill=GOLD_LIGHT)

    # AUREA text
    draw.text((90, 38), 'AUREA', font=get_font(20, bold=True), fill=GOLD_PRIMARY)
    draw.text((90, 60), 'CONSOLE', font=get_font(8, bold=True), fill=GOLD_LIGHT)

    # Sidebar nav items
    nav_items = [
        ('📊', 'Dashboard', True),
        ('📈', 'Monitoring', False),
        ('⚙️', 'Configuration', False),
        ('📋', 'Reports', False),
        ('💚', 'System Health', False),
    ]
    y = 130
    draw.text((20, y), 'MAIN', font=f_tiny, fill=GOLD_LIGHT)
    y += 25
    for icon, label, active in nav_items:
        if active:
            draw.rectangle([12, y - 4, 228, y + 28], fill=GOLD_PRIMARY)
            # Active state
            draw.rectangle([12, y - 4, 15, y + 28], fill=GOLD_LIGHT)
            text_color = NAVY_PRIMARY
        else:
            text_color = (200, 210, 220)
        draw.text((28, y + 2), icon, font=f_body, fill=text_color)
        draw.text((58, y + 4), label, font=f_body, fill=text_color)
        y += 40

    y += 30
    draw.text((20, y), 'MANAGEMENT', font=f_tiny, fill=GOLD_LIGHT)
    y += 25
    for label in ['Operations', 'Security', 'Backup']:
        draw.text((28, y + 4), '•', font=f_body, fill=(200, 210, 220))
        draw.text((48, y + 4), label, font=f_body, fill=(200, 210, 220))
        y += 32

    # Main content area
    # Top bar
    draw.rectangle([240, 0, W, 60], fill=WHITE)
    draw.rectangle([240, 58, W, 60], fill=GRAY_300)
    # Gold bottom border
    draw.rectangle([240, 0, W, 2], fill=GOLD_PRIMARY)
    draw.text((270, 22), 'Dashboard', font=f_title, fill=NAVY_PRIMARY)
    # AUREA badge
    badge = 'AUREA'
    draw.rectangle([400, 26, 460, 46], fill=GOLD_PRIMARY)
    draw.text((414, 30), badge, font=f_tiny, fill=NAVY_PRIMARY)

    # Real-time indicator (right)
    draw.ellipse([W - 180, 28, W - 168, 40], fill=(22, 163, 74))
    draw.text((W - 160, 30), 'Real-time', font=f_tiny, fill=GRAY_700)

    # Content
    y = 90
    # Welcome / brand
    draw.text((270, y), 'Welcome to AUREA Console', font=f_title, fill=NAVY_PRIMARY)
    draw.text((270, y + 28), 'The Gold Standard of Data — Master Data Management Platform', font=f_body, fill=GRAY_500)
    y += 70

    # Stat cards
    stats = [
        ('Golden Customers', '12,847', '+8.2%', True),
        ('Golden Accounts', '28,193', '+3.1%', True),
        ('Golden Products', '1,452', '+12.4%', True),
        ('Data Quality', '98.7%', '+0.4%', True),
    ]
    sx = 270
    for label, value, trend, up in stats:
        # Card
        draw.rectangle([sx, y, sx + 250, y + 110], fill=WHITE, outline=GRAY_300)
        # Top gold bar
        draw.rectangle([sx, y, sx + 250, y + 3], fill=GOLD_PRIMARY)
        # Label
        draw.text((sx + 16, y + 16), label.upper(), font=f_small, fill=GRAY_500)
        # Value
        draw.text((sx + 16, y + 40), value, font=get_font(28, bold=True), fill=NAVY_PRIMARY)
        # Trend
        trend_color = (22, 163, 74) if up else (220, 38, 38)
        draw.text((sx + 16, y + 80), f'↑ {trend}', font=f_small, fill=trend_color)
        sx += 270

    y += 140

    # Recent activity table
    draw.text((270, y), 'Recent Activity', font=f_h, fill=NAVY_PRIMARY)
    y += 30
    # Table header
    draw.rectangle([270, y, W - 50, y + 36], fill=NAVY_PRIMARY)
    headers = ['Time', 'Event', 'User', 'Status']
    col_x = [290, 440, 720, 1100]
    for i, h in enumerate(headers):
        draw.text((col_x[i], y + 10), h, font=f_small, fill=GOLD_PRIMARY)
    y += 36

    rows = [
        ('10:42', 'Customer record updated', 'Siti W.', '✓'),
        ('10:38', 'KYC verification completed', 'Ahmad R.', '✓'),
        ('10:35', 'Matching queue processed', 'System', '✓'),
        ('10:30', 'New customer registered', 'Budi S.', '✓'),
    ]
    for i, (t, ev, u, s) in enumerate(rows):
        row_y = y + i * 32
        if i % 2 == 0:
            draw.rectangle([270, row_y, W - 50, row_y + 32], fill=WHITE)
        draw.text((col_x[0], row_y + 8), t, font=f_tiny, fill=GRAY_700)
        draw.text((col_x[1], row_y + 8), ev, font=f_tiny, fill=NAVY_PRIMARY)
        draw.text((col_x[2], row_y + 8), u, font=f_tiny, fill=GRAY_700)
        draw.text((col_x[3], row_y + 8), s, font=f_tiny, fill=(22, 163, 74))

    # Footer
    draw.text((270, H - 30), 'AUREA Console v1.0.0  •  Bank XYZ  •  The Gold Standard of Data', font=f_tiny, fill=GRAY_500)

    return img


def create_app_mockup_mobile():
    """Mockup of AUREA Mobile app."""
    W, H = 800, 1100
    img = Image.new('RGB', (W, H), GRAY_50)
    draw = ImageDraw.Draw(img)

    f_title = get_font(22, bold=True)
    f_h = get_font(16, bold=True)
    f_body = get_font(13)
    f_small = get_font(11, bold=True)
    f_tiny = get_font(10)

    # Phone frame
    px, py = 220, 60
    pw, ph = 360, 900
    # Outer frame
    draw.rounded_rectangle([px - 8, py - 8, px + pw + 8, py + ph + 8], radius=40, fill=NAVY_PRIMARY)
    # Screen
    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=32, fill=WHITE)

    # Status bar
    draw.rectangle([px, py, px + pw, py + 30], fill=WHITE)
    draw.text((px + 20, py + 8), '9:41', font=f_tiny, fill=NAVY_PRIMARY)
    # Battery
    draw.rectangle([px + pw - 30, py + 10, px + pw - 10, py + 22], outline=NAVY_PRIMARY, width=1)
    draw.rectangle([px + pw - 28, py + 12, px + pw - 20, py + 20], fill=NAVY_PRIMARY)

    # === SPLASH (initial state - shown for 3.5s) ===
    # Navy bg
    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=32, fill=NAVY_PRIMARY)
    # Gold A
    cx, cy = px + pw // 2, py + 280
    a_w = 60
    a_h = 70
    draw.polygon([
        (cx, cy - a_h // 2), (cx + a_w // 2, cy + a_h // 2),
        (cx + a_w // 2 - 12, cy + a_h // 2), (cx + 4, cy - 3),
        (cx - 4, cy - 3), (cx - a_w // 2 + 12, cy + a_h // 2), (cx - a_w // 2, cy + a_h // 2)
    ], fill=GOLD_PRIMARY)
    # Inner cutout
    draw.polygon([
        (cx, cy - 8), (cx + 12, cy + 18), (cx + 8, cy + 18),
        (cx + 3, cy + 4), (cx - 3, cy + 4), (cx - 8, cy + 18), (cx - 12, cy + 18)
    ], fill=NAVY_PRIMARY)
    draw.rectangle([cx - 22, cy + 22, cx + 22, cy + 28], fill=GOLD_PRIMARY)
    for x_off in [-12, 0, 12]:
        draw.ellipse([cx + x_off - 2, cy + 38, cx + x_off + 2, cy + 42], fill=GOLD_LIGHT)

    # AUREA text
    draw.text((cx - 70, cy + 90), 'AUREA', font=get_font(28, bold=True), fill=GOLD_PRIMARY)
    # Divider
    draw.line([(cx - 80, cy + 130), (cx + 80, cy + 130)], fill=GOLD_PRIMARY, width=1)
    draw.text((cx - 80, cy + 145), 'THE GOLD STANDARD OF DATA', font=f_tiny, fill=GOLD_LIGHT)

    # === HOME SCREEN (below splash) ===
    # Header with greeting
    home_y = py + 380
    # Logo mini
    lcx, lcy = px + 30, home_y + 20
    draw.polygon([
        (lcx, lcy - 10), (lcx + 8, lcy + 10), (lcx + 5, lcy + 10),
        (lcx + 1, lcy + 1), (lcx - 1, lcy + 1), (lcx - 5, lcy + 10), (lcx - 8, lcy + 10)
    ], fill=GOLD_PRIMARY)
    draw.text((px + 60, home_y), 'Selamat datang,', font=f_tiny, fill=GRAY_500)
    draw.text((px + 60, home_y + 14), 'Budi Santoso', font=f_h, fill=NAVY_PRIMARY)

    # Golden Customer hero card
    hero_y = home_y + 50
    draw.rounded_rectangle([px + 20, hero_y, px + pw - 20, hero_y + 180], radius=12, fill=NAVY_PRIMARY)
    # Gold accent
    draw.rectangle([px + 20, hero_y, px + pw - 20, hero_y + 3], fill=GOLD_PRIMARY)
    # GC badge
    draw.rectangle([px + 35, hero_y + 20, px + 145, hero_y + 38], fill=GOLD_PRIMARY)
    draw.text((px + 50, hero_y + 23), 'GOLDEN CUSTOMER', font=f_tiny, fill=NAVY_PRIMARY)
    # VIP verified badge
    draw.rectangle([px + pw - 80, hero_y + 20, px + pw - 35, hero_y + 38], fill=(22, 163, 74))
    draw.text((px + pw - 70, hero_y + 23), 'VERIFIED', font=f_tiny, fill=WHITE)
    # Body
    draw.text((px + 35, hero_y + 55), 'VIP Customer', font=f_tiny, fill=GOLD_LIGHT)
    draw.text((px + 35, hero_y + 73), 'Budi Santoso', font=get_font(20, bold=True), fill=WHITE)
    draw.text((px + 35, hero_y + 100), 'CIF: GC-2024-001847', font=f_tiny, fill=GOLD_LIGHT)
    # Stats row
    draw.text((px + 35, hero_y + 125), 'CLV', font=f_tiny, fill=GOLD_LIGHT)
    draw.text((px + 35, hero_y + 142), 'Rp 25.4M', font=f_h, fill=WHITE)
    draw.text((px + 200, hero_y + 125), 'TIER', font=f_tiny, fill=GOLD_LIGHT)
    draw.text((px + 200, hero_y + 142), '⭐⭐⭐ GOLD', font=f_h, fill=GOLD_LIGHT)

    # Quick stats grid
    stat_y = hero_y + 200
    stats = [('1.24M', 'NASABAH'), ('892K', 'REKENING'), ('1.4K', 'PRODUK'), ('12K', 'CHURN')]
    for i, (val, lbl) in enumerate(stats):
        sx = px + 20 + (i % 2) * 170
        sy = stat_y + (i // 2) * 80
        draw.rounded_rectangle([sx, sy, sx + 160, sy + 70], radius=10, fill=WHITE, outline=GRAY_300)
        draw.text((sx + 14, sy + 10), val, font=get_font(18, bold=True), fill=NAVY_PRIMARY)
        draw.text((sx + 14, sy + 38), lbl, font=f_tiny, fill=GRAY_500)

    # Bottom nav
    nav_y = py + ph - 70
    draw.rectangle([px, nav_y - 10, px + pw, py + ph - 8], fill=WHITE)
    draw.line([(px, nav_y - 10), (px + pw, nav_y - 10)], fill=GRAY_300)
    nav_items = ['🏠', '👥', '💰', '👤']
    nav_labels = ['Home', 'Customer', 'Account', 'Profile']
    for i, (icon, lbl) in enumerate(zip(nav_items, nav_labels)):
        nx = px + 30 + i * 80
        color = GOLD_PRIMARY if i == 0 else GRAY_500
        draw.text((nx + 12, nav_y + 5), icon, font=get_font(18), fill=color)
        draw.text((nx + 2, nav_y + 35), lbl, font=f_tiny, fill=color)

    # Side info text
    info_x = W - 280
    draw.text((info_x, 60), 'AUREA Mobile', font=f_title, fill=NAVY_PRIMARY)
    draw.text((info_x, 90), 'iOS + Android', font=f_body, fill=GRAY_500)
    draw.text((info_x, 130), 'STACK', font=f_small, fill=GRAY_500)
    stack = [
        '• Flutter 3.10+',
        '• Dart 3.0+',
        '• Provider / Riverpod',
        '• Dio + secure storage',
        '• Material 3',
        '• Google Fonts',
    ]
    for i, item in enumerate(stack):
        draw.text((info_x, 158 + i * 22), item, font=f_tiny, fill=NAVY_PRIMARY)

    draw.text((info_x, 320), 'FEATURES', font=f_small, fill=GRAY_500)
    features = [
        '✓ AUREA Splash (3.5s)',
        '✓ Biometric login',
        '✓ Golden Customer card',
        '✓ Search & filter',
        '✓ Light + Dark mode',
        '✓ Offline-first ready',
    ]
    for i, item in enumerate(features):
        draw.text((info_x, 348 + i * 22), item, font=f_tiny, fill=NAVY_PRIMARY)

    return img


def create_app_mockup_customer360():
    """Mockup of AUREA 360 customer dashboard."""
    W, H = 1400, 900
    img = Image.new('RGB', (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    f_title = get_font(20, bold=True)
    f_h = get_font(16, bold=True)
    f_body = get_font(13)
    f_small = get_font(11, bold=True)
    f_tiny = get_font(10)

    # Header
    draw.rectangle([0, 0, W, 64], fill=WHITE)
    draw.rectangle([0, 62, W, 64], fill=GOLD_PRIMARY)
    # Logo
    cx, cy = 40, 32
    draw.polygon([
        (cx, cy - 12), (cx + 12, cy + 12), (cx + 7, cy + 12),
        (cx + 2, cy + 2), (cx - 2, cy + 2), (cx - 7, cy + 12), (cx - 12, cy + 12)
    ], fill=GOLD_PRIMARY)
    draw.text((70, 20), 'AUREA 360', font=get_font(18, bold=True), fill=NAVY_PRIMARY)
    draw.text((70, 42), 'CUSTOMER INTELLIGENCE', font=f_tiny, fill=GRAY_500)

    # Nav
    nav = ['Dashboard', 'Customers', 'Analytics', 'Segments']
    nx = 240
    for i, label in enumerate(nav):
        if i == 0:
            draw.rounded_rectangle([nx, 18, nx + 100, 46], radius=8, fill=GOLD_PRIMARY)
            draw.text((nx + 12, 25), label, font=f_body, fill=NAVY_PRIMARY)
        else:
            draw.text((nx + 12, 25), label, font=f_body, fill=GRAY_500)
        nx += 110

    # User area (right)
    draw.ellipse([W - 80, 20, W - 50, 50], fill=GOLD_PRIMARY)
    draw.text((W - 73, 28), 'BS', font=f_small, fill=NAVY_PRIMARY)
    draw.text((W - 45, 28), 'Budi S.', font=f_body, fill=NAVY_PRIMARY)

    # Content
    y = 90
    # Page title
    draw.text((40, y), 'AUREA 360', font=f_small, fill=GOLD_DARK)
    draw.text((40, y + 18), 'Customer Analytics Dashboard', font=f_title, fill=NAVY_PRIMARY)

    # KPI grid (6 cards in 2 rows of 3)
    y = 180
    kpis = [
        ('Total Customers', '1.24M', '↑ 8.2%', True),
        ('Active (30d)', '892K', '↑ 3.1%', True),
        ('New This Month', '18,294', '↑ 12.4%', True),
        ('Churn Risk', '12,456', '↓ 2.1%', False),
        ('Avg CLV', 'Rp 8.5M', '↑ 5.6%', True),
        ('NPS Score', '67/100', '↑ 1.2%', True),
    ]
    for i, (label, value, trend, up) in enumerate(kpis):
        col = i % 3
        row = i // 3
        sx = 40 + col * 440
        sy = y + row * 110
        # Card
        draw.rounded_rectangle([sx, sy, sx + 420, sy + 100], radius=12, fill=WHITE, outline=GRAY_300)
        # Icon box
        icon_colors = [GOLD_PRIMARY, (22, 163, 74), (2, 132, 199), (234, 88, 12), GOLD_DARK, (124, 58, 237)]
        draw.rounded_rectangle([sx + 16, sy + 20, sx + 64, sy + 68], radius=10, fill=icon_colors[i])
        draw.text((sx + 30, sy + 32), ['👥', '✅', '🆕', '⚠️', '💎', '⭐'][i], font=get_font(18), fill=WHITE)
        # Label
        draw.text((sx + 80, sy + 18), label.upper(), font=f_small, fill=GRAY_500)
        # Value
        draw.text((sx + 80, sy + 38), value, font=get_font(24, bold=True), fill=NAVY_PRIMARY)
        # Trend
        trend_color = (22, 163, 74) if up else (220, 38, 38)
        draw.text((sx + 80, sy + 72), trend, font=f_small, fill=trend_color)

    # Chart section
    chart_y = 430
    draw.text((40, chart_y), 'Customer Growth', font=f_h, fill=NAVY_PRIMARY)
    draw.line([(40, chart_y + 28), (300, chart_y + 28)], fill=GOLD_PRIMARY, width=2)

    # Simple line chart
    chart_data_x = 40
    chart_data_y = chart_y + 50
    cw, ch = 800, 280
    draw.rounded_rectangle([chart_data_x, chart_data_y, chart_data_x + cw, chart_data_y + ch], radius=10, fill=WHITE, outline=GRAY_300)
    # Grid lines
    for i in range(1, 5):
        gy = chart_data_y + i * ch // 5
        draw.line([(chart_data_x + 30, gy), (chart_data_x + cw - 20, gy)], fill=GRAY_100)
    # Data line (new customers)
    new_data = [40, 50, 60, 55, 70, 80, 90, 100, 110, 120, 130, 150]
    pts = []
    for i, v in enumerate(new_data):
        px = chart_data_x + 50 + i * (cw - 80) // 11
        py = chart_data_y + ch - 30 - v
        pts.append((px, py))
    # Draw line
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i + 1]], fill=GOLD_PRIMARY, width=3)
    # Draw points
    for p in pts:
        draw.ellipse([p[0] - 4, p[1] - 4, p[0] + 4, p[1] + 4], fill=GOLD_PRIMARY)
    # Labels
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']
    for i, m in enumerate(months):
        x = chart_data_x + 50 + i * (cw - 80) // 11
        draw.text((x - 10, chart_data_y + ch - 22), m, font=f_tiny, fill=GRAY_500)

    # Right side: Top segments
    seg_x = 870
    draw.text((seg_x, chart_y), 'Top Performing Segments', font=f_h, fill=NAVY_PRIMARY)
    draw.line([(seg_x, chart_y + 28), (seg_x + 200, chart_y + 28)], fill=GOLD_PRIMARY, width=2)

    segments = [
        ('VIP', '45,280', 'Rp 25.4M', '↑ 12.3%', True),
        ('Mass Affluent', '187,540', 'Rp 12.8M', '↑ 8.5%', True),
        ('Senior', '89,120', 'Rp 9.5M', '↑ 4.2%', True),
        ('Mass Market', '698,120', 'Rp 3.2M', '↓ 1.1%', False),
    ]
    for i, (name, count, clv, trend, up) in enumerate(segments):
        sy = chart_y + 50 + i * 65
        draw.rounded_rectangle([seg_x, sy, seg_x + 490, sy + 55], radius=8, fill=WHITE, outline=GRAY_300)
        draw.text((seg_x + 16, sy + 8), name, font=f_h, fill=NAVY_PRIMARY)
        draw.text((seg_x + 16, sy + 30), f'{count} customers', font=f_tiny, fill=GRAY_500)
        draw.text((seg_x + 200, sy + 8), clv, font=f_h, fill=GOLD_DARK)
        draw.text((seg_x + 200, sy + 30), 'Avg CLV', font=f_tiny, fill=GRAY_500)
        trend_color = (22, 163, 74) if up else (220, 38, 38)
        draw.text((seg_x + 380, sy + 18), trend, font=f_h, fill=trend_color)

    # Footer
    draw.text((40, H - 30), 'AUREA 360 v1.0.0  •  The Gold Standard of Data  •  © 2026 Bank XYZ', font=f_tiny, fill=GRAY_500)

    return img


def create_app_integration_diagram():
    """Show how 3 apps + mobile all use AUREA branding."""
    W, H = 1400, 800
    img = Image.new('RGB', (W, H), GRAY_50)
    draw = ImageDraw.Draw(img)

    f_title = get_font(24, bold=True)
    f_h = get_font(18, bold=True)
    f_body = get_font(14)
    f_small = get_font(12, bold=True)
    f_tiny = get_font(10)

    # Title
    draw.text((60, 50), 'AUREA Brand — Cross-Application Integration', font=f_title, fill=NAVY_PRIMARY)
    draw.text((60, 85), 'Single brand identity, four touchpoints', font=f_body, fill=GRAY_500)

    # Central AUREA hub
    hub_cx, hub_cy = W // 2, 400
    hub_r = 120
    # Navy circle
    draw.ellipse([hub_cx - hub_r, hub_cy - hub_r, hub_cx + hub_r, hub_cy + hub_r], fill=NAVY_PRIMARY)
    # Gold A
    ax, ay = hub_cx, hub_cy - 30
    a_w, a_h = 60, 70
    draw.polygon([
        (ax, ay - a_h // 2), (ax + a_w // 2, ay + a_h // 2),
        (ax + a_w // 2 - 12, ay + a_h // 2), (ax + 4, ay - 3),
        (ax - 4, ay - 3), (ax - a_w // 2 + 12, ay + a_h // 2), (ax - a_w // 2, ay + a_h // 2)
    ], fill=GOLD_PRIMARY)
    # Cutout
    draw.polygon([
        (ax, ay - 8), (ax + 12, ay + 18), (ax + 8, ay + 18),
        (ax + 3, ay + 4), (ax - 3, ay + 4), (ax - 8, ay + 18), (ax - 12, ay + 18)
    ], fill=NAVY_PRIMARY)
    draw.rectangle([ax - 22, ay + 22, ax + 22, ay + 28], fill=GOLD_PRIMARY)
    for x_off in [-12, 0, 12]:
        draw.ellipse([ax + x_off - 2, ay + 38, ax + x_off + 2, ay + 42], fill=GOLD_LIGHT)
    # AUREA text
    draw.text((hub_cx - 50, hub_cy + 80), 'AUREA', font=get_font(20, bold=True), fill=GOLD_PRIMARY)
    draw.text((hub_cx - 60, hub_cy + 105), 'THE GOLD STANDARD', font=f_tiny, fill=GOLD_LIGHT)

    # 4 application cards around the hub
    apps = [
        ('AUREA Console', 'Admin Dashboard', 'Vite + Alpine.js', 200, 200),
        ('AUREA 360', 'Customer Intelligence', 'Nuxt 3 + Element Plus', 1000, 200),
        ('AUREA Steward', 'Data Steward UI', 'Nuxt 3 + i18n', 200, 580),
        ('AUREA Mobile', 'iOS + Android', 'Flutter 3.10+', 1000, 580),
    ]

    for name, desc, stack, x, y in apps:
        # Card
        cw, ch = 280, 140
        draw.rounded_rectangle([x, y, x + cw, y + ch], radius=12, fill=WHITE, outline=GRAY_300)
        draw.rectangle([x, y, x + cw, y + 3], fill=GOLD_PRIMARY)
        # Icon
        draw.rounded_rectangle([x + 16, y + 16, x + 56, y + 56], radius=10, fill=NAVY_PRIMARY)
        icons = ['💻', '📊', '👥', '📱']
        draw.text((x + 24, y + 22), icons[apps.index((name, desc, stack, x, y))], font=get_font(18), fill=GOLD_PRIMARY)
        # Name
        draw.text((x + 72, y + 20), name, font=f_h, fill=NAVY_PRIMARY)
        draw.text((x + 72, y + 42), desc, font=f_tiny, fill=GRAY_500)
        # Stack
        draw.text((x + 16, y + 75), stack, font=f_small, fill=GOLD_DARK)
        # Status
        draw.rounded_rectangle([x + 16, y + 100, x + 70, y + 122], radius=6, fill=(22, 163, 74))
        draw.text((x + 26, y + 105), '✓ LIVE', font=f_tiny, fill=WHITE)
        # Files
        draw.text((x + 90, y + 105), '8 brand files', font=f_tiny, fill=GRAY_500)

        # Connection line to hub
        line_color = GOLD_PRIMARY
        if name in ['AUREA Console', 'AUREA 360']:
            line_y_start = y + ch // 2
            line_y_end = hub_cy - 50
            draw.line([(x + cw // 2, line_y_start), (hub_cx, line_y_end)], fill=line_color, width=2)
        else:
            line_y_start = y + ch // 2
            line_y_end = hub_cy + 50
            draw.line([(x + cw // 2, line_y_start), (hub_cx, line_y_end)], fill=line_color, width=2)

    # Bottom labels
    draw.text((W // 2 - 80, H - 30), 'AUREA — One Brand, Every Platform', font=f_small, fill=GOLD_DARK)

    return img


def create_stats_dashboard():
    """Visual stats summary of all deliverables."""
    W, H = 1400, 800
    img = Image.new('RGB', (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    f_title = get_font(28, bold=True)
    f_h = get_font(20, bold=True)
    f_body = get_font(14)
    f_small = get_font(11, bold=True)
    f_tiny = get_font(10)
    f_big = get_font(48, bold=True)

    # Header with navy gradient
    for y in range(160):
        ratio = y / 160
        r = int(NAVY_PRIMARY[0] + (NAVY_LIGHT[0] - NAVY_PRIMARY[0]) * ratio)
        g = int(NAVY_PRIMARY[1] + (NAVY_LIGHT[1] - NAVY_PRIMARY[1]) * ratio)
        b = int(NAVY_PRIMARY[2] + (NAVY_LIGHT[2] - NAVY_PRIMARY[2]) * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    draw.text((60, 50), 'AUREA — Delivery Summary', font=f_title, fill=GOLD_LIGHT)
    draw.text((60, 100), 'The Gold Standard of Data — Complete Brand & Implementation Package', font=f_body, fill=WHITE)

    # Stats grid
    y = 200
    stats = [
        ('30+', 'Brand Assets', 'Logo, favicon, GIF, SVG'),
        ('4', 'Applications', 'Console, 360, Steward, Mobile'),
        ('60+', 'Files Created', 'Code, assets, docs'),
        ('22', 'App Icons', 'Android (5) + iOS (15) + master (2)'),
        ('3', 'Animations', 'Splash, spinners, transitions'),
        ('3', 'Documentation', 'Brand, Integration, Mobile'),
    ]
    for i, (val, lbl, sub) in enumerate(stats):
        col = i % 3
        row = i // 3
        sx = 60 + col * 440
        sy = y + row * 180
        # Card with gold top
        draw.rounded_rectangle([sx, sy, sx + 420, sy + 160], radius=12, fill=GRAY_50, outline=GOLD_PRIMARY, width=1)
        draw.rectangle([sx, sy, sx + 420, sy + 4], fill=GOLD_PRIMARY)
        # Big number
        draw.text((sx + 24, sy + 18), val, font=f_big, fill=GOLD_PRIMARY)
        # Label
        draw.text((sx + 24, sy + 90), lbl, font=f_h, fill=NAVY_PRIMARY)
        # Sub
        draw.text((sx + 24, sy + 120), sub, font=f_body, fill=GRAY_500)

    # Bottom section
    y = 580
    draw.text((60, y), 'Implementation Highlights', font=f_h, fill=NAVY_PRIMARY)
    draw.line([(60, y + 32), (260, y + 32)], fill=GOLD_PRIMARY, width=2)
    y += 50

    highlights = [
        '✓ AUREA web app built and verified (Vite production build, 3.5s)',
        '✓ Logo + favicon in 6 SVG, 6 PNG, 5 ICO formats',
        '✓ Animated splash (HTML/CSS, SVG SMIL, GIF 860KB)',
        '✓ 8 brand-matched loading spinners',
        '✓ Page transitions with gold sweep effect',
        '✓ Dark mode + Light mode splash variants',
        '✓ Tailwind config with AUREA palette + 2 daisyUI themes',
        '✓ Element Plus theme override (gold primary)',
        '✓ Flutter app: 15 Dart files, 4 screens, biometric auth',
        '✓ App icons generated for Android (5) + iOS (15) sizes',
    ]
    for i, h in enumerate(highlights):
        draw.text((60, y + i * 22), h, font=f_body, fill=NAVY_PRIMARY)

    return img


def main():
    output_dir = '/home/user/aurea-docx-assets'
    os.makedirs(output_dir, exist_ok=True)

    generators = [
        ('brand_identity.png', create_brand_identity_card),
        ('color_palette.png', create_color_palette),
        ('mockup_admin.png', create_app_mockup_admin),
        ('mockup_customer360.png', create_app_mockup_customer360),
        ('mockup_mobile.png', create_app_mockup_mobile),
        ('integration_diagram.png', create_app_integration_diagram),
        ('stats_summary.png', create_stats_dashboard),
    ]

    print("Generating DOCX composite images...")
    print("=" * 60)

    for filename, generator in generators:
        print(f"  Creating {filename}...", end=" ")
        img = generator()
        path = os.path.join(output_dir, filename)
        img.save(path, 'PNG', optimize=True)
        size = os.path.getsize(path) / 1024
        print(f"OK ({size:.0f} KB)")

    print("=" * 60)
    print(f"All images saved to: {output_dir}")


if __name__ == '__main__':
    main()
