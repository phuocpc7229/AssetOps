# Current State

## Completed

- Added a Django REST Framework backend foundation under `backend/`.
- Added environment-driven backend settings and PostgreSQL database configuration.
- Added database migrations for administrator users and access tokens.
- Added `GET /api/v1/health`.
- Added secure password hashing through Django password hashers.
- Added idempotent initial administrator creation through `create_initial_admin`.
- Added `POST /api/v1/auth/login`.
- Added protected `GET /api/v1/auth/me`.
- Added backend API tests for health and authentication behavior.
- Connected the existing approved login page to the authentication API.
- Added Pinia authentication state and token storage.
- Added required-field validation, loading state, duplicate-submit prevention, and inline API errors to the login flow.
- Added protected `/dashboard` routing and a minimal dashboard placeholder.
- Added environment variable examples for backend and frontend.
- Added Asset Management as the first core module.
- Added the `assets` backend app with an `Asset` model, migration, validation, search, filters, ordering, pagination, and soft archive behavior.
- Added protected asset API endpoints for list, create, detail, update, and archive.
- Added backend tests for asset authentication, validation, duplicate prevention, list behavior, search, filtering, pagination, ordering, updates, and soft archive.
- Added the authenticated app shell, sidebar, and topbar.
- Added asset list, add, and edit frontend pages.
- Added asset search, filters, pagination, loading, empty, error, and archive confirmation states.
- Added Sites management with protected backend CRUD APIs and a functional authenticated Sites page.
- Updated assets to reference managed Sites through a nullable foreign key instead of free-text site values.
- Added an authenticated asset ping test endpoint and frontend Ping action for assets with IP addresses.
- Added Milestone 2.5 enterprise master data foundation for Asset Types, Vendors, Device Types, and Locations.
- Converted assets to reference Asset Type, Vendor, and Location master data through foreign keys while keeping Site as a foreign key.
- Added protected CRUD APIs for Asset Types, Vendors, Device Types, and Locations with search, pagination, validation, and soft delete.
- Added backend tests for all master-data CRUD, search, pagination, validation, and soft-delete behavior.
- Updated the Asset form so Asset Type, Vendor, and Location use searchable API-backed dropdown controls.
- Added authenticated master-data management pages and removed Coming Soon labels for implemented master-data modules in the sidebar.

## Notes

- The approved login visual design remains the baseline and should not be redesigned.
- The dashboard placeholder remains intentionally minimal until dashboard metrics are implemented.
- Sidebar entries outside Dashboard, Assets, Sites, Asset Types, Vendors, Device Types, and Locations are marked as Coming Soon.
- Asset archive is soft delete through `status=archived`; archived assets are excluded from the default list unless explicitly included.
- Master-data delete actions are soft deletes through `is_deleted=true`; deleted records are excluded from default master-data lists unless explicitly included.
- Sites and Milestone 2.5 master data are functional sidebar modules. Other non-implemented modules remain marked as Coming Soon.
- Asset site values are managed through `site_id` on create/update and returned as a site summary object in API responses.
- Asset type, vendor, and location values are managed through `asset_type_id`, `vendor_id`, and `location_id` on create/update and returned as nested master-data objects in API responses.
