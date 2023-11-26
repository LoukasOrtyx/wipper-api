from typing import List
from pydantic import BaseModel, Field

class RemovalResponse(BaseModel):
    inpainted_img: str = Field(
        ..., title='Inpainted Batch', 
        description='Base64 encoded image string whose target person was removed using Inpainting techniques.')