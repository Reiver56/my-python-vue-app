from fastapi import FastAPI
from app.api.endpoints.code_runner import router
from app.api.endpoints.pipelines import router as pipelines_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title = "My Cloud Backend")
app.include_router(router)
app.include_router(pipelines_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # oppure ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
