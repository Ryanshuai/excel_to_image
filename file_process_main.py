import os

import cv2

from registration_to_admission_info import decode_pdf
from compose_image import generate_admission_im

input_folder = ""
output_folder = ""

for pdf_path in os.listdir(input_folder):
    if not pdf_path.endswith(".pdf"):
        continue
    info, image = decode_pdf(os.path.join(input_folder, pdf_path))
    im = generate_admission_im(info, image)
    cv2.imwrite(os.path.join(output_folder, pdf_path.replace(".pdf", ".png")), im)
