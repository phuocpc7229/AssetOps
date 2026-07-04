# AGENTS.md

## Project

AssetOps Portal is an enterprise asset operations platform.

## Fixed Technology Stack

- Backend: Django
- API: Django REST Framework
- Frontend: Vue 3
- Language: TypeScript
- Build tool: Vite
- UI framework: Vuetify 3
- Database: PostgreSQL
- Local environment: Docker Compose

## Permanent Engineering Rules

- Follow the approved UI mockups inside `ImageUI`.
- Treat `docs/UI_REFERENCE.md` as the frontend visual reference.
- Never redesign the UI.
- Never change approved colors, spacing, typography, component styling, or layout unless explicitly instructed.
- Use reusable components for repeated frontend patterns.
- Use English everywhere: code, comments, labels, messages, documentation, seed data, and UI text.
- Follow enterprise coding practices.
- Keep backend and frontend separated.
- Never generate code outside the requested task.
- Complete one phase before starting another.
- Never add unnecessary dependencies.
- Do not install packages unless the task explicitly requires it.
- Always explain the implementation plan before coding.
- Always run lint and tests after completing a task when applicable.

## Backend Rules

- Use Django conventions for project structure, settings, apps, models, migrations, and management commands.
- Use Django REST Framework for API endpoints, serializers, permissions, pagination, filtering, and validation.
- Keep business logic out of views when it belongs in services, managers, or domain-specific modules.
- Use PostgreSQL-compatible field types, constraints, and indexes.
- Keep migrations intentional and reviewable.
- Validate all external input.
- Use explicit permissions for protected API resources.

## Frontend Rules

- Use Vue 3 with TypeScript.
- Use Vite as the frontend build system.
- Use Vuetify 3 as the UI component framework.
- Build pages from reusable components and shared layout primitives.
- Preserve the approved dark futuristic AssetOps Portal design from `ImageUI`.
- Do not introduce alternate design systems, palettes, page layouts, or visual themes.
- Keep frontend API access isolated in dedicated services or clients.
- Keep UI text in English.

## Docker Rules

- Use Docker Compose for local orchestration.
- Keep backend, frontend, database, and supporting services clearly separated.
- Do not add services unless the requested task requires them.
- Do not change ports, service names, or volumes unless instructed or necessary for the task.

## Workflow Rules

- Before coding, explain the implementation plan.
- Make scoped changes only for the requested task.
- Do not perform unrelated refactors.
- Do not create placeholder application features unless requested.
- Do not mix phases, such as scaffolding, styling, API work, and deployment work, unless the user explicitly asks for a combined task.
- After completing a task, run applicable linting and tests.
- If linting or tests cannot be run, state why.

