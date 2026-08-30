"""
AUREA DOCX Image Generator v2 - Better text rendering
"""

from PIL import Image, ImageDraw, ImageFont
import os

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


def get_font(size, bold=False, italic=False):
    candidates = []
    if bold and italic:
        candidates = ['/usr/share/fonts/truetype/dejavu/DejaVuSerif-BoldItalic.ttf']
    elif bold:
        candidates = ['/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',
                      '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']
    elif italic:
        candidates = ['/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf']
    else:
        candidates = ['/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',
                      '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']

    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                pass
    return ImageFont.load_default()


def draw_text_centered(draw, text, center_x, y, font, fill, max_width=None):
    """Draw text centered, returns total width used."""
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    if max_width and text_w > max_width:
        # Scale down by trying smaller font? For now just clip
        pass
    x = int(center_x - text_w / 2)
    draw.text((x, y), text, font=font, fill=fill)
    return text_w


def create_brand_identity_card():
    """Create a brand identity overview card - improved."""
    W, H = 1200, 800
    img = Image.new('RGB', (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    # Navy left half with gradient
    for y in range(H):
        ratio = y / H
        r = int(NAVY_PRIMARY[0] + (NAVY_LIGHT[0] - NAVY_PRIMARY[0]) * ratio * 0.5)
        g = int(NAVY_PRIMARY[1] + (NAVY_LIGHT[1] - NAVY_PRIMARY[1]) * ratio * 0.5)
        b = int(NAVY_PRIMARY[2] + (NAVY_LIGHT[2] - NAVY_PRIMARY[2]) * ratio * 0.5)
        draw.line([(0, y), (W // 2, y)], fill=(r, g, b))

    # === LEFT SIDE: Logo + AUREA wordmark ===
    # Gold A triangle - center
    cx, cy = W // 4, H // 2 - 100

    # A outer triangle
    a_top = (cx, cy - 80)
    a_right = (cx + 70, cy + 80)
    a_right_inner = (cx + 52, cy + 80)
    a_right_cross = (cx + 15, cy - 5)
    a_left_cross = (cx - 15, cy - 5)
    a_left_inner = (cx - 52, cy + 80)
    a_left = (cx - 70, cy + 80)

    a_polygon = [
        a_top,
        a_right,
        a_right_inner,
        a_right_cross,
        a_left_cross,
        a_left_inner,
        a_left,
    ]
    # Draw with gradient
    rows = 160
    for y_off in range(rows):
        t = y_off / rows
        color = tuple(int(GOLD_LIGHT[c] + (GOLD_DARK[c] - GOLD_LIGHT[c]) * t) for c in range(3))
        y_pos = cy - 80 + y_off
        # Width of A at this y (triangle)
        frac = y_off / rows
        half_w = 70 * (1 - frac) * 0.85
        if half_w > 0.5:
            x_start = int(cx - half_w)
            x_end = int(cx + half_w)
            if y_pos > a_right_cross[1] + 5:
                # Below crossbar - draw with cutout
                cross_frac = (y_pos - a_right_cross[1]) / (a_right[1] - a_right_cross[1])
                inner_half = 15 + (52 - 15) * cross_frac
                draw.line([(x_start, y_pos), (int(cx - inner_half), y_pos)], fill=color)
                draw.line([(int(cx + inner_half), y_pos), (x_end, y_pos)], fill=color)
            else:
                draw.line([(x_start, y_pos), (x_end, y_pos)], fill=color)

    # A bottom bar
    bar_y1 = cy + 60
    bar_y2 = cy + 78
    for y_off in range(bar_y2 - bar_y1):
        t = y_off / (bar_y2 - bar_y1)
        color = tuple(int(GOLD_LIGHT[c] + (GOLD_DARK[c] - GOLD_LIGHT[c]) * t) for c in range(3))
        draw.line([(cx - 55, bar_y1 + y_off), (cx + 55, bar_y1 + y_off)], fill=color)

    # 3 golden dots below the A
    for x_off in [-22, 0, 22]:
        dx = cx + x_off
        dy = cy + 105
        draw.ellipse([dx - 6, dy - 6, dx + 6, dy + 6], fill=GOLD_LIGHT)

    # AUREA wordmark - simpler, draw each letter with gradient
    word_y = cy + 150
    f_word = get_font(64, bold=True)
    word = "AUREA"
    # Get width per character
    char_widths = []
    total_w = 0
    for ch in word:
        bbox = draw.textbbox((0, 0), ch, font=f_word)
        w = bbox[2] - bbox[0] + 8  # spacing
        char_widths.append(w)
        total_w += w
    # Center
    start_x = cx - total_w // 2
    cur_x = start_x
    for i, ch in enumerate(word):
        ratio = i / (len(word) - 1)
        color = tuple(int(GOLD_LIGHT[c] + (GOLD_DARK[c] - GOLD_LIGHT[c]) * ratio) for c in range(3))
        draw.text((cur_x, word_y), ch, font=f_word, fill=color)
        cur_x += char_widths[i]

    # Tagline
    f_tag = get_font(13, bold=True)
    tag = "THE GOLD STANDARD OF DATA"
    bbox = draw.textbbox((0, 0), tag, font=f_tag)
    tag_w = bbox[2] - bbox[0]
    draw.text((cx - tag_w // 2, word_y + 80), tag, font=f_tag, fill=GOLD_LIGHT)

    # === RIGHT SIDE: Brand details ===
    f_title = get_font(36, bold=True)
    f_h = get_font(20, bold=True)
    f_body = get_font(15)
    f_small = get_font(12, bold=True)

    x_right = W // 2 + 60
    y = 80

    # Title
    draw.text((x_right, y), 'Brand Identity', font=f_title, fill=NAVY_PRIMARY)
    y += 50
    draw.rectangle([x_right, y, x_right + 120, y + 3], fill=GOLD_PRIMARY)
    y += 30

    # Name section
    draw.text((x_right, y), 'PRODUCT NAME', font=f_small, fill=GRAY_500)
    y += 22
    draw.text((x_right, y), 'AUREA', font=f_h, fill=NAVY_PRIMARY)
    draw.text((x_right + 90, y + 4), '(Latin: "Golden")', font=f_body, fill=GRAY_500)
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
        draw.rectangle([x_right, y, x_right + 40, y + 40], fill=color, outline=GRAY_300, width=1)
        draw.text((x_right + 54, y + 4), name, font=f_body, fill=NAVY_PRIMARY)
        draw.text((x_right + 54, y + 24), hex_code, font=f_small, fill=GRAY_500)
        y += 52

    y += 10
    draw.text((x_right, y), 'SYMBOLISM', font=f_small, fill=GRAY_500)
    y += 22
    symbols = [
        ('Letter A', '— Aurea = first letter of brand'),
        ('Triangle', '— Stability & trust'),
        ('3 Gold Dots', '— MD3G (GC, GA, GP)'),
    ]
    for label, desc in symbols:
        draw.text((x_right, y), f'•  {label}', font=f_body, fill=NAVY_PRIMARY)
        bbox = draw.textbbox((0, 0), f'•  {label}', font=f_body)
        text_w = bbox[2] - bbox[0]
        draw.text((x_right + text_w + 12, y), desc, font=f_body, fill=GRAY_500)
        y += 28

    return img


def create_color_palette():
    """Detailed color palette."""
    W, H = 1200, 700
    img = Image.new('RGB', (W, H), GRAY_50)
    draw = ImageDraw.Draw(img)

    f_title = get_font(32, bold=True)
    f_h = get_font(18, bold=True)
    f_body = get_font(14)
    f_small = get_font(12, bold=True)

    draw.text((60, 50), 'AUREA Color System', font=f_title, fill=NAVY_PRIMARY)
    draw.text((60, 95), 'Brand colors for digital and print', font=f_body, fill=GRAY_500)

    y = 160
    draw.text((60, y), 'PRIMARY', font=f_small, fill=GRAY_500)
    y += 25

    primary = [
        ('Gold 500', '#D4AF37', GOLD_PRIMARY, NAVY_PRIMARY),
        ('Gold 300', '#FFD764', GOLD_LIGHT, NAVY_PRIMARY),
        ('Gold 700', '#B8860B', GOLD_DARK, WHITE),
        ('Navy 600', '#0A1929', NAVY_PRIMARY, GOLD_PRIMARY),
        ('Navy 500', '#1A2F47', NAVY_LIGHT, GOLD_PRIMARY),
    ]
    x = 60
    for name, hex_c, color, text_color in primary:
        draw.rectangle([x, y, x + 200, y + 160], fill=color)
        draw.rectangle([x, y, x + 200, y + 160], outline=GRAY_300, width=1)
        draw.text((x + 16, y + 120), hex_c, font=get_font(16, bold=True), fill=text_color)
        draw.text((x, y + 175), name, font=f_h, fill=NAVY_PRIMARY)
        draw.text((x, y + 198), hex_c, font=f_body, fill=GRAY_500)
        x += 220

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
    """Mockup AUREA Console."""
    W, H = 1400, 900
    img = Image.new('RGB', (W, H), GRAY_50)
    draw = ImageDraw.Draw(img)

    f_title = get_font(20, bold=True)
    f_h = get_font(16, bold=True)
    f_body = get_font(13)
    f_small = get_font(11, bold=True)
    f_tiny = get_font(10)

    # Sidebar
    draw.rectangle([0, 0, 240, H], fill=NAVY_PRIMARY)
    draw.rectangle([0, 0, 240, 4], fill=GOLD_PRIMARY)

    # Logo mini
    cx, cy = 50, 50
    draw.polygon([
        (cx, cy - 14), (cx + 12, cy + 14), (cx + 7, cy + 14),
        (cx + 2, cy - 1), (cx - 2, cy - 1), (cx - 7, cy + 14), (cx - 12, cy + 14)
    ], fill=GOLD_PRIMARY)
    for x_off in [-12, 0, 12]:
        draw.ellipse([cx + x_off - 2, cy + 18, cx + x_off + 2, cy + 22], fill=GOLD_LIGHT)

    draw.text((90, 36), 'AUREA', font=get_font(20, bold=True), fill=GOLD_PRIMARY)
    draw.text((90, 60), 'CONSOLE', font=get_font(8, bold=True), fill=GOLD_LIGHT)

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

    # Top bar
    draw.rectangle([240, 0, W, 60], fill=WHITE)
    draw.rectangle([240, 58, W, 60], fill=GRAY_300)
    draw.rectangle([240, 0, W, 2], fill=GOLD_PRIMARY)
    draw.text((270, 22), 'Dashboard', font=f_title, fill=NAVY_PRIMARY)
    draw.rectangle([400, 26, 460, 46], fill=GOLD_PRIMARY)
    draw.text((412, 30), 'AUREA', font=f_tiny, fill=NAVY_PRIMARY)
    draw.ellipse([W - 180, 28, W - 168, 40], fill=(22, 163, 74))
    draw.text((W - 160, 30), 'Real-time', font=f_tiny, fill=GRAY_700)

    y = 90
    draw.text((270, y), 'Welcome to AUREA Console', font=f_title, fill=NAVY_PRIMARY)
    draw.text((270, y + 28), 'The Gold Standard of Data — Master Data Management', font=f_body, fill=GRAY_500)
    y += 70

    stats = [
        ('Golden Customers', '12,847', '+8.2%'),
        ('Golden Accounts', '28,193', '+3.1%'),
        ('Golden Products', '1,452', '+12.4%'),
        ('Data Quality', '98.7%', '+0.4%'),
    ]
    sx = 270
    for label, value, trend in stats:
        draw.rectangle([sx, y, sx + 250, y + 110], fill=WHITE, outline=GRAY_300)
        draw.rectangle([sx, y, sx + 250, y + 3], fill=GOLD_PRIMARY)
        draw.text((sx + 16, y + 16), label.upper(), font=f_small, fill=GRAY_500)
        draw.text((sx + 16, y + 40), value, font=get_font(28, bold=True), fill=NAVY_PRIMARY)
        draw.text((sx + 16, y + 80), f'↑ {trend}', font=f_small, fill=(22, 163, 74))
        sx += 270

    y += 140
    draw.text((270, y), 'Recent Activity', font=f_h, fill=NAVY_PRIMARY)
    y += 30
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

    draw.text((270, H - 30), 'AUREA Console v1.0.0  •  Bank XYZ  •  The Gold Standard of Data', font=f_tiny, fill=GRAY_500)

    return img


def create_app_mockup_customer360():
    """Mockup AUREA 360."""
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
    cx, cy = 40, 32
    draw.polygon([
        (cx, cy - 12), (cx + 12, cy + 12), (cx + 7, cy + 12),
        (cx + 2, cy + 2), (cx - 2, cy + 2), (cx - 7, cy + 12), (cx - 12, cy + 12)
    ], fill=GOLD_PRIMARY)
    draw.text((70, 20), 'AUREA 360', font=get_font(18, bold=True), fill=NAVY_PRIMARY)
    draw.text((70, 42), 'CUSTOMER INTELLIGENCE', font=f_tiny, fill=GRAY_500)

    nav = ['Dashboard', 'Customers', 'Analytics', 'Segments']
    nx = 240
    for i, label in enumerate(nav):
        if i == 0:
            draw.rounded_rectangle([nx, 18, nx + 100, 46], radius=8, fill=GOLD_PRIMARY)
            draw.text((nx + 12, 25), label, font=f_body, fill=NAVY_PRIMARY)
        else:
            draw.text((nx + 12, 25), label, font=f_body, fill=GRAY_500)
        nx += 110

    draw.ellipse([W - 80, 20, W - 50, 50], fill=GOLD_PRIMARY)
    draw.text((W - 73, 28), 'BS', font=f_small, fill=NAVY_PRIMARY)
    draw.text((W - 45, 28), 'Budi S.', font=f_body, fill=NAVY_PRIMARY)

    y = 90
    draw.text((40, y), 'AUREA 360', font=f_small, fill=GOLD_DARK)
    draw.text((40, y + 18), 'Customer Analytics Dashboard', font=f_title, fill=NAVY_PRIMARY)

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
        draw.rounded_rectangle([sx, sy, sx + 420, sy + 100], radius=12, fill=WHITE, outline=GRAY_300)
        icon_colors = [GOLD_PRIMARY, (22, 163, 74), (2, 132, 199), (234, 88, 12), GOLD_DARK, (124, 58, 237)]
        draw.rounded_rectangle([sx + 16, sy + 20, sx + 64, sy + 68], radius=10, fill=icon_colors[i])
        draw.text((sx + 30, sy + 32), ['👥', '✅', '🆕', '⚠️', '💎', '⭐'][i], font=get_font(18), fill=WHITE)
        draw.text((sx + 80, sy + 18), label.upper(), font=f_small, fill=GRAY_500)
        draw.text((sx + 80, sy + 38), value, font=get_font(24, bold=True), fill=NAVY_PRIMARY)
        trend_color = (22, 163, 74) if up else (220, 38, 38)
        draw.text((sx + 80, sy + 72), trend, font=f_small, fill=trend_color)

    chart_y = 430
    draw.text((40, chart_y), 'Customer Growth', font=f_h, fill=NAVY_PRIMARY)
    draw.line([(40, chart_y + 28), (300, chart_y + 28)], fill=GOLD_PRIMARY, width=2)

    chart_data_x = 40
    chart_data_y = chart_y + 50
    cw, ch = 800, 280
    draw.rounded_rectangle([chart_data_x, chart_data_y, chart_data_x + cw, chart_data_y + ch], radius=10, fill=WHITE, outline=GRAY_300)
    for i in range(1, 5):
        gy = chart_data_y + i * ch // 5
        draw.line([(chart_data_x + 30, gy), (chart_data_x + cw - 20, gy)], fill=GRAY_100)
    new_data = [40, 50, 60, 55, 70, 80, 90, 100, 110, 120, 130, 150]
    pts = []
    for i, v in enumerate(new_data):
        px = chart_data_x + 50 + i * (cw - 80) // 11
        py = chart_data_y + ch - 30 - v
        pts.append((px, py))
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i + 1]], fill=GOLD_PRIMARY, width=3)
    for p in pts:
        draw.ellipse([p[0] - 4, p[1] - 4, p[0] + 4, p[1] + 4], fill=GOLD_PRIMARY)
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']
    for i, m in enumerate(months):
        x = chart_data_x + 50 + i * (cw - 80) // 11
        draw.text((x - 10, chart_data_y + ch - 22), m, font=f_tiny, fill=GRAY_500)

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

    draw.text((40, H - 30), 'AUREA 360 v1.0.0  •  The Gold Standard of Data  •  © 2026 Bank XYZ', font=f_tiny, fill=GRAY_500)
    return img


def create_app_mockup_mobile():
    """Mockup AUREA Mobile - clean version without side overlap."""
    W, H = 800, 1100
    img = Image.new('RGB', (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    f_title = get_font(22, bold=True)
    f_h = get_font(16, bold=True)
    f_body = get_font(13)
    f_small = get_font(11, bold=True)
    f_tiny = get_font(10)

    # Phone frame
    px, py = 220, 60
    pw, ph = 360, 900
    draw.rounded_rectangle([px - 8, py - 8, px + pw + 8, py + ph + 8], radius=40, fill=NAVY_PRIMARY)
    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=32, fill=WHITE)

    # Status bar
    draw.rectangle([px, py, px + pw, py + 30], fill=WHITE)
    draw.text((px + 20, py + 8), '9:41', font=f_tiny, fill=NAVY_PRIMARY)
    draw.rectangle([px + pw - 30, py + 10, px + pw - 10, py + 22], outline=NAVY_PRIMARY, width=1)
    draw.rectangle([px + pw - 28, py + 12, px + pw - 20, py + 20], fill=NAVY_PRIMARY)

    # Navy bg (splash)
    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=32, fill=NAVY_PRIMARY)
    cx, cy = px + pw // 2, py + 280
    draw.polygon([
        (cx, cy - 35), (cx + 30, cy + 35), (cx + 18, cy + 35),
        (cx + 4, cy - 3), (cx - 4, cy - 3), (cx - 18, cy + 35), (cx - 30, cy + 35)
    ], fill=GOLD_PRIMARY)
    draw.polygon([
        (cx, cy - 8), (cx + 12, cy + 18), (cx + 8, cy + 18),
        (cx + 3, cy + 4), (cx - 3, cy + 4), (cx - 8, cy + 18), (cx - 12, cy + 18)
    ], fill=NAVY_PRIMARY)
    draw.rectangle([cx - 22, cy + 22, cx + 22, cy + 28], fill=GOLD_PRIMARY)
    for x_off in [-12, 0, 12]:
        draw.ellipse([cx + x_off - 2, cy + 38, cx + x_off + 2, cy + 42], fill=GOLD_LIGHT)

    # AUREA wordmark (cleaner)
    f_word = get_font(28, bold=True)
    word = "AUREA"
    char_widths = []
    total_w = 0
    for ch in word:
        bbox = draw.textbbox((0, 0), ch, font=f_word)
        w = bbox[2] - bbox[0] + 4
        char_widths.append(w)
        total_w += w
    cur_x = cx - total_w // 2
    for i, ch in enumerate(word):
        ratio = i / (len(word) - 1)
        color = tuple(int(GOLD_LIGHT[c] + (GOLD_DARK[c] - GOLD_LIGHT[c]) * ratio) for c in range(3))
        draw.text((cur_x, cy + 90), ch, font=f_word, fill=color)
        cur_x += char_widths[i]

    draw.line([(cx - 80, cy + 130), (cx + 80, cy + 130)], fill=GOLD_PRIMARY, width=1)
    f_tag = get_font(8, bold=True)
    draw.text((cx - 65, cy + 145), 'THE GOLD STANDARD OF DATA', font=f_tag, fill=GOLD_LIGHT)

    # === HOME SCREEN (below splash) ===
    home_y = py + 380
    lcx, lcy = px + 30, home_y + 20
    draw.polygon([
        (lcx, lcy - 10), (lcx + 8, lcy + 10), (lcx + 5, lcy + 10),
        (lcx + 1, lcy + 1), (lcx - 1, lcy + 1), (lcx - 5, lcy + 10), (lcx - 8, lcy + 10)
    ], fill=GOLD_PRIMARY)
    draw.text((px + 60, home_y), 'Selamat datang,', font=f_tiny, fill=GRAY_500)
    draw.text((px + 60, home_y + 14), 'Budi Santoso', font=f_h, fill=NAVY_PRIMARY)

    hero_y = home_y + 50
    draw.rounded_rectangle([px + 20, hero_y, px + pw - 20, hero_y + 180], radius=12, fill=NAVY_PRIMARY)
    draw.rectangle([px + 20, hero_y, px + pw - 20, hero_y + 3], fill=GOLD_PRIMARY)
    draw.rectangle([px + 35, hero_y + 20, px + 145, hero_y + 38], fill=GOLD_PRIMARY)
    draw.text((px + 50, hero_y + 23), 'GOLDEN CUSTOMER', font=f_tiny, fill=NAVY_PRIMARY)
    draw.rectangle([px + pw - 80, hero_y + 20, px + pw - 35, hero_y + 38], fill=(22, 163, 74))
    draw.text((px + pw - 70, hero_y + 23), 'VERIFIED', font=f_tiny, fill=WHITE)
    draw.text((px + 35, hero_y + 55), 'VIP Customer', font=f_tiny, fill=GOLD_LIGHT)
    draw.text((px + 35, hero_y + 73), 'Budi Santoso', font=get_font(20, bold=True), fill=WHITE)
    draw.text((px + 35, hero_y + 100), 'CIF: GC-2024-001847', font=f_tiny, fill=GOLD_LIGHT)
    draw.text((px + 35, hero_y + 125), 'CLV', font=f_tiny, fill=GOLD_LIGHT)
    draw.text((px + 35, hero_y + 142), 'Rp 25.4M', font=f_h, fill=WHITE)
    draw.text((px + 200, hero_y + 125), 'TIER', font=f_tiny, fill=GOLD_LIGHT)
    # GOLD with stars using text
    draw.text((px + 200, hero_y + 142), 'GOLD', font=f_h, fill=GOLD_LIGHT)

    stat_y = hero_y + 200
    stats = [('1.24M', 'NASABAH'), ('892K', 'REKENING'), ('1.4K', 'PRODUK'), ('12K', 'CHURN')]
    for i, (val, lbl) in enumerate(stats):
        sx = px + 20 + (i % 2) * 170
        sy = stat_y + (i // 2) * 80
        draw.rounded_rectangle([sx, sy, sx + 160, sy + 70], radius=10, fill=WHITE, outline=GRAY_300)
        draw.text((sx + 14, sy + 10), val, font=get_font(18, bold=True), fill=NAVY_PRIMARY)
        draw.text((sx + 14, sy + 38), lbl, font=f_tiny, fill=GRAY_500)

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

    # Side info (cleaner placement, no overlap)
    info_x = 30
    info_y = 990
    # Inline info strip at bottom
    draw.rounded_rectangle([20, info_y - 10, W - 20, H - 10], radius=8, fill=NAVY_PRIMARY)
    draw.text((info_x + 10, info_y), 'STACK:', font=f_small, fill=GOLD_LIGHT)
    stack_text = 'Flutter 3.10  •  Dart 3.0  •  Provider  •  Dio  •  Material 3'
    draw.text((info_x + 80, info_y), stack_text, font=f_tiny, fill=WHITE)
    draw.text((info_x + 10, info_y + 22), 'PLATFORMS:', font=f_small, fill=GOLD_LIGHT)
    draw.text((info_x + 110, info_y + 22), 'iOS 13+  •  Android API 23+  •  Biometric  •  Light + Dark', font=f_tiny, fill=WHITE)

    return img


def create_app_integration_diagram():
    """Cross-application integration."""
    W, H = 1400, 800
    img = Image.new('RGB', (W, H), GRAY_50)
    draw = ImageDraw.Draw(img)

    f_title = get_font(24, bold=True)
    f_h = get_font(18, bold=True)
    f_body = get_font(14)
    f_small = get_font(12, bold=True)
    f_tiny = get_font(10)

    draw.text((60, 50), 'AUREA Brand — Cross-Application Integration', font=f_title, fill=NAVY_PRIMARY)
    draw.text((60, 85), 'Single brand identity, four touchpoints', font=f_body, fill=GRAY_500)

    hub_cx, hub_cy = W // 2, 400
    hub_r = 120
    draw.ellipse([hub_cx - hub_r, hub_cy - hub_r, hub_cx + hub_r, hub_cy + hub_r], fill=NAVY_PRIMARY)
    ax, ay = hub_cx, hub_cy - 30
    a_w, a_h = 60, 70
    draw.polygon([
        (ax, ay - a_h // 2), (ax + a_w // 2, ay + a_h // 2),
        (ax + a_w // 2 - 12, ay + a_h // 2), (ax + 4, ay - 3),
        (ax - 4, ay - 3), (ax - a_w // 2 + 12, ay + a_h // 2), (ax - a_w // 2, ay + a_h // 2)
    ], fill=GOLD_PRIMARY)
    draw.polygon([
        (ax, ay - 8), (ax + 12, ay + 18), (ax + 8, ay + 18),
        (ax + 3, ay + 4), (ax - 3, ay + 4), (ax - 8, ay + 18), (ax - 12, ay + 18)
    ], fill=NAVY_PRIMARY)
    draw.rectangle([ax - 22, ay + 22, ax + 22, ay + 28], fill=GOLD_PRIMARY)
    for x_off in [-12, 0, 12]:
        draw.ellipse([ax + x_off - 2, ay + 38, ax + x_off + 2, ay + 42], fill=GOLD_LIGHT)
    draw.text((hub_cx - 50, hub_cy + 80), 'AUREA', font=get_font(20, bold=True), fill=GOLD_PRIMARY)
    draw.text((hub_cx - 60, hub_cy + 105), 'THE GOLD STANDARD', font=f_tiny, fill=GOLD_LIGHT)

    apps = [
        ('AUREA Console', 'Admin Dashboard', 'Vite + Alpine.js', 200, 200, '💻'),
        ('AUREA 360', 'Customer Intelligence', 'Nuxt 3 + Element Plus', 1000, 200, '📊'),
        ('AUREA Steward', 'Data Steward UI', 'Nuxt 3 + i18n', 200, 580, '👥'),
        ('AUREA Mobile', 'iOS + Android', 'Flutter 3.10+', 1000, 580, '📱'),
    ]

    for name, desc, stack, x, y, icon in apps:
        cw, ch = 280, 140
        draw.rounded_rectangle([x, y, x + cw, y + ch], radius=12, fill=WHITE, outline=GRAY_300)
        draw.rectangle([x, y, x + cw, y + 3], fill=GOLD_PRIMARY)
        draw.rounded_rectangle([x + 16, y + 16, x + 56, y + 56], radius=10, fill=NAVY_PRIMARY)
        draw.text((x + 24, y + 22), icon, font=get_font(18), fill=GOLD_PRIMARY)
        draw.text((x + 72, y + 20), name, font=f_h, fill=NAVY_PRIMARY)
        draw.text((x + 72, y + 42), desc, font=f_tiny, fill=GRAY_500)
        draw.text((x + 16, y + 75), stack, font=f_small, fill=GOLD_DARK)
        draw.rounded_rectangle([x + 16, y + 100, x + 70, y + 122], radius=6, fill=(22, 163, 74))
        draw.text((x + 26, y + 105), '✓ LIVE', font=f_tiny, fill=WHITE)
        draw.text((x + 90, y + 105), '8 brand files', font=f_tiny, fill=GRAY_500)

        line_color = GOLD_PRIMARY
        if name in ['AUREA Console', 'AUREA 360']:
            line_y_start = y + ch // 2
            line_y_end = hub_cy - 50
            draw.line([(x + cw // 2, line_y_start), (hub_cx, line_y_end)], fill=line_color, width=2)
        else:
            line_y_start = y + ch // 2
            line_y_end = hub_cy + 50
            draw.line([(x + cw // 2, line_y_start), (hub_cx, line_y_end)], fill=line_color, width=2)

    draw.text((W // 2 - 80, H - 30), 'AUREA — One Brand, Every Platform', font=f_small, fill=GOLD_DARK)
    return img


def create_stats_dashboard():
    """Delivery summary stats."""
    W, H = 1400, 800
    img = Image.new('RGB', (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    f_title = get_font(28, bold=True)
    f_h = get_font(20, bold=True)
    f_body = get_font(14)
    f_small = get_font(11, bold=True)
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
        draw.rounded_rectangle([sx, sy, sx + 420, sy + 160], radius=12, fill=GRAY_50, outline=GOLD_PRIMARY, width=1)
        draw.rectangle([sx, sy, sx + 420, sy + 4], fill=GOLD_PRIMARY)
        draw.text((sx + 24, sy + 18), val, font=f_big, fill=GOLD_PRIMARY)
        draw.text((sx + 24, sy + 90), lbl, font=f_h, fill=NAVY_PRIMARY)
        draw.text((sx + 24, sy + 120), sub, font=f_body, fill=GRAY_500)

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


def create_logo_showcase():
    """Show all logo variants side by side."""
    W, H = 1400, 700
    img = Image.new('RGB', (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    f_title = get_font(28, bold=True)
    f_h = get_font(16, bold=True)
    f_body = get_font(13)
    f_small = get_font(11, bold=True)

    draw.text((60, 50), 'AUREA Logo System', font=f_title, fill=NAVY_PRIMARY)
    draw.text((60, 90), 'Three variants + multi-format outputs', font=f_body, fill=GRAY_500)

    y = 160
    # Mark
    cx, cy = 200, y + 80
    draw.polygon([
        (cx, cy - 50), (cx + 45, cy + 50), (cx + 32, cy + 50),
        (cx + 8, cy - 5), (cx - 8, cy - 5), (cx - 32, cy + 50), (cx - 45, cy + 50)
    ], fill=GOLD_PRIMARY)
    draw.polygon([
        (cx, cy - 8), (cx + 16, cy + 22), (cx + 10, cy + 22),
        (cx + 4, cy + 5), (cx - 4, cy + 5), (cx - 10, cy + 22), (cx - 16, cy + 22)
    ], fill=WHITE)
    draw.rectangle([cx - 28, cy + 28, cx + 28, cy + 36], fill=GOLD_PRIMARY)
    for x_off in [-15, 0, 15]:
        draw.ellipse([cx + x_off - 3, cy + 50, cx + x_off + 3, cy + 56], fill=GOLD_DARK)
    draw.text((cx, cy + 80), 'Logo Mark', font=f_h, fill=NAVY_PRIMARY)
    bbox = draw.textbbox((0, 0), 'Logo Mark', font=f_h)
    draw.text((cx - (bbox[2]-bbox[0])//2, cy + 100), 'Icon only', font=f_body, fill=GRAY_500)

    # Horizontal
    cx, cy = 600, y + 80
    draw.polygon([
        (cx, cy - 30), (cx + 27, cy + 30), (cx + 19, cy + 30),
        (cx + 5, cy - 3), (cx - 5, cy - 3), (cx - 19, cy + 30), (cx - 27, cy + 30)
    ], fill=GOLD_PRIMARY)
    for x_off in [-9, 0, 9]:
        draw.ellipse([cx + x_off - 2, cy + 36, cx + x_off + 2, cy + 40], fill=GOLD_DARK)
    # AUREA text right of mark
    f_w = get_font(36, bold=True)
    word = "AUREA"
    char_widths = []
    total_w = 0
    for ch in word:
        bbox = draw.textbbox((0, 0), ch, font=f_w)
        w = bbox[2] - bbox[0] + 4
        char_widths.append(w)
        total_w += w
    text_x = cx + 50
    for i, ch in enumerate(word):
        ratio = i / (len(word) - 1)
        color = tuple(int(GOLD_LIGHT[c] + (GOLD_DARK[c] - GOLD_LIGHT[c]) * ratio) for c in range(3))
        draw.text((text_x, cy - 20), ch, font=f_w, fill=color)
        text_x += char_widths[i]
    draw.text((cx - 30, cy + 100), 'Logo Horizontal', font=f_h, fill=NAVY_PRIMARY)
    bbox = draw.textbbox((0, 0), 'Logo Horizontal', font=f_h)
    draw.text((cx - (bbox[2]-bbox[0])//2, cy + 120), 'Mark + text', font=f_body, fill=GRAY_500)

    # Stacked
    cx, cy = 1050, y + 60
    draw.polygon([
        (cx, cy - 50), (cx + 45, cy + 50), (cx + 32, cy + 50),
        (cx + 8, cy - 5), (cx - 8, cy - 5), (cx - 32, cy + 50), (cx - 45, cy + 50)
    ], fill=GOLD_PRIMARY)
    for x_off in [-15, 0, 15]:
        draw.ellipse([cx + x_off - 3, cy + 55, cx + x_off + 3, cy + 61], fill=GOLD_DARK)
    f_w = get_font(28, bold=True)
    word = "AUREA"
    char_widths = []
    total_w = 0
    for ch in word:
        bbox = draw.textbbox((0, 0), ch, font=f_w)
        w = bbox[2] - bbox[0] + 3
        char_widths.append(w)
        total_w += w
    text_x = cx - total_w // 2
    for i, ch in enumerate(word):
        ratio = i / (len(word) - 1)
        color = tuple(int(GOLD_LIGHT[c] + (GOLD_DARK[c] - GOLD_LIGHT[c]) * ratio) for c in range(3))
        draw.text((text_x, cy + 80), ch, font=f_w, fill=color)
        text_x += char_widths[i]
    f_tag = get_font(8, bold=True)
    tag = "THE GOLD STANDARD"
    bbox = draw.textbbox((0, 0), tag, font=f_tag)
    draw.text((cx - (bbox[2]-bbox[0])//2, cy + 130), tag, font=f_tag, fill=GRAY_500)
    draw.text((cx, cy + 170), 'Logo Stacked', font=f_h, fill=NAVY_PRIMARY)
    bbox = draw.textbbox((0, 0), 'Logo Stacked', font=f_h)
    draw.text((cx - (bbox[2]-bbox[0])//2, cy + 190), 'Vertical layout', font=f_body, fill=GRAY_500)

    # File formats at bottom
    y = 460
    draw.text((60, y), 'AVAILABLE FORMATS', font=f_small, fill=GRAY_500)
    y += 30
    formats = [
        ('SVG', 'logo-mark.svg • logo-horizontal.svg • logo-stacked.svg', 6),
        ('PNG', '64, 128, 256, 512 px (logo-mark); 256, 512 px (stacked)', 6),
        ('Favicon', 'favicon.ico (16, 32, 48, 64, 128, 256) + PNG variants', 5),
        ('Animated', 'aurea-animated-splash.gif (860 KB, 4s looped)', 2),
    ]
    for label, files, count in formats:
        # Card
        draw.rounded_rectangle([60, y, 1340, y + 50], radius=8, fill=GRAY_50, outline=GOLD_PRIMARY)
        draw.rectangle([60, y, 64, y + 50], fill=GOLD_PRIMARY)
        draw.text((80, y + 8), label, font=f_h, fill=NAVY_PRIMARY)
        draw.text((80, y + 28), files, font=f_body, fill=GRAY_500)
        # Count badge
        draw.rounded_rectangle([1280, y + 12, 1330, y + 38], radius=12, fill=GOLD_PRIMARY)
        draw.text((1295, y + 16), f'{count}', font=f_h, fill=NAVY_PRIMARY)
        y += 60

    return img


def create_animation_showcase():
    """Show animation variants."""
    W, H = 1400, 700
    img = Image.new('RGB', (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    f_title = get_font(28, bold=True)
    f_h = get_font(18, bold=True)
    f_body = get_font(13)
    f_small = get_font(12, bold=True)
    f_tiny = get_font(10)

    draw.text((60, 50), 'AUREA Animation Suite', font=f_title, fill=NAVY_PRIMARY)
    draw.text((60, 90), 'Splash, spinners, and transitions', font=f_body, fill=GRAY_500)

    # Three animation mockups side by side
    # 1. Splash
    splash_x, splash_y = 100, 180
    sw, sh = 380, 420
    # Navy bg
    draw.rounded_rectangle([splash_x, splash_y, splash_x + sw, splash_y + sh], radius=12, fill=NAVY_PRIMARY)
    # Gold A
    ax, ay = splash_x + sw // 2, splash_y + 130
    draw.polygon([
        (ax, ay - 50), (ax + 45, ay + 50), (ax + 32, ay + 50),
        (ax + 8, ay - 5), (ax - 8, ay - 5), (ax - 32, ay + 50), (ax - 45, ay + 50)
    ], fill=GOLD_PRIMARY)
    draw.polygon([
        (ax, ay - 8), (ax + 16, ay + 22), (ax + 10, ay + 22),
        (ax + 4, ay + 5), (ax - 4, ay + 5), (ax - 10, ay + 22), (ax - 16, ay + 22)
    ], fill=NAVY_PRIMARY)
    draw.rectangle([ax - 28, ay + 28, ax + 28, ay + 36], fill=GOLD_PRIMARY)
    for x_off in [-15, 0, 15]:
        draw.ellipse([ax + x_off - 3, ay + 50, ax + x_off + 3, ay + 56], fill=GOLD_LIGHT)

    # AUREA text
    f_w = get_font(32, bold=True)
    word = "AUREA"
    char_widths = []
    total_w = 0
    for ch in word:
        bbox = draw.textbbox((0, 0), ch, font=f_w)
        w = bbox[2] - bbox[0] + 4
        char_widths.append(w)
        total_w += w
    text_x = ax - total_w // 2
    for i, ch in enumerate(word):
        ratio = i / (len(word) - 1)
        color = tuple(int(GOLD_LIGHT[c] + (GOLD_DARK[c] - GOLD_LIGHT[c]) * ratio) for c in range(3))
        draw.text((text_x, ay + 90), ch, font=f_w, fill=color)
        text_x += char_widths[i]

    # Divider
    draw.line([(ax - 70, ay + 140), (ax + 70, ay + 140)], fill=GOLD_PRIMARY, width=1)
    f_tag = get_font(9, bold=True)
    tag = "THE GOLD STANDARD OF DATA"
    bbox = draw.textbbox((0, 0), tag, font=f_tag)
    draw.text((ax - (bbox[2]-bbox[0])//2, ay + 155), tag, font=f_tag, fill=GOLD_LIGHT)

    # Loader bar
    draw.rectangle([ax - 70, ay + 200, ax + 70, ay + 204], fill=GOLD_DARK)
    draw.rectangle([ax - 70, ay + 200, ax - 20, ay + 204], fill=GOLD_PRIMARY)

    draw.text((splash_x + sw // 2 - 50, splash_y + sh - 30), '1. Splash Screen', font=f_h, fill=NAVY_PRIMARY)
    draw.text((splash_x + sw // 2 - 60, splash_y + sh - 10), '3.5s, click to skip', font=f_tiny, fill=GRAY_500)

    # 2. Spinner
    spin_x, spin_y = 510, 180
    sw, sh = 380, 420
    draw.rounded_rectangle([spin_x, spin_y, spin_x + sw, spin_y + sh], radius=12, fill=GRAY_50)
    # 3 dots spinner
    for i, x_off in enumerate([-50, 0, 50]):
        sx = spin_x + sw // 2 + x_off
        sy = spin_y + 150
        # Pulse sizes
        size = 12 if i == 1 else (16 if i == 0 else 10)
        draw.ellipse([sx - size, sy - size, sx + size, sy + size], fill=GOLD_PRIMARY)
    # Label
    draw.text((spin_x + sw // 2, spin_y + 230), 'Loading AUREA...', font=f_body, fill=NAVY_PRIMARY)
    bbox = draw.textbbox((0, 0), 'Loading AUREA...', font=f_body)
    draw.text((spin_x + sw // 2 - (bbox[2]-bbox[0])//2, spin_y + 230), 'Loading AUREA...', font=f_body, fill=NAVY_PRIMARY)

    # Show 5 more spinner variants
    spinner_y = spin_y + 290
    spinners = [
        ('● ● ●', 'MD3G Dots'),
        ('◐', 'Gold Ring'),
        ('A', 'Rotating A'),
        ('━', 'Progress Bar'),
        ('AUREA', 'Text Flicker'),
    ]
    for i, (icon, lbl) in enumerate(spinners):
        col = i % 5
        ix = spin_x + 30 + col * 65
        draw.rounded_rectangle([ix, spinner_y, ix + 55, spinner_y + 60], radius=8, fill=WHITE, outline=GOLD_PRIMARY)
        # Icon
        if '●' in icon:
            draw.text((ix + 4, spinner_y + 5), icon, font=get_font(10), fill=GOLD_PRIMARY)
        elif icon == '◐':
            draw.ellipse([ix + 16, spinner_y + 12, ix + 40, spinner_y + 36], outline=GOLD_PRIMARY, width=2)
            draw.pieslice([ix + 16, spinner_y + 12, ix + 40, spinner_y + 36], 0, 270, fill=GOLD_PRIMARY)
        elif icon == 'A':
            f_a = get_font(20, bold=True)
            draw.text((ix + 20, spinner_y + 8), 'A', font=f_a, fill=GOLD_PRIMARY)
        elif icon == '━':
            draw.rectangle([ix + 8, spinner_y + 22, ix + 47, spinner_y + 28], fill=GOLD_PRIMARY)
        else:
            f_a = get_font(8, bold=True)
            draw.text((ix + 8, spinner_y + 16), 'AUREA', font=f_a, fill=GOLD_PRIMARY)
        draw.text((ix + 4, spinner_y + 64), lbl, font=f_tiny, fill=GRAY_500)

    draw.text((spin_x + sw // 2 - 60, spin_y + sh - 30), '2. Loading Spinners', font=f_h, fill=NAVY_PRIMARY)
    draw.text((spin_x + sw // 2 - 60, spin_y + sh - 10), '8 brand-matched', font=f_tiny, fill=GRAY_500)

    # 3. Page transition
    pt_x, pt_y = 920, 180
    sw, sh = 380, 420
    draw.rounded_rectangle([pt_x, pt_y, pt_x + sw, pt_y + sh], radius=12, fill=WHITE, outline=GRAY_300)
    # Two pages side by side
    p1_x, p1_y = pt_x + 20, pt_y + 30
    pw, ph = 150, 350
    # Page 1
    draw.rounded_rectangle([p1_x, p1_y, p1_x + pw, p1_y + ph], radius=8, fill=NAVY_PRIMARY)
    draw.text((p1_x + 30, p1_y + 50), 'SPLASH', font=get_font(12, bold=True), fill=GOLD_LIGHT)
    # Mini A
    ax, ay = p1_x + pw // 2, p1_y + 100
    draw.polygon([
        (ax, ay - 25), (ax + 22, ay + 25), (ax + 16, ay + 25),
        (ax + 4, ay - 2), (ax - 4, ay - 2), (ax - 16, ay + 25), (ax - 22, ay + 25)
    ], fill=GOLD_PRIMARY)
    draw.text((p1_x + 40, p1_y + 180), 'AUREA', font=get_font(18, bold=True), fill=GOLD_PRIMARY)

    # Gold sweep in middle
    sweep_x = p1_x + pw + 5
    draw.rectangle([sweep_x, p1_y, sweep_x + 30, p1_y + ph], fill=GOLD_PRIMARY)
    draw.text((sweep_x, p1_y + ph // 2 - 10), 'A', font=get_font(40, bold=True), fill=NAVY_PRIMARY)

    # Page 2
    p2_x = sweep_x + 35
    draw.rounded_rectangle([p2_x, p1_y, p2_x + pw, p1_y + ph], radius=8, fill=WHITE, outline=GRAY_300)
    draw.text((p2_x + 30, p1_y + 30), 'DASHBOARD', font=get_font(12, bold=True), fill=NAVY_PRIMARY)
    # Mini chart
    for i in range(4):
        h = 30 + i * 15
        draw.rectangle([p2_x + 20, p1_y + 100 - h, p2_x + 32, p1_y + 100], fill=GOLD_PRIMARY)
    # Stats
    for i in range(3):
        draw.rounded_rectangle([p2_x + 50, p1_y + 80 + i * 70, p2_x + 140, p1_y + 110 + i * 70], radius=4, fill=GOLD_PRIMARY)
    # Stat labels
    for i in range(3):
        draw.text((p2_x + 56, p1_y + 88 + i * 70), '12K', font=get_font(11, bold=True), fill=NAVY_PRIMARY)

    draw.text((pt_x + sw // 2 - 80, pt_y + sh - 30), '3. Page Transitions', font=f_h, fill=NAVY_PRIMARY)
    draw.text((pt_x + sw // 2 - 70, pt_y + sh - 10), 'Gold sweep + slide', font=f_tiny, fill=GRAY_500)

    # Stats below
    y = 630
    stats = [
        ('8', 'Spinners'),
        ('3', 'Animation Variants'),
        ('4s', 'Splash Duration'),
        ('60fps', 'Performance'),
    ]
    for i, (val, lbl) in enumerate(stats):
        x = 100 + i * 320
        draw.rounded_rectangle([x, y, x + 280, y + 50], radius=8, fill=NAVY_PRIMARY)
        draw.text((x + 20, y + 10), val, font=get_font(20, bold=True), fill=GOLD_PRIMARY)
        draw.text((x + 100, y + 16), lbl, font=f_h, fill=WHITE)

    return img


def main():
    output_dir = '/home/user/aurea-docx-assets'
    os.makedirs(output_dir, exist_ok=True)

    generators = [
        ('brand_identity.png', create_brand_identity_card),
        ('color_palette.png', create_color_palette),
        ('logo_showcase.png', create_logo_showcase),
        ('animation_showcase.png', create_animation_showcase),
        ('mockup_admin.png', create_app_mockup_admin),
        ('mockup_customer360.png', create_app_mockup_customer360),
        ('mockup_mobile.png', create_app_mockup_mobile),
        ('integration_diagram.png', create_app_integration_diagram),
        ('stats_summary.png', create_stats_dashboard),
    ]

    print("Generating v2 DOCX images...")
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
