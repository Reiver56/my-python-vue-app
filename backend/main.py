from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import io
import sys

app = FastAPI()

# Permette chiamate da frontend (localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class CodeRequest(BaseModel):
    code: str

@app.post("/run")
def run_code(req: CodeRequest):
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    try:
        exec(req.code, {})
        result = redirected_output.getvalue()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        sys.stdout = old_stdout
    return {"output": result}
