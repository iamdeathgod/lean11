from PIL import Image, ImageDraw, ImageFont

# Create 1200x630 image
img = Image.new('RGB', (1200, 630), '#0A1D2E')
draw = ImageDraw.Draw(img)

# Radial gradient wash (simplified) - using a more efficient approach
for y in range(630):
    for x in range(1200):
        cx, cy = 144, -50
        dx, dy = x - cx, y - cy
        dist = (dx*dx + dy*dy)**0.5
        max_dist = (1200*1200 + 630*630)**0.5 * 0.62
        if dist < max_dist:
            opacity = 0.18 * (1 - dist/max_dist)
            r = int(0x0A + (0x40 - 0x0A) * opacity)
            g = int(0x1D + (0x78 - 0x1D) * opacity)
            b = int(0x2E + (0xAA - 0x2E) * opacity)
            img.putpixel((x, y), (r, g, b))

# Draw paper sheet with shadow
sheet_x, sheet_y = 200, 80
sheet_w, sheet_h = 800, 470

# Shadow layers
for offset, alpha in [(16, 0.5), (8, 0.3)]:
    shadow = Image.new('RGBA', (sheet_w, sheet_h), (0, 0, 0, int(255*alpha)))
    img.paste(shadow, (sheet_x+offset, sheet_y+offset), shadow)

# Paper background
paper = Image.new('RGB', (sheet_w, sheet_h), '#EFEDE6')
img.paste(paper, (sheet_x, sheet_y))

# Perforated edges (top and bottom)
for x in range(7, sheet_w, 14):
    draw.ellipse([sheet_x+x-5, sheet_y-5, sheet_x+x+5, sheet_y+5], fill='#0A1D2E')
    draw.ellipse([sheet_x+x-5, sheet_y+sheet_h-5, sheet_x+x+5, sheet_y+sheet_h+5], fill='#0A1D2E')

# Fonts
try:
    font_title = ImageFont.truetype('C:/Windows/Fonts/georgia.ttf', 32)
    font_title_bold = ImageFont.truetype('C:/Windows/Fonts/georgiab.ttf', 32)
    font_record = ImageFont.truetype('C:/Windows/Fonts/cour.ttf', 14)
    font_record_bold = ImageFont.truetype('C:/Windows/Fonts/courbd.ttf', 14)
    font_stamp = ImageFont.truetype('C:/Windows/Fonts/courbd.ttf', 22)
    font_tagline = ImageFont.truetype('C:/Windows/Fonts/georgia.ttf', 20)
    font_small = ImageFont.truetype('C:/Windows/Fonts/cour.ttf', 13)
except:
    font_title = font_title_bold = font_record = font_record_bold = font_stamp = font_tagline = font_small = ImageFont.load_default()

# Sheet header
draw.text((sheet_x+40, sheet_y+70), 'Service order', font=font_title_bold, fill='#16222D')
draw.text((sheet_x+40, sheet_y+100), 'No. 11-0001 \u00b7 Sheet 1 of 1', font=font_record, fill='#4C5A66')

# Meta row
draw.line([(sheet_x+40, sheet_y+115), (sheet_x+760, sheet_y+115)], fill='#BDB7A7', width=1)
draw.text((sheet_x+40, sheet_y+140), 'Windows 11 \u00b7 Balanced', font=font_record, fill='#4C5A66')
draw.text((sheet_x+600, sheet_y+140), 'Preview \u00b7 not applied', font=font_record, fill='#4C5A66', anchor='ra')

# Stamp: NOT APPLIED
stamp_x, stamp_y = sheet_x+700, sheet_y+85
stamp_img = Image.new('RGBA', (240, 80), (0,0,0,0))
stamp_draw = ImageDraw.Draw(stamp_img)
stamp_draw.rectangle([0, 0, 220, 60], outline='#B3261E', width=3)
stamp_draw.text((110, 10), 'NOT APPLIED', font=font_stamp, fill='#B3261E', anchor='mm')
stamp_draw.line([(20, 40), (200, 40)], fill='#B3261E', width=1)
stamp_draw.text((110, 55), 'Nothing changed', font=font_small, fill='#B3261E', anchor='mm')
stamp_img = stamp_img.rotate(-7, expand=True, resample=Image.BICUBIC)
img.paste(stamp_img, (stamp_x - stamp_img.width//2, stamp_y - stamp_img.height//2), stamp_img)

# Service items
services = ['Diagnostics Tracking', 'Maps Broker', 'Xbox services (4)', 'Push To Install']
apps = ['Bing News', 'Clipchamp', 'Solitaire Collection', 'Office Hub']

y = sheet_y + 190
draw.text((sheet_x+40, y), 'Services', font=font_record, fill='#4C5A66')
draw.line([(sheet_x+40, y+8), (sheet_x+760, y+8)], fill='#D3CEC1', width=1)

for i, svc in enumerate(services):
    item_y = y + 30 + i * 35
    draw.text((sheet_x+70, item_y), f'\u2610 {svc}', font=font_title, fill='#16222D')
    draw.text((sheet_x+700, item_y), 'Off', font=font_record_bold, fill='#B3261E', anchor='ra')

y = sheet_y + 380
draw.text((sheet_x+40, y), 'Bundled apps', font=font_record, fill='#4C5A66')
draw.line([(sheet_x+40, y+8), (sheet_x+760, y+8)], fill='#D3CEC1', width=1)

for i, app in enumerate(apps):
    item_y = y + 30 + i * 35
    draw.text((sheet_x+70, item_y), f'\u2610 {app}', font=font_title, fill='#16222D')
    draw.text((sheet_x+700, item_y), 'Remove', font=font_record_bold, fill='#B3261E', anchor='ra')

# Bottom tagline
draw.text((600, 580), 'Every change, on the record.', font=font_tagline, fill='#EDEAE1', anchor='mm')
draw.text((600, 610), 'Lean11 \u00b7 Free for personal use', font=font_small, fill='#AEBECC', anchor='mm')

img.save('og-image.png')
print('PNG created successfully')