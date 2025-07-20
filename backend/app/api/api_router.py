from fastapi import APIRouter
from .endpoints import code_runner, pipelines

router = APIRouter()
router.include_router(code_runner.router, prefix="/code", tags=["code"])
router.include_router(pipelines.router, prefix="/pipelines", tags=["pipelines"])
