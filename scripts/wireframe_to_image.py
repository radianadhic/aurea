"""
ASCII Wireframe → PNG Image Generator
Convert ASCII wireframes to high-quality PNG images using Pillow.
"""
from __future__ import annotations

import argparse
import os
import re
from pathlib import Path
from typing import List, Tuple

from PIL import Image, ImageDraw, ImageFont


# Font configuration
def get_font(size: int = 12, bold: bool = False) -> ImageFont.FreeTypeFont:
    """Load monospace font (fallback to default if not found)."""
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
        "/usr/share/fonts/TTF/DejaVuSansMono.ttf",
        "/usr/share/fonts/TTF/DejaVuSansMono-Bold.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def detect_color(line: str) -> Tuple[int, int, int]:
    """Detect semantic color from ASCII line content."""
    # Headers/titles in red
    if any(kw in line.lower() for kw in ["wireframe", "screen ", "bab "]):
        return (220, 50, 50)
    # Tables/forms in blue
    if "┌" in line and "──" in line:
        return (40, 90, 200)
    # Section markers in green
    if "✓" in line or "✅" in line:
        return (30, 160, 80)
    # Warnings in orange
    if "⚠" in line or "🚨" in line:
        return (220, 130, 30)
    return (40, 40, 40)  # default dark


def render_ascii_to_png(
    ascii_text: str,
    output_path: str,
    title: str | None = None,
    font_size: int = 13,
    char_width: int = 8,
    char_height: int = 18,
    padding: int = 30,
    bg_color: str = "#fafafa",
    border_color: str = "#cccccc",
) -> None:
    """Render ASCII art to a PNG image.

    Args:
        ascii_text: Multi-line ASCII wireframe string
        output_path: Output PNG file path
        title: Optional title to render above the wireframe
        font_size: Font size in points
        char_width: Width per character in pixels
        char_height: Height per character line in pixels
        padding: Padding around the wireframe in pixels
        bg_color: Background color
        border_color: Border color
    """
    lines = ascii_text.splitlines()
    if not lines:
        return

    # Calculate dimensions
    max_line_len = max(len(line) for line in lines)
    width = max_line_len * char_width + 2 * padding
    title_height = 50 if title else 0
    height = len(lines) * char_height + 2 * padding + title_height

    # Create image with white background
    img = Image.new("RGB", (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Draw title if provided
    if title:
        title_font = get_font(font_size + 4, bold=True)
        draw.text(
            (padding, padding // 2),
            title,
            font=title_font,
            fill=(20, 20, 80),
        )
        # Title underline
        draw.line(
            [(padding, padding // 2 + 32), (width - padding, padding // 2 + 32)],
            fill=(100, 100, 200),
            width=2,
        )

    # Draw border
    border_offset = padding // 2
    draw.rectangle(
        [
            (border_offset, border_offset + title_height),
            (width - border_offset, height - border_offset),
        ],
        outline=border_color,
        width=1,
    )

    # Draw ASCII lines
    font = get_font(font_size)
    bold_font = get_font(font_size, bold=True)
    y_start = padding + title_height
    for i, line in enumerate(lines):
        y = y_start + i * char_height
        color = detect_color(line)
        # Use bold for headers (lines starting with ┌─ or containing emoji)
        use_bold = bool(re.match(r"^[┌└].*[A-Z]", line) or "🚨" in line)
        current_font = bold_font if use_bold else font
        draw.text((padding, y), line, font=current_font, fill=color)

    # Save
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, "PNG", optimize=True)
    print(f"  ✅ Saved: {output_path} ({width}x{height})")


def extract_wireframes_from_markdown(
    md_path: str,
) -> List[Tuple[str, str, str]]:
    """Extract all ASCII wireframes from a markdown file.

    Returns:
        List of (title, bab, ascii_text) tuples
    """
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    wireframes: List[Tuple[str, str, str]] = []
    # Pattern: ``` blocks that contain wireframe-like ASCII (┌, │, └, etc.)
    pattern = re.compile(
        r"###?\s+(\d+\.\d+)\s+(Wireframe|[^\n]*)\n\n```\n(.*?)```",
        re.DOTALL,
    )
    for match in pattern.finditer(content):
        bab = match.group(1)
        title = match.group(2).strip()
        ascii_text = match.group(3).strip()
        # Only include if it actually looks like a wireframe
        if "┌" in ascii_text and "└" in ascii_text and "│" in ascii_text:
            wireframes.append((bab, title, ascii_text))

    return wireframes


def main() -> None:
    parser = argparse.ArgumentParser(description="ASCII wireframe → PNG")
    parser.add_argument(
        "--source", default="/home/user/MDM-Technical-Documentation-v1.0.md",
        help="Source markdown file"
    )
    parser.add_argument(
        "--output-dir",
        default="/home/user/wireframes/images",
        help="Output directory for PNG images",
    )
    parser.add_argument(
        "--limit", type=int, default=0,
        help="Limit number of wireframes (0 = all)",
    )
    parser.add_argument(
        "--font-size", type=int, default=13,
        help="Font size",
    )
    args = parser.parse_args()

    print(f"📂 Source: {args.source}")
    print(f"📁 Output: {args.output_dir}")
    print()

    wireframes = extract_wireframes_from_markdown(args.source)
    if args.limit:
        wireframes = wireframes[: args.limit]
    print(f"🔍 Found {len(wireframes)} ASCII wireframes")
    print()

    for i, (bab, title, ascii_text) in enumerate(wireframes, 1):
        output_name = f"wireframe_bab_{bab.replace('.', '_')}_{i:02d}.png"
        # Sanitize title for filename
        safe_title = re.sub(r"[^A-Za-z0-9_-]", "_", title)[:40]
        if safe_title:
            output_name = f"wireframe_bab_{bab.replace('.', '_')}_{safe_title}.png"
        output_path = os.path.join(args.output_dir, output_name)
        full_title = f"BAB {bab} — {title}"
        print(f"  [{i:2d}/{len(wireframes)}] {full_title}")
        render_ascii_to_png(
            ascii_text,
            output_path,
            title=full_title,
            font_size=args.font_size,
        )

    print()
    print(f"✅ Done. {len(wireframes)} images saved to {args.output_dir}")


if __name__ == "__main__":
    main()
