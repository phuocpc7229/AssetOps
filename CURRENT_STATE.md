# Current State

## Project Status

AssetOps Portal has a working Django REST Framework backend and Vue 3/Vuetify frontend foundation. Authentication, the authenticated app shell, Asset Management, Site Management, master-data management, asset ping testing, and multi-IP asset support are implemented.

The dashboard remains intentionally minimal until operational metrics are implemented. Sidebar modules outside Dashboard, Assets, Sites, Asset Types, Vendors, Device Types, and Locations remain marked as Coming Soon.

## Completed Features

- Backend foundation under `backend/` with environment-driven settings and PostgreSQL configuration.
- Docker Compose PostgreSQL database service.
- Custom administrator model, hashed passwords, hashed bearer access tokens, and idempotent initial administrator creation.
- `GET /api/v1/health`.
- `POST /api/v1/auth/login` and protected `GET /api/v1/auth/me`.
- Authenticated Vue app shell with sidebar, topbar, protected routing, Pinia auth state, and token storage.
- Approved dark AssetOps login page connected to the authentication API.
- Asset Management with protected list, create, detail, update, archive, search, filters, ordering, and pagination.
- Site Management with protected CRUD APIs, frontend management page, search, validation, and soft delete.
- Master-data management for Asset Types, Vendors, Device Types, and Locations with protected CRUD APIs, search, pagination, validation, soft delete, and frontend pages.
- Asset records reference managed Site, Asset Type, Vendor, and Location records.
- Multiple IP addresses per asset with one primary IP, duplicate prevention, primary-IP synchronization, and legacy `ip_address` compatibility.
- Asset ping endpoint and frontend Ping action, including selecting a stored asset IP when multiple IP addresses exist.
- API-backed searchable dropdown controls for asset forms and filters.
- Frontend date display/input normalization for asset date fields.
- `seed_master_data` management command for default Asset Types, Vendors, Device Types, and Locations.
- Backend tests for health, authentication, assets, sites, master data, soft delete, validation, pagination, search, ordering, ping behavior, multi-IP behavior, and master-data seeding.

## Database Schema

- `admin_users`: administrator credentials and status fields.
- `access_tokens`: hashed bearer tokens linked to administrator users.
- `sites`: managed sites with soft-delete fields.
- `asset_types`, `vendors`, `device_types`, `locations`: reusable master-data tables with soft-delete fields.
- `assets`: core asset records with foreign keys to Site, Asset Type, Vendor, and Location; archived assets use `status=archived`.
- `asset_ip_addresses`: related IP addresses for assets, with `is_primary` and a uniqueness constraint on asset/address.

Existing `assets.ip_address` remains as the primary IP compatibility field and is synchronized from `asset_ip_addresses`.

## API Surface

- `GET /api/v1/health`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
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
- Implemented pages: Login, Dashboard placeholder, Assets, Add/Edit Asset, Sites, and Master Data.
- Reusable UI patterns include the app shell, logo, neon panel, primary button, Asset text field, Asset table/status pill, and searchable select.
- The approved dark futuristic AssetOps design in `ImageUI` and `docs/UI_REFERENCE.md` remains the visual baseline.

## Notes

- Asset archive is soft delete through `status=archived`; archived assets are excluded from the default asset list unless explicitly included.
- Site and master-data delete actions are soft deletes through `is_deleted=true`; deleted records are excluded from default lists unless explicitly included.
- Site is required for asset create/update.
- Asset Type is required for asset create/update.
- Deleted Sites and deleted master-data records cannot be selected for new asset writes.
- Other non-implemented sidebar modules remain Coming Soon.

## Remaining Known Issues

- Dashboard metrics and operational widgets are not implemented yet.
- Import, Reports, Users, and Settings modules are placeholders.
- Docker Compose currently defines the database service only; backend and frontend are run separately in local development.
- Frontend automated tests are not yet configured.
- Some frontend flows still use native browser dialogs for simple confirmation or IP selection.

## Recommended Next Milestone

Implement the operational Dashboard milestone: backend aggregate metrics plus frontend KPI cards, recent assets, warranty/maintenance indicators, and compact charts using the approved admin dashboard mockup.
