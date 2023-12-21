from models.removal_request import RemovalRequest
from models.removal_response import RemovalResponse
from models.wipper_exception import WipperException
from fastapi import APIRouter, HTTPException, status
from services.wipper_removal import *
from services.wipper_segmentation import *
from services.image_processing import *
from services.wipper_recognition import *

router = APIRouter(
    prefix='/removal',
	tags=['Person Removal']
)

@router.post("/", response_model=RemovalResponse, responses={
    status.HTTP_200_OK: {'model': RemovalResponse},
    status.HTTP_400_BAD_REQUEST: {'model': WipperException},
})
def remove_person(wippper_request: RemovalRequest) -> RemovalResponse:
    target, image = decode_base64_list([wippper_request.target, wippper_request.image])
    extra_non_targets_pts = []
    try:
        coordinates = generate_face_coordinates(target, image, extra_non_targets_pts)
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not find face in target image."
        )
    masks = generate_masks(image, coordinates)
    merged_mask = merge_masks(masks)
    non_target_person_mask = merged_mask - masks[0]
    if non_target_person_mask.max() == 255:
        if not extra_non_targets_pts:
            non_target_person_mask = remove_isolated_mask_pixels(non_target_person_mask)
        non_target_person_mask = smooth_out_mask(non_target_person_mask)
    filled_mask = fill_mask_holes(merged_mask)
    prompt = "((background)), ((empty background))"
    negative_prompt = "(((person))), (((Human))), (((face))), (((body))), (((clothes))), (((Ugly))), (((Man))), (((girl))), (((boy))), (((Woman))), (((kid))), (((teen))), (((child))), (((human presence))), (((human elements))), (((human features))), (((portrait)))"
    negative_prompt += ", (((anime))), (((cartoon))), (((anime character))), (((cartoon character))), (((manga))), (((animated character))), (((comic character)))"
    negative_prompt += ", (((ugly background))), ((ugly walls)), ((ugly surfaces)), (((unpleasant background))), (((messy background))), (((dirty background))), (((chaotic background))), (((unattractive background))), (((dull background)))"
    people_removed_img = inpaint_image(image, filled_mask, prompt, negative_prompt)
    img_with_non_target = overlay_empty_background(people_removed_img, non_target_person_mask, image)
    return RemovalResponse(inpainted_img=encode_base64(img_with_non_target))