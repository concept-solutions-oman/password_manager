import os
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# Set up paths
base_dir = r"d:\Odoo Servers\server\odoo\bharath-local-addons\password_managment\static\description"
os.makedirs(base_dir, exist_ok=True)
output_path = os.path.join(base_dir, "main_screenshot.png")

# URLs
logo_url = "https://www.csloman.com/public/images/logo/logo.png"
# Use Windows system fonts
font_bold_path = "C:/Windows/Fonts/segoeuib.ttf"
if not os.path.exists(font_bold_path):
    font_bold_path = "C:/Windows/Fonts/arialbd.ttf"
    
font_regular_path = "C:/Windows/Fonts/segoeui.ttf"
if not os.path.exists(font_regular_path):
    font_regular_path = "C:/Windows/Fonts/arial.ttf"

# Download logo
logo_response = requests.get(logo_url)
logo = Image.open(BytesIO(logo_response.content)).convert("RGBA")

# Resize logo to fit nicely (make it fairly prominent)
target_logo_width = 500
ratio = target_logo_width / logo.width
logo = logo.resize((target_logo_width, int(logo.height * ratio)), Image.Resampling.LANCZOS)

font_title = ImageFont.truetype(font_bold_path, 75)
font_subtitle = ImageFont.truetype(font_regular_path, 35)

# Create 1600x900 image (common for Odoo 16:9 banner)
width, height = 1600, 900
image = Image.new("RGB", (width, height))
draw = ImageDraw.Draw(image, "RGBA")

# Create gradient background
# Dark blue to lighter blue/slate
color1 = (15, 23, 42) # #0f172a
color2 = (51, 65, 85) # #334155
for y in range(height):
    r = int(color1[0] + (color2[0] - color1[0]) * y / height)
    g = int(color1[1] + (color2[1] - color1[1]) * y / height)
    b = int(color1[2] + (color2[2] - color1[2]) * y / height)
    draw.line([(0, y), (width, y)], fill=(r, g, b))

# Paste Logo (centered horizontally, top quarter)
logo_x = int((width - logo.width) / 2)
logo_y = 180
image.paste(logo, (logo_x, logo_y), logo)

# Add Text
title = "Concept Password Management"
subtitle = "A centralized, ultra-secure hub for managing your customer credentials."

# Get text bounding box for centering
bbox_title = draw.textbbox((0, 0), title, font=font_title)
title_w = bbox_title[2] - bbox_title[0]
title_x = (width - title_w) / 2
title_y = logo_y + logo.height + 80

bbox_sub = draw.textbbox((0, 0), subtitle, font=font_subtitle)
sub_w = bbox_sub[2] - bbox_sub[0]
sub_x = (width - sub_w) / 2
sub_y = title_y + 110

# Drop shadow for title
draw.text((title_x+3, title_y+3), title, font=font_title, fill=(0, 0, 0, 100))
draw.text((title_x, title_y), title, font=font_title, fill=(255, 255, 255))

draw.text((sub_x, sub_y), subtitle, font=font_subtitle, fill=(203, 213, 225)) # #cbd5e1

# Add some feature tags below
features = ["100% Secure", "Lightning Fast", "Access Controlled"]
font_tag = ImageFont.truetype(font_bold_path, 28)

# Calculate total width to center tags
padding_x = 40
padding_y = 20
spacing = 60

tag_boxes = []
total_tag_w = 0
for f in features:
    bbox = draw.textbbox((0,0), f, font=font_tag)
    w = bbox[2] - bbox[0]
    total_tag_w += w + (padding_x * 2)
total_tag_w += spacing * (len(features) - 1)

start_x = (width - total_tag_w) / 2
tag_y = sub_y + 120

curr_x = start_x
for f in features:
    bbox = draw.textbbox((0,0), f, font=font_tag)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    
    # Draw pill (semi-transparent white)
    draw.rounded_rectangle(
        [curr_x, tag_y, curr_x + w + (padding_x * 2), tag_y + h + (padding_y * 2)], 
        radius=30, 
        fill=(255, 255, 255, 40)
    )
    # Draw text
    draw.text((curr_x + padding_x, tag_y + padding_y), f, font=font_tag, fill=(255, 255, 255))
    curr_x += w + (padding_x * 2) + spacing

image.save(output_path)
print("Saved banner to", output_path)
