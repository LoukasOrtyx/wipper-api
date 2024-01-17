from typing import List

from pydantic import BaseModel, Field

class RecognitionResponse(BaseModel):
    fnames: List[str] = Field(
        ..., title='Wipper Image file names', 
        description='The file names of the images marked for deletion.')