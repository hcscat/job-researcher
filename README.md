# Job Researcher

Job Researcher is a local-first platform for collecting, normalizing, enriching, and reviewing job postings. It combines a FastAPI backend, SQLite storage, raw snapshot archiving, scheduled collection, and a browser dashboard for reviewing postings and collection runs.

The internal Python package is still named `job_harvest` for compatibility with the original collector code. The product-facing command and documentation use `job-researcher`.

## Features

- Web dashboard for collection status, stored postings, run history, and raw snapshots.
- Configurable collection targets for Saramin, JobKorea, LinkedIn, Wanted, Jumpit, Remember, JobPlanet, RocketPunch, and Blind.
- Broad IT/developer scan mode or explicit query mode.
- Collection filters for role, skill, company, location, experience, education, employment type, industry, salary, workplace type, and other job-site signals.
- Raw listing/detail response storage for audit and reprocessing.
- Normalized posting browser with profile-fit sorting, detail drawer, raw payload view, and external apply links.
- Preprocessing settings for deduplication strategy, minimum text length, whitespace normalization, and language hints.
- AI enrichment with heuristic fallback, OpenAI API-key mode, or an external command mode for locally authenticated OAuth CLI tools.
- JSON-based settings blocks for Harness engineering, MCP servers, skills, messaging, and AI runtime configuration.
- Optional email draft links for contacting recruiters or preparing application messages.
- Local CLI entry points for setup, serving, collection, query preview, and tests.

## Requirements

- Python 3.11 or newer
- Optional Node.js 18 or newer for the npm wrapper
- Optional Playwright browser support for protected job sites

## Quick Start

```bash
git clone https://github.com/hcscat/job-researcher.git
cd job-researcher
python3 -m venv .venv
.venv/bin/python -m job_researcher setup
.venv/bin/python -m job_researcher init-config
.venv/bin/python -m job_researcher serve --host 127.0.0.1 --port 8000
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000).

On Windows PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m job_researcher setup
.\.venv\Scripts\python.exe -m job_researcher init-config
.\.venv\Scripts\python.exe -m job_researcher serve --host 127.0.0.1 --port 8000
```

## npm Wrapper

The npm package does not replace Python. It provides a convenient command wrapper around the Python app.

```bash
npm install
npm run setup
npm run init-config
npm run serve
```

After publishing the package, you can also run:

```bash
npx @hcscat/job-researcher --help
```

Set `JOB_RESEARCHER_PYTHON=/absolute/path/to/python` if the wrapper should use a specific interpreter.

## CLI Commands

```bash
python -m job_researcher setup
python -m job_researcher init-config
python -m job_researcher serve --host 127.0.0.1 --port 8000
python -m job_researcher serve --host 127.0.0.1 --port 8000 --reload
python -m job_researcher --config ./config.yaml run
python -m job_researcher --config ./config.yaml schedule
python -m job_researcher --config ./config.yaml show-queries
python -m job_researcher test
```

The legacy command still works:

```bash
python -m job_harvest serve
```

## Configuration

Start from `config.example.yaml`:

```bash
python -m job_researcher init-config
```

The web settings page stores runtime settings in the local database. Settings include:

- collection sites, search mode, query seeds, fetch limits, browser options
- filter criteria and strict match groups
- schedule mode, fixed run times, interval, and timezone
- preprocessing options
- AI provider, model, auth mode, API-key environment variable, OAuth profile, external command, and extra JSON config
- Harness, MCP, skills, messaging, and contact settings as JSON objects

## AI Enrichment

The default enrichment mode is `heuristic`, which requires no external model.

For OpenAI-compatible API-key usage:

1. Set an environment variable such as `OPENAI_API_KEY`.
2. In settings, enable AI enrichment.
3. Set provider to `openai`.
4. Set the model name.
5. Set AI auth mode to `api_key_env` and the API key environment variable name.

For OAuth-authenticated local CLI usage:

1. Authenticate the CLI outside Job Researcher.
2. Create a wrapper command that reads the posting prompt from stdin.
3. Print strict JSON with these keys: `is_it_job`, `summary`, `relevance_reason`, `job_family`, `seniority`, `work_model`, `tech_stack`, `requirements`, `responsibilities`, `benefits`.
4. In settings, set provider to `external_command` and paste the command into `AI external command`.

This keeps account credentials outside the repository and avoids hardcoding provider-specific logic.

## Data Paths

Default local data is stored under `data/`.

- `data/app.db`: SQLite database
- `data/raw/...`: gzipped raw listing and detail bodies
- `data/exports/runs/...`: per-run JSON, CSV, Markdown, and optional HTML exports

These paths are ignored by Git.

## Environment Variables

- `JOB_RESEARCHER_DATABASE_URL`: override the database URL.
- `JOB_RESEARCHER_DATA_DIR`: override the data directory.
- `OPENAI_API_KEY`: optional, only when OpenAI enrichment is enabled.
- `JOB_HARVEST_BROWSER_EXECUTABLE`: optional browser executable override for Playwright collectors.
- `JOB_RESEARCHER_PYTHON`: optional Python path used by the npm wrapper.

Use `.env.example` as a reference. Do not commit real credentials or tokens.

## Main API

- `GET /api/settings`
- `PUT /api/settings`
- `POST /api/settings/interpret`
- `POST /api/collect`
- `GET /api/jobs`
- `GET /api/jobs/{job_id}`
- `GET /api/runs`
- `GET /api/runs/{run_id}`
- `GET /api/raw/{category}/{sha256_hex}`
- `GET /api/scheduler`
- `GET /health`

## Development

```bash
python3 -m venv .venv
.venv/bin/python -m job_researcher setup
.venv/bin/python -m job_researcher test
.venv/bin/python -m job_researcher serve --reload
```

The Homebrew formula under `packaging/homebrew/` is a release template. Replace the tarball hash and generate Python resources after publishing a tagged release.
