import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def paint_chinese_opencv(im, chinese, size, pos, color, font, align="center"):
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


if __name__ == '__main__':
    im = cv2.imread("01.png")
    photo = cv2.imread("photo.png")
    seal = cv2.imread("resources/seal.png", cv2.IMREAD_UNCHANGED)

    im = paint_chinese_opencv(im, "准   考   证", 34, (127, 94), (0, 255, 0), "NotoSansSC-Bold.ttf")
    im = paint_chinese_opencv(im, "文化和旅游部艺术发展中心", 19, (90, 65), (0, 255, 0), "SimSun.ttf")

    im = put_image(im, (120, 170), 170, photo)
    im = put_image(im, (110, 27), 180, seal)

    cv2.rectangle(im, (20, 25), (382, 744), (0, 0, 0), 2)

    cv2.imshow("image", im)
    cv2.waitKey(0)
