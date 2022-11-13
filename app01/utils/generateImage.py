from PIL import Image, ImageDraw, ImageFont
import string
import random

str_all = string.digits + string.ascii_letters
# 生成一个白色的背景图片
img = Image.new('RGB', (200, 50), color=(255, 255, 255))

# 生成一个和白色背景图片大小一样的画布
draw = ImageDraw.Draw(img)

# 生成字体对象
font = ImageFont.truetype(font='./font/New Asgard.ttf', size=32)

valid_code = ''
for i in range(4):
    random_char = random.choice(str_all)
    valid_code += random_char
    draw.text((40*i + 30, 0), random_char, (0, 0, 0), font=font)

print(valid_code)
img.save('new_img.png', 'PNG')
