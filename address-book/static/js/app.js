/* Address Book - Frontend logic
   EE308FZ Software Engineering, Extreme Programming Assignment
   Communicates with the Flask backend under /api. */

let contacts = [];
let filter = 'all';
let searchQuery = '';
let editingId = null;

// ------------------------------ API helpers ------------------------------
async function api(url, options) {
  const response = await fetch(url, options);
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.error || ('Request failed: ' + response.status));
  }
  return data;
}

async function loadContacts() {
  const params = new URLSearchParams();
  if (filter === 'favorite') params.set('favorite', '1');
  if (searchQuery) params.set('q', searchQuery);
  contacts = await api('/api/contacts?' + params.toString());
  render();
}

// ------------------------------ Rendering ------------------------------
function chipList(items, emptyText) {
  if (!items || items.length === 0) {
    return '<span class="badge">' + emptyText + '</span>';
  }
  return '<div class="chips">' + items.map(v => `<span class="chip">${escapeHtml(v)}</span>`).join('') + '</div>';
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

function render() {
  const grid = document.getElementById('grid');
  const favCount = contacts.filter(c => c.bookmarked).length;
  document.getElementById('stat-total').textContent = contacts.length;
  document.getElementById('stat-fav').textContent = favCount;

  if (contacts.length === 0) {
    grid.innerHTML = '<div class="empty">No contacts yet. Click "+ Add Contact" to create one.</div>';
    return;
  }

  grid.innerHTML = contacts.map(c => `
    <article class="card">
      <div class="card-top">
        <button class="star ${c.bookmarked ? 'on' : ''}" title="Toggle favorite" onclick="toggleBookmark(${c.id})">
          ${c.bookmarked ? '★' : '☆'}
        </button>
        <div class="card-title">
          <h3>${escapeHtml(c.name)}</h3>
          ${c.note ? '<span class="badge">' + escapeHtml(c.note) + '</span>' : ''}
        </div>
        <div class="card-actions">
          <button class="icon-btn" title="Edit" onclick="openModal(${c.id})">✎</button>
          <button class="icon-btn danger" title="Delete" onclick="removeContact(${c.id})">🗑</button>
        </div>
      </div>

      <div class="method-group">
        <div class="method-row"><span class="method-label">Phone</span>${chipList(c.phones, '-')}</div>
        <div class="method-row"><span class="method-label">Email</span>${chipList(c.emails, '-')}</div>
        <div class="method-row"><span class="method-label">Social</span>${chipList(c.socials, '-')}</div>
      </div>

      ${c.address ? '<div class="address-line">📍 ' + escapeHtml(c.address) + '</div>' : ''}
    </article>
  `).join('');
}

// ------------------------------ Filter / search ------------------------------
function setFilter(mode) {
  filter = mode;
  document.getElementById('tab-all').classList.toggle('active', mode === 'all');
  document.getElementById('tab-fav').classList.toggle('active', mode === 'favorite');
  loadContacts();
}

function onSearch() {
  searchQuery = document.getElementById('search').value.trim();
  loadContacts();
}

// ------------------------------ Contact operations ------------------------------
async function toggleBookmark(id) {
  await api(`/api/contacts/${id}/bookmark`, { method: 'POST' });
  loadContacts();
}

async function removeContact(id) {
  const target = contacts.find(c => c.id === id);
  if (!confirm(`Delete contact "${target ? target.name : id}"?`)) return;
  await api(`/api/contacts/${id}`, { method: 'DELETE' });
  toast('Contact deleted');
  loadContacts();
}

// ------------------------------ Modal form ------------------------------
function addMethodLine(field, value = '') {
  const editor = document.getElementById('editor-' + field);
  const line = document.createElement('div');
  line.className = 'line';
  line.innerHTML = `
    <input type="text" value="${escapeHtml(value)}" placeholder="${placeholderFor(field)}" />
    <button type="button" class="line-remove" title="Remove">✕</button>
  `;
  line.querySelector('.line-remove').onclick = () => line.remove();
  editor.appendChild(line);
}

function placeholderFor(field) {
  if (field === 'phones') return 'e.g. 138-0000-0000';
  if (field === 'emails') return 'e.g. name@example.com';
  return 'e.g. WeChat: id';
}

function clearMethodEditor(field) {
  document.getElementById('editor-' + field).innerHTML = '';
}

function collectMethod(field) {
  return [...document.querySelectorAll('#editor-' + field + ' input')]
    .map(input => input.value.trim())
    .filter(Boolean);
}

function openModal(id = null) {
  editingId = id;
  document.getElementById('modal-title').textContent = id ? 'Edit Contact' : 'Add Contact';
  document.getElementById('contact-form').reset();
  clearMethodEditor('phones');
  clearMethodEditor('emails');
  clearMethodEditor('socials');

  if (id) {
    const contact = contacts.find(c => c.id === id);
    if (!contact) return;
    document.getElementById('f-name').value = contact.name;
    document.getElementById('f-bookmarked').checked = contact.bookmarked;
    document.getElementById('f-address').value = contact.address;
    document.getElementById('f-note').value = contact.note;
    contact.phones.forEach(v => addMethodLine('phones', v));
    contact.emails.forEach(v => addMethodLine('emails', v));
    contact.socials.forEach(v => addMethodLine('socials', v));
  }

  // Ensure every method group has at least one empty row.
  ['phones', 'emails', 'socials'].forEach(field => {
    if (document.querySelectorAll('#editor-' + field + ' input').length === 0) {
      addMethodLine(field);
    }
  });

  document.getElementById('modal-mask').classList.add('open');
}

function closeModal() {
  document.getElementById('modal-mask').classList.remove('open');
  editingId = null;
}

function onMaskClick(event) {
  if (event.target === document.getElementById('modal-mask')) closeModal();
}

async function onSave(event) {
  event.preventDefault();
  const payload = {
    name: document.getElementById('f-name').value.trim(),
    bookmarked: document.getElementById('f-bookmarked').checked,
    phones: collectMethod('phones'),
    emails: collectMethod('emails'),
    socials: collectMethod('socials'),
    address: document.getElementById('f-address').value.trim(),
    note: document.getElementById('f-note').value.trim(),
  };

  try {
    if (editingId) {
      await api(`/api/contacts/${editingId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      toast('Contact updated');
    } else {
      await api('/api/contacts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      toast('Contact added');
    }
    closeModal();
    loadContacts();
  } catch (err) {
    toast(err.message);
  }
}

// ------------------------------ Excel import / export ------------------------------
async function onImport(event) {
  const file = event.target.files[0];
  if (!file) return;
  const formData = new FormData();
  formData.append('file', file);
  try {
    const result = await api('/api/import', { method: 'POST', body: formData });
    toast(`Imported ${result.imported} contact(s)` + (result.skipped ? `, skipped ${result.skipped}` : ''));
    loadContacts();
  } catch (err) {
    toast(err.message);
  } finally {
    event.target.value = '';
  }
}

// ------------------------------ Toast ------------------------------
let toastTimer = null;
function toast(message) {
  const box = document.getElementById('toast');
  box.textContent = message;
  box.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => box.classList.remove('show'), 2600);
}

// Initial load
loadContacts();
