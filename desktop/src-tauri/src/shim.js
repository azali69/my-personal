/* Runs in the Windows app only (added before the page loads). The page itself is unchanged: this makes the two
   things a plain browser does for it work inside the app window: links that open elsewhere, and file downloads. */
(function () {
  const inv = (c, a) => window.__TAURI_INTERNALS__.invoke(c, a || {});
  const say = t => { try { if (typeof window.toast === 'function') window.toast(t); } catch (e) {} };
  // links to other sites open in the normal browser
  window.addEventListener('click', function (e) {
    const a = e.target && e.target.closest && e.target.closest('a[href]');
    if (!a || a.hasAttribute('download')) return;
    const h = a.href;
    if (!/^(https?:|mailto:|tel:)/i.test(h)) return;
    if (/^https?:/i.test(h) && a.origin === location.origin) return;
    e.preventDefault(); e.stopPropagation();
    inv('open_url', { url: h }).catch(() => {});
  }, true);
  const wo = window.open;
  window.open = function (u) { if (u && /^(https?:|mailto:|tel:)/i.test(String(u))) { inv('open_url', { url: String(u) }).catch(() => {}); return null; } return wo.apply(window, arguments); };
  // a file the page offers for download (the backup) opens a Save as box
  const click = HTMLAnchorElement.prototype.click;
  HTMLAnchorElement.prototype.click = function () {
    if (this.hasAttribute('download') && /^blob:/i.test(this.href)) {
      const name = this.getAttribute('download') || 'file';
      fetch(this.href).then(r => r.blob()).then(b => new Promise(res => { const f = new FileReader(); f.onload = () => res(String(f.result).split(',')[1]); f.readAsDataURL(b); }))
        .then(b64 => inv('save_file', { name, b64 }))
        .then(dir => { say(dir ? 'Saved in ' + dir : 'Not saved'); })
        .catch(() => say('Could not save the file'));
      return;
    }
    return click.apply(this, arguments);
  };
})();
