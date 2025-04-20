import pydantic


class UploadResponse(pydantic.BaseModel):
    message: str
