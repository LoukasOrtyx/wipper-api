from typing import List
from pydantic import BaseModel, Field

class WipperResponse(BaseModel):
    inpainted_batch: List[str] = Field(
        ..., title="Inpainted Batch", 
        description="Base64 encoded image string batch whose target person was removed using Inpainting techniques.")