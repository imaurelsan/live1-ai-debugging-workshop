import json
from pathlib import Path

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)
INVALIDES = json.loads(
    (Path(__file__).parent / "payloads-invalides.json").read_text(
        encoding="utf-8"
    )
)


def test_get_taches_retourne_le_seed():
    response = client.get("/taches")
    assert response.status_code == 200
    assert len(response.json()) == 16


def test_get_tache_retourne_404_si_inconnue():
    assert client.get("/taches/9999").status_code == 404


def test_post_cree_une_tache_et_genere_id_et_date():
    response = client.post(
        "/taches",
        json={"titre": "Nouvelle tâche", "statut": "a_faire", "priorite": 2},
    )
    assert response.status_code == 201
    assert response.json()["id"] > 16
    assert response.json()["description"] == ""
    assert "creee_le" in response.json()


def test_patch_modifie_une_tache():
    response = client.patch("/taches/1", json={"statut": "terminee"})
    assert response.status_code == 200
    assert response.json()["statut"] == "terminee"


def test_delete_supprime_une_tache():
    response = client.delete("/taches/16")
    assert response.status_code == 204
    assert client.get("/taches/16").status_code == 404


def test_payloads_invalides_sont_rejetes():
    for payload in INVALIDES:
        body = {
            key: value for key, value in payload.items() if key != "_pourquoi"
        }
        response = client.post("/taches", json=body)
        assert response.status_code == 400, payload["_pourquoi"]
        assert "traceback" not in response.text.lower()
