import cv2
import numpy as np
import face_recognition

from typing import List

def mark_for_deletion(target_img: np.ndarray, unknown_img: np.ndarray):
	target_face = face_recognition.face_encodings(target_img, model='small')[0]

	face_locations = face_recognition.face_locations(unknown_img)
	face_encodings = face_recognition.face_encodings(unknown_img, face_locations, model='small')
	match = face_recognition.compare_faces(face_encodings, target_face)
	try:
		idx = match.index(True)
		top, right, bottom, left = face_locations[idx]
		x = (left + right) // 2
		y = (top + bottom) // 2
		mask = np.zeros_like(unknown_img)
		cv2.circle(mask, (x, y), 30, (0, 0, 255), thickness=-1)
		result_img = cv2.addWeighted(unknown_img, 1, mask, 0.3, 0)
		return result_img
	except ValueError:
		raise ValueError("The target face was not found in the image")


def get_idxs_containing_face(target_img: np.ndarray, batch: List[np.ndarray]):
	idx_list = []
	target_face = face_recognition.face_encodings(target_img, model='small')[0]
	for idx, img in enumerate(batch):
		unknown_faces = face_recognition.face_encodings(img, model='small')
		result = face_recognition.compare_faces(unknown_faces, target_face)
		if True in result:
			idx_list.append(idx)
	return idx_list