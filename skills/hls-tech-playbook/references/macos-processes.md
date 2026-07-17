# macOS Process Management (durable factory lanes)

## Detached lanes die with their parent session

- **Symptom:** lanes dispatched with `nohup … & disown` still die the moment
  the coordinator's headless session ends.
- **Root cause:** `nohup`/`disown` only guard against SIGHUP. Harnesses kill
  their children by *process group / session*, and macOS ships no `setsid`
  binary to break out of it.
- **Fix:** a tiny spawn helper that calls `os.setsid()` before exec, so the
  lane owns its session and process group and reparents to launchd:

  ```python
  #!/usr/bin/env python3
  # spawn_detached.py -- <command...>
  import os, sys
  args = sys.argv[sys.argv.index("--") + 1:]
  pid = os.fork()
  if pid == 0:
      os.setsid()
      os.execvp(args[0], args)
  print(pid)
  ```

  Redirect stdout/stderr to a lane log and write the printed pid to a pid
  file; liveness is `kill -0 $(cat pidfile)`. (Observed trial: after this fix,
  lanes survived ~12 coordinator exits and 2 API-drop session deaths.)

## Missing GNU tools

- No `timeout` command (GNU coreutils) — use the dispatching harness's own
  timeout mechanism, or `perl -e 'alarm N; exec @ARGV' -- cmd…`.
- BSD `sed -i` requires an argument (`sed -i ''`); BSD `date`, `stat`,
  `xargs` all differ from GNU flags — scripts written for Linux VPS mode
  need a pass before laptop mode.

## `pgrep -f` self-match traps

- **Symptom:** a supervisor or monitor script reports a process as running
  when it isn't (e.g. `codex exec` count is never 0).
- **Root cause:** `pgrep -f "codex exec"` matches *any* process whose
  command line contains the string — including the monitor script itself,
  whose own source embeds the pattern.
- **Fix:** break the self-match with a character class (`pgrep -f
  "codex[ ]exec"`), and make "is the coordinator running" checks match the
  exact coordinator invocation — a loose `pgrep claude` also matches
  reviewer lanes and stalls supervisor relaunches while long reviews run.
