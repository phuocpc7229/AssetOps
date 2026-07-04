# AssetOps Portal UI Reference

This document defines the approved visual direction for AssetOps Portal based on the local mockups in `ImageUI/login.png` and `ImageUI/UI page admin.png`.

These images are the single source of truth for frontend implementation. New screens should extend this visual system instead of introducing a different theme.

## Overall Style

AssetOps Portal uses a dark, futuristic operations-console style. The interface should feel like a high-end infrastructure, asset, and device management platform: technical, precise, luminous, and dense enough for professional daily use.

The visual language is built from:

- Deep black and navy backgrounds.
- Electric cyan and blue neon accents.
- Glass-like panels with subtle transparency.
- Thin luminous borders.
- Circuit-board textures and digital grid details.
- Compact dashboard cards, data tables, charts, and controls.
- Crisp iconography with light-line strokes.

The UI must not feel like a generic light enterprise dashboard. It should retain the dark sci-fi identity visible in both approved mockups.

## Dark Futuristic Theme

The entire application uses a dark theme by default. Backgrounds should be near-black with dark blue depth, not flat gray.

Approved theme characteristics:

- Main background: almost black with a blue cast.
- Decorative background: subtle digital circuit traces, glowing dots, and vertical data-line effects.
- Panels: dark translucent navy surfaces.
- Borders: thin neon blue or muted blue-gray outlines.
- Highlights: cyan-blue glows on active navigation, logo, primary buttons, and focused elements.
- Data visualization: saturated but controlled accent colors on dark surfaces.

Avoid bright white page backgrounds, beige themes, flat gray admin templates, or colorful marketing gradients.

## Logo Style

The AssetOps logo is a central brand element and must remain visually prominent.

Approved logo characteristics:

- Stylized angular `AS` mark.
- Futuristic geometric construction.
- Bright cyan-to-blue glow.
- Beveled or luminous edge treatment.
- Wordmark uses wide, technical, uppercase lettering.
- `ASSET` appears white or light silver.
- `OPS` appears cyan/blue.
- `PORTAL` appears spaced out below the wordmark in muted blue-gray.

Usage:

- Login page: large brand presentation on the left side with the full logo lockup.
- Login card: smaller glowing mark above the welcome heading.
- App shell sidebar: full logo lockup at the top.
- Do not replace the logo with plain text.
- Do not flatten the logo into a non-glowing monochrome mark unless required for a very small constrained state.

## Color Palette

Use a dark base with neon blues as the dominant brand accent.

Recommended palette:

- Page black: `#020713`, `#040B18`, `#050A14`
- Deep navy: `#071426`, `#081B33`, `#0B203A`
- Panel navy: `#071528`, `#0A1A2D`, `#0D2138`
- Border blue: `#0E73C8`, `#128CFF`, `#1E9BFF`
- Neon cyan: `#00D8FF`, `#00B7FF`
- Primary blue: `#006DFF`, `#0A84FF`, `#126BFF`
- Text white: `#F5F8FF`
- Text muted: `#8EA8CB`, `#9AB2D4`, `#AFC2DE`
- Divider blue-gray: `#16314F`, `#1D3D61`
- Success green: `#00D48A`, `#12C983`
- Warning yellow/orange: `#F6B52B`, `#FF951A`
- Danger red: `#FF4D5E`, `#E53946`
- Purple chart accent: `#7357FF`, `#8B4DFF`
- Teal chart accent: `#11C6C8`

Color rules:

- Blue and cyan are the primary brand accents.
- Orange is reserved for warranty warnings or expiring states.
- Green is reserved for valid, active, or healthy states.
- Red is reserved for expired, failed, high-risk, or destructive states.
- Purple, teal, yellow, and magenta may appear in charts only as secondary categorical colors.

## Sidebar Layout

The authenticated application uses a fixed left sidebar.

Approved sidebar structure:

- Full-height vertical navigation.
- Dark translucent navy background.
- Thin glowing blue border around the app frame and sidebar edge.
- Large AssetOps logo lockup at the top.
- Navigation items stacked vertically with icons on the left and labels on the right.
- Active item is a bright blue glowing rounded rectangle.
- Inactive items are transparent with muted light text and thin line icons.
- Bottom area contains a small product/version card, shown as `AssetOps Portal` and version text.
- Subtle circuit-board decorative texture appears in the lower sidebar background.

Navigation items visible in the approved admin mockup:

- Dashboard
- Devices
- Sites
- Locations
- Vendors
- Device Types
- Import
- Reports
- Users
- Settings

Sidebar sizing and spacing:

- Sidebar is wide enough for logo, icons, and labels without truncation.
- Navigation rows use consistent height and left padding.
- Icons align to a clean vertical column.
- Active navigation should have a strong glow but remain readable.

## Login Page Layout

The login page is a two-column composition.

Approved layout:

- Full-screen dark futuristic background.
- Left side contains large AssetOps brand mark and wordmark.
- Right side contains a large login panel.
- The login panel is vertically centered and framed by a thin neon-blue border.
- Footer copyright sits centered near the bottom.
- Background includes a digital circuit-board floor/grid and vertical data-line effects.

