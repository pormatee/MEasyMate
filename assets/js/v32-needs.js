/* V3.2 local-only, deterministic routing. No network, cookies or data collection. */
(() => {
  'use strict';
  const normalize = x => String(x || '').normalize('NFKC').trim().toLocaleLowerCase('th');
  const allowedHref = x => /^(?:product\/[a-z0-9-]+\.html|guides\/[a-z0-9-]+\.html|tools\/[a-z0-9-]+\.html|learn\.html|hub\/index\.html)$/.test(x);
  const scoreItem = (item, query) => {
    if (!query) return 1;
    const terms = normalize(query).split(/\s+/).filter(Boolean);
    const title = normalize(item.title);
    const tags = normalize([item.title,item.description,item.tags].join(' '));
    const exact = title.includes(normalize(query)) ? 4 : 0;
    return exact + terms.reduce((n, term) => n + (tags.includes(term) ? 2 : 0), 0);
  };
  const rank = (items, query, category) => items
    .map((item, i) => ({item, i, score:scoreItem(item,query)}))
    .filter(x => x.score>0 && (!category || category==='all' || (Array.isArray(x.item.categories) && x.item.categories.includes(category))))
    .sort((a,b) => b.score-a.score || a.i-b.i)
    .map(x => x.item);
  // Pure functions exposed solely for package tests; no remote service or AI judgment.
  window.MEasyMateV32Core={normalize,allowedHref,scoreItem,rank};
  const input = document.querySelector('[data-v32-query]');
  const results = document.querySelector('[data-v32-results]');
  const count = document.querySelector('[data-v32-count]');
  if (!input || !results || !count) return;
  const items = Array.isArray(window.MEasyMateV32Index)
    ? window.MEasyMateV32Index.filter(x => x && typeof x.title==='string' && typeof x.href==='string' && allowedHref(x.href)) : [];
  const buttons = [...document.querySelectorAll('[data-v32-cat]')];
  let category='all';
  function draw() {
    const q=input.value.trim();
    const found=rank(items,q,category);
    results.replaceChildren();
    count.textContent='พบ '+found.length+' รายการ'+(q?' สำหรับ “'+q.slice(0,60)+'”':'');
    if (!found.length) {
      const p=document.createElement('p');p.className='v32-empty';
      p.textContent='ยังไม่พบเครื่องมือที่ตรงกับคำค้นนี้ ลองใช้คำสั้น ๆ หรือดู Product Center';
      const a=document.createElement('a');a.href='../hub/index.html';a.textContent=' ดูผลิตภัณฑ์ทั้งหมด →';
      p.append(a);results.append(p);return;
    }
    found.slice(0,24).forEach(item => {
      const card=document.createElement('article'); card.className='v32-result';
      const label=document.createElement('span'); label.className='v32-label';label.textContent=item.label;
      const h=document.createElement('h3');h.textContent=item.title;
      const p=document.createElement('p');p.textContent=item.description;
      const a=document.createElement('a');a.href='../'+item.href;a.textContent=item.kind==='product'?'ดูรายละเอียดผลิตภัณฑ์ →':'เปิดใช้งาน / อ่านเพิ่มเติม →';
      card.append(label,h,p,a);results.append(card);
    });
  }
  document.querySelector('[data-v32-form]').addEventListener('submit',event=>{event.preventDefault();draw()});
  input.addEventListener('input',draw);
  buttons.forEach(button=>button.addEventListener('click',()=>{
    category=button.dataset.v32Cat;
    buttons.forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
    draw();
  }));
  draw();
})();
