import cv2
import base64
import numpy as np

from typing import List

def encode_base64(targets: List[np.ndarray]) -> List[str]:
	encoded = []
	for target in targets:
		_, buffer = cv2.imencode(".jpg", target)
		encoded_img = base64.b64encode(buffer).decode("utf-8")
		encoded.append(encoded_img)
	return encoded

def decode_base64(targets: List[str]) -> List[np.ndarray]:
	decoded = []
	for target in targets:
		image_data = base64.b64decode(target)
		nparr = np.frombuffer(image_data, np.uint8)
		decoded_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
		decoded.append(decoded_img)
	return decoded