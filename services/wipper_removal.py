import numpy as np
from services.wipper_recognition import mark_for_deletion

def inpaint_person(target: np.ndarray, unknown_img: np.ndarray) -> np.ndarray:
	result = mark_for_deletion(target, unknown_img)
	return result