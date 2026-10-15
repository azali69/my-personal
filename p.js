const { chromium } = require('playwright');
(async()=>{ const b=await chromium.launch(); const p=await b.newPage();
  for(const [u,f] of [['https://www.muis.gov.sg/mosque/Our-Mosques/Mosque-Directory','muis_dir_pw.html'],['https://www.muis.gov.sg/mosque','muis_mosque_pw.html']]){
    try{ await p.goto(u,{waitUntil:'networkidle',timeout:60000}); await p.waitForTimeout(4000); require('fs').writeFileSync(f, await p.content()); }catch(e){ console.log(u,e.message); } }
  await b.close(); })();
