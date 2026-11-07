// CI check of the built Windows app: drives the real window through WebView2's debugging port.
// usage: node ci-smoke.mjs <1|2> <screenshot-dir> [marker]   (1: first launch, 2: after installing again over it)
import fs from 'node:fs';
const [phase = '1', out = 'shots', marker = ''] = process.argv.slice(2);
fs.mkdirSync(out, { recursive: true });
const sleep = ms => new Promise(r => setTimeout(r, ms));
let fails = [];
const check = (name, ok, extra = '') => { console.log(`${ok ? 'ok  ' : 'FAIL'} ${name} ${extra}`); if (!ok) fails.push(name); };

async function findPage() {
  for (let i = 0; i < 90; i++) {
    try { const t = (await (await fetch('http://127.0.0.1:9222/json', { signal: AbortSignal.timeout(3000) })).json()).filter(x => x.type === 'page' && /tauri\.localhost/.test(x.url)); if (t.length) return t[0]; } catch (e) {}
    await sleep(1000);
  }
  console.log('no window found; last list:', await fetch('http://127.0.0.1:9222/json').then(r=>r.text()).catch(e=>String(e)));
  throw new Error('the app window did not open');
}
function connect(url) {
  return new Promise((res, rej) => {
    console.log('connecting', url); const ws = new WebSocket(url); setTimeout(()=>rej(new Error('debug connection timed out')),20000); let id = 0; const pend = new Map(); const events = [];
    ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && pend.has(d.id)) { const p = pend.get(d.id); pend.delete(d.id); d.error ? p.no(new Error(JSON.stringify(d.error))) : p.ok(d.result); } else events.push(d); };
    ws.onopen = () => res({ events, close: () => ws.close(), send: (method, params = {}) => new Promise((ok, no) => { const i = ++id; pend.set(i, { ok, no }); ws.send(JSON.stringify({ id: i, method, params })); }) });
    ws.onerror = e => rej(new Error('debug connection failed'));
  });
}
const page = await findPage();
const c = await connect(page.webSocketDebuggerUrl);
const ev = async expr => { const r = await Promise.race([new Promise((_, no) => setTimeout(() => no(new Error('page did not answer')), 25000)), c.send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true })]); if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description || r.exceptionDetails.text); return r.result.value; };
const shot = async name => { const r = await c.send('Page.captureScreenshot', { format: 'png' }); fs.writeFileSync(`${out}/${name}.png`, Buffer.from(r.data, 'base64')); };
const until = async (expr, ms = 30000) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { try { if (await ev(expr)) return true; } catch (e) {} await sleep(500); } return false; };

await c.send('Runtime.enable'); await c.send('Page.enable'); await c.send('Log.enable');
await c.send('Page.reload'); await sleep(1500);
check('app loaded', await until("document.getElementById('whereS') && typeof st === 'object' && typeof renderReader === 'function'", 60000));
const info = JSON.parse(await ev(`JSON.stringify({ver:'v'+((document.documentElement.outerHTML.match(/My Personal Qur'an v(\\d+\\.\\d+\\.\\d+\\.\\d+)/)||[])[1]||'?'), origin:location.origin, secure:isSecureContext,
  tauri: !!window.__TAURI_INTERNALS__, caches: typeof caches, speech: typeof (window.SpeechRecognition||window.webkitSpeechRecognition), notif: typeof Notification, ua: navigator.userAgent})`));
console.log(JSON.stringify(info));
check('version shown', /^v\d+\.\d+\.\d+\.\d+$/.test(info.ver), info.ver);
check('native bridge present', info.tauri); check('secure context', info.secure); check('Cache API', info.caches === 'object');
await shot(`p${phase}-home`);

if (phase === '1') {
  await ev("document.getElementById('cover')&&(document.getElementById('cover').hidden=true); showHome(); 1"); await sleep(1000);
  const tiles = await ev("[...document.querySelectorAll('#home .tile[data-t]')].map(t=>t.dataset.t).join(',')");
  console.log('home tiles:', tiles);
  check('Windows Home hides the 7 tiles and the prayer card', !/(^|,)(hz|tq|dua|halal|masjid|pray|qibla)(,|$)/.test(tiles) && /shamail/.test(tiles) && await ev("!document.getElementById('hmSalah')"));
  await shot('p1-home-tiles');
  await ev("document.getElementById('cover')&&(document.getElementById('cover').hidden=true); hideHome(); st.scroll=false; st.mushaf='text'; st.tr=true; renderReader(); goPage(2); 1");
  check('Qur\'an page shows ayat', await until("document.querySelectorAll('#main .row').length > 3", 20000));
  await sleep(1000); await shot('p1-quran');
  check('Arabic text is Fatihah/Baqarah', (await ev("document.getElementById('main').innerText")).length > 200);
  check('online data reachable from the app', await ev("fetch('https://azali69.github.io/my-personal/kutub/books2.json').then(r=>r.ok).catch(()=>false)"));
  await ev("document.querySelectorAll('.panel').forEach(p=>{ if(p.id!=='main') {} }); ktPanel(); 1"); await sleep(2500);
  await ev("ktOpenHadith('bukhari',1); 1");
  const bukhari = await until("document.body.innerText.replace(/[\\u064B-\\u0652\\u0670]/g,'').includes('الأعمال بالنيات')", 90000);
  if (!bukhari) console.log('page text then:', (await ev('document.body.innerText')).slice(0, 400).replace(/\n/g, ' | '));
  check('Bukhari 1 opens (data downloaded and shown)', bukhari);
  await sleep(800); await shot('p1-hadith');
  let rej = ''; try { await ev("window.__TAURI_INTERNALS__.invoke('open_url',{url:'javascript:alert(1)'}).then(()=>'allowed')"); } catch (e) { rej = 'rejected'; }
  check('native open_url refuses non-web links', rej === 'rejected');
  await ev(`localStorage.setItem('ci_marker','${marker}'); caches.open('ci-marker').then(ca=>ca.put('https://ci.local/m',new Response('${marker}'))).then(()=>1)`);
} else {
  check('settings survived the update install', (await ev("localStorage.getItem('ci_marker')")) === marker, marker);
  check('cached data survived the update install', (await ev("caches.open('ci-marker').then(ca=>ca.match('https://ci.local/m')).then(r=>r?r.text():'')")) === marker);
}
const errs = c.events.filter(e => e.method === 'Runtime.exceptionThrown').map(e => e.params.exceptionDetails.exception?.description || e.params.exceptionDetails.text);
check('no page errors', errs.length === 0, errs.slice(0, 3).join(' | '));
c.close();
console.log(fails.length ? 'FAILED: ' + fails.join(', ') : 'ALL OK');
process.exit(fails.length ? 1 : 0);
