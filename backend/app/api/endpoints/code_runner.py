from fastapi import APIRouter
from app.models.schema import CodeInput, CodeOutput
from app.core.executor import run_code

router = APIRouter()

@router.post("/code/run", response_model=CodeOutput)
def execute_code(payload: CodeInput):
    output = run_code(payload.code)
    return {"output": output}