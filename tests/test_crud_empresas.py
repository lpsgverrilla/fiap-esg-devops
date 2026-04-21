async def test_empresa_crud_cycle(client):
    # CREATE
    payload = {
        "nome": "EcoLog Transportes",
        "setor": "Logistica",
        "pais": "Brasil",
        "ano_fundacao": 2008,
    }
    r = await client.post("/empresas", json=payload)
    assert r.status_code == 201
    created = r.json()
    assert created["nome"] == "EcoLog Transportes"
    doc_id = created["_id"]

    # READ (list)
    r = await client.get("/empresas")
    assert r.status_code == 200
    assert any(d["nome"] == "EcoLog Transportes" for d in r.json())

    # READ (one)
    r = await client.get(f"/empresas/{doc_id}")
    assert r.status_code == 200
    assert r.json()["pais"] == "Brasil"

    # UPDATE
    updated = {**payload, "pais": "Argentina"}
    r = await client.put(f"/empresas/{doc_id}", json=updated)
    assert r.status_code == 200
    assert r.json()["pais"] == "Argentina"

    # COUNT
    r = await client.get("/empresas/stats/count")
    assert r.status_code == 200
    assert r.json()["count"] == 1

    # DELETE
    r = await client.delete(f"/empresas/{doc_id}")
    assert r.status_code == 204

    # NOT FOUND
    r = await client.get(f"/empresas/{doc_id}")
    assert r.status_code == 404


async def test_empresa_invalid_id(client):
    r = await client.get("/empresas/not-a-valid-oid")
    assert r.status_code == 400


async def test_empresa_validation(client):
    r = await client.post("/empresas", json={"nome": "X"})
    assert r.status_code == 422
