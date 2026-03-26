# Project Configuration

## Project Overview
This repository implements the **Login Flow Module** described in `srs/project-srs.md`.
The architecture is split into a frontend application and a backend service.

## Technology Stack

### Frontend
- **Framework:** Next.js (latest stable major version approved by the team)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **UI Goal:** Responsive, accessible login experience aligned with SRS UI and usability requirements.

### Backend
- **Runtime:** Node.js (LTS)
- **Language:** TypeScript (preferred) or modern JavaScript (ESM)
- **API Style:** REST API for authentication/session endpoints
- **Primary Responsibility:** Credential validation, authentication, session lifecycle, logout, and access control support.

## Suggested Folder Structure

```text
.
├─ frontend/                 # Next.js + Tailwind app
│  ├─ app/                  # Routes/pages (or pages/ if using Pages Router)
│  ├─ components/           # Reusable UI components
│  ├─ lib/                  # Client utilities
│  └─ styles/               # Tailwind/global styles
├─ backend/                  # Node.js auth service
│  ├─ src/
│  │  ├─ routes/            # Auth/session routes
│  │  ├─ controllers/       # Request handlers
│  │  ├─ services/          # Business logic
│  │  ├─ middleware/        # Auth, validation, error handling
│  │  └─ utils/             # Shared helpers
│  └─ tests/                # Unit/integration tests
└─ srs/
   └─ project-srs.md
```

## Implementation Guidelines

### Frontend (Next.js + Tailwind)
- Build login UI using reusable components and Tailwind utility classes.
- Keep forms accessible (labels, keyboard focus states, clear validation messages).
- Use client + server rendering patterns that fit authentication UX and route protection.
- Redirect authenticated users to dashboard/home according to the SRS.

### Backend (Node.js)
- Expose secure endpoints for login, session validation, and logout.
- Use hashed password verification only.
- Return generic authentication errors (do not reveal whether username/email or password was incorrect).
- Enforce session timeout/inactivity policies.
- Protect private routes using auth middleware.

## Security Baseline
- Enforce HTTPS in deployed environments.
- Never log plaintext passwords.
- Store secrets in environment variables.
- Use secure cookie/token settings (`HttpOnly`, `Secure`, `SameSite`) where applicable.
- Add basic rate limiting for login endpoints.

## Testing Expectations
- Frontend: component/form validation tests and route-guard behavior tests.
- Backend: unit tests for auth/session services + integration tests for login/logout flows.
- End-to-end: validate successful login, invalid login, logout, and protected route access.

## Definition of Done (for auth tasks)
- SRS-aligned acceptance criteria are met.
- Tests are added/updated and passing.
- Security checks are verified.
- Changes are documented when behavior/configuration changes.
