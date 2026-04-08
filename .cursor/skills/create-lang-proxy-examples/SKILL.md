---
name: create-lang-proxy-examples
description: Build a new language example suite in proxy-examples by researching HTTP clients and proxy behavior, implementing testable proxy examples, adding a run_tests harness, and creating a matching GitHub Actions integration workflow. Use when adding support for a new language in this repository.
---

# Create Language Proxy Examples

Create a new `<language>/` folder in `proxy-examples` that matches patterns used by:
- `javascript/`
- `python/`
- `php/`
- `ruby/`

## Goal

Given a target programming language, produce:
1. Runnable proxy examples for multiple HTTP client libraries.
2. A language-specific `run_tests` harness that can run all or selected examples.
3. Dependency manifest/lock setup appropriate for the language.
4. A GitHub Actions workflow in `.github/workflows/` for proxy integration tests.

## Required Runtime Contract

Every new language implementation must follow this env contract:
- `PROXY_URL` (required, fallback to `HTTPS_PROXY` when practical)
- `TEST_URL` (default `https://api.ipify.org?format=json`)
- Optional send/read headers depending on client capability:
  - `PROXY_HEADER`
  - `PROXY_VALUE`
  - `RESPONSE_HEADER`

Rules:
- Fail clearly when proxy config is missing.
- Mask proxy passwords when printing URLs in test runners.
- Keep examples runnable with only `PROXY_URL`.

## Privilege and Install Policy (Non-Negotiable)

- Do not run commands requiring `sudo`, root, or system-level package installation.
- If dependencies are needed, prefer user-space installation approaches first (language package managers, local virtual environments, project-local toolchains, non-root install flags).
- If a required dependency is not feasible without elevated privileges:
  1. Stop before attempting privileged commands.
  2. Output the exact install command the user must run.
  3. Explain briefly what is needed and why it cannot be completed in user space.
  4. Resume only after the user confirms the dependency is installed.

## Implementation Workflow

Use this checklist and complete each phase.

```text
Progress:
- [ ] Phase 1: Analyze existing language patterns in this repo
- [ ] Phase 2: Research target-language HTTP client libraries
- [ ] Phase 3: Select v1 library set and capability notes
- [ ] Phase 4: Implement per-library example modules
- [ ] Phase 5: Implement run_tests harness
- [ ] Phase 6: Add dependency files (package manager native)
- [ ] Phase 7: Add GitHub Actions integration workflow
- [ ] Phase 8: Run tests/lint and polish docs/comments
```

## Internal Self-Prompts (Use by Default)

Use these prompts internally at each phase so execution is autonomous and does not block on user feedback unless absolutely necessary.

### Phase 1 prompts
- "What exact naming, runner UX, and env var conventions are shared by `javascript/`, `python/`, `php/`, and `ruby/`?"
- "What is the minimum parity bar I must hit so the new language folder feels native to this repo?"
- "Which conventions are required vs optional niceties?"

### Phase 2 prompts
- "What are the top maintained HTTP client libraries in this language right now?"
- "For each client, how do I configure proxies and what proxy-related limitations exist?"
- "Which 5+ libraries give a practical spread across standard, mainstream, and lower-level APIs?"
- "Which capabilities can I verify directly from docs/code/examples vs assumptions I should avoid?"

### Phase 3 prompts
- "Which subset is the best v1 that is broad enough but still reliably testable in CI?"
- "How should I classify each selected client (`full`, `proxy-only`, `limited`)?"
- "What naming pattern should each example file use to match this repo?"

### Phase 4 prompts
- "Does each example fail fast on missing proxy config and exit non-zero on error?"
- "Does each example read `TEST_URL` with the default fallback?"
- "Where supported, have I wired optional `PROXY_HEADER`/`PROXY_VALUE`/`RESPONSE_HEADER` behavior without overpromising?"
- "Is each script simple and demonstrative rather than framework-heavy?"

### Phase 5 prompts
- "Does `run_tests` support help/list/filtering and produce clear CI-friendly output?"
- "Are subprocess invocation, timeout behavior, and pass/fail accounting robust?"
- "Are proxy credentials masked anywhere URLs are printed?"

### Phase 6 prompts
- "What is the idiomatic dependency manifest and lockfile for this language?"
- "Did I include only dependencies needed for examples and the runner?"
- "Are install commands reproducible enough for CI?"
- "Can setup be completed entirely in user space without `sudo` or root?"
- "If not, did I stop and provide exact privileged install commands with a short why?"

