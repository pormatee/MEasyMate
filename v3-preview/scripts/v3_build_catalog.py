#!/usr/bin/env python3
"""Safe static V3.1 public product index from existing Product Registry.

No side effects outside hub/index.html & assets/js/v3-public-catalog.js.
No direct app links or commercial availability claims; new products fail closed.
"""
import json
import re
import sys
import html
from pathlib import Path

SCHEMA = 'measymate_v3_publication_approvals_1'
ID = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
HTMLFILE = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*\.html$')
PILLARS = ('AI', 'Work', 'Life', 'Growth')
MAX_PRODUCTS = 150
MAX_HOMEPAGE_SEARCH_PRODUCTS = 24
CATEGORIES = {'All': 'ทั้งหมด', 'AI': 'AI', 'Work': 'งาน', 'Life': 'ชีวิต', 'Growth': 'เติบโต'}


def verified_label(item):
    """Conservative presentation derived only from internal readiness gates.
    Marketing display labels never override internal readiness flags.
    """
    status = item.get('status', '')
    availability = item.get('availability', '')
    if status not in ('beta','developing','concept-preview','future-direction'):
        raise ValueError('UNKNOWN_STATUS')
    if availability in ('source-reverify',):
        return 'รอตรวจสอบความพร้อม'
    if status == 'concept-preview' or status == 'future-direction':
        return 'แนวคิด / อยู่ระหว่างพัฒนา'
    if status == 'developing' or availability == 'not-public':
        return 'กำลังพัฒนา'
    if availability in ('release-gated', 'pilot'):
        return 'ทดลองใช้แบบจำกัด / สอบถามก่อน'
    # A later actual release gate must explicitly verify unknown statuses.
    return 'รอตรวจสอบการเปิดใช้งาน'


def safe_text(value, field, maxlen):
    if not isinstance(value, str) or not value.strip() or len(value) > maxlen:
        raise ValueError('INVALID_' + field.upper())
    return value.strip()


def read_json(path):
    with path.open(encoding='utf-8') as file:
        return json.load(file)


def load_public(repo):
    registry = read_json(repo / 'data/platform-products.json')
    approval = read_json(repo / 'data/v3-publication.json')
    if registry.get('schema') != 'measymate_platform_product_registry_v1':
        raise ValueError('REGISTRY_SCHEMA_GATE')
    if approval.get('schema') != SCHEMA:
        raise ValueError('APPROVAL_SCHEMA_GATE')
    if approval.get('allow_direct_app_links') is not False:
        raise ValueError('DIRECT_APP_LINKS_FORBIDDEN')
    ids = approval.get('approved_product_ids')
    if not isinstance(ids, list) or not ids or len(ids) > MAX_PRODUCTS or len(ids) != len(set(ids)):
        raise ValueError('APPROVAL_LIST_GATE')
    products = registry.get('products')
    if not isinstance(products, list) or len(products) > MAX_PRODUCTS:
        raise ValueError('REGISTRY_LIST_GATE')
    by_id = {}
    for product in products:
        if not isinstance(product, dict) or not ID.fullmatch(str(product.get('id',''))):
            raise ValueError('PRODUCT_ID_GATE')
        pid = product['id']
        if pid in by_id:
            raise ValueError('DUPLICATE_PRODUCT_ID')
        by_id[pid] = product
    aliases = approval.get('product_keywords', {})
    if not isinstance(aliases, dict) or any(k not in ids for k in aliases):
        raise ValueError('KEYWORD_APPROVAL_GATE')
    result=[]
    for pid in ids:
        if not isinstance(pid,str) or not ID.fullmatch(pid) or pid not in by_id:
            raise ValueError('UNRECOGNIZED_PUBLICATION_ID')
        p = by_id[pid]
        filename = p.get('file', '')
        if not isinstance(filename,str) or not HTMLFILE.fullmatch(filename):
            raise ValueError('UNSAFE_DETAIL_PATH')
        if p.get('pillar') not in PILLARS:
            raise ValueError('INVALID_PILLAR')
        detail = repo / 'product' / filename
        if not detail.is_file():
            raise ValueError('DETAIL_PAGE_MISSING:' + filename)
        title = safe_text(p.get('name'), 'name', 110)
        public = p.get('public_presentation') or {}
        summary = safe_text(public.get('summary') or p.get('summary'), 'summary', 350)
        icon_path = p.get('icon_asset')
        if icon_path is not None:
            if not isinstance(icon_path,str) or not re.fullmatch(r'assets/project-icons/[a-z0-9-]+\.webp',icon_path):
                raise ValueError('INVALID_ICON_PATH')
            if not (repo / icon_path).is_file():
                raise ValueError('ICON_FILE_MISSING:'+icon_path)
        keywords = aliases.get(pid, [])
        if not isinstance(keywords, list) or len(keywords)>16 or any(
            not isinstance(x,str) or not x.strip() or len(x)>40 or '<' in x or '>' in x
            for x in keywords
        ):
            raise ValueError('UNSAFE_PRODUCT_KEYWORDS')
        # Every clickable Product points ONLY to a preexisting public detail page.
        result.append({'id':pid,'title':title,'pillar':p['pillar'],
                       'summary':summary,'label':verified_label(p),
                       'detail':'product/'+filename,'icon':icon_path or '', 'keywords':' '.join(keywords)})
    return result


