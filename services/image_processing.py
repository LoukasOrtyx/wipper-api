import cv2
import base64
import numpy as np

from typing import List

def encode_base64(target: np.ndarray) -> str:
	_, buffer = cv2.imencode(".jpg", target)
	encoded_img = base64.b64encode(buffer).decode("utf-8")
	return encoded_img

def encode_base64_list(targets: List[np.ndarray]) -> List[str]:
	encoded = []
	for target in targets:
		encoded.append(encode_base64(target))
	return encoded

def decode_base64(target: str) -> np.ndarray:
	image_data = base64.b64decode(target)
	nparr = np.frombuffer(image_data, np.uint8)
	decoded_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
	return decoded_img

def decode_base64_list(targets: List[str]) -> List[np.ndarray]:
	decoded = []
	for target in targets:
		decoded.append(decode_base64(target))
	return decoded