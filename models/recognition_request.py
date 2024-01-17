from typing import List
from pydantic import BaseModel, Field
from models.wipper_image import WipperImage

class RecognitionRequest(BaseModel):
    target: WipperImage = Field(
        ..., title='Target Image', 
        description='WipperImage instance of the person to be wiped out.')
    batch: List[WipperImage] = Field(
        ..., title='Image Batch', 
        description='List of WipperImage containing the image batch to be processed.')