Login panel:

- Large rounded rectangle with dark glass-like fill.
- Thin cyan-blue border.
- Brighter glow points along the top and bottom border.
- Small glowing logo mark at the top.
- Centered `Welcome back` heading.
- Muted subtitle below the heading.
- Form fields stacked vertically.
- Large full-width primary `Sign in` button.

Login form:

- Labels appear above inputs.
- Inputs have dark translucent fill.
- Inputs use muted blue-gray placeholder text.
- Left-side icons indicate username and password.
- Password field includes a right-side visibility icon.
- Primary button uses vivid blue gradient with subtle circuit-line detail.

## Dashboard Layout

The dashboard uses a dense admin shell optimized for scanning operational status.

Approved layout:

- Sidebar on the left.
- Main content area inside a dark framed application canvas.
- Top header includes page title, short welcome text, search, action icons, and user profile.
- KPI cards appear in a single row across the top.
- Main content below is split into a wide table area and a narrower right analytics column.

Header:

- Title: `Admin Dashboard`.
- Subtitle: short welcome/status sentence.
- Search input aligned near the top center/right.
- Utility icons for notifications, settings, help, and user menu.
- Notification icon may show a small circular count badge.
- User avatar is circular with initials and an online status dot.

KPI cards:

- Five cards in one row in the approved desktop layout.
- Each card has a circular icon badge, label, large number, helper text, and small sparkline.
- Card borders are thin blue lines with subtle glow.
- Cards use a dark navy glass surface.
- Warning cards may switch sparkline and icon accents to orange.

Approved KPI examples:

- Total Devices
- Active Devices
- In Maintenance
- Expiring Warranty
- Archived Devices

Analytics column:

- Right side contains chart cards.
- Donut charts use vivid category colors.
- Chart legends sit to the right of the donut.
- Each chart card has a concise title and `View Report` action link.

## Device Management Layout

Device management should follow the table-first structure shown in the dashboard `Recent Devices` area.

Approved device layout characteristics:

- Primary content is a large bordered table panel.
- Panel header contains a section title, optional icon, filters button, primary add action, and overflow menu.
- Tables use compact rows and strong column alignment.
- Asset tags are blue clickable links.
- Status, criticality, and warranty states use colored pills or colored text.
- Pagination appears at the bottom right.
- Result count appears at the bottom left.

Device fields visible in the approved mockup:

- Asset Tag
- Device Name
- Type
- Vendor
- Site
- Status
- Criticality
- Warranty

Expected device management screens should preserve this data-dense, operational table style. Detail pages and edit forms should use the same dark panel, blue border, compact label, and neon-accent treatment.

## Site Management Layout

Site management should visually align with the dashboard and device table patterns.

Approved direction:

- Use the same app shell, sidebar, top header, and dark framed canvas.
- Site lists should use the same compact table style as devices.
- Site summary metrics may use KPI cards where useful.
- Site detail pages should use dark glass panels with thin blue borders.
- Location, capacity, device count, operational status, and related assets should be grouped into clear panels.
- Maps or location visuals, if added, should use dark map styling and cyan/blue markers.
- Site status should use the same pill system as device status.

The site section should not introduce a lighter CRM-style layout. It should remain consistent with the futuristic infrastructure operations dashboard.

## Typography

Typography is clean, modern, and technical.

Approved characteristics:

- Sans-serif typeface.
- High legibility on dark backgrounds.
- Headings are bright white and medium-to-bold weight.
- Body text is muted blue-gray.
- Labels are smaller and clearer than body copy.
- Numbers in KPI cards are large, bright, and easy to scan.
- Navigation labels use medium weight and consistent sizing.
- Logo wordmark uses a separate futuristic uppercase style.

Approximate type scale:

- Page title: 26-32px.
- Section title: 18-22px.
- KPI number: 28-36px.
- Table body: 13-15px.
- Table header: 12-14px.
- Form labels: 14-16px.
- Button text: 15-17px.
- Muted helper text: 13-15px.

Avoid playful fonts, serif body fonts, excessive letter spacing in normal UI text, or oversized marketing-style headings inside the admin app.

## Spacing

Spacing is disciplined and compact.

Approved spacing characteristics:

- App shell has generous outer framing but dense internal content.
- Sidebar items have comfortable vertical rhythm without wasting space.
- Dashboard cards have consistent gaps.
- Table rows are compact and readable.
- Form fields on login are generously spaced to feel premium.
- Login panel has larger internal padding than dashboard cards.

Recommended spacing:

- App frame inset: 8-16px.
- Main content padding: 28-36px desktop.
- Card gap: 16-24px.
- Card padding: 20-24px.
- Table cell horizontal padding: 16-20px.
- Table row height: 44-52px.
- Form field height: 56-64px.
- Login panel padding: 56-72px.

## Borders

Borders are central to the visual identity.

Approved border style:

- Thin 1px borders.
- Cyan-blue or dark blue-gray.
- Slightly brighter on active, focused, or primary panels.
- Large panels and cards use rounded corners.
- Login panel uses a larger radius than dashboard cards.
- Active sidebar item uses a rounded rectangular glowing border/fill.

