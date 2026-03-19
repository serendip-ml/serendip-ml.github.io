#!/usr/bin/env python3
"""Convert SVG files to PNG."""

import sys
from pathlib import Path

import cairosvg


def convert_svg_to_png(svg_path: Path, scale: float = 2.0) -> Path:
    """Convert an SVG file to PNG.

    Args:
        svg_path: Path to the SVG file
        scale: Scale factor for output resolution (default 2x for retina)

    Returns:
        Path to the generated PNG file
    """
    png_path = svg_path.with_suffix('.png')
    cairosvg.svg2png(
        url=str(svg_path),
        write_to=str(png_path),
        scale=scale,
    )
    print(f"Converted: {svg_path.name} -> {png_path.name}")
    return png_path


def main() -> None:
    if len(sys.argv) < 2:
        # Default: convert agent-stack SVGs
        assets_dir = Path(__file__).parent.parent / 'assets' / 'images'
        svg_files = [
            assets_dir / 'agent-stack.svg',
            assets_dir / 'agent-stack-light.svg',
        ]
    else:
        svg_files = [Path(arg) for arg in sys.argv[1:]]

    for svg_path in svg_files:
        if not svg_path.exists():
            print(f"Warning: {svg_path} not found, skipping")
            continue
        if svg_path.suffix.lower() != '.svg':
            print(f"Warning: {svg_path} is not an SVG file, skipping")
            continue
        try:
            convert_svg_to_png(svg_path)
        except Exception as e:
            print(f"Error converting {svg_path}: {e}")


if __name__ == '__main__':
    main()
