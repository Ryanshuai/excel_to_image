import pandas as pd
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from exam_dict import location_time_dict

chinese_level = ["", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]


def paint_chinese_opencv(im, chinese, pos, color):
    img_PIL = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
    font = ImageFont.truetype("STFANGSO.TTF", 90)
    fillColor = color  # (255,0,0)
    position = pos  # (100,100)
    # if not isinstance(chinese, unicode):
    #     chinese = chinese.decode('utf-8')
    draw = ImageDraw.Draw(img_PIL)
    draw.text(position, chinese, font=font, fill=fillColor, stroke_width=1)

    img = cv2.cvtColor(np.asarray(img_PIL), cv2.COLOR_RGB2BGR)
    return img


def add_one_user(img, zero_location, name, number, major, level, location):
    exam_time, exam_location = location_time_dict[location]
    x, y = zero_location
    dy = 175
    img = paint_chinese_opencv(img, name, (x, y), (0, 0, 0))
    img = paint_chinese_opencv(img, number, (x, y + dy), (0, 0, 0))
    img = paint_chinese_opencv(img, major + " " + chinese_level[level] + "级", (x, y + dy * 2), (0, 0, 0))
    img = paint_chinese_opencv(img, exam_location, (x, y + dy * 3), (0, 0, 0))
    img = paint_chinese_opencv(img, exam_time, (x, y + dy * 4), (0, 0, 0))
    return img


if __name__ == '__main__':
    image = cv2.imread("01.png")

    xl = pd.ExcelFile("2020 exam 8_17.xlsx")
    df = xl.parse(xl.sheet_names[0])
    names = df.name
    numbers = df.exam_number
    majors = df.major
    levels = df.level
    locations = df.location

    i = 0
    for i in range(0, len(names)):
        print(i)
        name = names[i]
        number = numbers[i]
        major = majors[i]
        level = levels[i]
        location = locations[i]
        user = name, number, major, level, location

        zero_location = (850, 2150)
        img = add_one_user(image.copy(), zero_location, name, number, major, level, location)
        cv2.imwrite('output/' + str(i + 1) + '.png', img)
        # break


