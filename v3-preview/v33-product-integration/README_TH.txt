MEasyMate.com V3.3 — Product Integration QA Kit

IMPORTANT: QA ONLY • NO PUSH • NO DEPLOY • NO SALE CLAIM

Run on Termux (after downloading the ZIP to /sdcard/Download):

    pkg install python unzip -y
    mkdir -p "$HOME/MEASYMATE_V33_KIT"
    unzip -q -o /sdcard/Download/MEASYMATE_V33_PRODUCT_INTEGRATION_QA.zip -d "$HOME/MEASYMATE_V33_KIT"
    bash "$HOME/MEASYMATE_V33_KIT/MEASYMATE_V33_QA/run.sh" "$HOME/MEasyMate-web"

If your local Website repo is in another directory, replace "$HOME/MEasyMate-web" with its actual path.

To view Android preview after installation:

    bash "$HOME/MEASYMATE_V33_KIT/MEASYMATE_V33_QA/start-preview.sh" "$HOME/MEasyMate-web"

Use Chrome Android to open:
    http://127.0.0.1:8877/v33-product-integration/preview.html
    http://127.0.0.1:8877/v33-product-integration/android-field-gate.html
    http://127.0.0.1:8877/          (original V3.2 on local repo, if installed)

Expected local script result: V33_LOCAL_GATE=PASS, STAGING_ONLY=YES
Manual Android Field Gate is still UNVERIFIED until completed in browser.

Notes:
- The eight HTTP 200 statuses are the user's known baseline; no network probe occurs in this kit.
- This kit intentionally does NOT alter or back up any V2 file because it does not touch those paths.
- Existing staging dir is never overwritten. The installer exits safely if it already exists.
- The local test report is saved in v33-product-integration/V33_LOCAL_REPORT.txt, and copied to /sdcard/Download if permitted.
- Android download report can be shared back to this chat.
