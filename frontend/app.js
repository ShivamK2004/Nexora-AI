let conversationId = null;
let pendingFiles = [];
const $ = (id) => document.getElementById(id);
const panels = ['chat', 'knowledge', 'memory', 'agents'];

function welcomeMarkup() {
  return `<div class="welcome"><div class="orb">✳</div><p class="eyebrow">WELCOME TO NEXORA</p><h2>Your workspace for ideas.</h2><p>Ask a question, upload a file or photo, and keep every conversation in your history.</p><div class="suggestions"><button>Explain how a large language model works</button><button>Help me understand a PDF</button><button>Review this screenshot</button></div></div>`;
}

function showPanel(name) {
  panels.forEach((p) => $(`panel-${p}`).classList.toggle('active', p === name));
  document.querySelectorAll('.nav-item').forEach((b) => b.classList.toggle('active', b.dataset.panel === name));
  $('page-title').textContent = { chat: 'Assistant', knowledge: 'Knowledge base', memory: 'Memory', agents: 'Agent workspace' }[name];
  if (name === 'knowledge') loadDocuments();
  if (name === 'memory') loadMemories();
}

document.querySelectorAll('.nav-item').forEach((b) => b.addEventListener('click', () => showPanel(b.dataset.panel)));

async function api(url, options = {}) {
  const headers = { ...(options.headers || {}) };
  const savedKey = sessionStorage.getItem('nexora-key');
  if (savedKey) headers['X-Nexora-Key'] = savedKey;
  if (options.body && !(options.body instanceof FormData)) headers['Content-Type'] = 'application/json';
  const res = await fetch(url, { ...options, headers });
  let data = {};
  try { data = await res.json(); } catch { /* non-JSON error */ }
  if (!res.ok) throw new Error(data.detail || `Request failed (${res.status})`);
  return data;
}

function appendAttachments(target, attachments = []) {
  if (!attachments.length) return;
  const list = document.createElement('div');
  list.className = 'message-attachments';
  attachments.forEach((item) => {
    const url = item.preview_url || item.url;
    if (item.kind === 'image' || (item.mime_type || '').startsWith('image/')) {
      const link = document.createElement('a');
      link.href = url;
      link.target = '_blank';
      link.rel = 'noreferrer';
      link.className = 'image-attachment';
      const img = document.createElement('img');
      img.src = url;
      img.alt = item.filename || 'Uploaded image';
      link.append(img);
      list.append(link);
    } else {
      const link = document.createElement('a');
      link.href = url;
      link.target = '_blank';
      link.rel = 'noreferrer';
      link.className = 'file-attachment';
      link.textContent = `▤  ${item.filename || 'Attached file'}`;
      list.append(link);
    }
  });
  target.append(list);
}

function addMessage(role, text, attachments = [], citations = []) {
  const box = document.createElement('div');
  box.className = `message ${role}`;
  const avatar = document.createElement('div');
  avatar.className = 'avatar';
  avatar.textContent = role === 'user' ? 'You' : 'N';
  const content = document.createElement('div');
  content.className = 'message-content';
  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.textContent = text;
  content.append(bubble);
  appendAttachments(content, attachments);
  if (citations.length) {
    const c = document.createElement('div');
    c.className = 'citations';
    c.textContent = 'Sources: ' + citations.map((x) => `[${x.index}] ${x.filename}`).join(' · ');
    content.append(c);
  }
  box.append(avatar, content);
  $('messages').append(box);
  $('messages').scrollTop = $('messages').scrollHeight;
  return { element: box, bubble };
}

function clearPendingFiles() {
  pendingFiles.forEach((item) => URL.revokeObjectURL(item.preview_url));
  pendingFiles = [];
  renderPendingFiles();
  $('chat-file-input').value = '';
}

