from models.wipper_exception import WipperException
from fastapi import APIRouter, HTTPException, status
from models.recognition_request import RecognitionRequest
from models.recognition_response import RecognitionResponse
from services.wipper_recognition import get_idxs_containing_face
from services.image_processing import *

router = APIRouter(
    prefix='/recognition',
	tags=['Face Recognition']
)

@router.post("/", response_model=RecognitionResponse, responses={
    status.HTTP_200_OK: {'model': RecognitionResponse},
    status.HTTP_400_BAD_REQUEST: {'model': WipperException}
})
def search_for_face(wippper_request: RecognitionRequest) -> RecognitionResponse:
    target, batch = decode_base64(wippper_request.target), decode_base64_list(wippper_request.batch)
    try:
        idx_list = get_idxs_containing_face(target, batch)
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not find face in target image."
        )
    return RecognitionResponse(indexes=idx_list)