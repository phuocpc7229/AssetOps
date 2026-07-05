# Current State

## Project Status

AssetOps Portal has a working Django REST Framework backend and Vue 3/Vuetify frontend foundation. Authentication, the authenticated app shell, Asset Management, Site Management, master-data management, asset ping testing, multi-IP asset support, the operational Dashboard, and account password management are implemented.

The Dashboard now includes backend aggregate APIs and frontend operational widgets. Sidebar modules outside Dashboard, Assets, Sites, Asset Types, Vendors, Device Types, and Locations remain marked as Coming Soon.

## Completed Features

- Backend foundation under `backend/` with environment-driven settings and PostgreSQL configuration.
- Docker Compose PostgreSQL database service.
- Custom administrator model, hashed passwords, hashed bearer access tokens, and idempotent initial administrator creation.
- `GET /api/v1/health`.
- `POST /api/v1/auth/login` and protected `GET /api/v1/auth/me`.
- Protected `POST /api/v1/auth/change-password`.
- Authenticated Vue app shell with sidebar, topbar, protected routing, Pinia auth state, and token storage.
- Approved dark AssetOps login page connected to the authentication API.
- Account Information modal with read-only account details and Change Password workflow.
- Asset Management with protected list, create, detail, update, archive, search, filters, ordering, and pagination.
- Site Management with protected CRUD APIs, frontend management page, search, validation, and soft delete.
- Master-data management for Asset Types, Vendors, Device Types, and Locations with protected CRUD APIs, search, pagination, validation, soft delete, and frontend pages.
- Asset records reference managed Site, Asset Type, Vendor, and Location records.
- Multiple IP addresses per asset with one primary IP, duplicate prevention, primary-IP synchronization, and legacy `ip_address` compatibility.
- Asset ping endpoint and frontend Ping action, including selecting a stored asset IP when multiple IP addresses exist.
- Dashboard backend app with aggregate metrics, recent asset summaries, quick-action badge counts, warranty status data, asset type distribution data, and temporary inferred recent activity.
- Dashboard frontend with KPI cards, compact charts, recent assets, recent activity, quick actions, loading states, and error states.
- API-backed searchable dropdown controls for asset forms and filters.
- Frontend date display/input normalization for asset date fields.
- UX interaction standard documented in `docs/UX_INTERACTION_STANDARD.md`.
- `seed_master_data` management command for default Asset Types, Vendors, Device Types, and Locations.
- Backend tests for health, authentication, password change, assets, sites, master data, dashboard metrics/activity, soft delete, validation, pagination, search, ordering, ping behavior, multi-IP behavior, and master-data seeding.

## Database Schema

- `admin_users`: administrator credentials and status fields.
- `access_tokens`: hashed bearer tokens linked to administrator users.
- `sites`: managed sites with soft-delete fields.
- `asset_types`, `vendors`, `device_types`, `locations`: reusable master-data tables with soft-delete fields.
- `assets`: core asset records with foreign keys to Site, Asset Type, Vendor, and Location; archived assets use `status=archived`.
- `asset_ip_addresses`: related IP addresses for assets, with `is_primary` and a uniqueness constraint on asset/address.

Existing `assets.ip_address` remains as the primary IP compatibility field and is synchronized from `asset_ip_addresses`.

The current network data model is intentionally temporary and still too flat for monitoring. Future asset network data should be refactored to `Asset -> NetworkInterface -> IPAddress` before Monitoring, SNMP, or traffic integrations are implemented.

## API Surface

- `GET /api/v1/health`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `POST /api/v1/auth/change-password`
- `GET /api/v1/dashboard/metrics`
- `GET /api/v1/dashboard/recent-assets`
- `GET /api/v1/dashboard/recent-activity`
- `GET|POST /api/v1/assets`
- `GET|PATCH|DELETE /api/v1/assets/<id>`
- `POST /api/v1/assets/<id>/ping`
- `GET|POST /api/v1/sites`
- `GET|PATCH|DELETE /api/v1/sites/<id>`
- `GET|POST /api/v1/asset-types`
- `GET|PATCH|DELETE /api/v1/asset-types/<id>`
- `GET|POST /api/v1/vendors`
- `GET|PATCH|DELETE /api/v1/vendors/<id>`
- `GET|POST /api/v1/device-types`
- `GET|PATCH|DELETE /api/v1/device-types/<id>`
- `GET|POST /api/v1/locations`
- `GET|PATCH|DELETE /api/v1/locations/<id>`

Asset create/update accepts `site_id`, `asset_type_id`, `vendor_id`, `location_id`, and `ip_addresses`. Asset responses return nested Site, master-data, and IP-address summaries.

## Frontend State

- Frontend is a Vue 3 TypeScript Vite app using Vuetify 3.
- API access is isolated in typed service modules under `frontend/src/services`.
- Authentication state is managed in Pinia and persisted through local storage.
- Implemented pages: Login, Dashboard, Assets, Add/Edit Asset, Sites, and Master Data.
- Reusable UI patterns include the app shell, logo, neon panel, primary button, Asset text field, Asset table/status pill, and searchable select.
- The approved dark futuristic AssetOps design in `ImageUI` and `docs/UI_REFERENCE.md` remains the visual baseline.
- Account actions are available through the topbar Account menu, including Account Information and Change Password.
- Dashboard visuals and account interactions follow the documented UX interaction standard.

## Notes

- Asset archive is soft delete through `status=archived`; archived assets are excluded from the default asset list unless explicitly included.
- Site and master-data delete actions are soft deletes through `is_deleted=true`; deleted records are excluded from default lists unless explicitly included.
- Site is required for asset create/update.
- Asset Type is required for asset create/update.
- Deleted Sites and deleted master-data records cannot be selected for new asset writes.
- Dashboard `Online Assets` is currently a placeholder metric based on non-archived assets with assigned IP addresses. It does not yet represent real ping status, reachability, monitoring state, or availability.
- Dashboard `Recent Activity` is temporary and inferred from existing record timestamps until an `AuditEvent` model exists.
- Other non-implemented sidebar modules remain Coming Soon.

## Remaining Known Issues

- Import, Reports, Users, and Settings modules are placeholders.
- Docker Compose currently defines the database service only; backend and frontend are run separately in local development.
- Frontend automated tests are not yet configured.
- Some frontend flows still use native browser dialogs for simple confirmation or IP selection.
- The asset network model is still too flat. MAC/IP data should be refactored into Network Interfaces before Monitoring, SNMP, or traffic integrations.
- Dashboard `Online Assets` is not a real network reachability metric yet.
- Dashboard `Recent Activity` is inferred rather than backed by durable audit events.

## Recommended Next Milestone

Implement the Audit/Event Log foundation so operational changes are recorded as durable `AuditEvent` records and the Dashboard Recent Activity panel can stop relying on inferred timestamps. Before starting Monitoring, refactor asset network data into Network Interfaces.
