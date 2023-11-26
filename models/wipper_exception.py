from pydantic import BaseModel, Field

class WipperException(BaseModel):
    detail: str = Field(
        ..., title='Detail', 
        description='Detailed information about the exception')