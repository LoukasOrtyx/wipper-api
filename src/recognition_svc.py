from typing import List
import face_recognition
import numpy as np

def get_idxs_containing_face(target_img: np.ndarray, batch: List[np.ndarray]):
	idx_list = []
	target_face = face_recognition.face_encodings(target_img, model='small')[0]
	for idx, img in enumerate(batch):
		unknown_faces = face_recognition.face_encodings(img, model='small')
		result = face_recognition.compare_faces(unknown_faces, target_face)
		if True in result:
			idx_list.append(idx)
	return idx_list