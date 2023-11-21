from typing import List
from pydantic import BaseModel, Field

class WipperRequest(BaseModel):
    target: str = Field(
        ..., title="Target Image", 
        description="Base64 encoded image string of the person to be wiped out.")
    batch: List[str] = Field(
        ..., title="Image Batch", 
        description="Base64 encoded image string batch to be processed based of the target image.")