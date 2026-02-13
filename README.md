# 🚗 Minerva Motors — Cotação Inteligente

Uma aplicação Streamlit para coleta, visualização e análise de cotações de veículos (baseada em uma tabela FIPE/coleções locais). Ideal para analistas e equipes de pesquisa que precisam comparar ofertas por modelo, ano e região.

---

## ✨ Visão geral

- Interface web interativa em `Streamlit` para filtrar e visualizar ofertas coletadas.
- Banco de dados PostgreSQL para armazenar coletas, lojas, regiões, marcas, modelos e usuários.
- Ferramentas para popular o banco com dados de exemplo (`seed.py`).

## 🧭 Principais funcionalidades

- Listagem e filtros por marca, modelo e ano
- Visualizações e KPIs com `plotly` e `pandas`
- Seed de dados para desenvolvimento e testes
- Conexão via SQLAlchemy/psycopg2 com PostgreSQL

## 📁 Estrutura do repositório

- `app.py` — frontend Streamlit
- `database.py` — utilitários de conexão com PostgreSQL
- `services/cotacao_service.py` — lógica de consulta ao banco
- `seed.py` — popula o banco com dados falsos
- `docker-compose.yaml` — orquestra app + postgres
- `requirements.txt` — dependências Python

## 🚀 Requisitos

- Python 3.10+ (recomendado)
- Docker & Docker Compose (opcional, para ambiente com container)
- Porta 8501 livre (Streamlit)
- Porta 5432 livre (Postgres) — quando rodando localmente

## ⚙️ Variáveis de ambiente (opcionais)

O projeto vem com valores padrão em `database.py` e `docker-compose.yaml`. Para sobrescrever, defina:

- `DB_HOST` — host do Postgres (default: `localhost` ou `db` no Docker)
- `DB_PORT` — porta do Postgres (default: `5432`)
- `DB_USER`, `DB_PASS`, `DB_NAME` — credenciais do banco

> Dica: em produção não mantenha credenciais hardcoded — use variáveis de ambiente ou secrets.

## 🧩 Instalação (local)

1. Criar e ativar virtualenv

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
```

2. Instalar dependências

```bash
pip install -r requirements.txt
```

3. Garantir que o PostgreSQL esteja disponível (ou use Docker, abaixo).

4. Popular o banco (opcional, para desenvolvimento)

```bash
python seed.py
```

5. Executar a aplicação

```bash
streamlit run app.py
```

Acesse http://localhost:8501

## 🐳 Executando com Docker Compose

Subir serviços:

```bash
docker compose up --build
```

- Serviço `db` expõe Postgres em `5432` (default user `postgres`, senha `vini1234`, DB `minerva_motors`).
- Serviço `app` expõe Streamlit em `8501`.

Depois que o DB estiver pronto, rode `python seed.py` dentro do container da aplicação ou localmente para popular dados.

## 🔧 Como popular o banco (seed)

```bash
python seed.py
```

O script `seed.py` executará inserts nas tabelas de exemplo e reiniciará os IDs.


## ⚠️ Problemas comuns

- Conexão recusada ao Postgres: verifique se o container está rodando (`docker ps`) ou se as credenciais/host em `database.py` estão corretos.
- Porta ocupada: altere portas no `docker-compose.yaml` ou pare o processo que está usando a porta.

## ✍️ Contribuição

Sinta‑se à vontade para abrir issues e pull requests. Sugestões:

- Adicionar testes automatizados
- Extrair configuração sensível para variáveis de ambiente
- Implementar autenticação real para `usuarios`

## 📜 Licença

Este projeto está licenciado sob a licença Apache‑2.0 (ver `LICENSE`).

## 📞 Contato

Projeto: Minerva Motors — Cotação Inteligente

---

Se quiser, eu atualizo o README com badges, exemplos de queries ou instruções de CI/CD — diga o que prefere. ✅
