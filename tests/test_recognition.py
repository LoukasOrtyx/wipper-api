import sys
import cv2

from pathlib import Path
sys.path.append(str(Path(sys.argv[0]).resolve().parent.parent))

from main import app
from fastapi.testclient import TestClient
from models.wipper_request import WipperRequest
from src.image_processing import encode_base64, decode_base64

client = TestClient(app)

def get_images_from_dir(path: Path):
	imgs = []
	for item in path.iterdir():
		if not item.is_dir():
			imgs.append(cv2.imread(str(item)))
	return imgs

def test_post_recognition():
	target = cv2.imread(str(Path('images/target/lucas.png')))
	encoded_target = encode_base64([target])[0]
	encoded_batch = encode_base64(get_images_from_dir(Path('images')))
	wipper_request = WipperRequest(target=encoded_target, batch=encoded_batch)
	response = client.post('/api/v1/recognition/', json=wipper_request.dict())
	status_code, json = response.status_code, response.json()
	assert status_code == 200, f'The response status code should be 200, but was {status_code}: ' \
							   f'{json["detail"]}'
										
	expected_repsonse = {'indexes': [0, 2, 3, 4, 5]}
	assert json == expected_repsonse, 'Target face recognition failed:\nExpected Response: ' \
									  f'{expected_repsonse}\nReceived: {json}'