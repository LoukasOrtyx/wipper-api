import cv2
import __init__
from main import app
from pathlib import Path
from fastapi import status
from fastapi.testclient import TestClient
from models.removal_request import RemovalRequest
from models.removal_response import RemovalResponse

from services.image_processing import *

client = TestClient(app)

def test_post_removal():
	target = cv2.imread(str(Path('images/target/lucas.png')))
	img = cv2.imread(str(Path('images/img8.jpeg')))
	encoded_target, encoded_img = encode_base64_list([target, img])
	wipper_request = RemovalRequest(target=encoded_target, image=encoded_img)
	response = client.post('/api/v1/removal/', json=wipper_request.dict())
	status_code = response.status_code
	expected_status_code = status.HTTP_200_OK
	assert status_code == expected_status_code, f'The response status code should be ' \
							   f'{expected_status_code}, but was {status_code}: ' \
							   f'{response.json()["detail"]}'
	wipper_response = RemovalResponse(**response.json())
	response_img = decode_base64(wipper_response.inpainted_img)
	cv2.imwrite(str(Path('test_outputs/inpainted_test.png')), response_img)
	