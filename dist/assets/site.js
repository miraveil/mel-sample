'use strict';
(async () => {
  const dialog = document.querySelector('#story-dialog');
  const content = document.querySelector('#article-content');
  const savedContainer = document.querySelector('#saved-stories');
  let stories;
  try {
    const response = await fetch('assets/stories.json');
    if (!response.ok) throw new Error('Could not load stories');
    stories = await response.json();
  } catch {
    stories = [];
    savedContainer.textContent = 'Stories could not be loaded. Refresh this page to try again.';
  }
  let saved = [];
  let storageAvailable = true;
  try { const data = JSON.parse(localStorage.getItem('offbeat-saved') || '[]'); saved = Array.isArray(data) ? data.filter(id => stories.some(s => s.id === id)) : []; }
  catch { storageAvailable = false; }
  const page = location.pathname.split('/').pop() || 'index.html';
  function updateSaved() {
    document.querySelectorAll('.saved-count').forEach(el => el.textContent = saved.length);
    if (!stories.length) return;
    savedContainer.replaceChildren();
    if (!saved.length) savedContainer.textContent = 'Nothing saved yet. Open a story and select “Save story”.';
    saved.forEach(id => {
      const story = stories.find(s => s.id === id);
      const link = document.createElement('a'); link.href = `${page}?story=${id}`; link.textContent = story.title;
      savedContainer.append(link);
    });
  }
  function openStory(id) {
    const story = stories.find(s => s.id === id);
    content.replaceChildren();
    const title = document.createElement('h2'); title.id = 'dialog-title';
    if (!story) {
      title.textContent = stories.length ? 'Story not found' : 'Unable to load this story';
      const message = document.createElement('p'); message.textContent = stories.length ? 'Close this window to explore the available stories.' : 'Check your connection and refresh the page to try again.';
      content.append(title, message);
    } else {
      title.textContent = story.title;
      const meta = document.createElement('p'); meta.className = 'card-meta'; meta.textContent = `${story.category} · The Offbeat edit · 3 min read`;
      const image = document.createElement('img'); image.src = `assets/images/${story.image}`; image.alt = story.desc;
      content.append(meta, title, image);
      story.body.forEach(text => { const p = document.createElement('p'); p.textContent = text; content.append(p); });
      const save = document.createElement('button'); save.className = 'button';
      const refreshLabel = () => { save.textContent = saved.includes(id) ? 'Remove from reading list' : 'Save story'; save.setAttribute('aria-pressed', String(saved.includes(id))); };
      refreshLabel();
      save.onclick = () => {
        saved = saved.includes(id) ? saved.filter(s => s !== id) : [...saved, id];
        try { localStorage.setItem('offbeat-saved', JSON.stringify(saved)); } catch { storageAvailable = false; }
        refreshLabel(); updateSaved();
        note.textContent = storageAvailable ? 'Illustrative editorial content created for this demo.' : 'Saved for this visit only. Browser storage is unavailable.';
      };
      const note = document.createElement('p'); note.className = 'demo-note'; note.setAttribute('role', 'status'); note.textContent = 'Illustrative editorial content created for this demo.';
      content.append(save, note);
    }
    if (!dialog.open) dialog.showModal();
    dialog.scrollTop = 0;
  }
  let origin = null;
  document.addEventListener('click', event => {
    const link = event.target.closest('a');
    if (!link || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || event.button !== 0) return;
    const url = new URL(link.href);
    if (url.origin !== location.origin || url.pathname !== location.pathname || !url.searchParams.has('story')) return;
    event.preventDefault(); origin = link;
    history.pushState({story:true}, '', url); openStory(url.searchParams.get('story'));
  });
  function closeArticle() {
    dialog.close();
    const url = new URL(location.href); url.searchParams.delete('story'); history.replaceState(null, '', url);
    if (origin?.isConnected) origin.focus();
  }
  document.querySelector('.close-button').onclick = closeArticle;
  dialog.addEventListener('cancel', event => { event.preventDefault(); closeArticle(); });
  dialog.addEventListener('click', event => { const r = dialog.getBoundingClientRect(); if (event.target === dialog && (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom)) closeArticle(); });
  window.addEventListener('popstate', () => { const id = new URLSearchParams(location.search).get('story'); if (id) openStory(id); else dialog.close(); });
  updateSaved();
  const id = new URLSearchParams(location.search).get('story'); if (id) openStory(id);
  let category = 'All';
  const input = document.querySelector('input[type=search]');
  function filter() {
    let count = 0;
    const query = input.value.trim().toLowerCase();
    document.querySelectorAll('.story-card').forEach(card => { const show = (category === 'All' || card.dataset.category === category) && card.dataset.search.includes(query); card.hidden = !show; count += Number(show); });
    document.querySelector('.empty').hidden = count > 0;
    document.querySelector('#result-status').textContent = `${count} ${count === 1 ? 'story' : 'stories'} found`;
  }
  document.querySelectorAll('.filter').forEach(button => button.onclick = () => { category = button.dataset.filter; document.querySelectorAll('.filter').forEach(b => b.setAttribute('aria-pressed', String(b === button))); filter(); });
  input.addEventListener('input', filter);
  document.querySelector('#reset').onclick = () => { input.value = ''; document.querySelector('[data-filter=All]').click(); input.focus(); };
  filter();
})();
