async def test_emissoes_flexible_schema(client):
    """Mongo schema-less: cada empresa pode enviar campos ESG distintos."""
    doc_a = {
        "empresa": "SolarWave",
        "ano": 2025,
        "emissao_CO2_ton": 150,
        "paineis_solares_instalados": 12000,
    }
    doc_b = {"empresa": "WindPower", "ano": 2025, "emissao_CO2_ton": 100, "turbinas_ativas": 45}

    r1 = await client.post("/emissoes", json=doc_a)
    r2 = await client.post("/emissoes", json=doc_b)
    assert r1.status_code == 201
    assert r2.status_code == 201

    assert r1.json()["paineis_solares_instalados"] == 12000
    assert r2.json()["turbinas_ativas"] == 45

    r = await client.get("/emissoes/stats/count")
    assert r.json()["count"] == 2
