from PIL import Image, ImageDraw, ImageFont
import string
import random
from io import BytesIO


# 生成随机颜色，这里返回的是一个元组
def generate_random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


str_all = string.digits + string.ascii_letters


# 生成随机验证码
def generate_random_code():
    # 生成一个白色的背景图片
    width = 200
    height = 50
    img = Image.new('RGB', (width, height), color=(255, 255, 255))

    # 生成一个和白色背景图片大小一样的画布
    draw = ImageDraw.Draw(img)

    # 生成字体对象
    font = ImageFont.truetype(font='./font/New Asgard.ttf', size=32)

    # 书写文字
    valid_code = ''
    for i in range(4):
        random_char = random.choice(str_all)
        valid_code += random_char
        draw.text((40 * i + 29, 0), random_char, (0, 0, 0), font=font)

    print(valid_code)

    # 随机生成点
    for i in range(80):
        x, y = random.randint(0, width), random.randint(0, height)
        draw.point((x, y), generate_random_color())

    # 随机生成线
    for i in range(8):
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, width), random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=generate_random_color())

    # 创建一个内存句柄
    f = BytesIO()

    # 直接将图片保存在内存句柄中
    img.save(f, 'PNG')

    # 读取内存句柄
    data = f.getvalue()
    print(data)


if __name__ == '__main__':
    generate_random_code()
