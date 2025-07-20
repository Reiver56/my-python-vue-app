from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import os
from typing import List, Dict, Any

router = APIRouter()

# Ogni nodo rappresenta un blocco di codice e connessioni ai successivi
class Node(BaseModel):
    id: str
    code: str
    next: List[str]  # ID dei nodi successivi

class Pipeline(BaseModel):
    nodes: List[Node]

PIPELINE_PATH = "tmp/pipeline.json"

@router.post("/pipeline/save")
async def save_pipeline(pipeline: Pipeline):
    try:
        with open(PIPELINE_PATH, "w") as f:
            json.dump(pipeline.dict(), f, indent=2)
        return {"message": "Pipeline salvata su file"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore nel salvataggio: {str(e)}")

@router.post("/pipeline/run")
def run_pipeline(_: Any = None):
    if not os.path.exists(PIPELINE_PATH):
        raise HTTPException(status_code=404, detail="Pipeline non trovata.")

    try:
        with open(PIPELINE_PATH, "r") as f:
            data = json.load(f)
            pipeline = Pipeline(**data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore nel caricamento: {str(e)}")

    executed = {}
    results = {}
    node_map = {node.id: node for node in pipeline.nodes}

    def execute_node(node_id):
        if node_id in executed:
            return
        node = node_map.get(node_id)
        if not node:
            raise HTTPException(status_code=400, detail=f"Nodo {node_id} non trovato.")
        try:
            local_env = {}
            exec(node.code, {}, local_env)
            results[node_id] = local_env
            executed[node_id] = True
            for next_id in node.next:
                execute_node(next_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Errore nel nodo {node_id}: {str(e)}")

    for node in pipeline.nodes:
        if all(node.id not in other.next for other in pipeline.nodes):
            execute_node(node.id)

    return {"executed": list(executed.keys()), "results": results}

class NewNode(BaseModel):
    id: str
    code: str
    position: Dict[str, float]  # per esempio {"x": 100, "y": 200}

@router.post("/pipeline/add_node")
async def add_node(node: NewNode):
    if "latest" not in pipeline_storage:
        pipeline_storage["latest"] = Pipeline(nodes=[])
    
    pipeline = pipeline_storage["latest"]
    
    if any(n.id == node.id for n in pipeline.nodes):
        raise HTTPException(status_code=400, detail="Nodo con ID già esistente.")

    pipeline.nodes.append(Node(id=node.id, code=node.code, next=[]))
    return {"message": f"Nodo {node.id} aggiunto con successo"}

class NewEdge(BaseModel):
    source: str
    target: str

@router.post("/pipeline/add_edge")
async def add_edge(edge: NewEdge):
    if "latest" not in pipeline_storage:
        raise HTTPException(status_code=400, detail="Nessuna pipeline trovata.")

    pipeline = pipeline_storage["latest"]
    node = next((n for n in pipeline.nodes if n.id == edge.source), None)
    if node is None:
        raise HTTPException(status_code=400, detail=f"Nodo sorgente {edge.source} non trovato.")

    if edge.target not in node.next:
        node.next.append(edge.target)

    return {"message": f"Arco da {edge.source} a {edge.target} aggiunto con successo"}