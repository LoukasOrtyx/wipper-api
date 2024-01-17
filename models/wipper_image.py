from typing import List
from pydantic import BaseModel, Field

class WipperImage(BaseModel):
    data: str = Field(
        ..., title='Image Data', 
        description='Base64 encoded image string of the image.')
    fname: str = Field(
        ..., title='File Name', 
        description='The complete path of the image in the client gallery.')