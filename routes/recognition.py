from http import HTTPStatus
from fastapi import APIRouter, HTTPException
from models.wipper_request import WipperRequest
from models.wipper_indexes import WipperIndexes
from models.wipper_exception import WipperException
from src.recognition_svc import get_idxs_containing_face
from src.image_processing import decode_base64, encode_base64

router = APIRouter(
    prefix='/recognition',
	tags=['Face Recognition']
)

@router.post("/", response_model=WipperIndexes, responses={
    int(HTTPStatus.OK): {'model': WipperIndexes},
    int(HTTPStatus.BAD_REQUEST): {'model': WipperException}
})
def search_for_face(wippper_request: WipperRequest) -> WipperIndexes:
    target, batch = decode_base64([wippper_request.target])[0], decode_base64(wippper_request.batch)
    try:
        idx_list = get_idxs_containing_face(target, batch)
    except IndexError:
        return WipperException(status_code=HTTPStatus.BAD_REQUEST, detail="Could not find face in target image.")
    return WipperIndexes(indexes=idx_list)