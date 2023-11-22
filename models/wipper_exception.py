from pydantic import BaseModel, Field

class WipperException(BaseModel):
    status_code: int = Field(title='Status Code', description="HTTP exception status code")
    detail: str = Field(
        ..., title="Detail", 
        description="Detailed information about the exception")
    