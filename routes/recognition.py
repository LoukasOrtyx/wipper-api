from fastapi import APIRouter
from models.wipper_request import WipperRequest
from models.wipper_indexes import WipperIndexes
from src.recognition_svc import get_idxs_containing_face
from src.image_processing import decode_base64, encode_base64

router = APIRouter(
    prefix='/recognition',
	tags=['Face Recognition']
)

@router.post("/", response_model=WipperIndexes)
def search_for_face(wippper_request: WipperRequest) -> WipperIndexes:
    target, batch = decode_base64([wippper_request.target])[0], decode_base64(wippper_request.batch)
    idx_list = get_idxs_containing_face(target, batch)
    return WipperIndexes(indexes=idx_list)