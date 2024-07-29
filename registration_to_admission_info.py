import io
import re

import cv2
import numpy as np
import pymupdf
from PIL import Image

location_mapping = {"大同": "大同艺诚文化", "灵丘": "灵丘县青少年宫", "线上考试": "大同艺诚文化线上考试"}


def extract_info(text):
    student_name = re.search(r"姓 名\n\s*(\S+)", text)
    student_id = re.search(r"考生编号：(\d+)", text)
    major = re.search(r"申报专业\n\s*(\S+)", text)
    level = re.search(r"申报级别\s*(\S+)", text)
    exam_time = re.search(r"考试时间\n\s*(.+)", text)
    exam_location = re.search(r"考场地址\n\s*(\S+)", text)

    exam_location = exam_location.group(1)
    exam_location = location_mapping.get(exam_location, exam_location)
    student_info = {
        '考生姓名 :': student_name.group(1),
        '考生编号 :': student_id.group(1),
        '专      业 :': major.group(1),
        '级      别 :': level.group(1),
        '考试时间 :': exam_time.group(1),
        '考试地点 :': exam_location
    }
    return student_info


def decode_pdf(pdf_path):
    pdf_document = pymupdf.open(pdf_path)

    page = pdf_document[0]
    text = page.get_text()
    info = extract_info(text)

    image_list = page.get_images()

    photo = image_list[1][0]
    base_image = pdf_document.extract_image(photo)
    image_bytes = base_image["image"]
    image = Image.open(io.BytesIO(image_bytes))

    pdf_document.close()

    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return info, image


if __name__ == '__main__':
    info, image = decode_pdf("2021_168578_张馨予.pdf")
    image.save("photo.png")
