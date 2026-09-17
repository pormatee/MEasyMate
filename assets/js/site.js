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


/* P6 COMBINED PRODUCT FILTER START */
(() => {
  const productGrid = document.querySelector('.product-grid');
  const cards = [...document.querySelectorAll('.product-card[data-product-id]')];
  const statusButtons = [...document.querySelectorAll('[data-status-filter]')];
  if (!productGrid || !cards.length || !statusButtons.length) return;

  let activeStatus = null;

  const getActiveCategory = () => {
    const active =
      document.querySelector('[data-filter].active') ||
      document.querySelector('[data-filter].is-active') ||
      document.querySelector('[data-category-filter].active') ||
      document.querySelector('[data-category-filter].is-active');
    if (!active) return 'All';
    return active.getAttribute('data-filter') ||
           active.getAttribute('data-category-filter') ||
           'All';
  };

  const applyCombinedFilter = () => {
    const category = getActiveCategory();
    cards.forEach(card => {
      const cardCategory = card.getAttribute('data-category') || 'All';
      const cardStatus = card.getAttribute('data-status') || '';
      const categoryOK = category === 'All' || category === cardCategory;
      const statusOK = !activeStatus || activeStatus === cardStatus;
      card.hidden = !(categoryOK && statusOK);
    });
  };

  statusButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const value = btn.getAttribute('data-status-filter');
      if (activeStatus === value) {
        activeStatus = null;
        btn.classList.remove('is-active');
        btn.setAttribute('aria-pressed', 'false');
      } else {
        activeStatus = value;
        statusButtons.forEach(b => {
          b.classList.toggle('is-active', b === btn);
          b.setAttribute('aria-pressed', b === btn ? 'true' : 'false');
        });
      }
      applyCombinedFilter();
    });
    btn.setAttribute('aria-pressed', 'false');
  });

  // Existing category filter remains responsible for category state.
  // Re-apply after its click handler has run so category + status work together.
  document.addEventListener('click', (event) => {
    if (event.target.closest('[data-filter], [data-category-filter]')) {
      setTimeout(applyCombinedFilter, 0);
    }
  });

  // If browser navigation/query-string changes the category state.
  window.addEventListener('popstate', () => setTimeout(applyCombinedFilter, 0));

  applyCombinedFilter();
})();
/* P6 COMBINED PRODUCT FILTER END */
