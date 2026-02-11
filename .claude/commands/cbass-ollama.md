---
name: cbass-ollama
description: |
  Audit and sync Apple Silicon Ollama config with CBass stack settings

  Usage: /cbass-ollama [mode]

  Examples:
  /cbass-ollama
  /cbass-ollama "sync"
  /cbass-ollama "audit"

  Modes:
  - (default) Compare launchd plist env vars against docker-compose x-ollama anchor
  - sync: Write missing env vars to plist, restart Ollama service
  - audit: Run memory math from ollama-optimize, present model context optimization

  Best for: Ensuring system Ollama on Apple Silicon matches CBass container config
argument-hint: "[sync|audit]"
user-invocable: true
allowed-tools:
  - Bash(*)
  - Read
  - Edit
  - Write
  - WebFetch
  - Task
---

# CBass Ollama Configuration Manager

**Mode**: $ARGUMENTS

## Step 1: Detect Environment

Run these in parallel:

```bash
# Check if Apple Silicon
sysctl -n machdep.cpu.brand_string
uname -m
```

```bash
# Check if system Ollama is running (Homebrew)
brew services list 2>/dev/null | grep ollama
curl -sf http://localhost:11434/api/version
```

```bash
# Check if Docker Ollama is running
docker ps --filter name=ollama --format '{{.Names}} {{.Status}}' 2>/dev/null
```

**Decision tree:**
- If `uname -m` is NOT `arm64` → Report "This command is for Apple Silicon Macs. Use `--profile gpu-nvidia` or `--profile cpu` instead." and stop.
- If system Ollama is running on :11434 → Continue with **system Ollama** path.
- If Docker Ollama container is running → Report "Docker Ollama detected. On Apple Silicon, system Ollama (via Homebrew) gives better performance because it can use Metal GPU directly. Docker on Mac cannot access the GPU." Suggest migration steps and stop.
- If neither is running → Report "Ollama is not running. Install with: `brew install ollama && brew services start ollama`"

## Step 2: Read Config Sources

Read both config sources in parallel:

1. **Launchd plist** (system Ollama actual config):
   ```
   Read: ~/Library/LaunchAgents/homebrew.mxcl.ollama.plist
   ```
   Extract all `<key>` / `<string>` pairs from the `EnvironmentVariables` dict.

2. **Docker Compose anchor** (CBass reference config):
   ```
   Read: docker-compose.yml
   ```
   Extract the `x-ollama` anchor's `environment:` list.

3. **Docker Compose override** (Open WebUI connection):
   ```
   Read: docker-compose.override.private.yml
   ```
   Check that `OLLAMA_BASE_URL=http://host.docker.internal:11434` is set for the `open-webui` service.

## Step 3: Compare and Report

Build a side-by-side comparison table:

```
| Env Variable              | docker-compose.yml | launchd plist | Status |
|---------------------------|--------------------|---------------|--------|
| OLLAMA_FLASH_ATTENTION    | 1                  | ?             | ...    |
| OLLAMA_KV_CACHE_TYPE      | q8_0               | ?             | ...    |
| OLLAMA_CONTEXT_LENGTH     | 8192               | ?             | ...    |
| OLLAMA_MAX_LOADED_MODELS  | 2                  | ?             | ...    |
| OLLAMA_MODELS             | (volume mount)     | ?             | ...    |
```

Status values:
- "Matched" — both sources have the same value
- "Missing from plist" — compose has it, plist doesn't
- "Plist only" — plist has it, compose doesn't (informational, not an error)
- "Mismatch" — both have it but values differ

Also check:
- **OLLAMA_BASE_URL**: Is `http://host.docker.internal:11434` set in the override for Open WebUI?
- **Default models installed**: Run `ollama list` and check for `qwen2.5:7b-instruct-q4_K_M` and `nomic-embed-text`

Report the table, then:
- If all statuses are "Matched" → "Configuration is in sync."
- If any are "Missing" or "Mismatch" → List what needs fixing.

## Step 4: Mode-Specific Actions

### Default mode (no argument or empty)

Just show the comparison table and model check from Step 3. No changes made.

### Sync mode (`$ARGUMENTS` contains "sync")

For each "Missing from plist" or "Mismatch" entry:

1. Show what will be added/changed in the plist
2. Edit the plist file to add/update the EnvironmentVariables
3. Validate the plist:
   ```bash
   plutil -lint ~/Library/LaunchAgents/homebrew.mxcl.ollama.plist
   ```
4. Restart Ollama:
   ```bash
   brew services restart ollama
   ```
5. Wait 3 seconds, then verify:
   ```bash
   curl -sf http://localhost:11434/api/version
   ```
6. Report what was changed and confirm service is healthy.

### Audit mode (`$ARGUMENTS` contains "audit")

This mode runs the ollama-optimize memory analysis. Invoke the global `/ollama-optimize` command with no arguments (audit mode) to get the full model analysis.

After the audit completes, add CBass-specific recommendations:
- If `OLLAMA_CONTEXT_LENGTH` in the plist differs from the optimal calculated context for the primary model, flag it.
- If `OLLAMA_MAX_LOADED_MODELS` could be higher based on available memory, suggest it.
- Recommend any missing default CBass models (`qwen2.5:7b-instruct-q4_K_M`, `nomic-embed-text`).

## Step 5: Summary

Present a final status block:

```
CBass Ollama Status
-------------------
Platform:       Apple Silicon (M4 Pro, 24GB)
Ollama:         System (Homebrew) on :11434
Profile:        --profile none
Config sync:    [In sync | N gaps found]
Models:         [N installed, M missing defaults]
Open WebUI:     [Connected via host.docker.internal | Not configured]
```

If any issues remain, provide exact fix commands.
