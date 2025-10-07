## API Contract Guardian

Detect and gate breaking API changes across OpenAPI and GraphQL in monorepos or multi-repo setups. Ideal for PR checks, release validation, and cross-service compatibility.

### What it does
- Scans OpenAPI 3.x (YAML/JSON) and GraphQL SDL files
- Diffs current branch against `main` (configurable)
- Flags breaking vs. non-breaking changes with severity
- Supports allowlist for intentional breakages with IDs
- Produces a machine-readable JSON report and CI-friendly pass/fail

### Why it stands out
- Multi-spec support (OpenAPI + GraphQL)
- Monorepo-aware service grouping
- Clear migration recommendations
- Zero-code setup via TOML agent config

### Inputs (arguments)
- `openapi_paths`: comma-separated globs for OpenAPI files. Example: `**/openapi.{yml,yaml,json}`
- `graphql_paths`: comma-separated globs for GraphQL SDL files. Example: `services/**/{schema.graphql,schema.gql}`
- `target_branch`: branch to compare against (default: `main`)
- `allowlist_file`: JSON/YAML of approved breaking changes
- `fail_on`: minimum severity to fail (`minor|moderate|major|critical`, default: `major`)

### Output
Structured JSON including `summary`, `findings[]`, `approved`, and `requires_changes` per the `agent.toml` `output_schema`.

### Install Qodo Command
```bash
npm install -g @qodo/command
qodo --version
```

### Run locally (this repo)
```bash
cd /Users/muhammadumairshahid/agents
qodo api_contract_guardian \
  --agent-file=agents/api-contract-guardian/agent.toml \
  --set openapi_paths="**/openapi.{yml,yaml,json}" \
  --set graphql_paths="**/*.{graphql,gql}" \
  --set target_branch=main \
  --set fail_on=major
```

### Run against another repository/workspace
Option A: clone the target repo and run from its root using a remote or local agent file.
```bash
git clone https://github.com/your-org/your-service.git
cd your-service
qodo api_contract_guardian \
  --agent-file=/Users/muhammadumairshahid/agents/agents/api-contract-guardian/agent.toml \
  --set openapi_paths="**/openapi.{yml,yaml,json}" \
  --set graphql_paths="**/*.{graphql,gql}" \
  --set target_branch=main
```

Option B: run from anywhere with a remote `--agent-file` URL (after you publish a raw link).

### Allowlist format (example)
```yaml
rules:
  - id: OAPI-REMOVE-USER-AGE
    file: services/user/openapi.yaml
    path: /users GET
    category: response.property.removal
    expires: 2026-01-01
    justification: Field removed; deprecation period communicated.
```

### CI: GitHub Actions (example)
```yaml
name: API Contract Guardian
on:
  pull_request:
    branches: [ main ]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm i -g @qodo/command
      - name: Run API Contract Guardian
        run: |
          qodo api_contract_guardian \
            --agent-file=agents/api-contract-guardian/agent.toml \
            --set openapi_paths="**/openapi.{yml,yaml,json}" \
            --set graphql_paths="**/*.{graphql,gql}" \
            --set target_branch=${{ github.base_ref || 'main' }} \
            --ci
```

### Local smoke test samples
Use the samples in `examples/samples/` to sanity-check behavior:
```bash
cd /Users/muhammadumairshahid/agents/agents/api-contract-guardian/examples/samples
git checkout -b test
# introduce a breaking change in the sample and run from repo root
cd /Users/muhammadumairshahid/agents
qodo api_contract_guardian --agent-file=agents/api-contract-guardian/agent.toml --ci
```

### Notes
- The agent verifies function/tool calls and structured output; business logic is kept declarative in the prompt to align with contest guidance.
- For monorepos, add service name hints by placing schemas under `services/<service>/`.


