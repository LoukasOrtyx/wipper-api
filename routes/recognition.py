from models.wipper_request import WipperRequest
from models.wipper_indexes import WipperIndexes
from models.wipper_exception import WipperException
from fastapi import APIRouter, HTTPException, status
from src.recognition_svc import get_idxs_containing_face
from src.image_processing import decode_base64, encode_base64

router = APIRouter(
    prefix='/recognition',
	tags=['Face Recognition']
)

@router.post("/", response_model=WipperIndexes, responses={
    status.HTTP_200_OK: {'model': WipperIndexes},
    status.HTTP_400_BAD_REQUEST: {'model': WipperException}
})
def search_for_face(wippper_request: WipperRequest) -> WipperIndexes:
    target, batch = decode_base64([wippper_request.target])[0], decode_base64(wippper_request.batch)
    try:
        idx_list = get_idxs_containing_face(target, batch)
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not find face in target image."
        )
    return WipperIndexes(indexes=idx_list)