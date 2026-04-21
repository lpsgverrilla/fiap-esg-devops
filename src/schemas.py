"""Pydantic schemas for the 5 ESG collections.

Intentionally permissive: MongoDB's schema-less nature is one of the design pillars
from the original academic project, so we accept extra fields via `model_config`.
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ESGBase(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)


class EmpresaIn(ESGBase):
    nome: str
    setor: str
    pais: str
    ano_fundacao: int


class EmissaoIn(ESGBase):
    empresa: str
    ano: int
    emissao_CO2_ton: float


class ImpactoSocialIn(ESGBase):
    empresa: str
    ano: int
    funcionarios_total: int


class GovernancaIn(ESGBase):
    empresa: str
    ano: int


class MetaSustentabilidadeIn(ESGBase):
    empresa: str
    meta: str
    prazo_ate: int
    status: str


class DocOut(ESGBase):
    id: str = Field(alias="_id")


def serialize(doc: dict[str, Any]) -> dict[str, Any]:
    if doc is None:
        return doc
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc
