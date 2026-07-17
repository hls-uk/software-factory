---
name: hls-publish-report
description: Publish a repo markdown document as a stakeholder-grade PDF with its Mermaid diagrams rendered — the "published report" convention. PDFs live in docs/published/, the regeneration command is recorded in the source doc, and a published PDF is never left stale behind its source. Use when a document needs to leave the repo (architecture sign-off, the factory-method doc, requirements or plan summaries for stakeholders) or when asked to publish or re-publish a doc.
---

# Publish Report

A repo's markdown is written for people who live in the repo. A **published
report** is the same document made portable: a single PDF with the Mermaid
diagrams rendered, suitable for a stakeholder, a sign-off record, or anyone
who will never run a toolchain. Markdown stays the source of truth; the PDF
is a build artifact — committed, because its whole point is to be readable
without building anything.

## The convention

- **Location:** `docs/published/<name>.pdf` — same basename as the source
  doc (`docs/factory-method.md` → `docs/published/factory-method.pdf`).
- **Regeneration command recorded in the source doc** — a short "Published"
  footer naming the exact command, so any session can re-publish without
  archaeology.
- **Staleness discipline:** a published PDF that lags its source is worse
  than none — it misinforms with authority. Any session that materially
  edits a published doc regenerates the PDF in the same session, or
  deletes it and notes why. Sign-off PDFs (e.g. a signed-off architecture
  doc) are point-in-time records: regenerate on re-sign, not on every typo.
- **Intermediates are never committed** — only the final PDF.

## The toolchain

| Option | Pros | Cons |
|---|---|---|
| **mermaid-cli + md-to-pdf** (npm) | npm-only, no accounts; mermaid-cli is the reference Mermaid renderer; md-to-pdf prints via Chromium so output matches GitHub-ish rendering | two steps; puppeteer downloads Chromium on first run (~200 MB) |
| pandoc + LaTeX (brew) | best print typography | multi-GB TeX install; Mermaid needs a separate filter anyway |
| pandoc + mermaid-filter + weasyprint | no Chromium | three tools across npm/pip/brew — most moving parts |
| hand-rolled puppeteer script | total control | building our own tool for a solved problem |

**Chosen: mermaid-cli + md-to-pdf.** Simplest proven chain inside the
npm-only constraint; both tools share the same headless-Chromium substrate.
Revisit if a single-step tool matures or Chromium downloads become a
problem on locked-down hosts.

## Publishing a doc

From the repo root (the working commands — adjust paths per doc):

```sh
mkdir -p docs/published
# 1. Render mermaid blocks to SVG images, emitting a transformed markdown copy
npx -y @mermaid-js/mermaid-cli -i docs/<name>.md -o docs/published/<name>.pub.md
# 2. Print the transformed markdown to PDF via Chromium
npx -y md-to-pdf docs/published/<name>.pub.md --basedir docs/published
mv docs/published/<name>.pub.pdf docs/published/<name>.pdf
# 3. Clean intermediates (transformed md + generated svg files)
rm docs/published/<name>.pub.md docs/published/<name>.pub-*.svg
```

Then add or refresh the source doc's footer:

```markdown
---
*Published: `docs/published/<name>.pdf` — regenerate with the
hls-publish-report skill (mermaid-cli + md-to-pdf).*
```

Verify before committing: open the PDF (or check its page count and file
size are sane) and confirm every Mermaid diagram rendered — a missing
diagram usually means a syntax error mermaid-cli reported and the run
ignored. The PDF is the deliverable; a broken diagram in it is a broken
deliverable.

Smoke test: [references/sample-report.md](references/sample-report.md) is a
minimal doc with one Mermaid diagram — run the chain against it once when
setting up a new machine or debugging the toolchain. Don't commit its
output.

## Anti-patterns

- Publishing a doc nobody asked to leave the repo. Published reports are
  for external eyes and sign-off records; routine docs stay markdown.
- Committing intermediates (`.pub.md`, generated SVGs) alongside the PDF.
- Regenerating a signed-off record because the source got a typo fix — the
  signed PDF is the record of *what was signed*; re-sign or leave it.
- Treating a Mermaid render failure as cosmetic. If the diagram didn't
  render, the report is wrong — fix the diagram, re-run.
