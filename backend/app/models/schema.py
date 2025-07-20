from pydantic import BaseModel

class CodeInput(BaseModel):
    code: str

class CodeOutput(BaseModel):
    output: str