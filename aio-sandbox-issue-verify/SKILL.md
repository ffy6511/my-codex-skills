---
name: aio-sandbox-issue-verify
description: >
  End-to-end workflow for investigating, fixing, and verifying AIO Sandbox issues.
  Trigger when the user reports a sandbox bug, wants to reproduce an issue on a remote/local sandbox,
  or says things like "验证这个问题", "复现一下", "sandbox 有个 bug", "构建验证一下",
  "跑一下 e2e", or asks to investigate container/shell/env issues in the sandbox.
  Also trigger when the user provides a PSM name (like bytedance.aiosandbox.xxx) and describes a problem to investigate.
---

# Sandbox Issue Verify

A structured workflow for reproducing, investigating, fixing, and verifying AIO Sandbox issues with full test coverage.

## Why this workflow matters

Sandbox issues often involve subtle interactions between Dockerfile build-time config, run.sh runtime setup, shell environments (login/interactive/non-interactive), and multiple users (tiger/root). A casual fix can easily break one context while fixing another. This workflow ensures changes are validated across all execution contexts before shipping.

## Phase 1: Reproduce on Remote Sandbox

Create a sandbox on aipaas to match the production environment. This avoids "works on my machine" issues from local-only testing.

```bash
# 1. Login (one-time)
aio login --region i18n

# 2. Set context — ask user for their PSM name
aio use <PSM_NAME> --region I18N

# Verify current context
aio use

# 3. Create a sandbox session
aio sandbox create

# List existing sessions
aio sandbox ls
```

Once the sandbox is ready, reproduce the reported issue:

```bash
# Execute commands in sandbox via aio CLI
aio shell "<command>"

# Upload files if needed
aio file upload ./local-file.txt
aio file upload ./local-file.txt --to /workspace/file.txt

# Read files in sandbox
aio file read /tmp/some-file
aio file list /tmp

# Or via direct curl if CLI has issues
curl -s -X POST "<SANDBOX_URL>/v1/bash/exec" \
  -H 'Content-Type: application/json' \
  -H "X-Jwt-Token: $TOKEN" \
  -d '{"command": "<command>"}' | jq .
```

Capture exact error messages, exit codes, and environment state. Compare behavior across different users (tiger vs root) and shell contexts.

## Phase 2: Root Cause Analysis

Investigate systematically — don't jump to solutions. Check these layers in order:

1. **Container environment** — `printenv`, `echo $PATH`, check what's set vs what's expected
2. **Shell config files** — `~/.bashrc`, `~/.profile`, `/etc/profile.d/`, `/etc/bash.bashrc`
3. **Dockerfile** — ENV statements, RUN commands that set up the environment
4. **run.sh** — Runtime exports that the python-server inherits
5. **Python server** — `build_sandbox_env()` in `python-server/src/app/core/version.py`
6. **Shell service** — How commands are spawned in `python-server/src/app/services/bash.py`

Map out which execution contexts are affected:

| Context                       | How env is set                         | Config source     |
| ----------------------------- | -------------------------------------- | ----------------- |
| Shell API (`/v1/bash/exec`)   | `build_sandbox_env()` → `os.environ`   | run.sh exports    |
| Login shell (`bash -l`)       | `/etc/profile` → `/etc/profile.d/*.sh` | profile.d scripts |
| Interactive shell (`bash -i`) | `/etc/bash.bashrc`                     | system bashrc     |
| JupyterLab terminal           | User's `~/.bashrc`                     | per-user bashrc   |
| code-server terminal          | User's `~/.bashrc`                     | per-user bashrc   |

## Phase 3: Discuss Fix Approach

Before implementing, evaluate the proposed fix against three criteria. Present this analysis to the user and ask for confirmation.

### Compatibility

- Does it work for ALL users (tiger, root, future users)?
- Does it work in ALL shell contexts (login, interactive, non-interactive, API)?
- Does it break any existing behavior?
- Does `sudo` or `su` clear the env vars? If so, how do we handle it?

### Usability

- Is the behavior intuitive? (e.g., `fnm use 20` should just work)
- Are global packages findable without extra steps?
- Do version switches persist across new shells?

### Performance

- Does it add latency to shell startup? (avoid `eval "$(cmd)"` patterns)
- Is the cost one-time or per-shell? (prefer one-time init with subsequent skip)
- Benchmark: `time bash -lc "exit"` before and after

