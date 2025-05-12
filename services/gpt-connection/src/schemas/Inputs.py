from pydantic import validator

from src.core.utils import remove_unicode_chars, replace_multiple_spaces_dots
from src.schemas.GlobalBaseModel import GlobalBaseModel

class Chat(GlobalBaseModel):
    userInput: str
    
    @validator("userInput")
    def contentMustExist(cls, v):
        v = remove_unicode_chars(v)
        v = replace_multiple_spaces_dots(v)
        if v == "":
            raise ValueError("Field UserInput cannot be empty")
        return v
    
    class Config:
        json_schema_extra = {"example":{"userInput":"What is a quasar?"}}
