# Flow PRD: Event Setup & Device Join

## Goal
An organizer creates an event and gets copy-paste links that turn each physical device
into its role (contestant station, monitor, admin) with zero further login.

## Actors & devices
- Organizer (any laptop) — creates the event, runs the admin page.
- Station 1 / Station 2 — the two contestant laptops.
- Monitor A / Monitor B — the two spectator screens.

## User flows

### 1. Create event (organizer)
1. Visit `/` (landing). Hero: app name "Code vs Racing", tagline, "Create event" card.
2. Enter event name → click Create.
3. Server generates event id + random secret (URL-safe, 24 chars), stores in `events`.
4. Redirect to `/e/<id>/admin?k=<secret>`; the admin page shows a "Device links" panel
   with all five links (admin, station 1/2, monitor A/B) and copy buttons.

### 2. Join a device (any role)
1. Open the link `/e/<id>/<role-path>?k=<secret>` on the target device.
2. Server component validates `k` against the event secret.
   - Valid → set an httpOnly cookie `cfr_<eventId>=<secret>` (so refreshes keep working
     without the query param) and render the role page.
   - Invalid/missing (and no valid cookie) → "Invalid or expired event link" error page.
3. Role pages:
   - `/e/<id>/station/1`, `/e/<id>/station/2` → check-in screen (flow 02).
   - `/e/<id>/monitor/a`, `/e/<id>/monitor/b` → spectator screens (flow 05).
   - `/e/<id>/admin` → admin console (flow 06).

## UX details
- Landing and all pages: dark theme, bold mono-accent styling (competitive-programming
  aesthetic), subtle animated gradient background on landing.
- Copy buttons give instant "Copied" feedback (sonner toast).
- Links QR-code rendered next to each device link on the admin page (easy to open on
  laptops at the booth). [v1.1 if time permits]

## Security model
- Possession of the secret link = access. No accounts.
- Secret only checked server-side; cookie is httpOnly.
- The service-role Supabase key is only used in server routes; the browser never
  talks to Supabase directly in v1.

## Out of scope (future)
- Public standalone mode without an event.
- Multiple simultaneous races per event.
