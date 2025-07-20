import json
import os
from fastapi import APIRouter, HTTPException, Path, Body
from pydantic import BaseModel, Extra
from typing import List, Dict, Any, Optional

router = APIRouter()

# Path di storage file
PIPELINE_PATH = "/tmp"
NODE_FOLDER = "../tmp/nodes"
class Node(BaseModel):
    id: str
    code: str
    next: List[str]
    position: Dict[str, float] = {}  # opzionale

    class Config:
        extra = Extra.ignore  # ignora campi extra

class Pipeline(BaseModel):
    nodes: List[Node]

@router.post("/pipeline/{node_id}/savenode")
async def save_node(
    node_id: str = Path(..., description="ID del nodo da salvare"),
    code: str = Body(
        ..., 
        media_type="application/json",
        description="Codice Python del nodo come stringa"
    )
):
    try:
        os.makedirs(NODE_FOLDER, exist_ok=True)
        path = os.path.join(NODE_FOLDER, f"node_{node_id}.py")
        with open(path, "w") as f:
            f.write(code)
        return {"message": f"Nodo {node_id} salvato in {path}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/pipeline/save")
async def save_pipeline(pipeline: Pipeline):
    # Scrive su file JSON
    try:
        with open(PIPELINE_PATH, "w") as f:
            json.dump(pipeline.dict(), f, indent=2)
        return {"message": "Pipeline salvata"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore salvataggio: {e}")

@router.post("/pipeline/run")
async def run_pipeline(pipeline: Pipeline = None):
    # Se chiamato senza body, carica da file
    if pipeline is None:
        if not os.path.exists(PIPELINE_PATH):
            raise HTTPException(status_code=404, detail="Pipeline non trovata.")
        with open(PIPELINE_PATH) as f:
            data = json.load(f)
        pipeline = Pipeline(**data)

    executed = {}
    results = {}
    node_map = {node.id: node for node in pipeline.nodes}

    def execute_node(node_id: str):
        if node_id in executed:
            return
        node = node_map.get(node_id)
        if not node:
            raise HTTPException(status_code=400, detail=f"Nodo {node_id} non trovato.")
        try:
            local_env: Dict[str, Any] = {}
            exec(node.code, {}, local_env)
            results[node_id] = local_env
            executed[node_id] = True
            for nxt in node.next:
                execute_node(nxt)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Errore nodo {node_id}: {e}")

    # Entry points
    for n in pipeline.nodes:
        if all(n.id not in other.next for other in pipeline.nodes):
            execute_node(n.id)

    return {"executed": list(executed.keys()), "results": results}