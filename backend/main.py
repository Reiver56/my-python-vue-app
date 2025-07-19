from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import io
import traceback

app = FastAPI()

# Permette chiamate da frontend (localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
# ⚠️ Parole vietate per sicurezza
FORBIDDEN_KEYWORDS = [
    "import os", "import sys", "import subprocess", "import shutil",
    "open(", "__import__", "eval(", "exec(", "compile(", "globals(", "locals("
]

class CodeRequest(BaseModel):
    code: str

@app.post("/run")
def run_code(req: CodeRequest):
    # 🔒 Verifica sicurezza
    lowered = req.code.lower()
    if any(forbidden in lowered for forbidden in FORBIDDEN_KEYWORDS):
        return {"output": "Errore: comando non consentito per motivi di sicurezza."}
    # 🧪 Test di sicurezza
    if "import" in req.code or "exec" in req.code:
        return {"output": "Errore: importazioni o esecuzioni dinamiche non sono consentite."}
    # 🧠 Esecuzione codice
    if not req.code.strip():
        return {"output": "Nessun codice da eseguire."}
    # 🧠 Esecuzione sicura
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    try:
        exec(req.code, {})
        result = redirected_output.getvalue()
    except Exception:
        result = "Errore:\n" + traceback.format_exc()
    finally:
        sys.stdout = old_stdout

    return {"output": result}
