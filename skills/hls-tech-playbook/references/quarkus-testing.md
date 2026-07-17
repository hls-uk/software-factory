# Quarkus Testing

## Fixed test port collides across concurrent suites

- **Symptom:** two worktrees running `@QuarkusTest` suites concurrently and
  one fails with port-bind errors, or auth tests fail oddly because a token
  validator fetched keys from the *other* suite's instance.
- **Root cause:** `quarkus.http.test-port` defaults to a fixed 8081 for
  every suite on the host; anything configured against that port (JWKS URLs,
  callback endpoints, wiremock base URLs) follows it.
- **Fix:** lease a port per lane and export it into the lane's environment —
  `QUARKUS_HTTP_TEST_PORT=<leased>` — **and move every coupled URL with it**
  (e.g. the JWKS/issuer URL env var must point at the same leased port).
  Record the lease in `.env.story`; verification commands must read ports
  from env, never hardcode. (Observed trial leases: 18091–18094; zero
  collisions across three concurrent instances.)
- **Coordinator notes:** grep the repo's `%test` config for the coupled
  URLs before assuming the port var alone is enough — the failure mode when
  you miss one is a *passing-but-wrong* cross-suite fetch, not a clean bind
  error.

## Dev services / Testcontainers memory footprint

- Each concurrent suite boots the app JVM **plus** its containers (Postgres
  etc.) — budget ≈ 5–6 GB per gate with a 2g test heap. Memory, not ports,
  is the binding constraint on how many gates run at once; see
  jvm-gradle.md for the heap default and capacity math.
- Containers need the Docker socket reachable from sandboxed lanes
  (`network_access` in the sandbox config); probe `docker ps` through the
  lane before wave 1.
- Orphaned containers from killed gates keep their memory — after killing a
  hung suite, check `docker ps` for its testcontainers and reap them.
