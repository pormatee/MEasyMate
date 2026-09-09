document.addEventListener('DOMContentLoaded', () => {
  const btn = document.querySelector('[data-menu]');
  const menu = document.querySelector('[data-nav]');
  if (btn && menu) {
    btn.addEventListener('click', () => {
      const isOpen = menu.classList.toggle('open');
      btn.setAttribute('aria-expanded', String(isOpen));
    });
  }

  const filterButtons = [...document.querySelectorAll('[data-filter]')];
  const cards = [...document.querySelectorAll('[data-category]')];

  const applyFilter = (value) => {
    if (!filterButtons.length || !cards.length) return;
    filterButtons.forEach(b => b.classList.toggle('active', b.dataset.filter === value));
    cards.forEach(card => {
      card.style.display = value === 'All' || card.dataset.category === value ? '' : 'none';
    });
  };

  filterButtons.forEach(filterBtn => filterBtn.addEventListener('click', () => {
    applyFilter(filterBtn.dataset.filter || 'All');
  }));

  const requestedCategory = new URLSearchParams(window.location.search).get('category');
  if (requestedCategory && filterButtons.some(b => b.dataset.filter === requestedCategory)) {
    applyFilter(requestedCategory);
  }
});
