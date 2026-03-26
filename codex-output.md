Implemented the requested minimal foundation setup for `NTP-62` and kept changes outside `.github/`.

### What changed
- Added root workspace + PR check command in [package.json](/home/runner/work/SRS-to-JIRA-Automation/SRS-to-JIRA-Automation/package.json).
- Initialized frontend baseline module under `frontend/` with Next.js/Tailwind/TypeScript scaffolding:
  - [frontend/package.json](/home/runner/work/SRS-to-JIRA-Automation/SRS-to-JIRA-Automation/frontend/package.json)
  - [frontend/app/layout.tsx](/home/runner/work/SRS-to-JIRA-Automation/SRS-to-JIRA-Automation/frontend/app/layout.tsx)
  - [frontend/app/page.tsx](/home/runner/work/SRS-to-JIRA-Automation/SRS-to-JIRA-Automation/frontend/app/page.tsx)
  - [frontend/styles/globals.css](/home/runner/work/SRS-to-JIRA-Automation/SRS-to-JIRA-Automation/frontend/styles/globals.css)
  - plus config files and folder placeholders.
- Initialized backend baseline module under `backend/` with Node.js service structure:
  - [backend/package.json](/home/runner/work/SRS-to-JIRA-Automation/SRS-to-JIRA-Automation/backend/package.json)
  - [backend/src/index.mjs](/home/runner/work/SRS-to-JIRA-Automation/SRS-to-JIRA-Automation/backend/src/index.mjs)
  - plus required folder placeholders under `backend/src/*`.
- Added lightweight checks/tests:
  - [frontend/tests/lint.test.mjs](/home/runner/work/SRS-to-JIRA-Automation/SRS-to-JIRA-Automation/frontend/tests/lint.test.mjs)
  - [frontend/tests/smoke.test.mjs](/home/runner/work/SRS-to-JIRA-Automation/SRS-to-JIRA-Automation/frontend/tests/smoke.test.mjs)
  - [backend/tests/smoke.test.mjs](/home/runner/work/SRS-to-JIRA-Automation/SRS-to-JIRA-Automation/backend/tests/smoke.test.mjs)
- Updated setup/check documentation in [README.md](/home/runner/work/SRS-to-JIRA-Automation/SRS-to-JIRA-Automation/README.md).
- Wrote exact change summary in [codex-output.md](/home/runner/work/SRS-to-JIRA-Automation/SRS-to-JIRA-Automation/codex-output.md).

### Validation
- Ran successfully: `npm run ci:pr` (frontend lint/test + backend lint/test).