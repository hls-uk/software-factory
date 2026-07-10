# JVM / Gradle

## Forked-test-heap OOM (the 512m cliff)

- **Symptom:** the full test suite dies with
  `Could not complete execution for Gradle Test Executor N > Java heap space`
  or app code under test returns 500s wrapping
  `java.lang.OutOfMemoryError: Java heap space` — sometimes only after new
  test classes were added, sometimes "only under parallel load".
- **Root cause:** Gradle forks test JVMs at **512m max heap by default**;
  almost no build file sets `Test.maxHeapSize`. A single-fork suite retains
  heap across all classes and one day outgrows 512m — then it OOMs even run
  *alone*. Concurrency doesn't cause it; it makes it fire sooner. (Chivo
  trial: two concurrent gates both died; the serial re-run died too; root
  cause was the default.)
- **Fix:** set `test { maxHeapSize = "2g" }` (or `org.gradle.jvmargs` for
  the fork line) in the tracked build. Until that lands, the coordinator can
  fix its own gate runs non-invasively with an init script:
  `./gradlew --init-script gate-heap.gradle …` where the script sets
  `tasks.withType(Test) { maxHeapSize = "2g" }`.
- **Coordinator notes:** with per-fork heap known you can do N-concurrent-
  gates capacity math (fork heap + app under test + containers ≈ 5–6 GB per
  Quarkus-style gate); until then serialize the full-suite gate. An OOM'd
  gate after green story tests is a bounce, not a story failure. File the
  permanent build change as a sweep issue.

## Build caches live outside sandboxed workspaces

- **Symptom:** first gradle command in a sandboxed lane fails with
  `…/.gradle/wrapper/dists/….zip.lck (Operation not permitted)` (or Maven
  equivalents under `~/.m2`).
- **Root cause:** workspace-write sandboxes allow the repo dir; the wrapper
  distribution, dependency caches, and daemon registry live in `~/.gradle` /
  `~/.m2`.
- **Fix:** grant `~/.gradle` and `~/.m2` as extra writable roots in the
  lane's dispatch flags. Probe with `./gradlew --version` through the *same*
  sandboxed lane before the first story.

## Misc

- `--no-daemon` gives CI-parity and avoids daemon crosstalk between
  concurrent worktree builds, at ~30–60s per invocation; fine for gates,
  wasteful for a lane's inner loop.
- Two parallel first-runs both downloading dependencies contend harmlessly
  but slowly; warm the cache once (baseline verify) before wave-1 dispatch.
