import cv2
import __init__
from main import app
from typing import List
from pathlib import Path
from fastapi import status
from fastapi.testclient import TestClient
from models.wipper_image import WipperImage
from models.recognition_request import RecognitionRequest
from models.recognition_response import RecognitionResponse
from services.image_processing import encode_base64, encode_base64_list

client = TestClient(app)

def get_wipper_images_from_dir(path: Path) -> List[WipperImage]:
	imgs = []
	for item in path.iterdir():
		if not item.is_dir():
			fname = str(item)
			img = cv2.imread(fname)
			encoded_img = encode_base64(img)
			imgs.append(WipperImage(fname=fname, data=encoded_img))
	return imgs

def test_post_recognition():
	target_path = str(Path('images/target/lucas.png'))
	target = cv2.imread(target_path)
	encoded_batch = get_wipper_images_from_dir(Path('images'))
	wipper_target = WipperImage(fname=target_path, data=encode_base64(target))
	wipper_request = RecognitionRequest(target=wipper_target, batch=encoded_batch)
	response = client.post('/api/v1/recognition/', json=wipper_request.dict())
	status_code = response.status_code
	expected_status_code = status.HTTP_200_OK
	assert status_code == expected_status_code, f'The response status code should be ' \
							   f'{expected_status_code}, but was {status_code}: ' \
							   f'{response.json()["detail"]}'

	wipper_response = RecognitionResponse(**response.json())
	expected_fnames = [
		'images\\img0.jpg', 
		'images\\img3.png', 
		'images\\img4.png', 
		'images\\img5.jpeg', 
		'images\\img6.png', 
		'images\\img7.png', 
		'images\\img8.jpeg'
	]
	expected_response = RecognitionResponse(fnames=expected_fnames)
	assert wipper_response == expected_response, 'Target face recognition failed:\nExpected Response: ' \
									  f'{expected_response}\nReceived: {wipper_response}'