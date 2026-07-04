---
name: hls-dev-browser
description: Verify web UIs and automate browsers with dev-browser — sandboxed Playwright scripts, persistent named pages, and screenshot evidence. Use when a story touches a web frontend and needs visual or behavioral verification, when capturing UI evidence for acceptance, or for any scripted browser automation during development.
---

# Dev-Browser Web Verification

dev-browser (https://github.com/sawyerhood/dev-browser) runs sandboxed
JavaScript with the full Playwright API against a real browser. Pages persist
across script invocations, so an agent can act, observe, and verify in small
steps without losing state.

## Setup (once per machine)

```sh
npm install -g dev-browser
dev-browser install          # installs Playwright + Chromium
```

## Running Scripts

Pipe a script on stdin; use `--headless` for CI/VPS, or `--connect` to attach
to a running Chrome (useful for authenticated sessions on a workstation):

```sh
dev-browser --headless <<'EOF'
const page = await browser.getPage("main");
await page.goto("http://localhost:3000", { waitUntil: "domcontentloaded" });
console.log(await page.title());
EOF
```

`browser.getPage("main")` gets or creates a **named page** that survives
between scripts. Use one name per flow (e.g. `"main"`, `"admin"`) and keep
reusing it — that is what makes stepwise verification cheap.

## Verification Pattern

Verify a UI story in three passes, each a separate small script:

1. **Reach** — navigate, assert the page loads and key elements exist:

```js
const page = await browser.getPage("main");
await page.goto("http://localhost:3000/reports");
const rows = await page.locator("table tbody tr").count();
if (rows === 0) throw new Error("expected at least one report row");
```

2. **Act** — perform the user journey (click, fill, submit) with assertions
   after each state change:

```js
await page.getByRole("button", { name: "New report" }).click();
await page.getByLabel("Title").fill("Smoke test report");
await page.getByRole("button", { name: "Save" }).click();
await page.waitForURL(/\/reports\/\d+/);
```

3. **Evidence** — capture screenshots and store them where the repo keeps
   verification artifacts (conventionally `evidence/`):

```js
const buf = await page.screenshot({ fullPage: true });
const path = await saveScreenshot(buf, "report-created");
console.log("screenshot:", path);
```

Copy saved screenshots into `evidence/<date>-<story>/` and reference them from
the story's acceptance notes or issue close reason. A UI story is not "done"
until a screenshot (or failed-assertion trace) exists for each acceptance
criterion that has a visible surface.

## Rules

- Prefer role/label locators (`getByRole`, `getByLabel`) over CSS selectors;
  they verify accessibility for free.
- Throw on unexpected state — a script that only logs cannot fail a
  verification gate.
- Check both light and dark themes when the app supports them.
- On a headless VPS, always `--headless`; on a MacBook, `--connect` lets you
  reuse the user's logged-in Chrome instead of scripting authentication.
- Keep scripts small and idempotent; re-running the sequence from the top must
  be safe.
