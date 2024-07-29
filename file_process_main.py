import os

from PIL import Image
import cv2
from tqdm import tqdm

from registration_to_admission_info import decode_pdf
from compose_image import generate_admission_im

input_folder = r"C:\Users\10187\Desktop\ouyun\报名表"
output_folder = r"C:\Users\10187\Desktop\ouyun\admission"

os.makedirs(output_folder, exist_ok=True)
for pdf_path in tqdm(os.listdir(input_folder)):
    if not pdf_path.endswith(".pdf"):
        continue
    info, image = decode_pdf(os.path.join(input_folder, pdf_path))
    im = generate_admission_im(info, image)

    output_path = os.path.join(output_folder, pdf_path.replace(".pdf", ".png"))
    im_rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(im_rgb)
    pil_image.save(output_path)

    # cv2.imwrite(output_path, im)
