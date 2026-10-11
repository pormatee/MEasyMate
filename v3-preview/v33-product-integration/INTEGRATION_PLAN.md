# MEasyMate.com V3.3 — Product Integration (safe staged plan)

Checkpoint: 2026-10-10. Website main and Products main matched supplied baseline on targeted GitHub comparison. The V3.2 local source has NOT been read; local gate remains unverified on this kit until run on Android.

## Boundaries

- This kit installs **only** `v33-product-integration/` in a local Website working copy. It never changes `index.html`, `products.html`, `assets/`, or Product source code.
- It never runs `git add`, `git commit`, `git push`, `git fetch`, merge or deployment.
- Registry is **internal QA**, not a production list. Eight URL baseline results (HTTP 200) come from the user's Termux check, not new probing. HTTP 200 does not imply a functional app.
- Source availability per product is UNVERIFIED because paths and relevant source versions were not mapped individually. Release approval is false (no approval evidence), not a claim a product was rejected.

## After staging

1. Run read-only LOCAL QA (`run.sh`). Check original V3.2 on Android via the site root and the 2 free tools; enter results in `android-field-gate.html`.
2. Verify each product's source mapping and owner/version **without modifying the product repo**. Check functional behavior and collect individual evidence.
3. Update the registry and evidence, retaining separate Source / HTTP / Function / Release gates.
4. Only when V3.2 Android Gate passes, implement a V3.3 Product Hub adapter as an **isolated V3 module**. Public purchase/trial/launch links are disabled by default. Do not include Factory Daily or Sale Center automatically.
5. Test responsive design, V2 preservation, route correctness, audit existing promotional copy that must not migrate from V2.
6. PRE_GIT_AUDIT PASS -> request explicit approval -> commit/push on the selected branch -> PRE_RELEASE_AUDIT PASS -> request production approval -> deploy. No auto merge/push/deploy.

## URL behavior

The staging preview shows QA links to the eight reachable URL baselines. They are explicitly for manual testers and do not imply public release. A production hub must NOT display these as public launch/buy/trial links unless functional verification, release approval and release audit have passed.

## Field Gate

The Android form is manual, and passing the local script is NOT an Android PASS. The manual report is stored in a downloaded text file and should be attached to the project conversation for review. If any field is unchecked, Android Field Gate stays UNVERIFIED/FAIL rather than PASS.
