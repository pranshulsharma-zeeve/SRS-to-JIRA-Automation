Implemented the NTP-62 foundation setup with minimal scoped changes.

### What changed
- Added baseline frontend/backend module structures and starter code:
  - [frontend/__init__.py](/home/runner/work/SRS-to-JIRA-Automation/SRS-to-JIRA-Automation/frontend/__init__.py)
  - [frontend/src/__init__.py](/home/runner/work/SRS-to-JIRA-Automation/SRS-to-JIRA-Automation/frontend/src/__init__.py)
  - [frontend/src/app.py](/home/runner/work/SRS-to-JIRA-Automation/SRS-to-JIRA-Automation/frontend/src/app.py)
  - [frontend/tests/test_frontend_smoke.py](/home/runner/work/SRS-to-JIRA-Automation/SRS-to-JIRA-Automation/frontend/tests/test_frontend_smoke.py)
  - [backend/__init__.py](/home/runner/work/SRS-to-JIRA-Automation/SRS-to-JIRA-Automation/backend/__init__.py)
  - [backend/src/__init__.py](/home/runner/work/SRS-to-JIRA-Automation/SRS-to-JIRA-Automation/backend/src/__init__.py)
  - [backend/src/app.py](/home/runner/work/SRS-to-JIRA-Automation/SRS-to-JIRA-Automation/backend/src/app.py)
  - [backend/tests/test_backend_smoke.py](/home/runner/work/SRS-to-JIRA-Automation/SRS-to-JIRA-Automation/backend/tests/test_backend_smoke.py)

- Added local/CI check scripts (without touching `.github/`):
  - [scripts/lint.sh](/home/runner/work/SRS-to-JIRA-Automation/SRS-to-JIRA-Automation/scripts/lint.sh)
  - [scripts/test.sh](/home/runner/work/SRS-to-JIRA-Automation/SRS-to-JIRA-Automation/scripts/test.sh)
  - [scripts/ci-check.sh](/home/runner/work/SRS-to-JIRA-Automation/SRS-to-JIRA-Automation/scripts/ci-check.sh)

- Updated setup and CI usage docs:
  - [README.md](/home/runner/work/SRS-to-JIRA-Automation/SRS-to-JIRA-Automation/README.md)

- Added exact change summary file as requested:
  - [codex-output.md](/home/runner/work/SRS-to-JIRA-Automation/SRS-to-JIRA-Automation/codex-output.md)

### Verification run
- `./scripts/lint.sh` passed
- `./scripts/test.sh` passed
- `./scripts/ci-check.sh` passed