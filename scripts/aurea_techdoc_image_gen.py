"""
AUREA Tech Doc Image Generator
Extracts ASCII wireframes + mermaid diagrams from .md files
and renders them to high-quality PNG images.
"""

import re
import os
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# Colors
GOLD = (212, 175, 55)
GOLD_LIGHT = (255, 215, 100)
GOLD_DARK = (184, 134, 11)
NAVY = (10, 25, 41)
NAVY_LIGHT = (26, 47, 71)
WHITE = (255, 255, 255)
GRAY_50 = (249, 250, 251)
GRAY_100 = (243, 244, 246)
GRAY_200 = (229, 231, 235)
GRAY_300 = (209, 213, 219)
GRAY_500 = (107, 114, 128)
GRAY_700 = (55, 65, 81)
GRAY_900 = (17, 24, 39)
SUCCESS = (22, 163, 74)
INFO = (2, 132, 199)
WARNING = (234, 88, 12)
ERROR = (220, 38, 38)

OUTPUT_DIR = '/home/user/aurea-techdoc-assets'
os.makedirs(OUTPUT_DIR, exist_ok=True)


def get_font(size, bold=False, mono=False):
    if mono:
        paths = [
            '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf' if bold
            else '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',
        ]
    else:
        paths = [
            '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf' if bold
            else '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold
            else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                pass
    return ImageFont.load_default()


def render_ascii_wireframe(text, title, output_path, max_width_px=1200):
    """Render ASCII art wireframe to a clean PNG."""
    lines = text.split('\n')

    # Calculate dimensions
    font = get_font(12, mono=True)
    line_height = 18

    # Find max line length
    max_len = max(len(line) for line in lines) if lines else 40
    char_w = 8  # approx mono char width at size 12

    # Content area
    title_height = 50 if title else 0
    padding = 30
    content_w = min(max_len * char_w + 20, max_width_px)
    content_h = len(lines) * line_height + 20
    W = int(content_w + padding * 2)
    H = int(content_h + title_height + padding * 2)

    img = Image.new('RGB', (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    # Title bar
    if title:
        draw.rectangle([0, 0, W, title_height], fill=NAVY)
        f_title = get_font(15, bold=True)
        draw.text((padding, 15), title, font=f_title, fill=GOLD_LIGHT)
        # Gold accent line
        draw.rectangle([0, title_height, W, title_height + 3], fill=GOLD)

    # Draw ASCII lines with semantic colors
    y = title_height + padding
    for line in lines:
        # Determine color based on content
        color = GRAY_900
        bold = False
        if '┌' in line or '└' in line or '┐' in line or '┘' in line:
            color = NAVY
        elif '│' in line:
            color = NAVY
        elif '─' in line or '═' in line or '┄' in line or '┈' in line:
            color = GRAY_300
        elif any(c in line for c in ['■', '●', '◼', '◾']):
            color = GOLD_DARK
        elif '✓' in line or '✅' in line:
            color = SUCCESS
        elif '⚠' in line or '⚡' in line or '🚨' in line:
            color = WARNING
        elif '🔍' in line or '📋' in line or '💡' in line:
            color = INFO
        elif '║' in line or '==' in line:
            color = NAVY
            bold = True

        f = get_font(12, bold=bold, mono=True)
        draw.text((padding, y), line, font=f, fill=color)
        y += line_height

    # Footer/border
    draw.rectangle([0, H - 1, W, H], fill=GOLD)

    img.save(output_path, 'PNG', optimize=True)
    return W, H


def parse_mermaid_diagram(mermaid_text):
    """Parse mermaid and produce a flowchart-style PNG."""
    lines = [l.strip() for l in mermaid_text.strip().split('\n') if l.strip() and not l.strip().startswith('```')]
    # Strip 'mermaid' header if present
    lines = [l for l in lines if l != 'mermaid']

    nodes = {}
    edges = []

    # Parse nodes and edges
    for line in lines:
        if line.startswith('graph') or line.startswith('flowchart') or line.startswith('sequenceDiagram'):
            continue
        # Edge patterns
        edge_match = re.findall(r'(\w+)\s*(-->\|--\||-->|---|-\||\.->)\s*(\w+)', line)
        for m in edge_match:
            edges.append((m[0], m[2], m[1]))
        # Node patterns
        node_match = re.findall(r'(\w+)\[([^\]]+)\]', line)
        for m in node_match:
            label = m[1].replace('<br/>', '\n').replace('\\n', '\n')
            nodes[m[0]] = label
        node_match2 = re.findall(r'(\w+)\(([^)]+)\)', line)
        for m in node_match2:
            label = m[1].replace('<br/>', '\n').replace('\\n', '\n')
            nodes[m[0]] = label
        node_match3 = re.findall(r'(\w+)\{([^}]+)\}', line)
        for m in node_match3:
            label = m[1].replace('<br/>', '\n').replace('\\n', '\n')
            nodes[m[0]] = label

    return nodes, edges


def render_mermaid_to_image(mermaid_text, title, output_path, diagram_type='graph'):
    """Render mermaid as a flowchart-style PNG."""
    nodes, edges = parse_mermaid_diagram(mermaid_text)

    if not nodes:
        return None

    # Layout: simple grid
    node_list = list(nodes.keys())
    n = len(node_list)

    # Determine box sizes based on label length
    f_label = get_font(11, bold=True)
    box_w = 220
    box_h = 70

    # Layout in a grid
    cols = min(4, max(2, int(n ** 0.5)))
    rows = (n + cols - 1) // cols

    padding = 40
    title_h = 50 if title else 0
    W = cols * box_w + (cols + 1) * padding
    H = rows * (box_h + 80) + (rows + 1) * padding + title_h

    img = Image.new('RGB', (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    # Title
    if title:
        draw.rectangle([0, 0, W, title_h], fill=NAVY)
        f_title = get_font(15, bold=True)
        draw.text((padding, 15), title, font=f_title, fill=GOLD_LIGHT)
        draw.rectangle([0, title_h, W, title_h + 3], fill=GOLD)

    # Position nodes
    positions = {}
    for i, node_id in enumerate(node_list):
        col = i % cols
        row = i // cols
        x = padding + col * (box_w + padding)
        y = title_h + padding + row * (box_h + 80)
        positions[node_id] = (x + box_w // 2, y + box_h // 2, x, y, x + box_w, y + box_h)

    # Draw edges first (so they go under nodes)
    f_edge = get_font(9, bold=True)
    for src, dst, _ in edges:
        if src in positions and dst in positions:
            sx, sy, _, _, _, _ = positions[src]
            dx, dy, _, _, _, _ = positions[dst]
            # Draw arrow
            draw.line([(sx, sy), (dx, dy)], fill=GRAY_500, width=2)
            # Arrowhead
            import math
            angle = math.atan2(dy - sy, dx - sx)
            ah_x = dx - 15 * math.cos(angle)
            ah_y = dy - 15 * math.sin(angle)
            draw.polygon([
                (dx, dy),
                (ah_x - 8 * math.cos(angle - 0.5), ah_y - 8 * math.sin(angle - 0.5)),
                (ah_x - 8 * math.cos(angle + 0.5), ah_y - 8 * math.sin(angle + 0.5)),
            ], fill=GRAY_500)

    # Draw nodes
    for node_id, (cx, cy, x1, y1, x2, y2) in positions.items():
        label = nodes[node_id]
        # Box
        draw.rounded_rectangle([x1, y1, x2, y2], radius=8, fill=NAVY_LIGHT, outline=GOLD, width=2)
        # Label (multiline)
        lines = label.split('\n')[:4]
        line_h = 14
        total_h = len(lines) * line_h
        start_y = y1 + (box_h - total_h) // 2
        for li, ln in enumerate(lines):
            bbox = draw.textbbox((0, 0), ln, font=f_label)
            text_w = bbox[2] - bbox[0]
            tx = x1 + (box_w - text_w) // 2
            draw.text((tx, start_y + li * line_h), ln, font=f_label, fill=WHITE)
        # Node ID label at bottom
        f_id = get_font(8, bold=True)
        draw.text((x1 + 5, y2 - 14), node_id, font=f_id, fill=GOLD_LIGHT)

    # Gold border at bottom
    draw.rectangle([0, H - 1, W, H], fill=GOLD)

    img.save(output_path, 'PNG', optimize=True)
    return W, H


def render_architecture_diagram(title, components, connections, output_path):
    """Render a system architecture diagram."""
    W, H = 1400, 900
    img = Image.new('RGB', (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([0, 0, W, 60], fill=NAVY)
    f_title = get_font(20, bold=True)
    draw.text((30, 18), title, font=f_title, fill=GOLD_LIGHT)
    draw.rectangle([0, 60, W, 63], fill=GOLD)

    # Components: list of (x, y, w, h, label, color)
    f_comp = get_font(13, bold=True)
    f_sub = get_font(10)

    for x, y, w, h, label, sub, color in components:
        # Shadow
        draw.rounded_rectangle([x + 3, y + 3, x + w + 3, y + h + 3], radius=8, fill=(220, 220, 220))
        # Box
        draw.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=color, outline=NAVY, width=2)
        # Top accent
        draw.rectangle([x, y, x + w, y + 4], fill=GOLD)
        # Label
        bbox = draw.textbbox((0, 0), label, font=f_comp)
        text_w = bbox[2] - bbox[0]
        draw.text((x + (w - text_w) // 2, y + 20), label, font=f_comp, fill=WHITE)
        # Sub label
        if sub:
            bbox2 = draw.textbbox((0, 0), sub, font=f_sub)
            text_w2 = bbox2[2] - bbox2[0]
            draw.text((x + (w - text_w2) // 2, y + 45), sub, font=f_sub, fill=WHITE)

    # Connections
    f_arrow = get_font(9, bold=True)
    for x1, y1, x2, y2, label in connections:
        # Draw arrow
        import math
        draw.line([(x1, y1), (x2, y2)], fill=GRAY_500, width=2)
        # Arrowhead
        angle = math.atan2(y2 - y1, x2 - x1)
        ah_x = x2 - 12 * math.cos(angle)
        ah_y = y2 - 12 * math.sin(angle)
        draw.polygon([
            (x2, y2),
            (ah_x - 7 * math.cos(angle - 0.5), ah_y - 7 * math.sin(angle - 0.5)),
            (ah_x - 7 * math.cos(angle + 0.5), ah_y - 7 * math.sin(angle + 0.5)),
        ], fill=GRAY_500)
        # Label
        if label:
            mx, my = (x1 + x2) // 2, (y1 + y2) // 2
            draw.text((mx + 5, my - 12), label, font=f_arrow, fill=NAVY)

    img.save(output_path, 'PNG', optimize=True)
    return W, H


def render_database_erd(tables, output_path, title='Database ERD'):
    """Render an Entity Relationship Diagram."""
    W, H = 1400, 900
    img = Image.new('RGB', (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    # Title
    draw.rectangle([0, 0, W, 50], fill=NAVY)
    f_title = get_font(18, bold=True)
    draw.text((30, 15), title, font=f_title, fill=GOLD_LIGHT)
    draw.rectangle([0, 50, W, 53], fill=GOLD)

    # Table positions (3 columns)
    f_table = get_font(12, bold=True)
    f_field = get_font(10)
    f_pk = get_font(10, bold=True)

    cols = 3
    col_w = 420
    padding = 30
    rows = (len(tables) + cols - 1) // cols

    for i, (name, fields) in enumerate(tables):
        col = i % cols
        row = i // cols
        x = padding + col * (col_w + padding)
        y = 80 + row * 380

        # Calculate table height
        row_h = 22
        header_h = 35
        table_h = header_h + len(fields) * row_h + 5

        # Table header
        draw.rounded_rectangle([x, y, x + col_w, y + table_h], radius=6, fill=WHITE, outline=NAVY, width=2)
        draw.rectangle([x, y, x + col_w, y + header_h], fill=NAVY)
        draw.text((x + 10, y + 8), name, font=f_table, fill=GOLD_LIGHT)

        # Fields
        for j, (field, type_, is_pk, is_fk) in enumerate(fields):
            fy = y + header_h + j * row_h
            if j % 2 == 0:
                draw.rectangle([x, fy, x + col_w, fy + row_h], fill=GRAY_50)
            color = NAVY
            prefix = '  '
            f_use = f_field
            if is_pk:
                color = GOLD_DARK
                prefix = '🔑 '
                f_use = f_pk
            elif is_fk:
                color = INFO
                prefix = '🔗 '
            draw.text((x + 8, fy + 4), f'{prefix}{field}', font=f_use, fill=color)
            draw.text((x + col_w - 90, fy + 4), type_, font=f_field, fill=GRAY_500)

    img.save(output_path, 'PNG', optimize=True)
    return W, H


def render_table_to_image(headers, rows, title, output_path):
    """Render a data table as a styled PNG image."""
    col_count = len(headers)
    col_w = max(140, 1200 // col_count)
    row_h = 28
    header_h = 36
    padding = 30
    title_h = 50 if title else 0

    W = col_count * col_w + padding * 2
    H = title_h + header_h + len(rows) * row_h + padding * 2 + 5

    img = Image.new('RGB', (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    # Title
    if title:
        draw.rectangle([0, 0, W, title_h], fill=NAVY)
        f_title = get_font(15, bold=True)
        draw.text((padding, 17), title, font=f_title, fill=GOLD_LIGHT)
        draw.rectangle([0, title_h, W, title_h + 3], fill=GOLD)

    # Header row
    f_h = get_font(11, bold=True)
    f_b = get_font(10)
    for i, h in enumerate(headers):
        x = padding + i * col_w
        draw.rectangle([x, title_h, x + col_w, title_h + header_h], fill=GOLD)
        # Truncate if too long
        text = str(h)[:20]
        bbox = draw.textbbox((0, 0), text, font=f_h)
        text_w = bbox[2] - bbox[0]
        draw.text((x + (col_w - text_w) // 2, title_h + 10), text, font=f_h, fill=NAVY)

    # Data rows
    for r_idx, row in enumerate(rows):
        y = title_h + header_h + r_idx * row_h
        bg = GRAY_50 if r_idx % 2 == 0 else WHITE
        draw.rectangle([padding, y, padding + col_count * col_w, y + row_h], fill=bg)
        for i, cell in enumerate(row):
            x = padding + i * col_w
            text = str(cell)[:30]
            draw.text((x + 8, y + 8), text, font=f_b, fill=GRAY_700)

    # Gold border
    draw.rectangle([0, H - 2, W, H], fill=GOLD)
    img.save(output_path, 'PNG', optimize=True)
    return W, H


def main():
    # Generate sample architecture diagrams, ERDs, and tables
    print("Generating AUREA Tech Doc images...")

    # 1. System Architecture
    print("  1. System Architecture...")
    components = [
        (50, 100, 280, 90, 'CLIENT LAYER', 'Web + Mobile (Flutter)', NAVY_LIGHT),
        (50, 230, 130, 80, 'AUREA Console', 'Admin', NAVY),
        (200, 230, 130, 80, 'AUREA 360', 'Customer', NAVY),
        (50, 350, 280, 80, 'Mobile App', 'iOS + Android', NAVY_LIGHT),
        (400, 100, 320, 90, 'API GATEWAY', 'Spring Cloud Gateway', NAVY_LIGHT),
        (400, 230, 150, 80, 'Auth Service', 'Keycloak', NAVY),
        (570, 230, 150, 80, 'BFF', 'Backend for Frontend', NAVY),
        (400, 350, 150, 80, 'Audit Service', 'Java 17', NAVY),
        (570, 350, 150, 80, 'Notification', 'Push/Email/SMS', NAVY),
        (800, 100, 250, 90, 'CORE SERVICES', 'MD3G Domain Logic', NAVY_LIGHT),
        (800, 230, 250, 80, 'Golden Customer', 'GC Service', GOLD_DARK),
        (800, 350, 250, 80, 'Golden Account', 'GA Service', GOLD_DARK),
        (1100, 100, 250, 90, 'DATA LAYER', 'PostgreSQL + Redis', NAVY_LIGHT),
        (1100, 230, 250, 80, 'PostgreSQL', 'Primary DB', NAVY),
        (1100, 350, 250, 80, 'Redis Cache', 'Session + Hot Data', NAVY),
    ]
    connections = [
        (185, 270, 185, 350, 'HTTPS'),
        (555, 190, 555, 230, 'REST'),
        (925, 190, 925, 230, 'gRPC'),
        (1225, 190, 1225, 230, 'JDBC'),
        (335, 270, 400, 270, ''),
        (335, 380, 400, 380, ''),
        (720, 270, 800, 270, ''),
        (720, 390, 800, 390, ''),
        (1050, 270, 1100, 270, ''),
        (1050, 390, 1100, 390, ''),
    ]
    render_architecture_diagram(
        'AUREA — System Architecture Overview',
        components, connections,
        os.path.join(OUTPUT_DIR, 'arch_system.png')
    )

    # 2. Database ERD
    print("  2. Database ERD...")
    tables = [
        ('customer (Golden Customer)', [
            ('id', 'UUID', True, False),
            ('cif', 'VARCHAR(20)', False, False),
            ('full_name', 'VARCHAR(200)', False, False),
            ('nik', 'VARCHAR(16)', False, False),
            ('email', 'VARCHAR(100)', False, False),
            ('phone', 'VARCHAR(20)', False, False),
            ('segment', 'VARCHAR(50)', False, False),
            ('tier', 'VARCHAR(20)', False, False),
            ('clv', 'DECIMAL(15,2)', False, False),
            ('kyc_status', 'VARCHAR(20)', False, False),
            ('created_at', 'TIMESTAMP', False, False),
        ]),
        ('account (Golden Account)', [
            ('id', 'UUID', True, False),
            ('account_number', 'VARCHAR(20)', False, False),
            ('customer_id', 'UUID', False, True),
            ('product_type', 'VARCHAR(50)', False, False),
            ('balance', 'DECIMAL(18,2)', False, False),
            ('currency', 'VARCHAR(3)', False, False),
            ('status', 'VARCHAR(20)', False, False),
            ('opened_date', 'DATE', False, False),
            ('branch_id', 'VARCHAR(20)', False, False),
        ]),
        ('product (Golden Product)', [
            ('id', 'UUID', True, False),
            ('product_code', 'VARCHAR(50)', False, False),
            ('product_name', 'VARCHAR(200)', False, False),
            ('category', 'VARCHAR(50)', False, False),
            ('is_active', 'BOOLEAN', False, False),
            ('effective_date', 'DATE', False, False),
        ]),
        ('matching_queue', [
            ('id', 'UUID', True, False),
            ('source_record_id', 'UUID', False, True),
            ('target_record_id', 'UUID', False, True),
            ('match_score', 'DECIMAL(5,4)', False, False),
            ('status', 'VARCHAR(20)', False, False),
            ('assigned_to', 'UUID', False, True),
            ('created_at', 'TIMESTAMP', False, False),
        ]),
        ('audit_log', [
            ('id', 'BIGSERIAL', True, False),
            ('entity_type', 'VARCHAR(50)', False, False),
            ('entity_id', 'UUID', False, False),
            ('action', 'VARCHAR(20)', False, False),
            ('user_id', 'UUID', False, True),
            ('old_value', 'JSONB', False, False),
            ('new_value', 'JSONB', False, False),
            ('timestamp', 'TIMESTAMP', False, False),
        ]),
        ('user_account', [
            ('id', 'UUID', True, False),
            ('username', 'VARCHAR(50)', False, False),
            ('email', 'VARCHAR(100)', False, False),
            ('password_hash', 'VARCHAR(255)', False, False),
            ('roles', 'JSONB', False, False),
            ('is_active', 'BOOLEAN', False, False),
            ('last_login', 'TIMESTAMP', False, False),
        ]),
    ]
    render_database_erd(tables, os.path.join(OUTPUT_DIR, 'db_erd.png'),
                        title='AUREA — Core Database Schema (ERD)')

    # 3. CI/CD Pipeline
    print("  3. CI/CD Pipeline...")
    pipeline_components = [
        (50, 100, 180, 80, 'Developer', 'Git Push', NAVY_LIGHT),
        (280, 100, 180, 80, 'GitHub', 'Source Control', NAVY),
        (510, 100, 180, 80, 'GitHub Actions', 'CI Build', GOLD_DARK),
        (740, 100, 180, 80, 'SonarQube', 'Code Quality', INFO),
        (970, 100, 180, 80, 'Docker Hub', 'Image Registry', NAVY),
        (1200, 100, 150, 80, 'ArgoCD', 'Deploy', SUCCESS),
        (50, 240, 180, 80, 'Unit Tests', 'JUnit + Mockito', NAVY),
        (280, 240, 180, 80, 'Integration', 'TestContainers', NAVY),
        (510, 240, 180, 80, 'SAST Scan', 'Trivy + Snyk', INFO),
        (740, 240, 180, 80, 'Build Image', 'Multi-stage', NAVY),
        (970, 240, 180, 80, 'Push Image', 'Tag :semver', NAVY),
        (1200, 240, 150, 80, 'K8s Apply', 'Rolling', SUCCESS),
        (50, 380, 350, 80, 'Dev Environment', 'Auto-deploy on develop branch', GRAY_500),
        (450, 380, 350, 80, 'Staging Environment', 'On PR merge to main', GRAY_500),
        (850, 380, 350, 80, 'Production', 'Manual approval + ArgoCD', WARNING),
    ]
    pipeline_conns = [
        (230, 140, 280, 140, 'push'),
        (460, 140, 510, 140, 'trigger'),
        (690, 140, 740, 140, 'analyze'),
        (920, 140, 970, 140, 'login'),
        (1150, 140, 1200, 140, 'sync'),
        (140, 180, 140, 240, ''),
        (370, 180, 370, 240, ''),
        (600, 180, 600, 240, ''),
        (830, 180, 830, 240, ''),
        (1060, 180, 1060, 240, ''),
        (225, 320, 225, 380, ''),
        (625, 320, 625, 380, ''),
        (1025, 320, 1025, 380, ''),
    ]
    render_architecture_diagram(
        'AUREA — CI/CD Pipeline',
        pipeline_components, pipeline_conns,
        os.path.join(OUTPUT_DIR, 'arch_cicd.png')
    )

    # 4. MD3G Framework (3 Golden Data)
    print("  4. MD3G Framework Diagram...")
    md3g_components = [
        (450, 100, 400, 100, 'MD3G', 'Master Data 3 Golden — Unified Data Framework', GOLD_DARK),
        (100, 280, 300, 200, 'GOLDEN CUSTOMER (GC)', '360° customer view\nSingle source of truth\nKYC verified', NAVY_LIGHT),
        (550, 280, 300, 200, 'GOLDEN ACCOUNT (GA)', 'All account relationships\nBalance & product info\nTransaction history', NAVY_LIGHT),
        (1000, 280, 300, 200, 'GOLDEN PRODUCT (GP)', 'Product catalog\nPricing & terms\nCross-sell matrix', NAVY_LIGHT),
        (250, 550, 350, 100, 'Customer 360', 'AUREA 360 Dashboard', NAVY),
        (650, 550, 300, 100, 'Account Aggregation', 'Real-time balance', NAVY),
        (1000, 550, 250, 100, 'Product Recommender', 'ML-powered', NAVY),
        (450, 700, 400, 80, 'AUREA PLATFORM', 'Bank-wide data unification', GOLD_DARK),
    ]
    md3g_conns = [
        (650, 200, 250, 280, ''),
        (650, 200, 700, 280, ''),
        (650, 200, 1150, 280, ''),
        (250, 480, 425, 550, ''),
        (700, 480, 800, 550, ''),
        (1150, 480, 1125, 550, ''),
        (250, 650, 600, 700, ''),
        (700, 650, 700, 700, ''),
        (1125, 650, 800, 700, ''),
    ]
    render_architecture_diagram(
        'AUREA — MD3G Framework: 3 Golden Data',
        md3g_components, md3g_conns,
        os.path.join(OUTPUT_DIR, 'arch_md3g.png')
    )

    # 5. Wireframe - Admin Dashboard
    print("  5. Admin Dashboard Wireframe...")
    admin_wf = """
┌────────────┬─────────────────────────────────────────────────────┐
│            │  AUREA CONSOLE  [● LIVE]                       🔔 👤  │
│  ◆ AUREA   ├─────────────────────────────────────────────────────┤
│  CONSOLE   │  Dashboard                                          │
│            │  ─────────────────────────────────────────────────  │
│  MAIN      │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐       │
│  ■ Dash    │  │ 12,847 │ │ 28,193 │ │  1,452 │ │ 98.7%  │       │
│  □ Monitor │  │ GC     │ │ GA     │ │ GP     │ │ Quality│       │
│  □ Config  │  │ +8.2%  │ │ +3.1%  │ │+12.4%  │ │ +0.4%  │       │
│  □ Reports │  └────────┘ └────────┘ └────────┘ └────────┘       │
│            │                                                     │
│  MANAGE    │  ┌─────────────────────┐  ┌───────────────────┐     │
│  □ Ops     │  │ System Health       │  │ Real-time Feed    │     │
│  □ Sec     │  │ ═══════════════     │  │ ─────────────     │     │
│  □ Backup  │  │ CPU: 45%  ▓▓▓░░    │  │ • New customer    │     │
│            │  │ MEM: 62%  ▓▓▓▓░░   │  │ • KYC verified    │     │
│            │  │ DB:  38%  ▓▓░░░    │  │ • Match completed │     │
│            │  └─────────────────────┘  └───────────────────┘     │
│            │                                                     │
│            │  ┌─────────────────────────────────────────────┐    │
│            │  │ Recent Activity                              │    │
│            │  ├─────────────────────────────────────────────┤    │
│            │  │ 10:42 Customer updated      Siti W.   ✓    │    │
│            │  │ 10:38 KYC verified          Ahmad R.  ✓    │    │
│            │  │ 10:35 Matching processed    System    ✓    │    │
│            │  └─────────────────────────────────────────────┘    │
└────────────┴─────────────────────────────────────────────────────┘
"""
    render_ascii_wireframe(admin_wf, 'Wireframe: AUREA Console Admin Dashboard',
                           os.path.join(OUTPUT_DIR, 'wf_admin.png'))

    # 6. Wireframe - Customer 360
    print("  6. Customer 360 Wireframe...")
    c360_wf = """
┌──────────────────────────────────────────────────────────────────────┐
│ ◆ AUREA 360  Customer Intelligence      [Live]      🔔  BS  Budi S. │
├──────────────────────────────────────────────────────────────────────┤
│ [Dashboard] Customers  Analytics  Segments                            │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────┐│
│  │ 1.24M   │ │ 892K    │ │ 18,294  │ │ 12,456  │ │ Rp 8.5M │ │ 67  ││
│  │ Total   │ │ Active  │ │ New Mth │ │ Churn   │ │ Avg CLV │ │ NPS ││
│  │ +8.2% ↑ │ │ +3.1% ↑ │ │+12.4% ↑ │ │ -2.1% ↓ │ │ +5.6% ↑ │ │+1.2% ││
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────┘│
│                                                                       │
│  ┌────────────────────────────────┐  ┌─────────────────────────────┐ │
│  │ Customer Growth (12 mo)        │  │ Segment Distribution        │ │
│  │ ╱╲    ╱╲                       │  │      ╱─────╲                │ │
│  │   ╲  ╱  ╲   ╱╲                 │  │    ╱  VIP   ╲___            │ │
│  │    ╲╱    ╲╱  ╲___              │  │   │   45K     │            │ │
│  │                  ╲___          │  │   │  Mass Aff  │           │ │
│  │ Jan Feb Mar Apr May Jun Jul    │  │    ╲ 187K    ╱            │ │
│  └────────────────────────────────┘  └─────────────────────────────┘ │
│                                                                       │
│  ┌──────────────────────────────────────────────────────────────────┐│
│  │ 🧠 ML Insights                                                     ││
│  ├──────────────────────────────────────────────────────────────────┤│
│  │ ⚠ 156 customers in "Young Prof" segment predicted to churn       ││
│  │ 💎 23 customers in "Mass Affluent" have high CLV (avg Rp 250M)   ││
│  │ 📈 5 customers with anomalous transactions (AML review)           ││
│  └──────────────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────────────┘
"""
    render_ascii_wireframe(c360_wf, 'Wireframe: AUREA 360 Customer Dashboard',
                           os.path.join(OUTPUT_DIR, 'wf_customer360.png'))

    # 7. Wireframe - Mobile
    print("  7. Mobile Wireframe...")
    mobile_wf = """
        ┌─────────────────────────┐
        │ 9:41           📶 🔋    │
        ├─────────────────────────┤
        │                         │
        │   ◆ AUREA               │
        │   THE GOLD STANDARD     │
        │                         │
        │  ┌───────────────────┐  │
        │  │ GOLDEN CUSTOMER   │  │
        │  │ ✓ VERIFIED        │  │
        │  │ ─────────────────│  │
        │  │ VIP Customer      │  │
        │  │ Budi Santoso      │  │
        │  │ CIF: GC-001847    │  │
        │  │ ─────────────────│  │
        │  │ CLV    TIER       │  │
        │  │ 25.4M  GOLD ⭐⭐⭐ │  │
        │  └───────────────────┘  │
        │                         │
        │  ┌──────────┐┌─────────┐│
        │  │ 1.24M    ││ 892K    ││
        │  │ NASABAH  ││REKENING ││
        │  └──────────┘└─────────┘│
        │  ┌──────────┐┌─────────┐│
        │  │ 1.4K     ││ 12K     ││
        │  │ PRODUK   ││ CHURN   ││
        │  └──────────┘└─────────┘│
        │                         │
        │  🏠    👥    💰    👤  │
        │ Home Cust. Acct Profile  │
        └─────────────────────────┘
"""
    render_ascii_wireframe(mobile_wf, 'Wireframe: AUREA Mobile App',
                           os.path.join(OUTPUT_DIR, 'wf_mobile.png'))

    # 8. Wireframe - Login
    print("  8. Login Wireframe...")
    login_wf = """
        ┌─────────────────────────┐
        │  9:41          🔋       │
        │                         │
        │                         │
        │         ◆ AUREA         │
        │     THE GOLD STANDARD   │
        │       OF DATA           │
        │                         │
        │  ┌───────────────────┐  │
        │  │                   │  │
        │  │  Selamat Datang   │  │
        │  │                   │  │
        │  │  👤 Username      │  │
        │  │  ┌─────────────┐  │  │
        │  │  │             │  │  │
        │  │  └─────────────┘  │  │
        │  │                   │  │
        │  │  🔒 Password      │  │
        │  │  ┌─────────────┐  │  │
        │  │  │             │  │  │
        │  │  └─────────────┘  │  │
        │  │                   │  │
        │  │  Lupa password? → │  │
        │  │                   │  │
        │  │  ┌─────────────┐  │  │
        │  │  │    MASUK    │  │  │
        │  │  └─────────────┘  │  │
        │  │                   │  │
        │  │  ┌─────────────┐  │  │
        │  │  │ 👆 Biometrik│  │  │
        │  │  └─────────────┘  │  │
        │  └───────────────────┘  │
        │                         │
        │   Bank XYZ © 2026       │
        └─────────────────────────┘
"""
    render_ascii_wireframe(login_wf, 'Wireframe: AUREA Login Screen',
                           os.path.join(OUTPUT_DIR, 'wf_login.png'))

    # 9. Wireframe - Matching Queue
    print("  9. Matching Queue Wireframe...")
    matching_wf = """
┌──────────────────────────────────────────────────────────────────────┐
│  AUREA STEWARD  [● LIVE]                                         👤  │
├──────────────────────────────────────────────────────────────────────┤
│  MAIN            OPERASIONAL                  COMPLIANCE             │
│  □ Dashboard     ■ Matching (47)              □ Audit Trail         │
│  □ Customers     □ Exceptions                 □ Reports              │
│  □ New Customer  □ KYC Review                                       │
│                                                                       │
├──────────────────────────────────────────────────────────────────────┤
│  Matching Queue                       Filter: [HIGH ▼] [PENDING ▼]    │
│  ════════════════                       Search: [_______________] 🔍 │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ #GC-8472  Source: BRM-001   Match: 0.92  AUTO-MATCH ✓        │ │
│  │   vs GC-8473  Target: CIF    Status: PENDING                 │ │
│  │   [ APPROVE ]  [ REJECT ]  [ DEFER ]                          │ │
│  ├────────────────────────────────────────────────────────────────┤ │
│  │ #GC-8475  Source: NIK-329  Match: 0.87  NEEDS REVIEW         │ │
│  │   vs GC-8476  Target: NAME  Status: PENDING                 │ │
│  │   [ APPROVE ]  [ REJECT ]  [ DEFER ]                          │ │
│  ├────────────────────────────────────────────────────────────────┤ │
│  │ #GC-8478  Source: PHONE-08 Match: 0.81  NEEDS REVIEW         │ │
│  │   vs GC-8479  Target: PHONE Status: PENDING                 │ │
│  │   [ APPROVE ]  [ REJECT ]  [ DEFER ]                          │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                       │
│  Page 1 of 16  [< Prev]  [1] 2 3 4 5 ... [Next >]                  │
└──────────────────────────────────────────────────────────────────────┘
"""
    render_ascii_wireframe(matching_wf, 'Wireframe: AUREA Matching Queue',
                           os.path.join(OUTPUT_DIR, 'wf_matching.png'))

    # 10. Wireframe - KYC Review
    print("  10. KYC Review Wireframe...")
    kyc_wf = """
┌──────────────────────────────────────────────────────────────────────┐
│  AUREA STEWARD  -  KYC REVIEW                                         │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Customer: Budi Santoso    CIF: GC-001847    Status: PENDING REVIEW  │
│  ───────────────────────────────────────────────────────────────────  │
│                                                                       │
│  ┌──────────────────┐  ┌──────────────────────────────────────────┐ │
│  │  📷 KTP Image     │  │  Personal Information                    │ │
│  │   [thumbnail]    │  │  Full Name : Budi Santoso                │ │
│  │                  │  │  NIK       : 3201234567890001             │ │
│  │  View: [Front]   │  │  DOB       : 1985-03-15                  │ │
│  │         [Back]   │  │  Gender    : M                            │ │
│  │                  │  │  Address   : Jl. Sudirman Kav. 45, JKT   │ │
│  └──────────────────┘  │  Phone     : +62 812-1234-5678           │ │
│                         │  Email     : budi.s@email.com            │ │
│  ┌──────────────────┐  └──────────────────────────────────────────┘ │
│  │  Risk Score       │                                              │
│  │   ▓▓▓▓▓▓░░░  62   │  ┌──────────────────────────────────────────┐ │
│  │  LOW RISK         │  │  Verification Checks                     │ │
│  │                  │  │  ✓ NIK match                             │ │
│  │  AML: CLEAN      │  │  ✓ Name match                            │ │
│  │  PEP: NO         │  │  ✓ DOB match                             │ │
│  │  Sanction: NO    │  │  ⚠ Phone not verified                   │ │
│  └──────────────────┘  │  ✗ Email not verified                    │ │
│                         └──────────────────────────────────────────┘ │
│                                                                       │
│  [ APPROVE KYC ]  [ REQUEST MORE INFO ]  [ REJECT ]                  │
└──────────────────────────────────────────────────────────────────────┘
"""
    render_ascii_wireframe(kyc_wf, 'Wireframe: AUREA KYC Review',
                           os.path.join(OUTPUT_DIR, 'wf_kyc.png'))

    # 11. Wireframe - Customer Search
    print("  11. Customer Search Wireframe...")
    search_wf = """
┌──────────────────────────────────────────────────────────────────────┐
│  AUREA STEWARD  -  Customer Search                                     │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Search:  [ Budi                              ] 🔍  [ Advanced ▼]     │
│                                                                       │
│  Filters:  [Segment: ALL ▼]  [Tier: ALL ▼]  [KYC: ALL ▼]            │
│            [Branch: ALL ▼]    [Date: LAST 30 DAYS ▼]                 │
│                                                                       │
│  Found 147 results                              [Export ▼] [+ New]  │
│  ════════════════                                                    │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ [BS] Budi Santoso      VIP      GOLD  ✓  12K   8.2%  ⋯      │ │
│  │      CIF: GC-001847   NIK: 3201...  Joined: 2020-03-15        │ │
│  ├────────────────────────────────────────────────────────────────┤ │
│  │ [SW] Siti Wahyuni    MASS-AFF   GOLD  ✓  15K   3.1%  ⋯      │ │
│  │      CIF: GC-001848   NIK: 3201...  Joined: 2021-07-22        │ │
│  ├────────────────────────────────────────────────────────────────┤ │
│  │ [AR] Ahmad Rizki     MASS-MKT  SILVER ⏳   3K  12.4%  ⋯      │ │
│  │      CIF: GC-001849   NIK: 3201...  Joined: 2023-01-10        │ │
│  ├────────────────────────────────────────────────────────────────┤ │
│  │ [DL] Dewi Lestari     SENIOR    GOLD  ✓  10K   4.2%  ⋯      │ │
│  │      CIF: GC-001850   NIK: 3201...  Joined: 2019-05-03        │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                       │
│  Page 1 of 5  [< Prev]  [1] 2 3 4 5 [Next >]                        │
└──────────────────────────────────────────────────────────────────────┘
"""
    render_ascii_wireframe(search_wf, 'Wireframe: AUREA Customer Search',
                           os.path.join(OUTPUT_DIR, 'wf_search.png'))

    # 12. Sequence Diagram (login flow)
    print("  12. Sequence Diagram (auth flow)...")
    seq_components = [
        (50, 100, 150, 60, 'User', 'Mobile App', NAVY_LIGHT),
        (250, 100, 150, 60, 'AUREA API', 'Gateway', NAVY),
        (450, 100, 150, 60, 'Keycloak', 'Auth Server', NAVY),
        (650, 100, 150, 60, 'AUREA Core', 'MD3G Service', NAVY),
        (850, 100, 150, 60, 'PostgreSQL', 'Database', NAVY),
    ]
    # Draw vertical lifelines
    f_label = get_font(10, bold=True)
    W, H = 1100, 700
    img = Image.new('RGB', (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    # Title
    draw.rectangle([0, 0, W, 50], fill=NAVY)
    f_title = get_font(16, bold=True)
    draw.text((30, 15), 'AUREA — Authentication Flow (Sequence Diagram)', font=f_title, fill=GOLD_LIGHT)
    draw.rectangle([0, 50, W, 53], fill=GOLD)

    # Re-draw lifelines
    for x, y, w, h, label, sub, _ in seq_components:
        # Lifeline
        draw.line([(x + w // 2, y + h), (x + w // 2, H - 30)], fill=GRAY_500, width=1, joint='curve')
        # Header box
        draw.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=NAVY_LIGHT, outline=GOLD, width=2)
        draw.text((x + 10, y + 8), label, font=f_label, fill=WHITE)
        draw.text((x + 10, y + 28), sub, font=get_font(9), fill=GOLD_LIGHT)

    # Sequence messages
    messages = [
        (125, 160, 250, 160, '1. POST /auth/login {username, password}'),
        (250, 200, 450, 200, '2. Authenticate user'),
        (450, 240, 250, 240, '3. JWT access_token + refresh_token'),
        (250, 280, 125, 280, '4. 200 OK + tokens'),
        (125, 320, 250, 320, '5. GET /api/customers/profile (Bearer)'),
        (250, 360, 850, 360, '6. Forward to GC service'),
        (850, 400, 650, 400, '7. Fetch customer record'),
        (650, 440, 850, 440, '8. Return customer data'),
        (850, 480, 250, 480, '9. Return response'),
        (250, 520, 125, 520, '10. 200 OK + customer'),
    ]
    f_msg = get_font(10, bold=True)
    for i, (x1, y1, x2, y2, label) in enumerate(messages):
        # Dashed for response
        width = 1
        if 'OK' in label or 'return' in label.lower() or 'Return' in label:
            for dx in range(0, abs(x2 - x1), 6):
                if x1 < x2:
                    draw.line([(x1 + dx, y1), (x1 + dx + 3, y1)], fill=NAVY, width=1)
                else:
                    draw.line([(x2 + dx, y1), (x2 + dx + 3, y1)], fill=NAVY, width=1)
        else:
            draw.line([(x1, y1), (x2, y2)], fill=NAVY, width=2)
            # Arrowhead
            import math
            angle = math.atan2(y2 - y1, x2 - x1)
            ah_x = x2 - 10 * math.cos(angle)
            ah_y = y2 - 10 * math.sin(angle)
            draw.polygon([
                (x2, y2),
                (ah_x - 6 * math.cos(angle - 0.5), ah_y - 6 * math.sin(angle - 0.5)),
                (ah_x - 6 * math.cos(angle + 0.5), ah_y - 6 * math.sin(angle + 0.5)),
            ], fill=NAVY)
        # Label
        mid_x = (x1 + x2) // 2
        if x1 < x2:
            draw.text((mid_x, y1 - 12), label, font=f_msg, fill=NAVY)
        else:
            draw.text((mid_x - 100, y1 - 12), label, font=f_msg, fill=NAVY)

    # Alt boxes
    draw.rounded_rectangle([40, 290, 1060, 360], radius=4, outline=SUCCESS, width=1)
    draw.text((50, 295), 'alt [success]', font=f_msg, fill=SUCCESS)
    draw.rounded_rectangle([40, 380, 1060, 560], radius=4, outline=INFO, width=1)
    draw.text((50, 385), 'loop [authenticated request]', font=f_msg, fill=INFO)

    # Footer
    draw.rectangle([0, H - 2, W, H], fill=GOLD)
    img.save(os.path.join(OUTPUT_DIR, 'seq_auth.png'), 'PNG', optimize=True)

    # 13. Sequence Diagram (matching)
    print("  13. Sequence Diagram (matching)...")
    W, H = 1100, 700
    img = Image.new('RGB', (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, W, 50], fill=NAVY)
    draw.text((30, 15), 'AUREA — Matching Engine Flow (Sequence Diagram)', font=f_title, fill=GOLD_LIGHT)
    draw.rectangle([0, 50, W, 53], fill=GOLD)

    match_components = [
        (50, 100, 150, 60, 'Steward UI', 'Vue/Nuxt', NAVY_LIGHT),
        (250, 100, 150, 60, 'API Gateway', 'Spring', NAVY),
        (450, 100, 150, 60, 'Matching', 'Service', GOLD_DARK),
        (650, 100, 150, 60, 'Kafka', 'Event Bus', NAVY),
        (850, 100, 150, 60, 'PostgreSQL', 'Database', NAVY),
    ]
    for x, y, w, h, label, sub, _ in match_components:
        draw.line([(x + w // 2, y + h), (x + w // 2, H - 30)], fill=GRAY_500, width=1)
        draw.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=NAVY_LIGHT, outline=GOLD, width=2)
        draw.text((x + 10, y + 8), label, font=f_label, fill=WHITE)
        draw.text((x + 10, y + 28), sub, font=get_font(9), fill=GOLD_LIGHT)

    match_messages = [
        (125, 200, 250, 200, '1. POST /matching/queue (new record)'),
        (250, 240, 450, 240, '2. Publish MatchRequest event'),
        (450, 280, 650, 280, '3. match.requested topic'),
        (650, 320, 450, 320, '4. consume event'),
        (450, 360, 850, 360, '5. Query similar records (Fuzzy Match)'),
        (850, 400, 450, 400, '6. Return candidates'),
        (450, 440, 850, 440, '7. Score + classify (auto/manual)'),
        (450, 480, 250, 480, '8. Return match result'),
        (250, 520, 125, 520, '9. Display in queue (score 0.87)'),
    ]
    for x1, y1, x2, y2, label in match_messages:
        draw.line([(x1, y1), (x2, y2)], fill=NAVY, width=2)
        import math
        angle = math.atan2(y2 - y1, x2 - x1)
        ah_x = x2 - 10 * math.cos(angle)
        ah_y = y2 - 10 * math.sin(angle)
        draw.polygon([
            (x2, y2),
            (ah_x - 6 * math.cos(angle - 0.5), ah_y - 6 * math.sin(angle - 0.5)),
            (ah_x - 6 * math.cos(angle + 0.5), ah_y - 6 * math.sin(angle + 0.5)),
        ], fill=NAVY)
        mid_x = (x1 + x2) // 2
        draw.text((mid_x - 50, y1 - 12), label, font=f_msg, fill=NAVY)

    draw.rectangle([0, H - 2, W, H], fill=GOLD)
    img.save(os.path.join(OUTPUT_DIR, 'seq_matching.png'), 'PNG', optimize=True)

    # 14. Tables - rendered as images
    print("  14. Tables...")
    # Tech stack table
    render_table_to_image(
        ['Layer', 'Technology', 'Version', 'Purpose'],
        [
            ['Frontend (Web)', 'Vue.js + Nuxt 3', '3.x', 'AUREA 360, Steward UI'],
            ['Frontend (Admin)', 'Vite + Alpine.js', '5.x', 'AUREA Console'],
            ['Frontend (Mobile)', 'Flutter', '3.10+', 'AUREA Mobile (iOS+Android)'],
            ['API Gateway', 'Spring Cloud Gateway', '6.x', 'Routing + Auth'],
            ['Backend', 'Spring Boot (Java)', '17+', 'Core services'],
            ['Auth', 'Keycloak', '24.x', 'SSO + Identity'],
            ['Database', 'PostgreSQL', '15+', 'Primary store'],
            ['Cache', 'Redis', '7.x', 'Session + hot data'],
            ['Event Bus', 'Apache Kafka', '3.5+', 'Async messaging'],
            ['Search', 'Elasticsearch', '8.x', 'Full-text + Fuzzy match'],
            ['Container', 'Docker + Kubernetes', '24+', 'Orchestration'],
            ['CI/CD', 'GitHub Actions + ArgoCD', '—', 'Automated deploy'],
            ['Monitoring', 'Prometheus + Grafana', '—', 'Metrics + Dashboards'],
        ],
        'AUREA Technology Stack',
        os.path.join(OUTPUT_DIR, 'table_techstack.png')
    )

    # API endpoints table
    render_table_to_image(
        ['Method', 'Endpoint', 'Description', 'Auth'],
        [
            ['POST', '/auth/login', 'Authenticate user', 'Public'],
            ['POST', '/auth/refresh', 'Refresh JWT token', 'Refresh'],
            ['POST', '/auth/logout', 'Invalidate session', 'JWT'],
            ['GET', '/api/customers', 'List golden customers', 'JWT'],
            ['GET', '/api/customers/{cif}', 'Get customer by CIF', 'JWT'],
            ['POST', '/api/customers', 'Create new customer', 'JWT+Role'],
            ['PUT', '/api/customers/{cif}', 'Update customer', 'JWT+Role'],
            ['DELETE', '/api/customers/{cif}', 'Soft-delete customer', 'JWT+Admin'],
            ['GET', '/api/accounts', 'List accounts (filtered)', 'JWT'],
            ['GET', '/api/accounts/{id}', 'Get account detail', 'JWT'],
            ['POST', '/api/matching/queue', 'Add to matching queue', 'JWT+Role'],
            ['GET', '/api/matching/{id}', 'Get match result', 'JWT'],
            ['POST', '/api/kyc/verify', 'Submit KYC document', 'JWT+Role'],
            ['GET', '/api/audit/{entity}', 'Get audit trail', 'JWT+Admin'],
        ],
        'AUREA REST API Endpoints',
        os.path.join(OUTPUT_DIR, 'table_api.png')
    )

    # Performance metrics
    render_table_to_image(
        ['Metric', 'Target', 'Measured', 'Status'],
        [
            ['API Response Time (p95)', '< 200ms', '156ms', '✓'],
            ['API Response Time (p99)', '< 500ms', '342ms', '✓'],
            ['Throughput', '> 1000 RPS', '1,847 RPS', '✓'],
            ['Error Rate', '< 0.1%', '0.03%', '✓'],
            ['Availability', '> 99.9%', '99.97%', '✓'],
            ['Database Query (p95)', '< 50ms', '38ms', '✓'],
            ['Cache Hit Rate', '> 80%', '87%', '✓'],
            ['Matching Throughput', '> 500/sec', '720/sec', '✓'],
        ],
        'AUREA Performance Metrics',
        os.path.join(OUTPUT_DIR, 'table_perf.png')
    )

    # 15. Deployment architecture
    print("  15. Deployment Architecture...")
    deploy_components = [
        (50, 100, 250, 80, 'CLIENT', 'Web Browser + Mobile App', NAVY_LIGHT),
        (50, 220, 110, 70, 'AUREA Console', 'Vite+Alpine', NAVY),
        (180, 220, 110, 70, 'AUREA 360', 'Nuxt 3', NAVY),
        (350, 100, 200, 80, 'CDN', 'CloudFlare', INFO),
        (600, 100, 250, 80, 'API GATEWAY', '3 instances (HA)', GOLD_DARK),
        (600, 220, 115, 70, 'Auth Svc', 'Keycloak', NAVY),
        (735, 220, 115, 70, 'Customer', 'Java', NAVY),
        (900, 100, 250, 80, 'KUBERNETES', 'Production Cluster', SUCCESS),
        (900, 220, 115, 70, 'Account Svc', 'Java', NAVY),
        (1035, 220, 115, 70, 'Matching', 'Java', NAVY),
        (1200, 100, 150, 80, 'Data Layer', 'HA Setup', GOLD_DARK),
        (1200, 220, 150, 70, 'PostgreSQL', 'Master', NAVY),
        (1200, 320, 150, 70, 'PostgreSQL', 'Replica', NAVY),
        (1200, 420, 150, 70, 'Redis', 'Cluster', NAVY),
        (50, 380, 200, 80, 'CI/CD', 'GitHub Actions', INFO),
        (300, 380, 200, 80, 'Container Registry', 'Harbor', INFO),
        (550, 380, 200, 80, 'GitOps', 'ArgoCD', SUCCESS),
        (800, 380, 200, 80, 'Monitoring', 'Prometheus + Grafana', WARNING),
        (1050, 380, 200, 80, 'Logging', 'ELK Stack', WARNING),
    ]
    deploy_conns = [
        (175, 180, 175, 220, 'HTTPS'),
        (450, 140, 600, 140, 'API'),
        (725, 180, 725, 220, ''),
        (850, 140, 900, 140, 'Route'),
        (1025, 180, 1025, 220, ''),
        (1275, 180, 1275, 220, ''),
        (150, 460, 300, 420, ''),
        (400, 420, 550, 420, ''),
        (650, 420, 800, 420, ''),
        (900, 420, 1050, 420, ''),
    ]
    render_architecture_diagram(
        'AUREA — Production Deployment Architecture',
        deploy_components, deploy_conns,
        os.path.join(OUTPUT_DIR, 'arch_deployment.png')
    )

    print()
    print(f"Total images: {len(os.listdir(OUTPUT_DIR))}")
    print(f"Location: {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
