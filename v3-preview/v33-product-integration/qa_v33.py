#!/usr/bin/env python3
"""Non-network, non-mutating V3.3 QA checks (except writing report into QA staging dir)."""
import json
import re
import sys
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse

STAGE = Path(__file__).resolve().parent
EXPECTED = ('caption-studio', 'contact-shift', 'hanasu', 'horajarn',
            'money', 'qingyun', 'report-pro', 'talknow')

class MarkupInspector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.meta = []
    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        if tag == 'meta':
            self.meta.append(dict(attrs))

def main(repo):
    checks=[]
    def check(label, condition, note=''):
        checks.append((label, bool(condition), note))
    registry_path=STAGE/'product-registry.v3.3.json'
    data=json.loads(registry_path.read_text(encoding='utf-8'))
    products=data.get('products', [])
    check('REGISTRY_PRODUCT_COUNT', len(products)==8)
    ids=[p.get('id','') for p in products]
    check('REGISTRY_IDS', tuple(ids)==EXPECTED, repr(ids))
    check('REGISTRY_URLS', all(
        p.get('url') == f'https://app.measymate.com/{p.get("id","")}/'
        and urlparse(p.get('url','')).scheme=='https' for p in products))
    check('REGISTRY_4_GATE_FIELDS',all(all(k in p for k in
        ('source_available','http_reachable','function_verified','release_approved')) for p in products))
    check('HTTP_BASELINE_8', all(p.get('http_reachable')=='PASS' for p in products),
          'Uses previously supplied Termux baseline; no network requests')
    check('SOURCE_EVIDENCE_NOT_INVENTED', all(p.get('source_available') in ('UNVERIFIED','PASS') for p in products))
    check('UNVERIFIED_FUNCTION_GUARD',all(
        p.get('function_verified') in ('UNVERIFIED','PASS') and
        (p.get('function_verified')=='PASS' or not p.get('public_cta_enabled',False)) for p in products))
    check('RELEASE_GUARD',all(not p.get('release_approved',False) and not p.get('public_cta_enabled',False) for p in products))
    check('EXCLUSIONS',set(data.get('excluded_from_public_integration',[]))=={'factory-daily','sale-center'})
    check('NO_PUBLIC_LISTING',data.get('policy',{}).get('public_listing_enabled') is False)
    for name in ('preview.html','android-field-gate.html'):
        path=STAGE/name
        parser=MarkupInspector();parser.feed(path.read_text(encoding='utf-8'))
        check(name.upper().replace('-','_')+'_HTML',
              'html' in parser.tags and 'viewport' in [x.get('name') for x in parser.meta]
              and 'noindex,nofollow' in [x.get('content') for x in parser.meta],
              'Manual JS and Android behavior remain field-unverified')
    preview=(STAGE/'preview.html').read_text(encoding='utf-8')
    check('NO_PUBLIC_BUY_CTA', 'public_cta_enabled=true' not in preview and
          'เปิด URL เพื่อตรวจสอบ (QA เท่านั้น)' in preview)
    check('REAL_LOGO_ONLY', '../assets/brand/measymate-logo.jpg' in preview)
    check('WEBSITE_DIRECTORY', repo.is_dir())
    home=repo/'index.html';productsh=repo/'products.html'
    check('WEBSITE_MAIN_FILES',home.is_file() and productsh.is_file())
    if home.is_file():
        txt=home.read_text(encoding='utf-8')
        check('V2_HOME_STRUCTURAL_MARKERS',all(tag in txt for tag in (
            'home-v2','v2-hero','v2-banner','assets/brand/measymate-banner.jpg')),
            'Static preservation check only; needs Android visual confirmation')
    v3js=repo/'assets/js/v3-hub.js'
    v32='PRESENT' if v3js.is_file() else 'NOT_FOUND_AT_EXPECTED_PATH'
    local_report=[
      'MEASYMATE V3.3 LOCAL QA REPORT',
      'NETWORK_PROBE=NO',
      'STAGING_ONLY=YES',
      'GIT_ADD_COMMIT_PUSH_DEPLOY=NO',
      f'REPO={repo}',
      f'V32_JS={v32}',
      'V32_ANDROID_FIELD_GATE=UNVERIFIED',
      'PRODUCT_FUNCTION_VERIFIED=UNVERIFIED',
      'CUSTOMER_RELEASE=NO',
    ]
    for label,result,note in checks:
        local_report.append(f'{label}={"PASS" if result else "FAIL"}'+(f' // {note}' if note else ''))
    gate='PASS' if all(x[1] for x in checks) else 'FAIL'
    local_report.append(f'V33_LOCAL_GATE={gate}')
    text='\n'.join(local_report)+'\n'
    out=STAGE/'V33_LOCAL_REPORT.txt';out.write_text(text,encoding='utf-8')
    print(text)
    return 0 if gate=='PASS' else 2

if __name__=='__main__':
    if len(sys.argv)!=2:
        print('Usage: python qa_v33.py WEBSITE_REPO_PATH',file=sys.stderr);sys.exit(2)
    sys.exit(main(Path(sys.argv[1]).expanduser().resolve()))
