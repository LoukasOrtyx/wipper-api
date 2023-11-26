from typing import List
from pydantic import BaseModel, Field

class RemovalRequest(BaseModel):
    target: str = Field(
        ..., title='Target Image', 
        description='Base64 encoded image string of the person to be wiped out.')
    image: str = Field(
        ..., title='Inpainted Batch', 
        description='Base64 encoded image string whose target person will be removed using' \
    	'Inpainting techniques.')