function renderPendingFiles() {
  const area = $('attachment-preview');
  area.innerHTML = '';
  pendingFiles.forEach((item, index) => {
    const chip = document.createElement('div');
    chip.className = 'pending-chip';
    if (item.file.type.startsWith('image/')) {
      const img = document.createElement('img');
      img.src = item.preview_url;
      img.alt = item.file.name;
      chip.append(img);
    } else {
      const icon = document.createElement('span');
      icon.className = 'pending-file-icon';
      icon.textContent = '▤';
      chip.append(icon);
    }
    const name = document.createElement('span');
    name.textContent = item.file.name;
    const remove = document.createElement('button');
    remove.type = 'button';
    remove.textContent = '×';
    remove.title = 'Remove attachment';
    remove.addEventListener('click', () => {
      URL.revokeObjectURL(item.preview_url);
      pendingFiles.splice(index, 1);
      renderPendingFiles();
    });
    chip.append(name, remove);
    area.append(chip);
  });
}

function queueFiles(fileList) {
  const accepted = /\.(pdf|txt|md|markdown|csv|json|py|sql|png|jpe?g|webp|gif)$/i;
  for (const file of fileList) {
    if (!accepted.test(file.name)) {
      alert(`Unsupported file type: ${file.name}`);
      continue;
    }
    if (file.size > 10 * 1024 * 1024) {
      alert(`${file.name} is larger than 10 MB.`);
      continue;
    }
    if (pendingFiles.length >= 5) {
      alert('You can attach up to 5 files per message.');
      break;
    }
    if (pendingFiles.some((x) => x.file.name === file.name && x.file.size === file.size)) continue;
    pendingFiles.push({ file, preview_url: URL.createObjectURL(file) });
  }
  renderPendingFiles();
}

async function sendMessage(text) {
  text = text.trim();
  if (!text && !pendingFiles.length) return;
  const selectedFiles = [...pendingFiles];
  const displayAttachments = selectedFiles.map((x) => ({
    filename: x.file.name,
    mime_type: x.file.type,
    kind: x.file.type.startsWith('image/') ? 'image' : 'document',
    preview_url: x.preview_url,
  }));
  const welcome = document.querySelector('.welcome');
  if (welcome) welcome.remove();
  const sentMessage = addMessage('user', text || 'Please analyze the attached file(s).', displayAttachments);
  $('chat-input').value = '';
  $('send-button').disabled = true;
  $('attach-button').disabled = true;
  const waiting = addMessage('assistant', 'Nexora is thinking…');
  const form = new FormData();
  form.append('message', text);
  if (conversationId) form.append('conversation_id', conversationId);
  selectedFiles.forEach((item) => form.append('files', item.file, item.file.name));
  try {
    const data = await api('/api/chat', { method: 'POST', body: form });
    conversationId = data.conversation_id;
    waiting.bubble.textContent = data.answer;
    const oldAttachmentBlock = sentMessage.element.querySelector('.message-attachments');
    if (oldAttachmentBlock) oldAttachmentBlock.remove();
    appendAttachments(sentMessage.element.querySelector('.message-content'), data.attachments || []);
    if (data.citations?.length) {
      const c = document.createElement('div');
      c.className = 'citations';
      c.textContent = 'Sources: ' + data.citations.map((x) => `[${x.index}] ${x.filename}`).join(' · ');
      waiting.bubble.parentElement.append(c);
    }
    $('mode-pill').textContent = `${(data.provider || 'mock').toUpperCase()} · ${data.model || ''}`;
    $('chat-hint').textContent = `Provider: ${data.provider} · ${data.model || ''}`;
    loadConversations();
  } catch (e) {
    waiting.bubble.textContent = 'Error: ' + e.message;
  } finally {
    $('send-button').disabled = false;
    $('attach-button').disabled = false;
    clearPendingFiles();
    $('chat-input').focus();
  }
}

