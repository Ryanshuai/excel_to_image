import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

scale = 4
seal = cv2.imread("resources/seal.png", cv2.IMREAD_UNCHANGED)


def paint_chinese_opencv(im, chinese, size, pos, color, font, align="center"):
    pos = (pos[0] * scale, pos[1] * scale)
    size = size * scale

    font = "resources/" + font
    img_PIL = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
    font = ImageFont.truetype(font, size)
    fillColor = color  # (255,0,0)
    position = pos  # (100,100)
    draw = ImageDraw.Draw(img_PIL)
    draw.text(position, chinese, font=font, fill=fillColor, align=align)
    img = cv2.cvtColor(np.asarray(img_PIL), cv2.COLOR_RGB2BGR)
    return img


def put_image(background_im, pos, w, im):
    pos = (pos[0] * scale, pos[1] * scale)
    w = w * scale

    h_w_ratio = im.shape[0] / im.shape[1]
    h = int(w * h_w_ratio)
    im = cv2.resize(im, (w, h))
    h, w = im.shape[:2]
    x, y = pos
    if im.shape[2] == 4:
        im_rgb = im[:, :, :3]
        mask = im[:, :, [3]] / 255.
        background_im[y:y + h, x:x + w] = im_rgb * mask + background_im[y:y + h, x:x + w] * (1 - mask)
    else:
        background_im[y:y + h, x:x + w] = im
    return background_im


def generate_admission_im(student_info, student_photo, size=(400, 771), im=None):
    im = im if im is not None else np.ones((size[1] * scale, size[0] * scale, 3), dtype=np.uint8) * 255
    # im = paint_chinese_opencv(im, "准   考   证", 34, (127, 94), (0, 0, 0), "NotoSansSC-Bold.ttf")
    im = paint_chinese_opencv(im, "准   考   证", 34, (127, 94), (0, 0, 0), "NotoSansSC-Bold.ttf")
    im = paint_chinese_opencv(im, "文化和旅游部艺术发展中心", 19, (90, 65), (0, 0, 0), "SimSun.ttf")

    im = put_image(im, (120, 170), 170, student_photo)
    im = put_image(im, (110, 27), 180, seal)
    cv2.rectangle(im, (20 * scale, 25 * scale), (382 * scale, 744 * scale), (0, 0, 0), 2 * scale)

    for y, (k, v) in zip(range(460, 460 + 246, 41), student_info.items()):
        im = paint_chinese_opencv(im, k, 15, (58, y - 1), (0, 0, 0), "微软雅黑.ttf")
        im = paint_chinese_opencv(im, v, 19, (160, y - 2), (0, 0, 0), "SimSun.ttf")
        y_line = (y + 19) * scale
        im = cv2.line(im, (158 * scale, y_line), (345 * scale, y_line), (0, 0, 0), 1 * scale)

    return im


if __name__ == '__main__':
    im = cv2.imread("01.png")
    im = cv2.resize(im, (400 * scale, 771 * scale))

    im = None

    student_info = {
        '考生姓名 :': '张梓宁',
        '考生编号 :': '120520240161061',
        '专      业 :': '钢琴',
        '级      别 :': '七级',
        '考试时间 :': '8月3日-5日',
        '考试地点 :': '大同'
    }
    photo = cv2.imread("photo.png")

    im = generate_admission_im(student_info, photo, im=im)

    cv2.imshow("admission_example", im)
    cv2.waitKey(0)
    cv2.imwrite("admission_example.png", im)
