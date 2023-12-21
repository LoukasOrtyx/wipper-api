# import cv2
# import __init__
# from main import app
# from pathlib import Path
# from fastapi import status
# from fastapi.testclient import TestClient
# from models.recognition_request import RecognitionRequest
# from models.recognition_response import RecognitionResponse
# from services.image_processing import encode_base64, encode_base64_list

# client = TestClient(app)

# def get_images_from_dir(path: Path):
# 	imgs = []
# 	for item in path.iterdir():
# 		if not item.is_dir():
# 			imgs.append(cv2.imread(str(item)))
# 	return imgs

# def test_post_recognition():
# 	target = cv2.imread(str(Path('images/target/lucas.png')))
# 	encoded_target = encode_base64(target)
# 	encoded_batch = encode_base64_list(get_images_from_dir(Path('images')))
# 	wipper_request = RecognitionRequest(target=encoded_target, batch=encoded_batch)
# 	response = client.post('/api/v1/recognition/', json=wipper_request.dict())
# 	status_code = response.status_code
# 	expected_status_code = status.HTTP_200_OK
# 	assert status_code == expected_status_code, f'The response status code should be ' \
# 							   f'{expected_status_code}, but was {status_code}: ' \
# 							   f'{response.json()["detail"]}'
										
# 	wipper_response = RecognitionResponse(**response.json())
# 	expected_repsonse = RecognitionResponse(indexes=[0, 2, 3, 4, 5, 6, 7, 8])
# 	assert wipper_response == expected_repsonse, 'Target face recognition failed:\nExpected Response: ' \
# 									  f'{expected_repsonse}\nReceived: {wipper_response}'