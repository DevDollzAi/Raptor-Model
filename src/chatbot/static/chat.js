/* Raptor AI Chatbot — Frontend Script
   Handles UI interactions, API calls, and Markdown rendering
   ============================================================ */

(function () {
  'use strict';

  // ── State ──────────────────────────────────────────────────────
  let sessionId = null;

  // ── DOM refs ────────────────────────────────────────────────────
  const form            = document.getElementById('chatForm');
  const input           = document.getElementById('messageInput');
  const messagesEl      = document.getElementById('messages');
  const sendBtn         = document.getElementById('sendBtn');
  const clearBtn        = document.getElementById('clearBtn');
  const typingIndicator = document.getElementById('typingIndicator');

  // ── Boot ────────────────────────────────────────────────────────
  renderWelcome();
  restoreSession();

  // ── Event listeners ─────────────────────────────────────────────
  form.addEventListener('submit', handleSubmit);

  // Auto-resize textarea
  input.addEventListener('input', () => {
    input.style.height = 'auto';
    input.style.height = Math.min(input.scrollHeight, 160) + 'px';
  });

  // Submit on Enter (Shift+Enter = newline)
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      form.dispatchEvent(new Event('submit'));
    }
  });

  clearBtn.addEventListener('click', handleClear);

  // Quick-topic buttons
  document.querySelectorAll('.topic-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      const msg = btn.dataset.msg;
      if (msg) sendMessage(msg);
    });
  });

  // ── Session persistence ─────────────────────────────────────────
  function restoreSession() {
    const stored = sessionStorage.getItem('raptor_session_id');
    if (stored) sessionId = stored;
  }

  function saveSession(id) {
    sessionId = id;
    sessionStorage.setItem('raptor_session_id', id);
  }

  // ── Submit handler ──────────────────────────────────────────────
  async function handleSubmit(e) {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;
    sendMessage(text);
  }

  async function sendMessage(text) {
    // Clear welcome if visible
    const welcome = messagesEl.querySelector('.empty-state');
    if (welcome) welcome.remove();

    appendMessage('user', text);
    input.value = '';
    input.style.height = 'auto';
    setSending(true);

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, session_id: sessionId }),
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.error || `HTTP ${res.status}`);
      }

      const data = await res.json();
      saveSession(data.session_id);
      appendMessage('assistant', data.response);
    } catch (err) {
      appendMessage('assistant', `⚠️ Error: ${err.message}`);
    } finally {
      setSending(false);
    }
  }

  // ── Clear handler ───────────────────────────────────────────────
  async function handleClear() {
    if (!sessionId) {
      messagesEl.innerHTML = '';
      renderWelcome();
      return;
    }

    try {
      await fetch('/api/clear', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId }),
      });
    } catch (_) { /* ignore */ }

    messagesEl.innerHTML = '';
    renderWelcome();
  }

  // ── UI helpers ──────────────────────────────────────────────────
  function setSending(isSending) {
    sendBtn.disabled = isSending;
    typingIndicator.hidden = !isSending;
    if (isSending) messagesEl.appendChild(typingIndicator);
    if (!isSending) typingIndicator.remove();
  }

  function appendMessage(role, content) {
    const wrap = document.createElement('div');
    wrap.className = `message ${role}`;

    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    avatar.textContent = role === 'user' ? '👤' : '⚔️';

    const bubble = document.createElement('div');
    bubble.className = 'bubble';
    bubble.innerHTML = renderMarkdown(content);

    wrap.appendChild(avatar);
    wrap.appendChild(bubble);
    messagesEl.appendChild(wrap);
    scrollToBottom();
  }

  function renderWelcome() {
    const el = document.createElement('div');
    el.className = 'empty-state';
    el.innerHTML = `
      <div class="icon">⚔️</div>
      <h2>Sovereign Shield Assistant</h2>
      <p>Ask me anything about the Raptor Model — Bio-Hash, BARK, Inevitability Gate, C=0 Proof Chains, and more.</p>
      <p style="font-size:.78rem;opacity:.6;margin-top:.5rem">Try: <em>"What is the Sovereign Shield?"</em> or click a topic on the left.</p>
    `;
    messagesEl.appendChild(el);
  }

  function scrollToBottom() {
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  // ── Lightweight Markdown renderer ───────────────────────────────
  function renderMarkdown(text) {
    // Escape HTML first (except intentional HTML)
    let html = escapeHtml(text);

    // Fenced code blocks ```lang\n...\n```
    html = html.replace(/```(\w*)\n([\s\S]*?)```/g, (_, lang, code) => {
      return `<pre><code class="language-${lang}">${code.trimEnd()}</code></pre>`;
    });

    // Inline code `...`
    html = html.replace(/`([^`\n]+)`/g, '<code>$1</code>');

    // Bold **...**
    html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

    // Italic *...* (single asterisk only; ** is already replaced above)
    html = html.replace(/\*([^*\n]+)\*/g, '<em>$1</em>');

    // Headings (## H2, ### H3, #### H4)
    html = html.replace(/^#{3} (.+)$/gm, '<h3>$1</h3>');
    html = html.replace(/^#{2} (.+)$/gm, '<h2>$1</h2>');
    html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');

    // Horizontal rule
    html = html.replace(/^---$/gm, '<hr>');

    // Tables (simple GFM-style)
    html = renderTables(html);

    // Unordered list items (• or -)
    html = html.replace(/^[•\-]\s+(.+)$/gm, '<li>$1</li>');
    html = html.replace(/(<li>[\s\S]*?<\/li>)/g, '<ul>$1</ul>');
    // Collapse consecutive <ul> wrappers
    html = html.replace(/<\/ul>\s*<ul>/g, '');

    // Numbered list items
    html = html.replace(/^\d+\.\s+(.+)$/gm, '<li>$1</li>');

    // Paragraphs: blank-line separated blocks that aren't block elements
    const blockTags = /^<(h[1-6]|ul|ol|li|pre|hr|table)/;
    const lines = html.split('\n');
    const result = [];
    let para = [];
    for (const line of lines) {
      if (line.trim() === '') {
        if (para.length) { result.push(`<p>${para.join(' ')}</p>`); para = []; }
      } else if (blockTags.test(line.trim())) {
        if (para.length) { result.push(`<p>${para.join(' ')}</p>`); para = []; }
        result.push(line);
      } else {
        para.push(line);
      }
    }
    if (para.length) result.push(`<p>${para.join(' ')}</p>`);

    return result.join('\n');
  }

  function renderTables(html) {
    // Match GFM table blocks
    return html.replace(
      /((?:^[^\n]*\|[^\n]*\n)+)/gm,
      (block) => {
        const rows = block.trim().split('\n').filter(Boolean);
        if (rows.length < 2) return block;
        const isSep = (r) => /^\|?[\s\-:|]+\|/.test(r);
        if (!isSep(rows[1])) return block;

        const parseRow = (r) =>
          r.replace(/^\||\|$/g, '').split('|').map((c) => c.trim());

        const head = parseRow(rows[0]);
        const body = rows.slice(2).map(parseRow);

        let t = '<table><thead><tr>';
        head.forEach((h) => { t += `<th>${h}</th>`; });
        t += '</tr></thead><tbody>';
        body.forEach((cells) => {
          t += '<tr>';
          cells.forEach((c) => { t += `<td>${c}</td>`; });
          t += '</tr>';
        });
        t += '</tbody></table>';
        return t;
      }
    );
  }

  function escapeHtml(str) {
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }
})();
