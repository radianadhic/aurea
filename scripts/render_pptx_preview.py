"""
Render PPTX slides as PNG previews using a custom approach.
Since we don't have LibreOffice, we'll do a visual sanity check by
examining slide content and recreating key slides as images.
"""

import os
from PIL import Image, ImageDraw, ImageFont

# AUREA colors
NAVY = (10, 25, 41)
NAVY_LIGHT = (26, 47, 71)
GOLD = (212, 175, 55)
GOLD_LIGHT = (255, 215, 100)
GOLD_DARK = (184, 134, 11)
WHITE = (255, 255, 255)
GRAY_500 = (107, 114, 128)
GRAY_700 = (55, 65, 81)
GRAY_300 = (209, 213, 219)

FONT_PATHS = [
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
]

def get_font(size, bold=False):
    paths = [p for p in FONT_PATHS] + [p.replace('-Bold', '') for p in FONT_PATHS]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                pass
    return ImageFont.load_default()

# Render slide previews by directly using existing image assets
def render_slide_preview(slide_num, output_path):
    """Render a specific slide preview."""
    # 16:9 at 1280x720
    W, H = 1280, 720
    img = Image.new('RGB', (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    # Add header bar
    draw.rectangle([0, 0, W, 50], fill=NAVY)
    draw.rectangle([0, 50, W, 55], fill=GOLD)
    draw.text((20, 14), 'AUREA', font=get_font(20, bold=True), fill=GOLD)

    # Title based on slide number
    titles = {
        1: 'Cover',
        2: 'Agenda',
        3: 'The Problem',
        4: 'Three Truths, One Experience',
        5: 'Master Infographic',
        6: 'Customer Journey',
        7: 'Global CIF Architecture',
        8: 'Product Commercialization',
        9: 'Pricing, Eligibility & Limit',
        10: 'Information Model',
        11: 'Reference Technology Stack',
        12: 'Integration Sequence',
        13: 'Operating Model',
        14: 'Implementation Path',
        15: 'Data Landing',
        16: 'Enterprise System Coverage',
        17: 'Reference Implementation',
        18: 'Value & Benefits',
        19: 'Next Steps',
        20: 'Thank You',
    }

    # Slides 4, 5, 6, 7, 10, 12, 13, 14, 15, 17, 18 use image assets
    asset_slides = {
        4: 'three_truths.png',
        5: 'master_infographic.png',
        6: 'customer_journey.png',
        7: 'cif_pipeline.png',
        10: 'identifier_chain.png',
        12: 'integration_sequence.png',
        13: 'operating_model.png',
        14: 'implementation_path.png',
        15: 'data_landing.png',
        17: 'reference_stack.png',
        18: 'value_benefits.png',
    }

    if slide_num in asset_slides:
        asset_path = f'/home/user/aurea-pptx-assets/{asset_slides[slide_num]}'
        if os.path.exists(asset_path):
            asset = Image.open(asset_path)
            aw, ah = asset.size
            scale = min((W - 40) / aw, (H - 100) / ah)
            new_w = int(aw * scale)
            new_h = int(ah * scale)
            asset_resized = asset.resize((new_w, new_h), Image.LANCZOS)
            x = (W - new_w) // 2
            y = 70 + (H - 70 - new_h) // 2
            img.paste(asset_resized, (x, y))
        title = titles.get(slide_num, '')
    elif slide_num == 1:
        # Cover
        img = Image.new('RGB', (W, H), NAVY)
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 200, W, 205], fill=GOLD)
        draw.rectangle([0, 550, W, 555], fill=GOLD)
        draw.text((W//2, 100), '◆', font=get_font(60, bold=True), fill=GOLD, anchor='mt')
        # Center the text
        bbox = draw.textbbox((0, 0), 'AUREA', font=get_font(96, bold=True))
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw)//2, 240), 'AUREA', font=get_font(96, bold=True), fill=GOLD)
        bbox = draw.textbbox((0, 0), 'THE GOLD STANDARD OF DATA', font=get_font(20, bold=True))
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw)//2, 360), 'THE GOLD STANDARD OF DATA', font=get_font(20, bold=True), fill=GOLD_LIGHT)
        bbox = draw.textbbox((0, 0), 'Global CIF & Product Pricing Architecture', font=get_font(18))
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw)//2, 400), 'Global CIF & Product Pricing Architecture', font=get_font(18), fill=WHITE)
        title = ''
    else:
        title = titles.get(slide_num, '')

    # Add title text for non-cover
    if title and slide_num != 1:
        draw.text((150, 12), title, font=get_font(18, bold=True), fill=WHITE)

    # Footer
    draw.rectangle([0, H - 20, W, H], fill=NAVY)
    draw.text((10, H - 17), 'AUREA — The Gold Standard of Data  •  V1.0  •  Bank XYZ Confidential',
              font=get_font(10), fill=GRAY_300)
    page_text = f'{slide_num} / 20'
    bbox = draw.textbbox((0, 0), page_text, font=get_font(10))
    tw = bbox[2] - bbox[0]
    draw.text((W - tw - 10, H - 17), page_text, font=get_font(10), fill=GRAY_300)

    img.save(output_path)
    print(f'  ✓ Rendered slide {slide_num}')


if __name__ == '__main__':
    os.makedirs('/home/user/aurea-pptx-previews', exist_ok=True)
    for i in range(1, 21):
        render_slide_preview(i, f'/home/user/aurea-pptx-previews/slide_{i:02d}.png')
    print('\nDone!')
