from pydantic import BaseModel


class ErrorResponse(BaseModel):
    detail: str

    class Config:
        json_schema_extra = {"example": {"detail": "An error occurred"}}
