import cv2
import numpy as np
import face_recognition

from typing import List

def generate_face_coordinates(target_img: np.ndarray, unknown_img: np.ndarray, extra_non_target_pts=[]):
	target_face = face_recognition.face_encodings(target_img, model='small')[0]
	face_locations = face_recognition.face_locations(unknown_img)
	face_encodings = face_recognition.face_encodings(unknown_img, face_locations, model='small')
	match = face_recognition.compare_faces(face_encodings, target_face)
	coordinates = []
	try:
		idx = match.index(True)
		target_location = face_locations.pop(idx)
		top, right, bottom, left = target_location
		x = (left + right) // 2
		y = (top + bottom) // 2
		target_center_coordinate = (x, y)
	except ValueError:
		raise ValueError("The target face was not found in the image")
	for face_location in face_locations:
		top, right, bottom, left = face_location
		x = (left + right) // 2
		y = (top + bottom) // 2
		coordinates.append((x, y))
	if extra_non_target_pts:
		coordinates.extend(extra_non_target_pts)
	
	coordinates = np.array([target_center_coordinate, *coordinates])
	return coordinates
	
def get_idxs_containing_face(target_img: np.ndarray, batch: List[np.ndarray]):
	idx_list = []
	target_face = face_recognition.face_encodings(target_img, model='small')[0]
	for idx, img in enumerate(batch):
		unknown_faces = face_recognition.face_encodings(img, model='small')
		result = face_recognition.compare_faces(unknown_faces, target_face)
		if True in result:
			idx_list.append(idx)
	return idx_list