### Phase 7 prompts
- "Does the workflow trigger on `pull_request` with correct path filters?"
- "Does it explicitly fail when `secrets.PROXY_URL` is missing?"
- "Are runtime setup and test commands correct for this language folder?"
- "Are comments consistent with existing workflow guidance in this repo?"

### Phase 8 prompts
- "Did I run the local harness (or explain why I could not)?"
- "Do list/help/filtering and exit codes behave correctly?"
- "Are limitations documented truthfully with no unverified claims?"
- "Is the final handoff concise: selected libraries, limitations, files changed, and exact test command?"

### Escalation prompt (only when blocked)
- "Can I proceed with a safe default and document assumptions, or is a user decision truly required?"

## Phase 1 - Mirror Existing Repository Conventions

Follow these conventions already used in this repo:
- One directory per language at repo root: `<language>/`
- One example file per library with a `-proxy` or `_proxy` suffix
- Single test harness entrypoint:
  - JavaScript: `run_tests.js`
  - Python: `run_tests.py`
  - PHP: `run_tests.php`
  - Ruby: `run_tests.rb`
- Harness supports at least:
  - `-l/--list`
  - `-h/--help`
  - optional example filtering by name
  - pass/fail summary and non-zero exit on failures

## Phase 2 - Research HTTP Clients (Mandatory)

For the target language:
1. Identify popular, maintained HTTP clients (prefer 5+ where reasonable).
2. Learn each library's proxy configuration model:
   - env-driven proxy support
   - explicit proxy URL settings
   - tunnel/CONNECT behavior
   - custom header support (if any)
3. Prefer a mix of:
   - standard library client
   - one or more mainstream framework clients
   - one lower-level client if available

Document a quick support table in comments or README notes:
- `full` (proxy use + useful response/header visibility)
- `proxy-only` (can route through proxy)
- `limited` (significant proxy limitations)

Do not claim support that cannot be verified.

## Phase 3 - Example Scope and Naming

Create example scripts with consistent naming:
- Use library-focused names (`<library>-proxy.<ext>` or `<library>_proxy.<ext>`).
- Each script should:
  - read `PROXY_URL` (or fallback `HTTPS_PROXY` if idiomatic)
  - call `TEST_URL` (or default)
  - optionally use send/read header env vars when supported
  - print concise success info
  - exit non-zero on failure

Keep script internals simple and demonstrative; avoid over-abstracting.

## Phase 4 - run_tests Harness Requirements

Implement `run_tests.<ext>` with:
- help/list flags
- optional verbose mode when idiomatic
- optional filtering to run specific modules
- subprocess execution of each example
- clear output:
  - start banner
  - per-example result (`OK/PASS` or `FAILED/FAIL`)
  - final summary

Behavior:
- Validate proxy env var early and show example export command.
- Return non-zero when any example fails.
- Keep timeouts reasonable for slower libraries.

## Phase 5 - Dependency Files

Add/update language package manager files:
- JavaScript: `package.json`, lockfile
- Python: `requirements.txt` (or pyproject + lock if repo pattern changes)
- PHP: `composer.json`, `composer.lock`
- Ruby: `Gemfile`, `Gemfile.lock`
- New language: idiomatic equivalent + lockfile where standard

Only include dependencies required to run examples/tests.

## Phase 6 - GitHub Actions Workflow

Add `.github/workflows/proxy_integration_tests_<language>.yml` modeled on existing workflows.

Required workflow behavior:
1. Trigger on `pull_request`.
2. Path filter includes:
   - `<language>/**`
   - the workflow file itself
3. Checkout repository.
4. Install runtime and dependencies.
5. Require `secrets.PROXY_URL` with explicit failure message.
6. Run `<language>/run_tests.<ext>` (or language-equivalent test command).

Keep workflow comments concise and include the repo's current guidance:
- integration tests require a real proxy
- secrets are unavailable to fork PRs

## Phase 7 - Verification

Before finishing:
- Run the language test harness locally if environment permits.
- Verify list/help modes.
- Confirm filtering works.
- Confirm non-zero exit on failure.
- Ensure workflow YAML validates and references correct paths.

## Output Expectations

When delivering changes, include:
1. Libraries selected and why.
2. Any proxy-related limitations found.
3. Files created/updated.
4. Exact command to run local integration tests.

Example command pattern:
- `PROXY_URL='http://user:pass@host:port' <language-run-command>`

## Notes

- Keep parity with the four existing language folders, but adapt to target language idioms.
- Prefer practical, testable examples over exhaustive coverage.
- If a library cannot support a header feature, mark it as a limitation and continue.
