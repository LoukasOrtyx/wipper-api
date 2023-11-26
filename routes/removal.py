from models.removal_request import RemovalRequest
from models.removal_response import RemovalResponse
from models.wipper_exception import WipperException
from fastapi import APIRouter, HTTPException, status
from services.wipper_removal import inpaint_person
from services.image_processing import *

router = APIRouter(
    prefix='/removal',
	tags=['Person Removal']
)

@router.post("/", response_model=RemovalResponse, responses={
    status.HTTP_200_OK: {'model': RemovalResponse},
    status.HTTP_400_BAD_REQUEST: {'model': WipperException}
})
def remove_person(wippper_request: RemovalRequest) -> RemovalResponse:
    target, image = decode_base64_list([wippper_request.target, wippper_request.image])
    marked_img = inpaint_person(target, image)
    return RemovalResponse(inpainted_img=encode_base64(marked_img))