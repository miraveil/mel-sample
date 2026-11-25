'use strict';
(async () => {
  // Old links from the first edition continue to resolve to dedicated articles.
  const legacy = new URLSearchParams(location.search).get('story');
  let stories = [];
  let storageAvailable = true;
  let saved = [];
  try {
    const response = await fetch('assets/stories.json');
    if (!response.ok) throw new Error('Stories unavailable');
    stories = await response.json();
  } catch {
    const note = document.querySelector('#storage-note');
    if (note) note.textContent = 'The reading list could not load. Refresh this page to try again.';
  }
  if (legacy && stories.some(s => s.id === legacy)) {
    location.replace(`story-${encodeURIComponent(legacy)}.html`);
    return;
  }
  try {
    const value = JSON.parse(localStorage.getItem('offbeat-saved') || '[]');
    saved = Array.isArray(value) ? [...new Set(value.filter(id => stories.some(s => s.id === id)))] : [];
  } catch { storageAvailable = false; }
  function renderSaved() {
    document.querySelectorAll('.saved-count').forEach(el => el.textContent = saved.length);
    document.querySelectorAll('[data-save]').forEach(button => {
      const active = saved.includes(button.dataset.save);
      button.textContent = active ? 'Remove from reading list' : 'Save story';
      button.setAttribute('aria-pressed', String(active));
    });
    const container = document.querySelector('#saved-stories');
    if (!container) return;
    container.replaceChildren();
    if (!saved.length) {
      const empty = document.createElement('div'); empty.className = 'saved-empty';
      const h2 = document.createElement('h2'); h2.textContent = 'Your next favourite is still out there.';
      const p = document.createElement('p'); p.textContent = 'Open an article and select “Save story” to keep it here.';
      empty.append(h2,p); container.append(empty);
    }
    for (const id of saved) {
      const story = stories.find(s => s.id === id);
      const article = document.createElement('article'); article.className = 'saved-card';
      const imageLink = document.createElement('a'); imageLink.href = `story-${id}.html`; imageLink.setAttribute('aria-label',`Read ${story.title}`);
      const image = document.createElement('img'); image.src = `assets/images/${story.image}`; image.alt = ''; imageLink.append(image);
      const copy = document.createElement('div');
      const meta = document.createElement('p'); meta.className = 'card-meta'; meta.textContent = `${story.category} · ${story.minutes} min read`;
      const h2 = document.createElement('h2'); const link = document.createElement('a'); link.href=imageLink.href; link.textContent=story.title; h2.append(link);
      const p = document.createElement('p'); p.textContent=story.desc;
      const remove = document.createElement('button'); remove.className='share-button'; remove.textContent='Remove'; remove.setAttribute('aria-label',`Remove ${story.title} from reading list`);
      remove.onclick=()=>{ toggle(id); const next=container.querySelector('button') || document.querySelector('.saved-page > a'); next?.focus(); };
      copy.append(meta,h2,p,remove); article.append(imageLink,copy); container.append(article);
    }
    if (!storageAvailable) document.querySelector('#storage-note').textContent = 'Browser storage is unavailable. This list lasts for this page visit only.';
  }
  function toggle(id) {
    saved=saved.includes(id)?saved.filter(x=>x!==id):[...saved,id];
    try { localStorage.setItem('offbeat-saved',JSON.stringify(saved)); } catch { storageAvailable=false; }
    renderSaved();
    const status=document.querySelector('.action-status');
    if(status) status.textContent=storageAvailable?(saved.includes(id)?'Added to your reading list.':'Removed from your reading list.'):'Browser storage is unavailable. This change lasts for this page visit only.';
  }
  document.querySelectorAll('[data-save]').forEach(button=>button.onclick=()=>toggle(button.dataset.save));
  renderSaved();
  window.addEventListener('storage',event=>{ if(event.key==='offbeat-saved'||event.key===null){try{const value=JSON.parse(event.newValue||'[]');saved=Array.isArray(value)?value.filter(id=>stories.some(s=>s.id===id)):[];}catch{saved=[];}renderSaved();} });
  document.querySelector('[data-share]')?.addEventListener('click',async()=>{
    const status=document.querySelector('.action-status');
    try { await navigator.clipboard.writeText(location.href); status.textContent='Article link copied.'; }
    catch { status.replaceChildren(); const label=document.createElement('label');label.textContent='Copy this article link: ';const field=document.createElement('input');field.readOnly=true;field.value=location.href;field.setAttribute('aria-label','Article link');label.append(field);status.append(label);field.focus();field.select(); }
  });
  const browse=document.querySelector('.browse');
  if(!browse)return;
  const grid=browse.querySelector('.story-grid');
  const cards=[...grid.children];
  const input=browse.querySelector('input[type=search]');
  const sort=browse.querySelector('#sort');
  const pageSize=Number(browse.dataset.pageSize);
  let category='All',topic='All topics',page=1;
  input.value=new URLSearchParams(location.search).get('q')||'';
  function render(){
    const query=input.value.trim().toLowerCase();
    const filtered=cards.filter(card=>(category==='All'||card.dataset.category===category)&&(topic==='All topics'||card.dataset.topic===topic)&&card.dataset.search.includes(query));
    if(sort.value==='title')filtered.sort((a,b)=>a.querySelector('h3').textContent.localeCompare(b.querySelector('h3').textContent));
    if(sort.value==='short')filtered.sort((a,b)=>Number(a.dataset.minutes)-Number(b.dataset.minutes));
    const pages=Math.max(1,Math.ceil(filtered.length/pageSize));page=Math.min(page,pages);
    cards.forEach(card=>card.hidden=true);
    filtered.forEach((card,i)=>{grid.append(card);card.hidden=i<(page-1)*pageSize||i>=page*pageSize;});
    browse.querySelector('.empty').hidden=filtered.length>0;
    browse.querySelector('#result-status').textContent=`${filtered.length} ${filtered.length===1?'story':'stories'} found`;
    browse.querySelector('#page-status').textContent=`Page ${page} of ${pages}`;
    browse.querySelector('#previous').disabled=page===1;
    browse.querySelector('#next').disabled=page===pages;
    browse.querySelector('.pagination').hidden=pages===1;
    const url=new URL(location.href);if(query)url.searchParams.set('q',input.value);else url.searchParams.delete('q');history.replaceState(null,'',url);
  }
  cards.forEach(card=>{const id=card.querySelector('a').getAttribute('href').replace('story-','').replace('.html','');card.dataset.minutes=stories.find(s=>s.id===id)?.minutes||2;});
  browse.querySelectorAll('.filter').forEach(button=>button.onclick=()=>{
    if(button.dataset.filter)category=button.dataset.filter;
    if(button.dataset.topicFilter)topic=button.dataset.topicFilter;
    browse.querySelectorAll('.filter').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));page=1;render();
  });
  input.addEventListener('input',()=>{page=1;render();});sort.addEventListener('change',()=>{page=1;render();});
  browse.querySelector('#reset').onclick=()=>{input.value='';sort.value='editorial';category='All';topic='All topics';page=1;browse.querySelectorAll('.filter').forEach((b,i)=>b.setAttribute('aria-pressed',String(i===0)));render();input.focus();};
  for(const [id,delta] of [['previous',-1],['next',1]])browse.querySelector('#'+id).onclick=()=>{page+=delta;render();browse.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});browse.querySelector('#latest-title').setAttribute('tabindex','-1');browse.querySelector('#latest-title').focus({preventScroll:true});};
  render();
})();
