# Harness CLIs (codex, claude) as factory lanes

## Model availability depends on how the CLI is authenticated

- **Symptom:** a dispatch fails instantly with
  `400 invalid_request_error: The '<model>' model is not supported when
  using Codex with a ChatGPT account` (or the vendor's equivalent).
- **Root cause:** subscription-authenticated CLIs expose different model ids
  than API keys. Observed: `gpt-5.5-codex` rejected under ChatGPT-account
  auth while plain `gpt-5.5` works.
- **Fix:** the CLI's own configured default (`~/.codex/config.toml` `model`)
  is the best first guess for what the account can run. Preflight every lane
  with a "Reply with exactly: OK" dispatch before wave 1 — a lane that can't
  answer cheaply will not deliver a story expensively.

## Silent per-token API billing (subscription bypass)

- **Symptom:** none — that's the problem. The CLI behaves identically but
  bills per-token API credits instead of the engineer's subscription.
- **Root cause:** both CLIs honor environment API keys over (or alongside)
  subscription login: `ANTHROPIC_API_KEY` for claude, `OPENAI_API_KEY` for
  codex. Headless lanes inherit the launching shell's environment, so one
  exported key in a profile flips every lane.
- **Fix / verification (run through the dispatch shell, before wave 1):**
  - `env | grep -E "^(ANTHROPIC|OPENAI)_API_KEY"` — must be empty for
    subscription-only operation.
  - `codex login status` — must say `Logged in using ChatGPT` (not API
    key); also check `preferred_auth_method` in `~/.codex/config.toml` if
    both auths exist.
  - claude: no `apiKeyHelper` in `~/.claude/settings.json` and no
    `ANTHROPIC_API_KEY`/`ANTHROPIC_AUTH_TOKEN` in env; subscription login
    lives in the OS keychain.
  - Belt-and-braces in dispatch commands:
    `env -u ANTHROPIC_API_KEY -u OPENAI_API_KEY <dispatch cmd>` unless the
    lane explicitly declares `"billing": "api"`.
- **Coordinator notes:** usage-limit cooling is never resolved by switching
  to an API key — wait for the window or shift same-tier lanes (see the
  Billing Guardrail in the orchestrate skill's parallel-dispatch reference).

## Two versions of the same CLI on one machine

- **Symptom:** a flag works interactively but a supervisor/cron launch fails
  with `error: unknown option '--effort'` — and may still exit 0.
- **Root cause:** non-login shells resolve a different PATH; an older
  install (e.g. `~/.local/bin/claude` 2.1.20) shadows the current one
  (`/opt/homebrew/bin/claude` 2.1.201) outside your interactive shell.
- **Fix:** absolute paths to harness binaries in every dispatch/launch
  command, and run preflight probes through the *same shell and launcher*
  the real dispatches will use.

## Codex sandbox flags for factory lanes (known-good set)

```
codex exec --sandbox workspace-write \
  -c approval_policy=never \
  -c sandbox_workspace_write.network_access=true \
  -c 'sandbox_workspace_write.writable_roots=["~/.gradle","~/.m2","<repo>/.git"]' \
  --model <auth-appropriate id> -c model_reasoning_effort="xhigh" "$(cat goal.txt)"
```

- `network_access=true` also opens the Docker socket (testcontainers).
- Writable roots cover build caches (jvm-gradle.md) and the git common dir
  (git-worktrees.md). Full bypass
  (`--dangerously-bypass-approvals-and-sandbox`) is the blunt fallback —
  prefer named roots so scope violations stay detectable.

## Print-mode sessions and their children

- A `claude -p` / `codex exec` session ends when its final message is
  written; harness-managed background tasks **and their child processes die
  with it**. Never dispatch lanes through the harness's background-task
  feature from a print-mode coordinator — use OS-durable spawning
  (macos-processes.md) with pid files, and let a supervisor relaunch the
  coordinator on lane completion or a heartbeat.
- Long xhigh turns can die with `API Error: Connection closed mid-response`;
  uncommitted in-session context is lost. Cheap insurance: checkpoint
  (commit ledger/log) after every decision the next run must not re-derive.
