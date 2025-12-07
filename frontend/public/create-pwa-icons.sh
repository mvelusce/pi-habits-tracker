#!/bin/bash

# Create simple SVG icon
cat > temp-icon.svg << 'SVGEOF'
<svg width="512" height="512" xmlns="http://www.w3.org/2000/svg">
  <rect width="512" height="512" fill="#3B82F6"/>
  <circle cx="256" cy="256" r="180" fill="white" opacity="0.2"/>
  <path d="M 150 256 L 230 336 L 380 186" stroke="white" stroke-width="40" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
  <text x="256" y="420" font-family="Arial" font-size="48" fill="white" text-anchor="middle" font-weight="bold">Habits</text>
</svg>
SVGEOF

# Convert SVG to PNG using ImageMagick or create with Python
if command -v convert &> /dev/null; then
    convert temp-icon.svg -resize 192x192 pwa-192x192.png
    convert temp-icon.svg -resize 512x512 pwa-512x512.png
elif command -v python3 &> /dev/null && python3 -c "import PIL" 2>/dev/null; then
    python3 << 'PYEOF'
from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, filename):
    img = Image.new('RGB', (size, size), color='#3B82F6')
    draw = ImageDraw.Draw(img)
    
    # Draw circle
    circle_r = int(size * 0.35)
    circle_xy = [(size//2 - circle_r, size//2 - circle_r), 
                  (size//2 + circle_r, size//2 + circle_r)]
    draw.ellipse(circle_xy, fill=(255, 255, 255, 50))
    
    # Draw checkmark
    check_points = [
        (size * 0.3, size * 0.5),
        (size * 0.45, size * 0.65),
        (size * 0.75, size * 0.35)
    ]
    draw.line(check_points, fill='white', width=int(size * 0.08), joint='curve')
    
    # Save
    img.save(filename)
    print(f'Created {filename}')

create_icon(192, 'pwa-192x192.png')
create_icon(512, 'pwa-512x512.png')
PYEOF
else
    echo "Neither ImageMagick nor Python PIL available, creating placeholder files"
    # Just touch the files so build doesn't fail
    touch pwa-192x192.png pwa-512x512.png
fi

rm -f temp-icon.svg
echo "PWA icons created!"
