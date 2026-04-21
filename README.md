# Projeto - Cidades ESGInteligentes

Plataforma de monitoramento de indicadores ESG (Environmental, Social, Governance), empacotada com pipeline de CI/CD, containerização Docker e deploy automatizado em ambientes de staging e produção.

**Integrantes:**
- João Pedro Fernandes Silva — RM561005
- Pedro Teixeira Spinola — RM560104
- Thiago C. G. Antunes — RM559359

**Ambientes ativos:**

| Ambiente  | URL                                           | Branch      |
| --------- | --------------------------------------------- | ----------- |
| Produção  | https://esg.pedrots.com.br                    | `main`      |
| Staging   | https://esg-staging.pedrots.com.br            | `develop`   |

---

## Como executar localmente com Docker

Pré-requisitos: Docker Engine 24+ e Docker Compose v2.

```bash
git clone https://github.com/lpsgverrilla/fiap-esg-devops.git
cd fiap-esg-devops
cp .env.example .env
docker compose up --build
```

A API sobe em `http://localhost:8000`. A documentação interativa (Swagger) fica em `http://localhost:8000/docs`.

A primeira subida do MongoDB executa automaticamente o script `mongo-init/01-seed.js`, populando as 5 collections com 10 documentos cada (baseado no projeto acadêmico original "Monitoramento de Emissões de Carbono").

Validação rápida:

```bash
curl -s http://localhost:8000/health
curl -s http://localhost:8000/empresas/stats/count   # -> {"count":10}
```

Derrubar e limpar dados:

```bash
docker compose down -v
```

### Rodar testes

```bash
uv venv --python 3.12
. .venv/bin/activate
uv pip install -e ".[dev]"
pytest -q
ruff check .
```

---

## Pipeline CI/CD

**Ferramenta:** GitHub Actions.

Dois workflows em `.github/workflows/`:

### `ci.yml` — validação contínua

Dispara em todo push ou pull request em qualquer branch. Jobs:

1. **lint-and-test** — roda Ruff (lint + format) e a suíte Pytest (7 testes cobrindo health, OpenAPI, CRUD de empresas com cycle completo, e flexibilidade do schema em emissões).
2. **docker-build** — monta a imagem via Buildx com cache GHA, validando que o Dockerfile está íntegro antes de promover o código.

### `deploy.yml` — deploy automático

Dispara em pushes nas branches protegidas:

| Branch      | Job                 | Ambiente GHA  | Webhook VPS                             |
| ----------- | ------------------- | ------------- | --------------------------------------- |
| `develop`   | `deploy-staging`    | `staging`     | `/hooks/deploy-fiap-esg-staging`        |
| `main`      | `deploy-production` | `production`  | `/hooks/deploy-fiap-esg-production`     |

Etapas do deploy:

1. Roda a suíte de testes novamente (guard-rail).
2. Faz `POST` no webhook correspondente passando o header `X-Deploy-Token` (segredo armazenado em GitHub Environments — `STAGING_DEPLOY_TOKEN` / `PROD_DEPLOY_TOKEN`).
3. O `adnanh/webhook` no VPS valida o token e invoca o `deploy.sh` do ambiente, que executa:
   - `git pull` na branch correta
   - `docker compose build`
   - `docker compose up -d`
4. Aguarda o endpoint `/health` responder `"status":"ok"` por até 150 s antes de marcar o deploy como verde.

Fluxo recomendado de trabalho: feature branch → PR → merge em `develop` (sobe staging) → validar → PR `develop` → `main` (promove para produção).

---

## Containerização

### Dockerfile (multi-stage)

- **Stage builder:** `python:3.12-slim`, instala dependências em `/install` isolado.
- **Stage runtime:** `python:3.12-slim`, copia apenas o site-packages instalado e o código-fonte, executa como usuário não-root `app`, expõe 8000, define `HEALTHCHECK` interno via `/health`.

Racional: imagem final ~180 MB, sem toolchain de build, superfície de ataque mínima.

### docker-compose.yml

Dois serviços em rede Docker dedicada:

- `api` — FastAPI + Uvicorn, dependências externas injetadas via env.
- `mongo` — MongoDB 7, volume nomeado `mongo-data`, healthcheck via `mongosh ping`, seed automático via `/docker-entrypoint-initdb.d/`.

Variáveis de ambiente (ver `.env.example`): `APP_ENV`, `MONGO_ROOT_USER`, `MONGO_ROOT_PASSWORD`, `MONGO_DB`, `HOST_BIND`, `HOST_PORT`. O compose suporta múltiplas instâncias na mesma máquina (staging + produção no mesmo VPS) via interpolação de `${APP_ENV}` nos nomes de container/volume/network.

### Arquitetura no VPS

```
Internet ─┬─► nginx (443 TLS) ─► esg.pedrots.com.br          ─► 127.0.0.1:8007 ─► api (prod)    ─► mongo (prod)
          └─► nginx (443 TLS) ─► esg-staging.pedrots.com.br  ─► 127.0.0.1:8006 ─► api (staging) ─► mongo (staging)

                                 adnanh/webhook (127.0.0.1:9000) ─► /opt/fiap-esg/{staging,production}/deploy.sh
```

Cada ambiente tem container, volume e rede isolados — zero cross-contamination entre staging e produção.

---

## Prints do funcionamento

Ver `docs/evidence/` no repositório e a documentação PDF anexa (`docs/documentacao.pdf`).

- Pipeline GitHub Actions (build/test/deploy verdes)
- `docker ps` no VPS mostrando os 4 containers (api + mongo × 2 ambientes)
- Swagger UI em `https://esg.pedrots.com.br/docs` e `https://esg-staging.pedrots.com.br/docs`
- Endpoints `/health` e `/empresas/stats/count` respondendo em ambos os ambientes

---

## Tecnologias utilizadas

| Camada              | Ferramentas                                                   |
| ------------------- | ------------------------------------------------------------- |
| Linguagem / Runtime | Python 3.12                                                   |
| Framework Web       | FastAPI + Uvicorn                                             |
| Validação / DTOs    | Pydantic v2 + pydantic-settings                               |
| Banco de dados      | MongoDB 7 (driver assíncrono Motor)                           |
| Testes              | pytest + pytest-asyncio + httpx + mongomock-motor             |
| Qualidade           | Ruff (lint + format)                                          |
| Containerização     | Docker multi-stage + Docker Compose v2                        |
| CI/CD               | GitHub Actions + GitHub Environments                          |
| Webhook deploy      | adnanh/webhook                                                |
| Reverse proxy       | nginx + Let's Encrypt (certbot)                               |
| Hospedagem          | Hetzner Cloud CX33 (Ubuntu 24.04) + domínio pedrots.com.br    |

---

## Checklist de Entrega

| Item                                                        | OK |
| ----------------------------------------------------------- | -- |
| Projeto compactado em .ZIP com estrutura organizada         | ✅ |
| Dockerfile funcional                                        | ✅ |
| docker-compose.yml                                          | ✅ |
| Pipeline com etapas de build, teste e deploy                | ✅ |
| README.md com instruções e prints                           | ✅ |
| Documentação técnica com evidências (PDF)                   | ✅ |
| Deploy realizado nos ambientes staging e produção           | ✅ |