def html_escape(x):
    return html.escape(x, quote=True)


def generate_html(products):
    cards=[]
    for p in products:
        image = ('<img src="../'+html_escape(p['icon'])+'" width="46" height="46" loading="lazy" decoding="async" alt="">') if p['icon'] else '<span aria-hidden="true">🧰</span>'
        searchable = (p['title']+' '+p['summary']+' '+p['pillar']+' '+p['label']+' '+p['keywords']).lower()
        cards.append('''<article class="v31-card" data-v31-card data-pillar="{pillar}" data-search="{search}">
<div class="v31-top">{image}<strong>{title}</strong></div>
<span class="v31-status">{label}</span><p>{summary}</p>
<a href="../{detail}" aria-label="ดูรายละเอียด {title}">ดูรายละเอียด →</a>
</article>'''.format(pillar=html_escape(p['pillar']),search=html_escape(searchable),image=image,title=html_escape(p['title']),label=html_escape(p['label']),summary=html_escape(p['summary']),detail=html_escape(p['detail'])))
    buttons=''.join('<button type="button" data-v31-category="{key}" aria-pressed="{pressed}">{label}</button>'.format(key=k,pressed='true' if k=='All' else 'false',label=html_escape(v)) for k,v in CATEGORIES.items())
    return '''<!doctype html>
<html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#0879d9"><title>Product Center | MEasyMate</title>
<meta name="description" content="เลือกเครื่องมือ MEasyMate จากความต้องการ พร้อมดูสถานะและรายละเอียดที่ตรวจสอบได้">
<link rel="canonical" href="https://measymate.com/hub/">
<meta name="robots" content="noindex,follow"><meta property="og:site_name" content="MEasyMate">
<meta property="og:title" content="MEasyMate Product Center"><meta property="og:url" content="https://measymate.com/hub/">
<link rel="icon" href="../assets/brand/measymate-logo.jpg">
<link rel="stylesheet" href="../assets/css/site.css"><link rel="stylesheet" href="../assets/css/v3-product-hub.css?v=1">
</head><body class="mm-v3-catalog">
<!-- AUTO-GENERATED BY scripts/v3_build_catalog.py — do not edit directly -->
<header class="container"><nav class="v31-hero"><a href="../index.html">← MEasyMate หน้าแรก</a><h1>Product Center</h1>
<p>ค้นหาเครื่องมือที่ช่วยเรื่องงาน ชีวิต และการเติบโต เราแสดงสถานะอย่างระมัดระวัง และไม่เปิดใช้งานผลิตภัณฑ์ที่ยังไม่ได้รับการยืนยัน</p></nav></header>
<main class="container">
<section class="v31-panel" aria-label="เครื่องมือฟรี"><h2>🎁 เริ่มจากเครื่องมือฟรี</h2>
<div class="v31-tools"><a href="../tools/deadline-checker.html">📅 ตรวจวันครบกำหนด<small>คำนวณวันคงเหลือในเครื่อง</small></a>
<a href="../tools/safe-payment-checklist.html">🛡️ เช็กลิสต์ก่อนโอนเงิน<small>ทบทวนรายการความเสี่ยงก่อนชำระเงิน</small></a></div></section>
<section class="v31-panel" aria-labelledby="v31-products-title">
<h2 id="v31-products-title">🧰 ผลิตภัณฑ์ MEasyMate</h2>
<div class="v31-controls" role="group" aria-label="ค้นหาและกรองผลิตภัณฑ์">
<input type="search" id="v31-search" aria-label="ค้นหาผลิตภัณฑ์" placeholder="ค้นหาชื่อหรือความต้องการ..." autocomplete="off">
{buttons}</div>
<p id="v31-count" role="status" aria-live="polite">แสดง {count} รายการ</p>
<div class="v31-grid" id="v31-grid">{cards}</div><p id="v31-empty" class="v31-empty" hidden>ไม่พบรายการที่ตรงกับคำค้น ลองเลือกหมวดทั้งหมด</p>
</section>
<p class="v31-warning">สถานะบนหน้านี้อ้างอิงข้อมูล Registry ที่ผ่านการตรวจสอบเบื้องต้น และไม่ถือเป็นการรับรองการจำหน่ายหรือสิทธิ์เข้าถึงแอปโดยตรง โปรดดูรายละเอียดสินค้าและติดต่อ MEasyMate เพื่อยืนยัน</p>
</main><footer class="container" style="padding:22px 0"><a href="../products.html">ดูรายการผลิตภัณฑ์เดิม</a> · <a href="../privacy.html">Privacy</a></footer>
<script>
(() => {{
'use strict';
const input=document.getElementById('v31-search');
const buttons=[...document.querySelectorAll('[data-v31-category]')];
const cards=[...document.querySelectorAll('[data-v31-card]')];
const count=document.getElementById('v31-count');
const empty=document.getElementById('v31-empty');
let selected='All';
function apply() {{
  const q=input.value.normalize('NFKC').toLocaleLowerCase('th').trim();
  let visible=0;
  cards.forEach(card=>{{
    const ok=(selected==='All'||card.dataset.pillar===selected)&&(!q||card.dataset.search.includes(q));
    card.hidden=!ok;if(ok)visible++;
  }});
  count.textContent='แสดง '+visible+' จาก '+cards.length+' รายการ';
  empty.hidden=visible!==0;
}}
buttons.forEach(btn=>btn.addEventListener('click',()=>{{
  selected=btn.dataset.v31Category;
  buttons.forEach(b=>b.setAttribute('aria-pressed',String(b===btn)));
  apply();
}}));
input.addEventListener('input',apply);
apply();
}})();
</script>
</body></html>
'''.format(buttons=buttons,count=len(products),cards='\n'.join(cards))


