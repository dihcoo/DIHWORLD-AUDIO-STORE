/* DIH document viewer v1
   Every link that opens a PDF, text file, image, or standalone guide page opens in a full-screen
   viewer with an X (close) button instead of leaving the site in a bare browser tab.
   - X button, Esc key, and the browser Back button all close it.
   - "Open in new tab" is kept for people who want the raw file.
   - Ctrl/Cmd/Shift/middle-click, external links, downloads (.zip) and #anchors are left alone. */
(function () {
  'use strict';
  var inFrame = false;
  try { inFrame = window.self !== window.top; } catch (e) { inFrame = true; }

  /* Inside the viewer the page's own X would be a second X: hide it. */
  if (inFrame) {
    var st = document.createElement('style');
    st.textContent = '.dih-close{display:none!important}';
    (document.head || document.documentElement).appendChild(st);
  }

  function isViewable(a) {
    if (!a || !a.href || a.hasAttribute('download')) return false;
    var u;
    try { u = new URL(a.href, location.href); } catch (e) { return false; }
    if (u.origin !== location.origin) return false;
    if (u.pathname === location.pathname && u.hash && !u.search) return false;
    var p = u.pathname.toLowerCase();
    if (/\.(pdf|txt|png|jpe?g|webp|gif)$/.test(p)) return true;
    /* standalone guide pages (not the site's own sections) */
    if (/\/downloads\/.+\.html$/.test(p)) return true;
    return false;
  }

  var overlay, frame, titleEl, newTab, closeBtn, lastFocus, pushed = false, prevOverflow = '';

  function build() {
    if (overlay) return;
    var css = document.createElement('style');
    css.textContent =
      '.dihv{position:fixed;inset:0;z-index:2147483600;display:none;flex-direction:column;background:rgba(3,8,7,.94)}' +
      '.dihv.open{display:flex}' +
      '.dihv-bar{flex:0 0 auto;display:flex;align-items:center;gap:12px;padding:10px 14px;background:#07100f;border-bottom:1px solid rgba(240,201,107,.35)}' +
      '.dihv-title{flex:1 1 auto;min-width:0;color:#f0c96b;font:600 14px/1.3 system-ui,-apple-system,Segoe UI,sans-serif;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}' +
      '.dihv-new{flex:0 0 auto;color:#f0c96b;font:500 13px/1 system-ui,-apple-system,sans-serif;text-decoration:none;border:1px solid rgba(240,201,107,.5);border-radius:999px;padding:9px 14px}' +
      '.dihv-new:hover,.dihv-new:focus-visible{background:#f0c96b;color:#07100f;outline:none}' +
      '.dihv-x{flex:0 0 auto;width:44px;height:44px;padding:0;display:grid;place-items:center;border-radius:50%;border:1px solid #f0c96b;background:rgba(7,16,15,.92);color:#f0c96b;cursor:pointer;-webkit-tap-highlight-color:transparent}' +
      '.dihv-x svg{width:18px;height:18px;display:block}' +
      '.dihv-x:hover,.dihv-x:focus-visible{background:#f0c96b;color:#07100f;outline:none}' +
      '.dihv-x:focus-visible{box-shadow:0 0 0 3px rgba(240,201,107,.45)}' +
      '.dihv-frame{flex:1 1 auto;width:100%;border:0;background:#fff;-webkit-overflow-scrolling:touch}' +
      '@media (max-width:720px){.dihv-bar{padding:8px 10px;gap:8px}.dihv-x{width:40px;height:40px}.dihv-new{padding:8px 11px}}' +
      '@media print{.dihv{display:none!important}}';
    document.head.appendChild(css);

    overlay = document.createElement('div');
    overlay.className = 'dihv';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-label', 'Document viewer');
    overlay.innerHTML =
      '<div class="dihv-bar"><div class="dihv-title"></div>' +
      '<a class="dihv-new" target="_blank" rel="noopener">Open in new tab ↗</a>' +
      '<button type="button" class="dihv-x" aria-label="Close document" title="Close (Esc)">' +
      '<svg viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M3 3l12 12M15 3L3 15"/></svg></button></div>' +
      '<iframe class="dihv-frame" title="Document"></iframe>';
    document.body.appendChild(overlay);
    frame = overlay.querySelector('.dihv-frame');
    titleEl = overlay.querySelector('.dihv-title');
    newTab = overlay.querySelector('.dihv-new');
    closeBtn = overlay.querySelector('.dihv-x');
    closeBtn.addEventListener('click', close);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && overlay.classList.contains('open')) { e.preventDefault(); close(); }
    });
    window.addEventListener('popstate', function () {
      if (overlay.classList.contains('open')) { pushed = false; hide(); }
    });
  }

  function nameFor(u, label) {
    if (label) return label;
    var f = decodeURIComponent(u.pathname.split('/').pop() || '').replace(/\.[a-z0-9]+$/i, '');
    return f.replace(/[_]+/g, ' ').replace(/\s+/g, ' ').trim();
  }

  function open(href, label) {
    build();
    var u = new URL(href, location.href);
    var src = u.href;
    if (/\.pdf$/i.test(u.pathname) && !u.hash) src += '#view=FitH';
    if (!overlay.classList.contains('open')) {
      lastFocus = document.activeElement;
      prevOverflow = document.documentElement.style.overflow;
    }
    titleEl.textContent = nameFor(u, label);
    newTab.href = u.href;
    frame.src = src;
    document.documentElement.style.overflow = 'hidden';
    var already = overlay.classList.contains('open');
    overlay.classList.add('open');
    if (!already) {
      try { history.pushState({ dihViewer: 1 }, '', location.href); pushed = true; } catch (e) { pushed = false; }
    }
    closeBtn.focus();
  }

  function hide() {
    if (!overlay) return;
    overlay.classList.remove('open');
    frame.src = 'about:blank';
    document.documentElement.style.overflow = prevOverflow;
    if (lastFocus && lastFocus.focus) { try { lastFocus.focus(); } catch (e) {} }
  }

  function close() {
    if (pushed) { history.back(); } else { hide(); }
  }

  document.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target.closest && e.target.closest('a[href]');
    if (!isViewable(a)) return;
    e.preventDefault();
    var label = a.getAttribute('data-viewer-title') || '';
    var t = inFrame ? window.top : window;
    if (t.DIHViewer) t.DIHViewer.open(a.href, label); else open(a.href, label);
  }, true);

  window.DIHViewer = { open: open, close: close };
})();
