document.addEventListener('DOMContentLoaded', function() {
    const ITEMS_PER_PAGE = 15;
    const analysisCards = document.querySelectorAll('.analysis-card');
    const filterButtons = document.querySelectorAll('.filter-btn');
    const prevButton = document.getElementById('prevPage');
    const nextButton = document.getElementById('nextPage');
    const pageIndicator = document.getElementById('pageIndicator');
    
    let currentPage = 1;
    let currentFilter = 'all';

    function getFilteredCards() {
        return Array.from(analysisCards).filter(card => {
            if (currentFilter === 'all') return true;
            return card.dataset.result === currentFilter;
        });
    }

    function showPage(page) {
        const filteredCards = getFilteredCards();
        const totalPages = Math.ceil(filteredCards.length / ITEMS_PER_PAGE);
        const startIndex = (page - 1) * ITEMS_PER_PAGE;
        const endIndex = startIndex + ITEMS_PER_PAGE;

        // Cacher toutes les cartes
        gsap.set(analysisCards, { display: 'none', opacity: 0, y: 20 });

        // Afficher les cartes de la page courante avec animation
        const cardsToShow = filteredCards.slice(startIndex, endIndex);
        cardsToShow.forEach((card, index) => {
            card.style.display = 'flex';
            card.dataset.index = index;
        });

        gsap.to(cardsToShow, {
            opacity: 1,
            y: 0,
            duration: 0.3,
            stagger: 0.05,
            ease: "power2.out"
        });

        // Mettre à jour les boutons de pagination
        prevButton.disabled = page <= 1;
        nextButton.disabled = page >= totalPages;
        pageIndicator.textContent = `Page ${page} sur ${totalPages || 1}`;
    }

    // Gestionnaires d'événements pour les filtres
    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            filterButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            currentFilter = button.dataset.filter;
            currentPage = 1;
            showPage(currentPage);
        });
    });

    // Gestionnaires pour la pagination
    prevButton.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            showPage(currentPage);
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    });

    nextButton.addEventListener('click', () => {
        const totalPages = Math.ceil(getFilteredCards().length / ITEMS_PER_PAGE);
        if (currentPage < totalPages) {
            currentPage++;
            showPage(currentPage);
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    });

    // Initialisation
    showPage(1);
}); 