Recommended radii:

- App frame: 12-16px.
- Sidebar active item: 6-8px.
- Dashboard cards: 8-10px.
- Table panel: 10-12px.
- Login panel: 28-36px.
- Inputs: 8-10px.
- Buttons: 8px.
- Pills: 4-6px.

## Shadows

Shadows should create depth without making the UI look soft or material-design-like.

Approved shadow style:

- Dark outer shadows for panel separation.
- Blue glow shadows around active elements.
- Subtle inset shadows inside fields and cards.
- Strongest shadows are reserved for the login panel, active navigation item, logo, and primary button.

Avoid heavy gray drop shadows, soft floating white cards, or shadows that imply a light theme.

## Glow Effects

Glow is a signature part of the approved direction.

Approved glow usage:

- Logo mark and wordmark.
- Login panel border highlights.
- Primary sign-in button.
- Active sidebar navigation item.
- Selected pagination item.
- KPI icon badges.
- Chart accents and sparklines.
- Focused form controls.

Glow rules:

- Use cyan and electric blue as default glow colors.
- Use orange glow only for warning or expiring warranty states.
- Keep glow controlled and local to the element.
- Do not add large decorative gradient blobs or unrelated background orbs.
- Maintain text readability over glowing backgrounds.

## Table Style

Tables are dark, compact, and data-rich.

Approved table characteristics:

- Table sits inside a bordered panel.
- Header row uses a slightly different dark navy fill.
- Column labels are muted blue-gray.
- Sort indicators appear beside sortable columns.
- Rows are separated by thin blue-gray dividers.
- Body text is light and readable.
- Links use bright blue.
- Status and criticality use small colored pills.
- Expired warranty can appear as red text.
- Hover and selected states should use subtle dark-blue highlights.
- Pagination uses small square buttons with blue active state.

Table panels should include:

- Title and icon at top left.
- Filter button and primary action at top right when relevant.
- Overflow menu where secondary actions exist.
- Result count at bottom left.
- Pagination at bottom right.

## Card Style

Cards use glassy dark surfaces with technical accents.

Approved card characteristics:

- Dark navy translucent fill.
- Thin blue border.
- Subtle inner gradient from top-left or top edge.
- Rounded corners.
- Optional circular icon badge.
- Minimal text, clear hierarchy.
- Data visualization elements aligned and compact.

KPI card structure:

- Icon badge on the left.
- Label beside or near the icon.
- Large number below label.
- Supporting percentage or description below the number.
- Sparkline anchored near the lower right or lower area.

Chart card structure:

- Title at top left.
- Optional `View Report` link at top right.
- Donut chart centered left.
- Legend and percentages aligned right.

## Form Style

Forms use dark glass inputs with icon support.

Approved form characteristics:

- Labels are bright white or near-white.
- Inputs are dark navy with subtle transparency.
- Input borders are muted blue-gray by default.
- Focus state uses cyan-blue border and glow.
- Placeholder text is muted blue-gray.
- Icons are thin-line and cyan/blue.
- Password visibility icon is right-aligned.
- Validation states should use the approved green, orange, and red status colors.

Login forms should be spacious and centered. Admin forms should be more compact but retain the same color, border, and focus language.

## Button Style

Buttons should feel technical, luminous, and precise.

Primary button:

- Bright blue gradient fill.
- Thin brighter blue border.
- Subtle glow.
- White text.
- Optional faint circuit-line texture.
- Rounded corners around 8px.

Secondary button:

- Dark navy fill.
- Thin blue border.
- Light text.
- Cyan icon or accent.
- Subtle hover glow.

Icon button:

- Transparent or dark circular/square surface.
- Thin-line icon.
- Muted default color.
- Cyan/blue hover and active states.

Danger button:

- Dark red or red-accented style.
- Use sparingly.
- Must still fit the dark neon system.

## Icon Style

Icons are thin-line, geometric, and technical.

Approved icon characteristics:

- Line icons, not filled cartoon icons.
- Simple strokes with rounded joins where appropriate.
- Default color is muted blue-gray or light blue.
- Active icons use cyan/blue.
- Status icons may use semantic colors.
- KPI icons sit inside glowing circular badges.
- Sidebar icons are consistently sized and aligned.

Use icons for navigation, search, filters, add, notifications, settings, help, user state, visibility, and entity types. Icons should support scanning and should not compete with the logo.

## Implementation Guardrails

When implementing frontend screens:

- Treat `ImageUI/login.png` and `ImageUI/UI page admin.png` as the visual baseline.
- Preserve the dark futuristic identity across every page.
- Reuse the same app shell, sidebar, card, table, form, and button patterns.
- Keep spacing compact in the admin app and generous on the login page.
- Use blue/cyan glow intentionally on brand, focus, active, and primary elements.
- Use semantic colors consistently for active, maintenance, warning, expired, criticality, and archive states.
- Do not introduce a light theme, flat generic admin template, pastel palette, rounded bubbly SaaS style, or marketing landing-page layout.

