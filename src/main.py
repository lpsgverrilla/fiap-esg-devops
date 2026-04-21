from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config import settings
from src.db.mongo import get_db
from src.routers.crud import build_router
from src.schemas import (
    EmissaoIn,
    EmpresaIn,
    GovernancaIn,
    ImpactoSocialIn,
    MetaSustentabilidadeIn,
)

COLLECTIONS = [
    ("/empresas", "empresas", "empresas", EmpresaIn),
    ("/emissoes", "emissoes", "emissoes", EmissaoIn),
    ("/impacto-social", "impacto_social", "impacto_social", ImpactoSocialIn),
    ("/governanca", "governanca", "governanca", GovernancaIn),
    ("/metas", "metas_sustentabilidade", "metas_sustentabilidade", MetaSustentabilidadeIn),
]


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield


app = FastAPI(
    title="Cidades ESG Inteligentes",
    description="Plataforma de monitoramento ESG — FIAP DevOps",
    version="0.1.0",
    lifespan=lifespan,
)


for prefix, tag, coll, schema in COLLECTIONS:
    app.include_router(build_router(prefix=prefix, tag=tag, collection_name=coll, schema_in=schema))


@app.get("/", tags=["meta"])
async def root() -> dict[str, str]:
    return {
        "app": "Cidades ESG Inteligentes",
        "env": settings.app_env,
        "docs": "/docs",
    }


@app.get("/health", tags=["meta"])
async def health() -> dict[str, str]:
    try:
        await get_db().command("ping")
        db_status = "ok"
    except Exception as e:  # noqa: BLE001
        db_status = f"error: {type(e).__name__}"
    return {"status": "ok", "env": settings.app_env, "db": db_status}
