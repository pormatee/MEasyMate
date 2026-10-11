# MEasyMate Platform Showcase V1

Status: LOCAL IMPLEMENTATION PREVIEW — NOT RELEASED

## Positioning
MEasyMate.com presents MEasyMate as a long-term ecosystem/platform for:

- AI
- Work
- Life
- Growth

The website must show what exists today, what is being developed, what is only a concept preview, and what is future direction without making an unfinished concept look released.

## Public status contract
1. `beta` — ทดลองใช้ / Beta
2. `developing` — กำลังพัฒนา
3. `concept-preview` — Concept Preview
4. `future-direction` — Future Direction

Status is maturity, not access entitlement. Availability is tracked separately.

## Concept rule
Every Concept Preview page must show:

`Concept Preview — หน้าตาและฟังก์ชันอาจเปลี่ยนแปลง`

Mockups are explanatory UI previews, not claims that the product is released.

## Product access rule
A real source or deployed URL is not enough to expose a customer CTA by itself.
Direct access is enabled only after the relevant release readiness gate is verified.

## Visual rule
- Keep approved Homepage V2 as the visual baseline.
- Use existing MEasyMate logo/banner assets.
- Do not generate or redraw the logo.
- Mobile-first, compact, blue/cyan/teal family.

## Analytics default
For new customer-facing web products:
- ANALYTICS_MODE = LOCAL
- CENTRAL_TRANSPORT = OFF
- EVENT_ALLOWLIST = REQUIRED
- PRIVATE_CONTENT = FORBIDDEN
- FAILURE_MODE = NON_BLOCKING

MEasyMate Money F2.1.12 is the reference implementation.

## Governance
- Website presentation registry: `data/platform-products.json`
- Portfolio/governance source: `SECRETARY_MASTER`
- Product truth: latest verified project repository/checkpoint
- If sources conflict, do not guess; downgrade public claims until re-verified.
- PRE_GIT_AUDIT before add/commit/push.
- PRE_RELEASE_AUDIT before customer release.

## Commercial presentation update

Launch Promotion is customer-facing commercial status and is separate from internal maturity.
Current launch set: Contact Shift Pro, Report Pro, MEasyMate Caption Studio.
Before PRE_RELEASE_AUDIT passes, use: `โปรโมชั่นเปิดตัว — โปรโมชั่นเปิดตัวช่วงแรก`.
