from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO


def generate_card(username, avatar_url, member_count):

    width = 900
    height = 300

    image = Image.new("RGB", (width, height))

    draw = ImageDraw.Draw(image)

    # gradient background
    for y in range(height):
        r = int(40 + y * 0.3)
        g = int(0 + y * 0.2)
        b = int(120 + y * 0.1)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    avatar_size = 180

    response = requests.get(avatar_url)
    avatar = Image.open(BytesIO(response.content)).resize((avatar_size, avatar_size))

    mask = Image.new("L", (avatar_size, avatar_size), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0, avatar_size, avatar_size), fill=255)

    image.paste(avatar, (50, 60), mask)

    font_big = ImageFont.truetype("assets/font.ttf", 60)
    font_small = ImageFont.truetype("assets/font.ttf", 40)

    draw.text((260, 90), f"Welcome {username}", font=font_big, fill=(255,255,255))
    draw.text((260, 170), f"Member #{member_count}", font=font_small, fill=(200,200,200))

    file_path = "welcome.png"
    image.save(file_path)

    return file_path