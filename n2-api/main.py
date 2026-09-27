from datetime import datetime, timezone
import json
from pathlib import Path
import re
from typing import Any

from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator


BASE_DIR = Path(__file__).parent
SEED_PATH = BASE_DIR / "taches-seed.json"
STATUTS = {"a_faire", "en_cours", "terminee"}
HTML_TAG = re.compile(r"<[^>]+>")


class TacheBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    titre: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=1000)
    statut: str
    priorite: int
    etiquettes: list[str] = Field(default_factory=list)

    @field_validator("titre")
    @classmethod
    def valider_titre(cls, value: str) -> str:
        value = value.strip()
        if not value or HTML_TAG.search(value):
            raise ValueError(
                "Le titre doit être un texte non vide sans balise HTML"
            )
        return value

    @field_validator("statut")
    @classmethod
    def valider_statut(cls, value: str) -> str:
        if value not in STATUTS:
            raise ValueError("Le statut est invalide")
        return value

    @field_validator("priorite")
    @classmethod
    def valider_priorite(cls, value: int) -> int:
        if value not in {1, 2, 3}:
            raise ValueError("La priorité doit être 1, 2 ou 3")
        return value


class Tache(TacheBase):
    id: int
    creee_le: datetime


class CreationTache(TacheBase):
    id: int | None = None

    @field_validator("id")
    @classmethod
    def id_interdit(cls, value: int | None) -> None:
        if value is not None:
            raise ValueError("L'id est généré par le serveur")
        return None


class ModificationTache(BaseModel):
    model_config = ConfigDict(extra="forbid")

    titre: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    statut: str | None = None
    priorite: int | None = None
    etiquettes: list[str] | None = None
    id: int | None = None

    @field_validator("titre")
    @classmethod
    def valider_titre(cls, value: str | None) -> str | None:
        if value is not None:
            value = value.strip()
            if not value or HTML_TAG.search(value):
                raise ValueError(
                    "Le titre doit être un texte non vide sans balise HTML"
                )
        return value

    @field_validator("statut")
    @classmethod
    def valider_statut(cls, value: str | None) -> str | None:
        if value is not None and value not in STATUTS:
            raise ValueError("Le statut est invalide")
        return value

    @field_validator("priorite")
    @classmethod
    def valider_priorite(cls, value: int | None) -> int | None:
        if value is not None and value not in {1, 2, 3}:
            raise ValueError("La priorité doit être 1, 2 ou 3")
        return value

    @field_validator("id")
    @classmethod
    def id_interdit(cls, value: int | None) -> None:
        if value is not None:
            raise ValueError("L'id ne peut pas être modifié")
        return None


def charger_taches() -> dict[int, dict[str, Any]]:
    donnees = json.loads(SEED_PATH.read_text(encoding="utf-8"))
    return {tache["id"]: tache for tache in donnees}


app = FastAPI()
taches = charger_taches()
prochain_id = max(taches, default=0) + 1


@app.exception_handler(RequestValidationError)
async def validation_error_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    erreurs = []
    for erreur in exc.errors():
        erreur = dict(erreur)
        if "ctx" in erreur:
            erreur["ctx"] = {
                key: str(value) for key, value in erreur["ctx"].items()
            }
        erreurs.append(erreur)
    return JSONResponse(
        status_code=400,
        content={"detail": "Requête invalide", "erreurs": erreurs},
    )


@app.get("/taches", response_model=list[Tache])
def lister_taches() -> list[dict[str, Any]]:
    return list(taches.values())


@app.get("/taches/{tache_id}", response_model=Tache)
def obtenir_tache(tache_id: int) -> dict[str, Any]:
    if tache_id not in taches:
        raise HTTPException(status_code=404, detail="Tâche inconnue")
    return taches[tache_id]


@app.post("/taches", response_model=Tache, status_code=status.HTTP_201_CREATED)
def creer_tache(payload: CreationTache) -> dict[str, Any]:
    global prochain_id
    tache = payload.model_dump(exclude={"id"})
    tache.update(id=prochain_id, creee_le=datetime.now(timezone.utc))
    taches[prochain_id] = tache
    prochain_id += 1
    return tache


@app.patch("/taches/{tache_id}", response_model=Tache)
def modifier_tache(
    tache_id: int, payload: ModificationTache
) -> dict[str, Any]:
    if tache_id not in taches:
        raise HTTPException(status_code=404, detail="Tâche inconnue")
    modifications = payload.model_dump(exclude_unset=True, exclude={"id"})
    if not modifications:
        raise HTTPException(
            status_code=400, detail="Aucun champ modifiable fourni"
        )
    taches[tache_id].update(modifications)
    return taches[tache_id]


@app.delete("/taches/{tache_id}", status_code=status.HTTP_204_NO_CONTENT)
def supprimer_tache(tache_id: int) -> Response:
    if tache_id not in taches:
        raise HTTPException(status_code=404, detail="Tâche inconnue")
    del taches[tache_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)