Present the tradeoffs explicitly:

```
Approach A: [description] — [pros] / [cons]
Approach B: [description] — [pros] / [cons]
Recommended: [which and why]
```

Wait for user confirmation before proceeding.

## Phase 4: Implement Fix

Apply the fix. Common patterns in aio-sandbox:

- **System-wide env for all users**: `/etc/profile.d/*.sh` + source from `/etc/bash.bashrc`
- **Per-user writable state**: Use `$HOME/...` paths so each user has their own
- **Build-time vs runtime**: Operations that can be in Dockerfile should NOT be in run.sh
- **Consistent env**: run.sh should `source /etc/profile.d/*.sh` so python-server inherits the same env as interactive shells

After code changes, also fix any related CLI bugs discovered during reproduction (e.g., error handling in aio-cli).

## Phase 5: Build and Verify Locally

```bash
# Build the image
make build

# Restart container
docker compose down && docker compose up -d

# Wait for ready
for i in $(seq 1 20); do
  STATUS=$(curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/v1/bash/exec \
    -X POST -H 'Content-Type: application/json' -d '{"command":"echo ok"}' 2>/dev/null)
  [ "$STATUS" = "200" ] && echo "Ready" && break
  sleep 2
done
```

Manually verify the original issue is fixed. Use a shell script to batch all verification commands:

```bash
#!/bin/bash
API="http://localhost:8080"
run() {
  local desc="$1"; local cmd="$2"
  echo "=== $desc ==="
  curl -s -X POST "$API/v1/bash/exec" -H 'Content-Type: application/json' \
    -d "$cmd" | jq '{stdout: .data.stdout, stderr: .data.stderr, exit_code: .data.exit_code}'
  echo ""
}
# Add test cases here...
```

## Phase 6: Write E2E Tests

Create tests in `e2e/tests/` following existing patterns. Key principles:

- **Use `_exec_ok` helper** — assert exit_code == 0 and return stdout in one call
- **Test ALL contexts** — login shell (`bash -l`), interactive (`bash -i`), and shell API (direct)
- **Test ALL users** — `sudo -u tiger bash -lc "..."` and `sudo -u root bash -lc "..."`
- **Use `printenv`** not `echo $VAR` — avoids outer shell variable expansion
- **Reset state** — don't assume initial state; explicitly set it (e.g., `fnm use 22` before testing)
- **Test persistence** — verify state survives across separate shell invocations
- **Test full workflows** — install → use → switch → verify → switch back → verify again

```python
class _ShellHelper:
    @pytest.fixture
    def base_url(self) -> str:
        return os.getenv("TEST_BASE_URL", "http://127.0.0.1:8080")

    async def _exec(self, client, base_url, command, timeout=60):
        resp = await client.post(
            f"{base_url}/v1/bash/exec",
            json={"command": command}, timeout=timeout,
        )
        assert resp.status_code == 200
        return resp.json()["data"]

    async def _exec_ok(self, client, base_url, command, timeout=60):
        data = await self._exec(client, base_url, command, timeout)
        assert data["exit_code"] == 0, f"Failed: {command}\nstderr: {data.get('stderr')}"
        return (data["stdout"] or "").strip()
```

Group tests by concern (environment setup, version switching, package management, etc.).

## Phase 7: Run Tests and Report

```bash
cd e2e && uv run pytest tests/test_<name>.py -xvs
```

Output a structured report with:

1. **Summary table** — test name, status (PASSED/FAILED), what it verifies
2. **File change list** — every modified/created file and what changed
3. **Coverage matrix** — which contexts × which users are tested

Format:

```
## Test Report
- File: `e2e/tests/test_xxx.py`
- Results: X passed, Y failed (Z.Zs)

| # | Test | Verifies | Status |
|---|------|----------|--------|
| 1 | test_name | description | PASSED/FAILED |

## Changes
| File | Change |
|------|--------|
| path | description |
```

If any test fails, investigate and fix before reporting. The report should show a clean pass.

## Cleanup

After all tests pass:

- Clean up remote sandbox: `aio sandbox ls` then `aio sandbox rm <name>`
- Offer to commit changes
- Suggest any follow-up items discovered during investigation
