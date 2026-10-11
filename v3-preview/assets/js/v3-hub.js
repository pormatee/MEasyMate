/* MEasyMate V3: deterministic need-to-tool lookup, no AI or network required */
(() => {
  'use strict';
  const form = document.querySelector('[data-v3-search]');
  if (!form) return;
  const input = form.querySelector('input[type="search"]');
  const output = document.querySelector('[data-v3-results]');
  const freeItems = [
    {title:'ตรวจวันครบกำหนด', href:'tools/deadline-checker.html', description:'ประกันรถ ภาษีรถ เอกสาร และวันสำคัญ', tags:'ประกัน ภาษี รถ ต่อทะเบียน วันหมดอายุ ครบกำหนด เตือน เอกสาร deadline'},
    {title:'เช็กลิสต์ก่อนโอนเงิน', href:'tools/safe-payment-checklist.html', description:'ตรวจรายการเสี่ยงก่อนจ่ายเงิน', tags:'โอน เงิน มิจฉาชีพ โกง หลอก จ่าย บัญชี ซื้อสินค้า ปลอดภัย scam'},
    {title:'Easy Guides', href:'learn.html', description:'เรียนรู้เรื่อง AI, Privacy และมือถือ', tags:'เรียนรู้ ความรู้ คู่มือ ai ภาษา เรียน สอน เริ่มต้น guide'},
    {title:'ศูนย์รวมเครื่องมือ MEasyMate', href:'hub/index.html', description:'ดูรายละเอียดและสถานะผลิตภัณฑ์', tags:'เครื่องมือ แอปพลิเคชัน app product measy mate'}
  ];
  // This index is generated offline from the explicitly approved public Product Registry.
  // Fail closed to core free tools if a generated index is absent or malformed.
  const productItems = Array.isArray(window.MEasyMateV3PublicProducts)
    ? window.MEasyMateV3PublicProducts.filter(p => p && typeof p.title === 'string' && typeof p.href === 'string' && /^product\/[a-z0-9-]+\.html$/.test(p.href))
    : [];
  const items = freeItems.concat(productItems);
  const normalize = value => value.normalize('NFKC').trim().toLocaleLowerCase('th');
  const draw = () => {
    const query = normalize(input.value);
    output.replaceChildren();
    if (!query) { output.hidden = true; return; }
    const words = query.split(/\s+/).filter(Boolean);
    const matches = items.map(item => {
      const bag = normalize(item.title+' '+item.description+' '+item.tags);
      return {item, score:words.reduce((n,w)=>n+(bag.includes(w)?1:0),0)+(normalize(item.title).includes(query)?2:0)};
    }).filter(entry => entry.score>0).sort((a,b)=>b.score-a.score).slice(0,5);
    const summary = document.createElement('p');
    summary.textContent = matches.length?'เครื่องมือและข้อมูลที่เกี่ยวข้อง':'ยังไม่พบคำที่ตรงกัน ลองใช้คำสั้น ๆ หรือดูเครื่องมือทั้งหมด';
    output.append(summary);
    const ul = document.createElement('ul');
    (matches.length?matches:[{item:freeItems[3]}]).forEach(({item}) => {
      const li=document.createElement('li'); const a=document.createElement('a');
      a.href=item.href; a.textContent=item.title;
      const sub=document.createElement('small'); sub.textContent=item.description;
      a.append(sub); li.append(a); ul.append(li);
    });
    output.append(ul); output.hidden=false;
  };
  form.addEventListener('submit',event=>{event.preventDefault();draw();});
  input.addEventListener('input',draw);
})();
