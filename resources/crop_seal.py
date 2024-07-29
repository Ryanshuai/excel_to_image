import cv2
import numpy as np

mask = cv2.imread('./mask.png', cv2.IMREAD_UNCHANGED)
seal = cv2.imread('./raw_seal.png', cv2.IMREAD_UNCHANGED)

res_seal = mask[:, :, None] / 255 * seal
res_seal = np.concatenate([res_seal, mask[:, :, None]], axis=-1)
cv2.imwrite('./seal.png', res_seal)
