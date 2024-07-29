import os

import cv2
from tqdm import tqdm

from registration_to_admission_info import decode_pdf
from compose_image import generate_admission_im

input_folder = r"C:\Users\10187\Desktop\欧韵\报名表"
output_folder = r"C:\Users\10187\Desktop\欧韵\准考证"

for pdf_path in tqdm(os.listdir(input_folder)):
    if not pdf_path.endswith(".pdf"):
        continue
    info, image = decode_pdf(os.path.join(input_folder, pdf_path))
    im = generate_admission_im(info, image)
    cv2.imwrite(os.path.join(output_folder, pdf_path.replace(".pdf", ".png")), im)