$('send-button').addEventListener('click', () => sendMessage($('chat-input').value));
$('chat-input').addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage($('chat-input').value); }
});
$('attach-button').addEventListener('click', () => $('chat-file-input').click());
$('chat-file-input').addEventListener('change', (e) => queueFiles(e.target.files));
$('chat-input').addEventListener('paste', (e) => {
  const images = [...(e.clipboardData?.items || [])].filter((item) => item.type.startsWith('image/')).map((item) => item.getAsFile()).filter(Boolean);
  if (images.length) queueFiles(images);
});
$('messages').addEventListener('dragover', (e) => { e.preventDefault(); $('messages').classList.add('drag-over'); });
$('messages').addEventListener('dragleave', () => $('messages').classList.remove('drag-over'));
$('messages').addEventListener('drop', (e) => { e.preventDefault(); $('messages').classList.remove('drag-over'); if (e.dataTransfer?.files) queueFiles(e.dataTransfer.files); });
$('new-chat').addEventListener('click', () => startNewChat());
document.addEventListener('click', (e) => {
  const suggestion = e.target.closest('.suggestions button');
  if (suggestion) sendMessage(suggestion.textContent);
});

function startNewChat() {
  conversationId = null;
  clearPendingFiles();
  $('messages').innerHTML = welcomeMarkup();
  document.querySelectorAll('.conversation-item').forEach((x) => x.classList.remove('active'));
  showPanel('chat');
  $('chat-input').focus();
}

async function loadConversations() {
  const list = $('conversation-list');
  try {
    const items = await api('/api/conversations');
    const query = $('history-search').value.trim().toLowerCase();
    list.innerHTML = '';
    const filtered = items.filter((x) => x.title.toLowerCase().includes(query));
    if (!filtered.length) {
      const empty = document.createElement('div');
      empty.className = 'history-empty';
      empty.textContent = query ? 'No matching conversations.' : 'Your conversations will appear here.';
      list.append(empty);
      return;
    }
    filtered.forEach((item) => {
      const row = document.createElement('div');
      row.className = 'conversation-row';
      const open = document.createElement('button');
      open.className = 'conversation-item' + (item.id === conversationId ? ' active' : '');
      open.textContent = item.title || 'New conversation';
      open.title = item.title;
      open.addEventListener('click', () => openConversation(item.id));
      const del = document.createElement('button');
      del.className = 'delete-conversation';
      del.textContent = '×';
      del.title = 'Delete conversation';
      del.addEventListener('click', async () => {
        if (!confirm('Delete this conversation and its uploaded attachments?')) return;
        try {
          await api(`/api/conversations/${item.id}`, { method: 'DELETE' });
          if (conversationId === item.id) startNewChat();
          loadConversations();
        } catch (err) { alert(err.message); }
      });
      row.append(open, del);
      list.append(row);
    });
  } catch (e) {
    list.textContent = 'Could not load chat history: ' + e.message;
  }
}

async function openConversation(id) {
  try {
    const data = await api(`/api/conversations/${id}`);
    conversationId = id;
    $('messages').innerHTML = '';
    if (!data.messages.length) $('messages').innerHTML = welcomeMarkup();
    data.messages.forEach((m) => addMessage(m.role, m.content, m.attachments || []));
    showPanel('chat');
    loadConversations();
  } catch (e) { alert('Could not open conversation: ' + e.message); }
}
$('refresh-chats').addEventListener('click', loadConversations);
$('history-search').addEventListener('input', loadConversations);

async function loadDocuments() {
  try {
    const docs = await api('/api/documents');
    $('documents-list').innerHTML = '';
    if (!docs.length) $('documents-list').textContent = 'No documents indexed yet.';
    docs.forEach((d) => {
      const el = document.createElement('div'); el.className = 'item';
      const info = document.createElement('div');
      const name = document.createElement('strong'); name.textContent = d.filename;
      const sub = document.createElement('small'); sub.textContent = `${d.chunks} chunks · ${new Date(d.created_at + 'Z').toLocaleString()}`;
      info.append(name, sub);
      const del = document.createElement('button'); del.textContent = 'Delete';
      del.onclick = async () => { await api('/api/documents/' + d.id, { method: 'DELETE' }); loadDocuments(); };
      el.append(info, del); $('documents-list').append(el);
    });
  } catch (e) { $('documents-list').textContent = e.message; }
}
$('file-input').addEventListener('change', async (e) => {
  const file = e.target.files[0]; if (!file) return;
  $('upload-status').textContent = 'Uploading and indexing…';
  const form = new FormData(); form.append('file', file);
  try {
    const data = await api('/api/documents', { method: 'POST', body: form });
    $('upload-status').textContent = `Indexed ${data.filename}: ${data.chunks} chunks${data.embedding ? ' · embeddings enabled' : ''}.`;
    loadDocuments();
  } catch (err) { $('upload-status').textContent = 'Upload failed: ' + err.message; }
  e.target.value = '';
});
$('refresh-docs').addEventListener('click', loadDocuments);

