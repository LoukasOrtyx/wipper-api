from typing import List

from pydantic import BaseModel, Field

class RecognitionResponse(BaseModel):
    indexes: List[int] = Field(
        ..., title='Wipper Image Indexes', 
        description='The index of the images marked for deletion.')