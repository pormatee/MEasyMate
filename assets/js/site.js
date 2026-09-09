document.addEventListener('DOMContentLoaded', () => {
  const btn = document.querySelector('[data-menu]');
  const menu = document.querySelector('[data-nav]');

  if (btn && menu) {
    btn.addEventListener('click', () => {
      const isOpen = menu.classList.toggle('open');
      btn.setAttribute('aria-expanded', String(isOpen));
    });

    menu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        menu.classList.remove('open');
        btn.setAttribute('aria-expanded', 'false');
      });
    });

    document.addEventListener('keydown', event => {
      if (event.key === 'Escape') {
        menu.classList.remove('open');
        btn.setAttribute('aria-expanded', 'false');
      }
    });
  }

  const cleanPath = window.location.pathname.replace(/\/+$/, '');
  const currentFile = cleanPath.split('/').pop() || 'index.html';
  const sectionFile = cleanPath.includes('/product/') ? 'products.html' : currentFile;

  document.querySelectorAll('[data-nav] a').forEach(link => {
    const rawHref = link.getAttribute('href') || '';
    if (!rawHref || /^(https?:|mailto:|tel:)/i.test(rawHref)) return;

    const href = rawHref.split('?')[0].split('#')[0];
    const targetFile = href.split('/').pop() || 'index.html';

    if (targetFile === sectionFile && !link.classList.contains('nav-cta')) {
      link.setAttribute('aria-current', 'page');
      link.style.background = '#eaf6fc';
      link.style.color = '#0879d9';
    }
  });

  const filterButtons = [...document.querySelectorAll('[data-filter]')];
  const cards = [...document.querySelectorAll('[data-category]')];

  const applyFilter = value => {
    if (!filterButtons.length || !cards.length) return;
    filterButtons.forEach(b => b.classList.toggle('active', b.dataset.filter === value));
    cards.forEach(card => {
      card.style.display = value === 'All' || card.dataset.category === value ? '' : 'none';
    });
  };

  filterButtons.forEach(filterBtn => {
    filterBtn.addEventListener('click', () => {
      applyFilter(filterBtn.dataset.filter || 'All');
    });
  });

  const requestedCategory = new URLSearchParams(window.location.search).get('category');
  if (requestedCategory && filterButtons.some(b => b.dataset.filter === requestedCategory)) {
    applyFilter(requestedCategory);
  }
});
