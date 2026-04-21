async def test_root(client):
    r = await client.get("/")
    assert r.status_code == 200
    body = r.json()
    assert body["app"] == "Cidades ESG Inteligentes"
    assert body["docs"] == "/docs"


async def test_health(client):
    r = await client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["db"] == "ok"


async def test_openapi_schema(client):
    r = await client.get("/openapi.json")
    assert r.status_code == 200
    schema = r.json()
    assert schema["info"]["title"] == "Cidades ESG Inteligentes"
    paths = schema["paths"]
    for prefix in ("/empresas", "/emissoes", "/impacto-social", "/governanca", "/metas"):
        assert prefix in paths
