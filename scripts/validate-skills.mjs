#!/usr/bin/env node
// Validates every skill in skills/ against the Agent Skills spec used by
// `npx skills add` (https://vercel.com/docs/agent-resources/skills).
//
// Checks per skill:
//   - skills/<name>/SKILL.md exists
//   - YAML frontmatter with `name` and `description`
//   - name is lowercase-hyphenated and matches its directory
//   - description is non-empty and <= 1024 chars
//   - body is non-empty
//   - relative markdown links resolve to real files
//
// Repo-level checks:
//   - at least one skill exists
//   - README.md mentions every skill (warning only)
//   - delivery-contract skills retain the four orthogonal control fields
//   - rapid planning/orchestration and issue ownership invariants are present
//
// Usage: node scripts/validate-skills.mjs   (exit 1 on any error)

import { readdirSync, readFileSync, existsSync, statSync } from "node:fs";
import { join, dirname, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const skillsDir = join(repoRoot, "skills");

const errors = [];
const warnings = [];
const skillSources = new Map();
const error = (skill, msg) => errors.push(`${skill}: ${msg}`);
const warn = (skill, msg) => warnings.push(`${skill}: ${msg}`);

function parseFrontmatter(raw, skill) {
  if (!raw.startsWith("---\n")) {
    error(skill, "SKILL.md must start with `---` YAML frontmatter");
    return null;
  }
  const end = raw.indexOf("\n---", 4);
  if (end === -1) {
    error(skill, "frontmatter is not closed with `---`");
    return null;
  }
  const block = raw.slice(4, end);
  const body = raw.slice(raw.indexOf("\n", end + 1) + 1);
  const fields = {};
  let currentKey = null;
  for (const line of block.split("\n")) {
    if (/^\s*#/.test(line) || line.trim() === "") continue;
    const topLevel = line.match(/^([A-Za-z_][\w-]*):\s*(.*)$/);
    if (topLevel) {
      currentKey = topLevel[1];
      fields[currentKey] = topLevel[2].replace(/^["']|["']$/g, "");
    } else if (/^\s+/.test(line) && currentKey) {
      // folded/nested continuation — append for length checks
      fields[currentKey] = `${fields[currentKey]} ${line.trim()}`.trim();
    } else {
      error(skill, `unparseable frontmatter line: ${JSON.stringify(line)}`);
    }
  }
  return { fields, body };
}

function checkLinks(mdPath, content, skill) {
  // Fenced code blocks and inline code are example content, not real links.
  const prose = content
    .replace(/^(`{3,}|~{3,})[^\n]*\n[\s\S]*?^\1\s*$/gm, "")
    .replace(/`[^`\n]*`/g, "");
  const linkRe = /\[[^\]]*\]\(([^)\s]+)\)/g;
  for (const match of prose.matchAll(linkRe)) {
    const target = match[1];
    if (/^(https?:|mailto:|#)/.test(target)) continue;
    const targetPath = resolve(dirname(mdPath), target.split("#")[0]);
    if (!targetPath.startsWith(repoRoot + sep)) {
      error(skill, `link escapes repo: ${target}`);
    } else if (!existsSync(targetPath)) {
      error(skill, `broken link in ${mdPath.slice(repoRoot.length + 1)}: ${target}`);
    }
  }
}

if (!existsSync(skillsDir)) {
  console.error("No skills/ directory found.");
  process.exit(1);
}

const skillDirs = readdirSync(skillsDir)
  .filter((d) => !d.startsWith(".") && statSync(join(skillsDir, d)).isDirectory())
  .sort();

if (skillDirs.length === 0) {
  console.error("skills/ contains no skill directories.");
  process.exit(1);
}

const names = [];
for (const dir of skillDirs) {
  const skillPath = join(skillsDir, dir, "SKILL.md");
  if (!existsSync(skillPath)) {
    error(dir, "missing SKILL.md");
    continue;
  }
  const raw = readFileSync(skillPath, "utf8");
  skillSources.set(dir, raw);
  const parsed = parseFrontmatter(raw, dir);
  if (!parsed) continue;
  const { fields, body } = parsed;

  if (!fields.name) error(dir, "frontmatter missing `name`");
  else {
    if (!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(fields.name))
      error(dir, `name \`${fields.name}\` must be lowercase-hyphenated`);
    if (fields.name !== dir)
      error(dir, `name \`${fields.name}\` does not match directory \`${dir}\``);
    names.push(fields.name);
  }

  if (!fields.description || fields.description.trim() === "")
    error(dir, "frontmatter missing or empty `description`");
  else if (fields.description.length > 1024)
    error(dir, `description is ${fields.description.length} chars (max 1024)`);

  if (body.trim() === "") error(dir, "SKILL.md body is empty");

  checkLinks(skillPath, body, dir);

  // Validate links in any references/*.md too
  const refsDir = join(skillsDir, dir, "references");
  if (existsSync(refsDir)) {
    for (const ref of readdirSync(refsDir).filter((f) => f.endsWith(".md"))) {
      const refPath = join(refsDir, ref);
      checkLinks(refPath, readFileSync(refPath, "utf8"), dir);
    }
  }
}

const readmePath = join(repoRoot, "README.md");
if (existsSync(readmePath)) {
  const readme = readFileSync(readmePath, "utf8");
  for (const name of names) {
    if (!readme.includes(name)) warn(name, "not mentioned in README.md");
  }
} else {
  warnings.push("README.md missing at repo root");
}

const deliveryContractSkills = [
  "hls-requirements-interview",
  "hls-architecture",
  "hls-plan-builder",
  "hls-factory-orchestrate",
  "hls-process-init",
  "hls-issue-iteration",
];
const deliveryFields = [
  "operatingMode",
  "modelRoutingProfile",
  "assuranceProfile",
  "releaseStage",
];

for (const skill of deliveryContractSkills) {
  const source = skillSources.get(skill);
  if (!source) {
    error(skill, "required by the risk-calibrated delivery contract");
    continue;
  }
  for (const field of deliveryFields) {
    if (!source.includes(`\`${field}\``))
      error(skill, `delivery contract must name \`${field}\` explicitly`);
  }
}

const deliveryInvariants = new Map([
  ["hls-plan-builder", ["first usable", "foundation-only", "mandatory-review"]],
  ["hls-factory-orchestrate", ["P0/P1", "P2/P3", "mandatory-review"]],
  ["hls-issue-iteration", ["GitHub Issues", "Beads", "user journey"]],
]);

for (const [skill, phrases] of deliveryInvariants) {
  const source = skillSources.get(skill) || "";
  for (const phrase of phrases) {
    if (!source.toLowerCase().includes(phrase.toLowerCase()))
      error(skill, `risk-calibrated delivery invariant missing: ${phrase}`);
  }
}

for (const w of warnings) console.warn(`WARN  ${w}`);
for (const e of errors) console.error(`ERROR ${e}`);
console.log(
  `\n${skillDirs.length} skill(s) checked — ${errors.length} error(s), ${warnings.length} warning(s)`
);
process.exit(errors.length ? 1 : 0);