async function loadMemories() {
  try {
    const items = await api('/api/memories'); $('memory-list').innerHTML = '';
    if (!items.length) $('memory-list').textContent = 'No saved memories yet.';
    items.forEach((m) => {
      const el = document.createElement('div'); el.className = 'item';
      const info = document.createElement('div'); const name = document.createElement('strong'); name.textContent = m.content;
      const sub = document.createElement('small'); sub.textContent = m.category; info.append(name, sub);
      const del = document.createElement('button'); del.textContent = 'Forget';
      del.onclick = async () => { await api('/api/memories/' + m.id, { method: 'DELETE' }); loadMemories(); };
      el.append(info, del); $('memory-list').append(el);
    });
  } catch (e) { $('memory-list').textContent = e.message; }
}
$('memory-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  try {
    await api('/api/memories', { method: 'POST', body: JSON.stringify({ content: $('memory-content').value, category: $('memory-category').value }) });
    $('memory-content').value = ''; loadMemories();
  } catch (err) { alert(err.message); }
});
$('refresh-memory').addEventListener('click', loadMemories);

$('agent-form').addEventListener('submit', async (e) => {
  e.preventDefault(); const out = $('agent-result'); out.classList.remove('hidden'); out.textContent = 'Agent is working…';
  try {
    const data = await api('/api/agents/run', { method: 'POST', body: JSON.stringify({ task: $('agent-task').value, agent: $('agent-type').value || null }) });
    out.textContent = `Agent: ${data.agent}\nRun ID: ${data.id}\n\n${data.result}`;
  } catch (err) { out.textContent = 'Error: ' + err.message; }
});

$('set-key').addEventListener('click', () => {
  const key = prompt('Enter the Nexora local API access key (API_KEY in .env). This is not your Gemini API key. Leave blank to clear it:', sessionStorage.getItem('nexora-key') || '');
  if (key === null) return;
  if (key.trim()) sessionStorage.setItem('nexora-key', key.trim()); else sessionStorage.removeItem('nexora-key');
  location.reload();
});

function renderProviderStatus(data) {
  const provider = data.provider || data.active_provider || 'mock';
  const model = data.model || data.configured_model || '';
  $('provider-select').value = provider;
  $('mode-pill').textContent = `${provider.toUpperCase()} · ${model}`;
  $('provider-status').textContent = data.provider_configured === false
    ? 'Gemini selected · API key missing'
    : `API online · ${provider}`;
  $('chat-hint').textContent = data.provider_message || `Provider: ${provider} · ${model}`;
  if (data.provider_configured === false) $('chat-hint').textContent += ' Add GEMINI_API_KEY to .env, then restart Nexora.';
}

$('provider-select').addEventListener('change', async (event) => {
  const select = event.currentTarget;
  const nextProvider = select.value;
  select.disabled = true;
  $('provider-status').textContent = 'Switching provider…';
  try {
    const data = await api('/api/provider', {
      method: 'POST',
      body: JSON.stringify({ provider: nextProvider }),
    });
    renderProviderStatus(data);
    if (data.provider_configured === false) {
      alert('Gemini is selected, but no API key is configured. Add GEMINI_API_KEY to your .env file.');
    }
  } catch (error) {
    alert('Could not change provider: ' + error.message);
    try { renderProviderStatus(await api('/api/health')); } catch { /* keep current status */ }
  } finally {
    select.disabled = false;
  }
});

(async () => {
  try {
    const h = await api('/api/health');
    renderProviderStatus(h);
  } catch (e) {
    $('provider-status').textContent = 'API unavailable';
    $('chat-hint').textContent = e.message;
  }
  loadConversations();
})();
