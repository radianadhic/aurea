"""
AUREA Presentation Image Generator
Generate additional diagrams and images for the AUREA Gold Standard PPTX
based on RKT Global CIF & Product Pricing Architecture concept.
"""

import os
from PIL import Image, ImageDraw, ImageFont
import math

# Brand colors
NAVY = (10, 25, 41)
NAVY_LIGHT = (26, 47, 71)
NAVY_DARK = (5, 15, 25)
GOLD = (212, 175, 55)
GOLD_LIGHT = (255, 215, 100)
GOLD_DARK = (184, 134, 11)
WHITE = (255, 255, 255)
GRAY_50 = (249, 250, 251)
GRAY_100 = (243, 244, 246)
GRAY_200 = (229, 231, 235)
GRAY_300 = (209, 213, 219)
GRAY_500 = (107, 114, 128)
GRAY_700 = (55, 65, 81)
SUCCESS = (22, 163, 74)
INFO = (2, 132, 199)
WARNING = (234, 88, 12)

# Fonts (try multiple paths)
FONT_PATHS = [
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
]
MONO_PATHS = [
    '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',
]

def get_font(size, bold=False, mono=False):
    paths = MONO_PATHS if mono else FONT_PATHS
    if not bold:
        paths = [p.replace('-Bold', '') for p in paths] + FONT_PATHS
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                pass
    return ImageFont.load_default()

def draw_text_centered(draw, x, y, text, font, fill, max_width=None):
    """Draw text centered at (x, y)."""
    if max_width:
        # Truncate if too long
        while text and font.getlength(text) > max_width:
            text = text[:-2]
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text((x - w/2, y - h/2), text, font=font, fill=fill)
    return w, h

def draw_text_in_box(draw, x, y, w, h, text, font, fill=WHITE, bg=None, border=None, border_width=2, bold=False):
    """Draw a rounded rectangle box with text inside."""
    if bg:
        draw.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=bg, outline=border, width=border_width)
    # Word wrap
    words = text.split(' ')
    lines = []
    current = ''
    for word in words:
        test = (current + ' ' + word).strip()
        if font.getlength(test) > w - 20:
            if current:
                lines.append(current)
            current = word
        else:
            current = test
    if current:
        lines.append(current)
    line_h = font.getbbox('Ay')[3] + 4
    total_h = line_h * len(lines)
    start_y = y + (h - total_h) / 2
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        line_w = bbox[2] - bbox[0]
        draw.text((x + (w - line_w) / 2, start_y + i * line_h), line, font=font, fill=fill)

def draw_title_bar(draw, w, h, title, subtitle=None):
    """Draw navy title bar at top of image."""
    bar_h = 80
    draw.rectangle([0, 0, w, bar_h], fill=NAVY)
    # Gold accent line
    draw.rectangle([0, bar_h, w, bar_h + 6], fill=GOLD)
    # Title
    title_font = get_font(28, bold=True)
    draw.text((24, 22), title, font=title_font, fill=GOLD_LIGHT)
    if subtitle:
        sub_font = get_font(14)
        draw.text((24, 54), subtitle, font=sub_font, fill=GRAY_300)
    return bar_h + 6  # Y where content starts


# ============================================================
# 1. Three Truths Diagram
# ============================================================
def gen_three_truths():
    W, H = 1400, 900
    img = Image.new('RGB', (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    title_h = draw_title_bar(draw, W, H, 'AUREA — Three Truths, One Experience',
                              'Party Truth • Commercial Truth • Contract Truth')

    # 3 main truth boxes
    box_w = 380
    box_h = 380
    box_y = title_h + 60
    box_x_start = (W - 3 * box_w - 2 * 40) / 2
    gap = 40

    truths = [
        {
            'num': '01',
            'title': 'PARTY TRUTH',
            'subtitle': 'Global CIF / MDM',
            'icon': '◆',
            'color': GOLD,
            'color_dark': GOLD_DARK,
            'items': [
                'Global Party ID',
                'Local CIF crosswalk',
                'Identity, KYC, Consent',
                'Relationships, Segments',
                'Risk flags, Context',
                'Customer 360',
            ]
        },
        {
            'num': '02',
            'title': 'COMMERCIAL TRUTH',
            'subtitle': 'Product Catalogue + Decisioning',
            'icon': '◆',
            'color': GOLD,
            'color_dark': GOLD_DARK,
            'items': [
                'Product specifications',
                'Market offers, Bundles',
                'Channel availability',
                'Pricing, Eligibility',
                'Policy limits, Documents',
                'Offer Snapshot',
            ]
        },
        {
            'num': '03',
            'title': 'CONTRACT TRUTH',
            'subtitle': 'Core / Cards / Lending',
            'icon': '◆',
            'color': GOLD,
            'color_dark': GOLD_DARK,
            'items': [
                'Account / facility / arrangement',
                'Booked rate and fees',
                'Approved limit',
                'Balance, Status',
                'Ledger and events',
                'Servicing history',
            ]
        },
    ]

    for i, t in enumerate(truths):
        x = box_x_start + i * (box_w + gap)
        # Outer card
        draw.rounded_rectangle([x, box_y, x + box_w, box_y + box_h], radius=12,
                              fill=NAVY, outline=GOLD, width=3)
        # Top accent
        draw.rectangle([x, box_y, x + box_w, box_y + 6], fill=GOLD)
        # Number circle
        cx = x + 50
        cy = box_y + 50
        draw.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], fill=GOLD, outline=GOLD_LIGHT, width=2)
        num_font = get_font(22, bold=True)
        draw_text_centered(draw, cx, cy, t['num'], num_font, NAVY)
        # Title
        title_font = get_font(24, bold=True)
        bbox = draw.textbbox((0, 0), t['title'], font=title_font)
        draw.text((x + 95, box_y + 30), t['title'], font=title_font, fill=GOLD)
        # Subtitle
        sub_font = get_font(13, bold=True)
        draw.text((x + 95, box_y + 60), t['subtitle'], font=sub_font, fill=GRAY_300)
        # Gold divider
        draw.line([(x + 30, box_y + 110), (x + box_w - 30, box_y + 110)], fill=GOLD, width=2)
        # Items
        item_y = box_y + 135
        for it in t['items']:
            # Diamond marker
            draw.polygon([(x + 40, item_y + 8), (x + 48, item_y + 16), (x + 40, item_y + 24), (x + 32, item_y + 16)], fill=GOLD)
            font = get_font(14)
            draw.text((x + 60, item_y), '  ' + it, font=font, fill=WHITE)
            item_y += 35

    # Bottom: critical distinction
    crit_y = box_y + box_h + 50
    draw.rounded_rectangle([100, crit_y, W - 100, crit_y + 130], radius=10,
                          fill=GOLD_LIGHT, outline=GOLD_DARK, width=3)
    # Title
    crit_title_font = get_font(18, bold=True)
    draw.text((130, crit_y + 15), '◆  CRITICAL DISTINCTION', font=crit_title_font, fill=NAVY)
    # Body
    body_font = get_font(14)
    body1 = 'A Global CIF is an enterprise party/customer identifier that maps every local CIF.'
    body2 = 'It does NOT require every legacy core to share one physical customer number.'
    draw.text((130, crit_y + 50), body1, font=body_font, fill=NAVY)
    draw.text((130, crit_y + 80), body2, font=body_font, fill=NAVY)
    # right-side arrow
    draw.text((W - 230, crit_y + 50), '◄── AUREA owns identity', font=get_font(13, bold=True), fill=GOLD_DARK)

    img.save('/home/user/aurea-pptx-assets/three_truths.png')
    print('  ✓ three_truths.png')


