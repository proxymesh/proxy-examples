# Reference: New Language Example Skeleton

Use this file as a quick copy/paste starter when adding a new language folder to `proxy-examples`.

## 1) Folder Layout

```text
<language>/
  run_tests.<ext>
  <client-a>-proxy.<ext>
  <client-b>-proxy.<ext>
  <client-c>-proxy.<ext>
  <dependency-manifest>
  <lockfile>
```

Keep filenames library-centric and consistent with existing folders.

## 2) Example Module Checklist

Each example script should:
- Read `PROXY_URL` (fallback `HTTPS_PROXY` when idiomatic)
- Read `TEST_URL` (default `https://api.ipify.org?format=json`)
- Optionally consume:
  - `PROXY_HEADER`
  - `PROXY_VALUE`
  - `RESPONSE_HEADER`
- Print success output concise enough for CI logs
- Exit non-zero on failure

## 3) run_tests Harness Skeleton

Use equivalent logic in the target language:

```text
parse args:
  -h/--help
  -l/--list
  optional -v/--verbose
  optional example filters

if PROXY_URL and HTTPS_PROXY missing:
  print actionable error
  exit 1

resolve example list
run each example in subprocess
collect pass/fail
print summary
exit 1 if any failed, else 0
```

Runner output should include:
- masked proxy URL when displayed
- test URL
- number of examples selected
- per-example result
- final totals

## 4) GitHub Actions Workflow Skeleton

Create `.github/workflows/proxy_integration_tests_<language>.yml`:

```yaml
# Integration tests against a real proxy (PROXY_URL). Add repository secret PROXY_URL
# under Settings -> Secrets and variables -> Actions, then mark this workflow as a required
# status check under branch protection (pull_request events only receive secrets for PRs
# from the same repository, not from forks).

name: Proxy integration tests (<Language>)

on:
  pull_request:
    paths:
      - "<language>/**"
      - ".github/workflows/proxy_integration_tests_<language>.yml"

permissions:
  contents: read

jobs:
  integration:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<pinned-sha>
        with:
          persist-credentials: false

      - name: Set up <Language runtime>
        uses: <runtime-action>@<pinned-sha-or-version>
        with:
          <runtime-version-key>: "<version>"

      - name: Install dependencies
        working-directory: <language>
        run: <install-command>

      - name: Require PROXY_URL Actions secret
        env:
          PROXY_URL: ${{ secrets.PROXY_URL }}
        run: |
          if [ -z "${PROXY_URL}" ]; then
            echo "::error::PROXY_URL is not set. Add a repository (or environment) secret named PROXY_URL under Settings -> Secrets and variables -> Actions."
            exit 1
          fi

      - name: Run integration tests
        working-directory: <language>
        env:
          PROXY_URL: ${{ secrets.PROXY_URL }}
        run: <test-command>
```

## 5) Suggested Delivery Notes Template

When finishing a new language addition, report:
1. Libraries selected and why.
2. Proxy limitations discovered.
3. Files added/updated.
4. Local test command:

```bash
PROXY_URL='http://user:pass@host:port' <language-test-command>
```

## 6) No-Root Execution Rule

- Never run `sudo` or root-required commands while implementing the task.
- Prefer user-space installs first:
  - local virtual environment or user-site installs
  - language package manager installs scoped to project/user
  - project-local toolchain managers where applicable
- If a dependency truly requires elevated privileges:
  1. Stop immediately.
  2. Provide the exact command the user should run.
  3. Explain what dependency is required and why user-space install is not sufficient.
  4. Continue only after user confirmation.