def generate_search(products):
    items=[{'title':p['title'], 'href':p['detail'],
            'description':'ดูรายละเอียด • '+p['label'],
            'tags':p['title']+' '+p['summary']+' '+p['pillar']+' '+p['keywords']} for p in products[:MAX_HOMEPAGE_SEARCH_PRODUCTS]]
    data=json.dumps(items,ensure_ascii=False,separators=(',',':'))
    data=data.replace('<','\\u003c').replace('>','\\u003e').replace('\u2028','\\u2028').replace('\u2029','\\u2029')
    return '/* AUTO-GENERATED BY scripts/v3_build_catalog.py */\nwindow.MEasyMateV3PublicProducts='+data+';\n'


def write_guarded(path, content):
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists() and 'AUTO-GENERATED BY scripts/v3_build_catalog.py' not in path.read_text(encoding='utf-8'):
        raise ValueError('EXISTING_UNMANAGED_OUTPUT:' + str(path))
    path.write_text(content,encoding='utf-8')


def main():
    if len(sys.argv)!=2:raise SystemExit('Usage: python scripts/v3_build_catalog.py REPO_ROOT')
    repo=Path(sys.argv[1]).resolve()
    try:
        products=load_public(repo)
        page=generate_html(products)
        search=generate_search(products)
        htmlpath=repo/'hub/index.html'
        searchpath=repo/'assets/js/v3-public-catalog.js'
        # Preflight both outputs before writing either.
        for target in (htmlpath,searchpath):
            if target.exists() and 'AUTO-GENERATED BY scripts/v3_build_catalog.py' not in target.read_text(encoding='utf-8'):
                raise ValueError('EXISTING_UNMANAGED_OUTPUT:' + str(target))
        write_guarded(htmlpath,page)
        write_guarded(searchpath,search)
        print('PUBLICATION_APPROVAL_GATE=PASS')
        print('DIRECT_LAUNCH_LINKS=0')
        print('PRODUCT_HUB_ITEMS='+str(len(products)))
        print('PRODUCT_HUB_GENERATE=PASS')
    except (ValueError,KeyError,TypeError,FileNotFoundError,json.JSONDecodeError) as exc:
        print('PRODUCT_HUB_GENERATE=BLOCKED',exc)
        raise SystemExit(2)

if __name__=='__main__':main()