# ============================================================
# 2. Master Infographic — Channel → Platform → Core
# ============================================================
def gen_master_infographic():
    W, H = 1600, 1000
    img = Image.new('RGB', (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    title_h = draw_title_bar(draw, W, H, 'AUREA — Master Infographic: Channel → Truth → Booking',
                              'Every channel receives one customer and one offer')

    # Stage labels at top
    stages = ['1. DISCOVER', '2. PRE-QUALIFY', '3. ONBOARD', '4. BOOK', '5. SERVE']
    stage_w = (W - 200) / 5
    stage_y = title_h + 30
    stage_font = get_font(13, bold=True)
    for i, s in enumerate(stages):
        x = 100 + i * stage_w + stage_w/2
        # Number circle
        draw.ellipse([x - 18, stage_y, x + 18, stage_y + 36], fill=GOLD, outline=NAVY, width=2)
        n = str(i + 1)
        draw_text_centered(draw, x, stage_y + 18, n, get_font(20, bold=True), NAVY)
        # Label below
        draw.text((x - 60, stage_y + 42), s, font=stage_font, fill=NAVY)

    # 4 layers vertical
    layer_y_start = stage_y + 90
    layer_h = 150
    layer_gap = 25
    layer_x = 100
    layer_w = W - 200

    # Layer 1: Banking Channels
    layers = [
        {
            'title': 'BANKING CHANNELS',
            'subtitle': 'Unified Experience Layer',
            'color': NAVY_LIGHT,
            'items': ['MOBILE', 'WEB', 'BRANCH', 'RM', 'CONTACT', 'PARTNER API'],
        },
        {
            'title': 'CUSTOMER + OFFER EXPERIENCE FAÇADE',
            'subtitle': 'API Gateway • FAPI/OIDC • mTLS + Consent',
            'color': NAVY,
            'items': ['resolveCustomer', 'getContext', 'listEligibleOffers', 'calculatePriceAndLimit', 'startOnboarding'],
        },
        {
            'title': 'AUREA — CUSTOMER & COMMERCIAL TRUTH',
            'subtitle': 'Global CIF + Product Catalogue + Pricing & Limits',
            'color': NAVY_DARK,
            'items': ['Golden Customer (GC)', 'Golden Account (GA)', 'Golden Product (GP)', 'Offer Snapshot', 'Customer 360'],
        },
        {
            'title': 'BANKING SOURCES & BOOKING SYSTEMS',
            'subtitle': 'Vendor-neutral systems of record',
            'color': NAVY,
            'items': ['CRM/KYC', 'CORE BANKING', 'CARDS/LENDING', 'PAYMENTS/DEPOSITS', 'DATA/AI/FRAUD'],
        },
    ]

    for i, layer in enumerate(layers):
        y = layer_y_start + i * (layer_h + layer_gap)
        # Background
        draw.rounded_rectangle([layer_x, y, layer_x + layer_w, y + layer_h], radius=8,
                              fill=layer['color'], outline=GOLD, width=2)
        # Title
        title_font = get_font(15, bold=True)
        draw.text((layer_x + 20, y + 12), layer['title'], font=title_font, fill=GOLD)
        sub_font = get_font(11)
        draw.text((layer_x + 20, y + 32), layer['subtitle'], font=sub_font, fill=GRAY_300)
        # Items
        item_w = (layer_w - 60) / len(layer['items'])
        item_y = y + 70
        for j, it in enumerate(layer['items']):
            ix = layer_x + 30 + j * item_w
            # Item box
            if i == 2:  # Truth layer - gold
                draw.rounded_rectangle([ix, item_y, ix + item_w - 15, item_y + 60], radius=6,
                                      fill=GOLD, outline=GOLD_LIGHT, width=2)
                text_color = NAVY
            else:
                draw.rounded_rectangle([ix, item_y, ix + item_w - 15, item_y + 60], radius=6,
                                      fill=NAVY_LIGHT, outline=GOLD, width=1)
                text_color = WHITE
            item_font = get_font(11, bold=True)
            draw_text_in_box(draw, ix, item_y, item_w - 15, 60, it, item_font, fill=text_color)

    # Cross-cutting services between layers 2-3
    cc_y = layer_y_start + 2 * (layer_h + layer_gap) + layer_h - 10
    # Already drawn — skip

    # Cross-cutting icons at bottom
    bottom_y = layer_y_start + 4 * (layer_h + layer_gap) + 20
    services = ['API GATEWAY', 'EVENT STREAM', 'WORKFLOW + DMN', 'CDC ADAPTERS', 'AUDIT + OBSERVABILITY']
    sx = 100
    sw = (W - 200) / 5
    for i, s in enumerate(services):
        x = sx + i * sw + 20
        draw.rounded_rectangle([x, bottom_y, x + sw - 40, bottom_y + 40], radius=6,
                              fill=GOLD, outline=GOLD_DARK, width=2)
        sfont = get_font(11, bold=True)
        draw_text_in_box(draw, x, bottom_y, sw - 40, 40, s, sfont, fill=NAVY)

    img.save('/home/user/aurea-pptx-assets/master_infographic.png')
    print('  ✓ master_infographic.png')


# ============================================================
# 3. Customer Journey — 7 Steps
# ============================================================
def gen_customer_journey():
    W, H = 1600, 1000
    img = Image.new('RGB', (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    title_h = draw_title_bar(draw, W, H, 'AUREA — Customer Journey: From Discover to Serve',
                              'The customer is recognized before the bank creates a contract')

    steps = [
        ('1', 'DISCOVER', 'Browse and\ncompare', 'Channel-ready\ncatalogue', 'Session ID'),
        ('2', 'IDENTIFY', 'Log in or\nprovide ID', 'Resolve party /\nprospect', 'Global Party ID'),
        ('3', 'PRE-QUALIFY', 'See relevant\noffers', 'Eligibility +\nsoft limit', 'Offer candidates'),
        ('4', 'ONBOARD', 'Submit data\n+ consent', 'KYC, dedupe,\nenrich', 'Verified CIF'),
        ('5', 'DECIDE', 'Accept price\n+ limit', 'Final rules +\nsnapshot', 'Offer Snapshot'),
        ('6', 'BOOK', 'Open\nproduct', 'Create local\nCIF if needed', 'Account /\nFacility'),
        ('7', 'SERVE', 'Continue on\nany channel', 'Events refresh\n360 view', 'Customer 360'),
    ]

    n = len(steps)
    step_w = (W - 200) / n
    step_y = title_h + 80
    step_h = 360

    for i, (num, title, cust, plat, output) in enumerate(steps):
        x = 100 + i * step_w
        # Card
        draw.rounded_rectangle([x + 10, step_y, x + step_w - 10, step_y + step_h], radius=10,
                              fill=WHITE, outline=NAVY, width=2)
        # Top header
        draw.rectangle([x + 10, step_y, x + step_w - 10, step_y + 60], fill=NAVY)
        # Number badge
        cx = x + 40
        cy = step_y + 30
        draw.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=GOLD, outline=GOLD_LIGHT, width=2)
        draw_text_centered(draw, cx, cy, num, get_font(18, bold=True), NAVY)
        # Step name
        sn_font = get_font(16, bold=True)
        draw.text((cx + 30, step_y + 18), title, font=sn_font, fill=GOLD_LIGHT)

        # Customer block
        by1 = step_y + 80
        draw.rounded_rectangle([x + 20, by1, x + step_w - 20, by1 + 90], radius=6,
                              fill=GRAY_100, outline=GRAY_300, width=1)
        # Label
        lbl_font = get_font(10, bold=True)
        draw.text((x + 30, by1 + 8), 'CUSTOMER', font=lbl_font, fill=GRAY_500)
        # Text
        for j, line in enumerate(cust.split('\n')):
            tfont = get_font(12)
            draw.text((x + 30, by1 + 28 + j * 18), line, font=tfont, fill=NAVY)

        # Down arrow
        ax = x + step_w/2
        ay1 = by1 + 95
        ay2 = ay1 + 20
        draw.line([(ax, ay1), (ax, ay2)], fill=GOLD, width=3)
        draw.polygon([(ax - 6, ay2), (ax + 6, ay2), (ax, ay2 + 8)], fill=GOLD)

        # Platform block
        by2 = ay2 + 15
        draw.rounded_rectangle([x + 20, by2, x + step_w - 20, by2 + 90], radius=6,
                              fill=NAVY, outline=GOLD, width=1)
        lbl2_font = get_font(10, bold=True)
        draw.text((x + 30, by2 + 8), 'AUREA PLATFORM', font=lbl2_font, fill=GOLD)
        for j, line in enumerate(plat.split('\n')):
            tfont = get_font(12)
            draw.text((x + 30, by2 + 28 + j * 18), line, font=tfont, fill=WHITE)

        # Output pill
        by3 = by2 + 105
        ow = step_w - 60
        draw.rounded_rectangle([x + 30, by3, x + 30 + ow, by3 + 30], radius=15,
                              fill=GOLD, outline=GOLD_DARK, width=1)
        ofont = get_font(11, bold=True)
        draw_text_in_box(draw, x + 30, by3, ow, 30, output, ofont, fill=NAVY)

        # Arrow to next step
        if i < n - 1:
            ax = x + step_w - 10
            ay = step_y + step_h/2
            draw.line([(ax, ay), (ax + 20, ay)], fill=GOLD, width=3)
            draw.polygon([(ax + 20, ay - 5), (ax + 20, ay + 5), (ax + 28, ay)], fill=GOLD)

    # Bottom: Continuity rule
    cr_y = step_y + step_h + 50
    draw.rounded_rectangle([100, cr_y, W - 100, cr_y + 130], radius=10,
                          fill=NAVY, outline=GOLD, width=3)
    cr_title = get_font(18, bold=True)
    draw.text((130, cr_y + 15), '◆  CONTINUITY RULE', font=cr_title, fill=GOLD)
    cr_body = get_font(14)
    body1 = 'Every step carries Global Party ID + Offer Snapshot ID + Journey ID.'
    body2 = 'The core receives a deterministic booking request — not a re-priced or re-matched customer.'
    draw.text((130, cr_y + 55), body1, font=cr_body, fill=WHITE)
    draw.text((130, cr_y + 85), body2, font=cr_body, fill=WHITE)

    img.save('/home/user/aurea-pptx-assets/customer_journey.png')
    print('  ✓ customer_journey.png')


# ============================================================
# 4. Global CIF — 6-step Pipeline
# ============================================================
def gen_cif_pipeline():
    W, H = 1600, 900
    img = Image.new('RGB', (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    title_h = draw_title_bar(draw, W, H, 'AUREA — Global CIF: 6-Step Identity Resolution Pipeline',
                              'Capture → Standardize → Match → Survive → Govern → Publish')

    steps = [
        ('CAPTURE', 'API + events + CDC', GOLD, 'IN'),
        ('STANDARDIZE', 'names • addresses • IDs', NAVY_LIGHT, ''),
        ('MATCH', 'exact + fuzzy + graph', NAVY_LIGHT, ''),
        ('SURVIVE', 'source trust + recency', NAVY_LIGHT, ''),
        ('GOVERN', 'steward exceptions', NAVY_LIGHT, ''),
        ('PUBLISH', 'API + Customer events', GOLD, 'OUT'),
    ]

    n = len(steps)
    step_w = 220
    total_w = n * step_w
    start_x = (W - total_w) / 2
    step_y = title_h + 100
    step_h = 240

    for i, (title, sub, color, marker) in enumerate(steps):
        x = start_x + i * step_w
        # Card
        draw.rounded_rectangle([x + 5, step_y, x + step_w - 5, step_y + step_h], radius=10,
                              fill=color, outline=GOLD, width=3)
        # Number
        num_font = get_font(60, bold=True)
        draw_text_centered(draw, x + step_w/2, step_y + 50, str(i+1), num_font, GOLD if color != GOLD else NAVY)
        # Title
        t_font = get_font(18, bold=True)
        draw_text_centered(draw, x + step_w/2, step_y + 130, title, t_font, GOLD if color != GOLD else NAVY)
        # Sub
        s_font = get_font(11)
        draw_text_centered(draw, x + step_w/2, step_y + 160, sub, s_font, WHITE if color != GOLD else NAVY)

        # Arrow
        if i < n - 1:
            ax1 = x + step_w - 5
            ax2 = x + step_w + 15
            ay = step_y + step_h/2
            draw.line([(ax1, ay), (ax2, ay)], fill=GOLD, width=4)
            draw.polygon([(ax2, ay - 8), (ax2, ay + 8), (ax2 + 12, ay)], fill=GOLD)

    # Bottom: Golden Record Domains
    gd_y = step_y + step_h + 60
    draw.rounded_rectangle([100, gd_y, W - 100, gd_y + 250], radius=10,
                          fill=NAVY, outline=GOLD, width=3)
    gd_title = get_font(20, bold=True)
    draw.text((130, gd_y + 20), '◆  GOLDEN RECORD DOMAINS', font=gd_title, fill=GOLD)

    domains = [
        ('Identity', 'legal name • DOB/incorporation • national ID'),
        ('Contact', 'address • phone • email • preferred language'),
        ('Compliance', 'KYC/CDD • screening • tax • consent'),
        ('Relationships', 'household • group • beneficial owner • mandate'),
        ('Context', 'segment • lifecycle • risk flags • preferences'),
    ]
    col_w = (W - 260) / 5
    for i, (name, desc) in enumerate(domains):
        x = 130 + i * col_w
        # Card
        draw.rounded_rectangle([x, gd_y + 70, x + col_w - 20, gd_y + 170], radius=8,
                              fill=NAVY_LIGHT, outline=GOLD, width=2)
        # Name
        nf = get_font(15, bold=True)
        draw.text((x + 15, gd_y + 85), name, font=nf, fill=GOLD)
        # Description
        for j, line in enumerate(desc.split(' • ')):
            df = get_font(11)
            draw.text((x + 15, gd_y + 110 + j * 16), '• ' + line, font=df, fill=WHITE)

    img.save('/home/user/aurea-pptx-assets/cif_pipeline.png')
    print('  ✓ cif_pipeline.png')


# ============================================================
# 5. 3-identifier chain
# ============================================================
def gen_identifier_chain():
    W, H = 1400, 700
    img = Image.new('RGB', (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    title_h = draw_title_bar(draw, W, H, 'AUREA — Three Identifiers: Loose Coupling Across Systems',
                              'Party → Offer → Arrangement — the identifier chain that travels everywhere')

    items = [
        {
            'letter': 'P',
            'title': 'PARTY / GLOBAL CIF',
            'subtitle': 'Person or organization',
            'color': NAVY,
            'sub': 'enterprise identity + local CIF map',
            'content': [
                'Identity + Contact',
                'identifiers • names • address',
                'KYC + Consent',
                'CDD • screening • privacy',
                'Core CIF Crosswalk',
                'system + customer number',
            ]
        },
        {
            'letter': 'O',
            'title': 'OFFER SNAPSHOT',
            'subtitle': 'Terms shown and accepted',
            'color': GOLD,
            'sub': 'pricing + limit + conditions',
            'content': [
                'Product Spec',
                'capabilities • lifecycle',
                'Price + Limit',
                'components • rules • versions',
            ]
        },
        {
            'letter': 'A',
            'title': 'ARRANGEMENT / ACCOUNT',
            'subtitle': 'Booked contract / facility',
            'color': NAVY,
            'sub': 'core account + lifecycle status',
            'content': [
                'Balance + Exposure',
                'utilization • status • events',
                'Lifecycle',
                'open • service • close',
            ]
        },
    ]

    card_w = 380
    card_h = 480
    card_y = title_h + 50
    start_x = (W - 3 * card_w - 2 * 60) / 2
    gap = 60

    for i, it in enumerate(items):
        x = start_x + i * (card_w + gap)
        # Card
        draw.rounded_rectangle([x, card_y, x + card_w, card_y + card_h], radius=12,
                              fill=it['color'], outline=GOLD, width=3)
        # Top accent
        draw.rectangle([x, card_y, x + card_w, card_y + 6], fill=GOLD)
        # Big letter
        lf = get_font(120, bold=True)
        letter_color = NAVY if it['color'] == GOLD else GOLD
        draw.text((x + 30, card_y + 30), it['letter'], font=lf, fill=letter_color)
        # Title
        tf = get_font(20, bold=True)
        title_color = NAVY if it['color'] == GOLD else GOLD
        draw.text((x + 30, card_y + 180), it['title'], font=tf, fill=title_color)
        # Subtitle
        sf = get_font(13, bold=True)
        sub_color = NAVY if it['color'] == GOLD else GRAY_300
        draw.text((x + 30, card_y + 215), it['subtitle'], font=sf, fill=sub_color)
        # Sub-sub
        ssf = get_font(11, bold=True)
        ssub_color = NAVY if it['color'] == GOLD else GRAY_300
        draw.text((x + 30, card_y + 240), it['sub'], font=ssf, fill=ssub_color)
        # Divider
        draw.line([(x + 30, card_y + 275), (x + card_w - 30, card_y + 275)], fill=GOLD, width=2)
        # Content
        cy = card_y + 295
        ccolor = NAVY if it['color'] == GOLD else WHITE
        for line in it['content']:
            f = get_font(13)
            draw.text((x + 30, cy), '◆ ' + line, font=f, fill=ccolor)
            cy += 28

    # Bottom: chain
    chain_y = card_y + card_h + 30
    chain = 'Journey ID  →  Global Party ID  →  Offer Snapshot ID  →  Arrangement / Account ID  →  local CIF / system keys'
    cf = get_font(16, bold=True)
    # Background
    bbox = draw.textbbox((0, 0), chain, font=cf)
    cw = bbox[2] - bbox[0] + 60
    cx = (W - cw) / 2
    draw.rounded_rectangle([cx, chain_y, cx + cw, chain_y + 60], radius=30,
                          fill=NAVY, outline=GOLD, width=3)
    draw_text_centered(draw, cx + cw/2, chain_y + 30, chain, cf, GOLD_LIGHT)

    img.save('/home/user/aurea-pptx-assets/identifier_chain.png')
    print('  ✓ identifier_chain.png')


# ============================================================
# 6. Integration Sequence (8 steps with swimlanes)
# ============================================================
def gen_integration_sequence():
    W, H = 1600, 900
    img = Image.new('RGB', (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    title_h = draw_title_bar(draw, W, H, 'AUREA — Integration Sequence: One Booking, All Channels',
                              'Core books the same answer every channel presented')

    # 6 swimlanes
    lanes = ['CHANNEL', 'EXPERIENCE', 'FAÇADE', 'GLOBAL CIF', 'PRODUCT + DECISION', 'CORE / LENDING']
    lane_w = (W - 200) / 6
    lane_h = 600
    lane_y_start = title_h + 60
    lane_x_start = 100

    # Lane headers
    for i, l in enumerate(lanes):
        x = lane_x_start + i * lane_w
        # Header
        draw.rounded_rectangle([x, lane_y_start, x + lane_w - 10, lane_y_start + 50], radius=8,
                              fill=NAVY, outline=GOLD, width=2)
        lf = get_font(11, bold=True)
        draw_text_in_box(draw, x, lane_y_start, lane_w - 10, 50, l, lf, fill=GOLD)
        # Body
        draw.rectangle([x, lane_y_start + 50, x + lane_w - 10, lane_y_start + lane_h + 50],
                      outline=GRAY_300, width=1, fill=WHITE)
        # Dashed line down center
        for y in range(lane_y_start + 60, lane_y_start + lane_h + 50, 15):
            draw.line([(x + (lane_w - 10)/2, y), (x + (lane_w - 10)/2, y + 6)], fill=GRAY_300, width=2)

    # 8 steps
    steps = [
        ('1', 'Start journey', 0, ['CHANNEL'], GOLD),
        ('2', 'Resolve / create prospect', 1, ['FAÇADE', 'GLOBAL CIF'], GOLD),
        ('3', 'Eligible offers + price + limit', 1, ['PRODUCT + DECISION', 'GLOBAL CIF'], GOLD),
        ('4', 'Consent + KYC + selected offer', 0, ['CHANNEL', 'GLOBAL CIF', 'PRODUCT + DECISION'], GOLD),
        ('5', 'Verify → Global Party ID', 1, ['GLOBAL CIF'], GOLD),
        ('6', 'Persist final Offer Snapshot', 1, ['PRODUCT + DECISION'], GOLD),
        ('7', 'Book idempotently with snapshot', 1, ['CORE / LENDING', 'GLOBAL CIF', 'PRODUCT + DECISION'], GOLD),
        ('8', 'Publish events', 1, ['GLOBAL CIF', 'PRODUCT + DECISION'], GOLD),
    ]

    n = len(steps)
    step_spacing = (lane_h - 100) / n
    for i, (num, text, row, lanes_in, color) in enumerate(steps):
        sy = lane_y_start + 80 + i * step_spacing
        # Step number badge
        for j, l in enumerate(lanes):
            if l in lanes_in:
                x = lane_x_start + j * lane_w
                cx = x + (lane_w - 10)/2
                # Activate icon (filled circle)
                draw.ellipse([cx - 14, sy - 14, cx + 14, sy + 14], fill=GOLD, outline=GOLD_LIGHT, width=2)
                draw_text_centered(draw, cx, sy, num, get_font(13, bold=True), NAVY)
        # Label
        if i == 0:
            label_x = lane_x_start
        else:
            label_x = 20
        lf = get_font(10, bold=True)
        draw.text((label_x + 5, sy - 8), f'STEP {num}', font=lf, fill=GOLD_DARK)
        tf = get_font(11)
        draw.text((label_x + 5, sy + 4), text, font=tf, fill=NAVY)

    # Bottom controls
    ctrl_y = lane_y_start + lane_h + 80
    draw.rounded_rectangle([100, ctrl_y, W - 100, ctrl_y + 60], radius=8,
                          fill=GOLD_LIGHT, outline=GOLD_DARK, width=2)
    cf = get_font(13, bold=True)
    draw_text_centered(draw, W/2, ctrl_y + 30,
                       'CONTROLS:  correlation ID  •  idempotency key  •  rule/version trace  •  consent evidence  •  reconciliation  •  replay-safe events',
                       cf, NAVY)

    img.save('/home/user/aurea-pptx-assets/integration_sequence.png')
    print('  ✓ integration_sequence.png')


# ============================================================
# 7. Operating Model — 6 stages + roles
# ============================================================
def gen_operating_model():
    W, H = 1600, 900
    img = Image.new('RGB', (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    title_h = draw_title_bar(draw, W, H, 'AUREA — Operating Model: Governance as a First-Class Concern',
                              'Product lifecycle, accountable roles, minimum controls')

    # Left side: Product lifecycle (6 stages)
    lc_x = 100
    lc_y = title_h + 50
    lc_w = 700
    lc_h = 700

    draw.rounded_rectangle([lc_x, lc_y, lc_x + lc_w, lc_y + lc_h], radius=10,
                          fill=NAVY, outline=GOLD, width=3)
    lc_title = get_font(20, bold=True)
    draw.text((lc_x + 20, lc_y + 20), '◆  PRODUCT LIFECYCLE', font=lc_title, fill=GOLD)

    stages = ['DRAFT', 'REVIEW', 'APPROVE', 'PUBLISH', 'MONITOR', 'RETIRE']
    stage_colors = [GRAY_500, WARNING, GOLD, SUCCESS, INFO, GRAY_700]
    n = len(stages)
    sw = (lc_w - 80) / n
    sy = lc_y + 100
    for i, (s, c) in enumerate(zip(stages, stage_colors)):
        x = lc_x + 40 + i * sw
        # Stage box
        draw.rounded_rectangle([x, sy, x + sw - 15, sy + 120], radius=8, fill=c, outline=GOLD, width=2)
        # Number
        nf = get_font(30, bold=True)
        draw_text_centered(draw, x + (sw - 15)/2, sy + 30, str(i+1), nf, WHITE)
        # Name
        nf2 = get_font(11, bold=True)
        draw_text_centered(draw, x + (sw - 15)/2, sy + 80, s, nf2, WHITE)
        # Arrow
        if i < n - 1:
            ax1 = x + sw - 15
            ax2 = x + sw
            ay = sy + 60
            draw.line([(ax1, ay), (ax2, ay)], fill=GOLD, width=3)
            draw.polygon([(ax2, ay - 5), (ax2, ay + 5), (ax2 + 5, ay)], fill=GOLD)

    # Minimum controls
    mc_y = sy + 160
    draw.rounded_rectangle([lc_x + 20, mc_y, lc_x + lc_w - 20, mc_y + 220], radius=8,
                          fill=NAVY_LIGHT, outline=GOLD, width=1)
    mct = get_font(15, bold=True)
    draw.text((lc_x + 40, mc_y + 15), 'MINIMUM CONTROLS', font=mct, fill=GOLD)
    controls = ['four-eyes approval', 'effective dating', 'simulation', 'rollback',
                'audit trail', 'DQ thresholds', 'exception queue']
    for i, c in enumerate(controls):
        row, col = i // 2, i % 2
        x = lc_x + 40 + col * 320
        y = mc_y + 50 + row * 28
        draw.text((x, y), '✓ ' + c, font=get_font(13), fill=WHITE)

    # Right side: Accountable roles
    rr_x = 820
    rr_y = title_h + 50
    rr_w = W - rr_x - 100
    rr_h = 700

    draw.rounded_rectangle([rr_x, rr_y, rr_x + rr_w, rr_y + rr_h], radius=10,
                          fill=WHITE, outline=NAVY, width=3)
    rrt = get_font(20, bold=True)
    draw.text((rr_x + 20, rr_y + 20), '◆  ACCOUNTABLE ROLES & CONTROLS', font=rrt, fill=NAVY)

    roles = [
        ('Product Owner', GOLD, 'Defines offer intent, target segments, economics and retirement.'),
        ('Pricing / Risk', GOLD_DARK, 'Approves price components, eligibility, exposure and limit policies.'),
        ('Customer Data Owner', NAVY, 'Owns identity model, source authority, consent and quality thresholds.'),
        ('Data Steward', NAVY_LIGHT, 'Resolves match exceptions, monitors duplicates and repairs lineage.'),
        ('Architecture / Platform', GOLD, 'Owns API contracts, events, security, resilience and observability.'),
        ('Operations / Compliance', NAVY, 'Validates fulfillment, disclosures, KYC controls and audit evidence.'),
    ]

    ry = rr_y + 70
    rh = 90
    for name, color, desc in roles:
        # Card
        draw.rounded_rectangle([rr_x + 20, ry, rr_x + rr_w - 20, ry + rh], radius=8,
                              fill=GRAY_100, outline=color, width=2)
        # Color bar
        draw.rectangle([rr_x + 20, ry, rr_x + 28, ry + rh], fill=color)
        # Name
        nf = get_font(15, bold=True)
        draw.text((rr_x + 50, ry + 15), name, font=nf, fill=color)
        # Description
        df = get_font(11)
        draw.text((rr_x + 50, ry + 45), desc, font=df, fill=NAVY)
        ry += rh + 8

    img.save('/home/user/aurea-pptx-assets/operating_model.png')
    print('  ✓ operating_model.png')


# ============================================================
# 8. Data Landing — Bronze → Silver → Gold
# ============================================================
def gen_data_landing():
    W, H = 1600, 900
    img = Image.new('RGB', (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    title_h = draw_title_bar(draw, W, H, 'AUREA — Data Landing: Bronze → Silver → Gold',
                              'Operational truth resolves identity; the lakehouse progressively standardizes events')

    # 3 main tiers
    tiers = [
        {
            'name': 'RAW / BRONZE',
            'subtitle': 'Immutable source payloads',
            'color': NAVY,
            'items': [
                'party_event', 'customer_event', 'local_cif',
                'account_event', 'product_offer', 'price_decision',
                'limit_decision', 'exposure_event', 'market_tick',
                'channel_interaction', 'source_timestamp', 'schema_id',
            ]
        },
        {
            'name': 'CONFORMED / SILVER',
            'subtitle': 'Enterprise keys + normalized structures',
            'color': NAVY_LIGHT,
            'items': [
                'party_master', 'party_identifier', 'local_cif_xref',
                'party_relationship', 'product_spec', 'market_offer',
                'price_component', 'limit_policy', 'arrangement',
                'account', 'exposure', 'market_instrument',
            ]
        },
        {
            'name': 'CURATED / GOLD',
            'subtitle': 'Dimensional facts and reusable metrics',
            'color': GOLD,
            'items': [
                'dim_party', 'dim_customer', 'dim_product', 'dim_offer',
                'dim_account', 'dim_instrument', 'bridge_party_account',
                'fact_interaction', 'fact_offer_decision',
                'fact_account_snapshot', 'fact_exposure', 'fact_market_price',
            ]
        },
    ]

    tier_w = 420
    tier_h = 500
    tier_y = title_h + 50
    start_x = (W - 3 * tier_w - 2 * 60) / 2
    gap = 60

    for i, t in enumerate(tiers):
        x = start_x + i * (tier_w + gap)
        # Card
        text_color = NAVY if t['color'] == GOLD else WHITE
        draw.rounded_rectangle([x, tier_y, x + tier_w, tier_y + tier_h], radius=12,
                              fill=t['color'], outline=GOLD, width=3)
        # Top
        draw.rectangle([x, tier_y, x + tier_w, tier_y + 6], fill=GOLD)
        # Name
        nf = get_font(22, bold=True)
        draw.text((x + 20, tier_y + 25), t['name'], font=nf, fill=GOLD if t['color'] != GOLD else NAVY)
        # Sub
        sf = get_font(12, bold=True)
        draw.text((x + 20, tier_y + 60), t['subtitle'], font=sf, fill=text_color)
        # Divider
        draw.line([(x + 20, tier_y + 90), (x + tier_w - 20, tier_y + 90)], fill=GOLD, width=2)
        # Items in 2 columns
        col_h = (tier_h - 110) / 6
        for j, it in enumerate(t['items']):
            row, col = j // 2, j % 2
            ix = x + 20 + col * (tier_w/2 - 5)
            iy = tier_y + 110 + row * 28
            # Marker
            marker_color = NAVY if t['color'] == GOLD else GOLD
            draw.polygon([(ix + 4, iy + 8), (ix + 12, iy + 16), (ix + 4, iy + 24), (ix - 4, iy + 16)], fill=marker_color)
            # Text
            font_color = NAVY if t['color'] == GOLD else WHITE
            f = get_font(11, bold=True)
            draw.text((ix + 20, iy), it, font=f, fill=font_color)
        # Arrow
        if i < 2:
            ax1 = x + tier_w
            ax2 = x + tier_w + 30
            ay = tier_y + tier_h/2
            draw.line([(ax1, ay), (ax2, ay)], fill=GOLD, width=4)
            draw.polygon([(ax2, ay - 8), (ax2, ay + 8), (ax2 + 12, ay)], fill=GOLD)

    # Bottom: marts
    marts_y = tier_y + tier_h + 50
    draw.rounded_rectangle([100, marts_y, W - 100, marts_y + 200], radius=10,
                          fill=GOLD, outline=GOLD_DARK, width=3)
    m_title = get_font(18, bold=True)
    draw.text((130, marts_y + 15), '◆  MARTS — DWH + DATA PRODUCTS', font=m_title, fill=NAVY)
    marts = [
        'Customer 360', 'Pricing & Limit', 'Risk / Exposure',
        'Product Profitability', 'Treasury / Liquidity', 'Channel Funnel',
        'Regulatory / Finance', 'AI features'
    ]
    mw = (W - 260) / 4
    for i, m in enumerate(marts):
        col, row = i % 4, i // 4
        x = 130 + col * mw
        y = marts_y + 60 + row * 60
        # Pill
        draw.rounded_rectangle([x, y, x + mw - 20, y + 45], radius=22, fill=NAVY, outline=GOLD_LIGHT, width=2)
        pf = get_font(13, bold=True)
        draw_text_in_box(draw, x, y, mw - 20, 45, m, pf, fill=GOLD)

    img.save('/home/user/aurea-pptx-assets/data_landing.png')
    print('  ✓ data_landing.png')


# ============================================================
# 9. Implementation Path — 4 Waves
# ============================================================
def gen_implementation_path():
    W, H = 1600, 900
    img = Image.new('RGB', (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    title_h = draw_title_bar(draw, W, H, 'AUREA — Indicative Implementation Path: 4 Waves',
                              'Deliver value without a core replacement')

    waves = [
        {
            'name': 'WAVE 0',
            'subtitle': 'FOUNDATION',
            'duration': '0–6 weeks',
            'color': GRAY_500,
            'items': [
                'Ownership + canonical model',
                'API / event standards',
                'Security + consent pattern',
            ]
        },
        {
            'name': 'WAVE 1',
            'subtitle': 'CUSTOMER HUB',
            'duration': '6–16 weeks',
            'color': NAVY,
            'items': [
                'Global Party ID + crosswalk',
                'Match / merge + stewardship',
                'Customer Context API',
            ]
        },
        {
            'name': 'WAVE 2',
            'subtitle': 'PRODUCT + DECISION',
            'duration': '12–24 weeks',
            'color': GOLD_DARK,
            'items': [
                'Catalogue + offer versioning',
                'Pricing / eligibility / limit',
                'Offer Snapshot API',
            ]
        },
        {
            'name': 'WAVE 3',
            'subtitle': 'CHANNEL + CORE ROLLOUT',
            'duration': '20–36+ weeks',
            'color': GOLD,
            'items': [
                'Priority journeys + products',
                'Core booking adapters',
                'Events, monitoring, adoption',
            ]
        },
    ]

    n = len(waves)
    wave_w = 320
    wave_h = 480
    wave_y = title_h + 80
    start_x = (W - n * wave_w - (n-1) * 30) / 2

    for i, w in enumerate(waves):
        x = start_x + i * (wave_w + 30)
        # Card
        text_color = NAVY if w['color'] in [GOLD, GOLD_LIGHT] else WHITE
        # Background gradient (solid)
        draw.rounded_rectangle([x, wave_y, x + wave_w, wave_y + wave_h], radius=15,
                              fill=w['color'], outline=GOLD, width=3)
        # Top bar with number
        draw.rectangle([x, wave_y, x + wave_w, wave_y + 80], fill=NAVY)
        # Number
        nf = get_font(40, bold=True)
        draw_text_centered(draw, x + wave_w/2, wave_y + 40, f'W{i}', nf, GOLD)
        # Subtitle
        sf = get_font(20, bold=True)
        sub_color = NAVY if w['color'] in [GOLD, GOLD_LIGHT] else GOLD
        draw_text_centered(draw, x + wave_w/2, wave_y + 110, w['subtitle'], sf, sub_color)
        # Duration
        df = get_font(12, bold=True)
        dur_color = NAVY if w['color'] in [GOLD, GOLD_LIGHT] else GRAY_300
        draw_text_centered(draw, x + wave_w/2, wave_y + 140, w['duration'], df, dur_color)
        # Divider
        draw.line([(x + 30, wave_y + 175), (x + wave_w - 30, wave_y + 175)], fill=GOLD, width=2)
        # Items
        iy = wave_y + 210
        for it in w['items']:
            # Marker
            draw.polygon([(x + 40, iy + 12), (x + 50, iy + 22), (x + 40, iy + 32), (x + 30, iy + 22)], fill=GOLD)
            tf = get_font(14)
            draw.text((x + 65, iy + 5), it, font=tf, fill=text_color)
            iy += 60

        # Arrow to next
        if i < n - 1:
            ax1 = x + wave_w
            ax2 = x + wave_w + 25
            ay = wave_y + wave_h/2
            draw.line([(ax1, ay), (ax2, ay)], fill=GOLD, width=4)
            draw.polygon([(ax2, ay - 8), (ax2, ay + 8), (ax2 + 12, ay)], fill=GOLD)

    # Bottom: KPIs
    kpi_y = wave_y + wave_h + 60
    draw.rounded_rectangle([100, kpi_y, W - 100, kpi_y + 200], radius=10,
                          fill=NAVY, outline=GOLD, width=3)
    kt = get_font(18, bold=True)
    draw.text((130, kpi_y + 15), '◆  MEASURE PROGRESS BY', font=kt, fill=GOLD)
    kpis = [
        ('DUPLICATE RATE', '15% → 2%'),
        ('MATCH PRECISION', '0.91 → 0.97'),
        ('DECISION LATENCY', '800ms → 120ms'),
        ('PRICE VARIANCE', '±5% → ±0.5%'),
        ('ONBOARDING COMPLETION', '60% → 88%'),
        ('BOOKING RECONCILIATION', '12 → 0 issues/day'),
    ]
    kw = (W - 260) / 6
    for i, (name, val) in enumerate(kpis):
        x = 130 + i * kw
        draw.rounded_rectangle([x + 5, kpi_y + 60, x + kw - 10, kpi_y + 180], radius=8,
                              fill=NAVY_LIGHT, outline=GOLD, width=1)
        nf = get_font(11, bold=True)
        draw.text((x + 15, kpi_y + 75), name, font=nf, fill=GOLD)
        vf = get_font(20, bold=True)
        draw.text((x + 15, kpi_y + 110), val, font=vf, fill=WHITE)

    img.save('/home/user/aurea-pptx-assets/implementation_path.png')
    print('  ✓ implementation_path.png')


# ============================================================
# 10. Reference Stack — 6 layers
# ============================================================
def gen_reference_stack():
    W, H = 1600, 900
    img = Image.new('RGB', (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    title_h = draw_title_bar(draw, W, H, 'AUREA — Reference Implementation Stack',
                              'Capability boundaries and contracts matter more than any single vendor')

    layers = [
        {
            'name': 'CHANNELS',
            'color': GOLD,
            'text_color': NAVY,
            'items': [
                ('React', 'Web and assisted-channel UI'),
                ('Flutter', 'Mobile applications and shared UI components'),
                ('Design system + BFF', 'Channel capability contracts, journey state, accessibility, telemetry, feature flags'),
            ]
        },
        {
            'name': 'ACCESS + JOURNEY',
            'color': NAVY_LIGHT,
            'text_color': WHITE,
            'items': [
                ('Kong', 'API gateway, routing, security and policy'),
                ('Camunda', 'BPMN/DMN orchestration, case and decision flow'),
                ('FAPI 2.0 • OIDC • mTLS', 'Consent, throttling, idempotency, service mesh, secrets/KMS, zero-trust segmentation'),
            ]
        },
        {
            'name': 'STREAM + COMPUTE',
            'color': NAVY,
            'text_color': WHITE,
            'items': [
                ('Kafka', 'Event backbone and schema-governed domain events'),
                ('Debezium', 'Log-based change data capture from source databases'),
                ('Apache Flink', 'On-the-fly market, pricing, exposure and enrichment'),
            ]
        },
        {
            'name': 'OPERATIONAL DATA',
            'color': NAVY_LIGHT,
            'text_color': WHITE,
            'items': [
                ('PostgreSQL', 'Operational Global CIF, catalogue and configuration'),
                ('Redis', 'Low-latency context, price and eligibility cache'),
                ('OpenSearch', 'Customer, crosswalk, product and audit search'),
            ]
        },
        {
            'name': 'LAKEHOUSE + DWH',
            'color': NAVY,
            'text_color': WHITE,
            'items': [
                ('Iceberg', 'Open lakehouse tables for Bronze/Silver/Gold'),
                ('Object storage', 'S3-compatible / cloud object store, immutable raw + governed tables'),
                ('Warehouse + semantic', 'DWH engine, marts, BI, feature store, governed metrics'),
            ]
        },
    ]

    ly = title_h + 50
    lh = 140
    gap = 20
    for i, layer in enumerate(layers):
        x = 100
        w = W - 200
        # Card
        draw.rounded_rectangle([x, ly, x + w, ly + lh], radius=10, fill=layer['color'], outline=GOLD, width=2)
        # Title
        tf = get_font(16, bold=True)
        title_fill = GOLD if layer['text_color'] == WHITE else NAVY
        draw.text((x + 20, ly + 12), '◆  ' + layer['name'], font=tf, fill=title_fill)
        # Items in 3 columns
        col_w = (w - 40) / 3
        for j, (name, desc) in enumerate(layer['items']):
            ix = x + 20 + j * col_w
            iy = ly + 50
            # Name
            nf = get_font(14, bold=True)
            name_fill = GOLD if layer['text_color'] == WHITE else NAVY
            draw.text((ix, iy), name, font=nf, fill=name_fill)
            # Desc
            df = get_font(11)
            draw.text((ix, iy + 22), desc, font=df, fill=layer['text_color'])
        ly += lh + gap

    # Bottom: cross-cutting
    cc_y = ly + 10
    draw.rounded_rectangle([100, cc_y, W - 100, cc_y + 50], radius=8,
                          fill=GOLD, outline=GOLD_DARK, width=2)
    cf = get_font(13, bold=True)
    draw_text_centered(draw, W/2, cc_y + 25,
                       'CROSS-CUTTING:  Kubernetes/OpenShift  •  OpenTelemetry  •  Vault/KMS  •  CI/CD  •  policy-as-code  •  lineage/catalogue  •  data quality  •  immutable audit',
                       cf, NAVY)

    img.save('/home/user/aurea-pptx-assets/reference_stack.png')
    print('  ✓ reference_stack.png')


# ============================================================
# 11. Benefits & Value
# ============================================================
def gen_value_benefits():
    W, H = 1600, 900
    img = Image.new('RGB', (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    title_h = draw_title_bar(draw, W, H, 'AUREA — Business Value & Outcomes',
                              'What the bank gains from one truth and one offer everywhere')

    # 4 benefit quadrants
    benefits = [
        {
            'icon': '◆',
            'title': 'CONVERSION',
            'subtitle': 'More sales, faster',
            'color': GOLD,
            'text_color': NAVY,
            'kpis': [
                ('+25%', 'Cross-sell rate'),
                ('+18%', 'Onboarding completion'),
                ('-40%', 'Time-to-quote'),
            ]
        },
        {
            'icon': '◆',
            'title': 'RISK & COMPLIANCE',
            'subtitle': 'Always explainable',
            'color': NAVY,
            'text_color': WHITE,
            'kpis': [
                ('100%', 'KYC coverage'),
                ('-90%', 'Duplicate exposure'),
                ('0', 'Pricing disputes'),
            ]
        },
        {
            'icon': '◆',
            'title': 'OPERATIONS',
            'subtitle': 'Less manual work',
            'color': NAVY_LIGHT,
            'text_color': WHITE,
            'kpis': [
                ('-70%', 'Manual reconciliation'),
                ('-60%', 'Steward workload'),
                ('+5x', 'Faster decisions'),
            ]
        },
        {
            'icon': '◆',
            'title': 'EXPERIENCE',
            'subtitle': 'One truth, every channel',
            'color': GOLD,
            'text_color': NAVY,
            'kpis': [
                ('1', 'Customer view'),
                ('1', 'Offer set'),
                ('7', 'Channels'),
            ]
        },
    ]

    bw = 380
    bh = 360
    by = title_h + 50
    bx_start = (W - 2 * bw - 60) / 2
    gap_x = 60
    gap_y = 30

    for i, b in enumerate(benefits):
        col, row = i % 2, i // 2
        x = bx_start + col * (bw + gap_x)
        y = by + row * (bh + gap_y)
        # Card
        draw.rounded_rectangle([x, y, x + bw, y + bh], radius=12, fill=b['color'], outline=GOLD, width=3)
        # Header strip
        draw.rectangle([x, y, x + bw, y + 8], fill=GOLD)
        # Title
        tf = get_font(26, bold=True)
        title_fill = GOLD if b['text_color'] == WHITE else NAVY
        draw.text((x + 25, y + 35), b['icon'] + '  ' + b['title'], font=tf, fill=title_fill)
        # Subtitle
        sf = get_font(13, bold=True)
        sub_fill = GRAY_300 if b['text_color'] == WHITE else NAVY
        draw.text((x + 25, y + 75), b['subtitle'], font=sf, fill=sub_fill)
        # Divider
        draw.line([(x + 25, y + 110), (x + bw - 25, y + 110)], fill=GOLD, width=2)
        # KPIs
        ky = y + 140
        for kpi, label in b['kpis']:
            # Value (large)
            vf = get_font(36, bold=True)
            val_fill = GOLD if b['text_color'] == WHITE else NAVY
            draw.text((x + 30, ky), kpi, font=vf, fill=val_fill)
            # Label
            lf = get_font(13)
            lbl_fill = GRAY_300 if b['text_color'] == WHITE else GRAY_700
            draw.text((x + 30, ky + 50), label, font=lf, fill=lbl_fill)
            ky += 90

    img.save('/home/user/aurea-pptx-assets/value_benefits.png')
    print('  ✓ value_benefits.png')


# ============================================================
# Main
# ============================================================
if __name__ == '__main__':
    os.makedirs('/home/user/aurea-pptx-assets', exist_ok=True)
    print('Generating AUREA presentation images...')
    gen_three_truths()
    gen_master_infographic()
    gen_customer_journey()
    gen_cif_pipeline()
    gen_identifier_chain()
    gen_integration_sequence()
    gen_operating_model()
    gen_data_landing()
    gen_implementation_path()
    gen_reference_stack()
    gen_value_benefits()
    print('\nDone!')
