// Gestionnaire de fichiers et d'upload
class FileHandler {
    constructor() {
        this.dropZone = document.getElementById('dropZone');
        this.fileInput = document.getElementById('fileInput');
        this.preview = document.getElementById('preview');
        this.imagePreview = document.getElementById('imagePreview');
        
        if (this.dropZone) {
            this.initializeEventListeners();
        }
    }

    initializeEventListeners() {
        this.dropZone.addEventListener('dragover', (e) => this.handleDragOver(e));
        this.dropZone.addEventListener('dragleave', (e) => this.handleDragLeave(e));
        this.dropZone.addEventListener('drop', (e) => this.handleDrop(e));
        this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
    }

    handleDragOver(e) {
        e.preventDefault();
        this.dropZone.classList.add('drag-over');
    }

    handleDragLeave(e) {
        e.preventDefault();
        this.dropZone.classList.remove('drag-over');
    }

    handleDrop(e) {
        e.preventDefault();
        this.dropZone.classList.remove('drag-over');
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            this.processImage(file);
        }
    }

    handleFileSelect(e) {
        const file = e.target.files[0];
        if (file) {
            this.processImage(file);
        }
    }

    processImage(file) {
        // Lancer directement l'analyse avec l'image
        this.analyzeImage(file);
    }

    async analyzeImage(file) {
        // Afficher un état de chargement
        this.showLoadingState();

        const formData = new FormData();
        formData.append('image', file);

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Une erreur est survenue lors de l\'analyse');
            }

            this.showResult(data);
        } catch (error) {
            console.error('Error details:', error);
            this.showError(error.message || 'Une erreur est survenue lors de l\'analyse');
        }
    }

    showLoadingState() {
        const modal = document.getElementById('resultModal');
        const modalContent = document.getElementById('modalContent');
        
        modalContent.innerHTML = `
            <div class="text-center">
                <div class="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-emerald-100 mb-6">
                    <div class="animate-spin rounded-full h-12 w-12 border-4 border-emerald-500 border-t-transparent"></div>
                </div>
                
                <h3 class="text-2xl font-semibold text-gray-900 mb-2">
                    Analyse en cours...
                </h3>
                
                <p class="text-sm text-gray-500">
                    Veuillez patienter pendant que nous analysons votre image
                </p>
            </div>
        `;
        
        modal.classList.remove('hidden');
    }

    showError(message) {
        const modal = document.getElementById('resultModal');
        const modalContent = document.getElementById('modalContent');
        
        modalContent.innerHTML = `
            <div class="text-center">
                <div class="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-red-100 mb-6">
                    <svg class="h-12 w-12 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                </div>
                
                <h3 class="text-2xl font-semibold text-gray-900 mb-2">
                    Erreur
                </h3>
                
                <p class="text-sm text-gray-500 mb-6">
                    ${message}
                </p>

                <button onclick="document.getElementById('resultModal').classList.add('hidden')"
                    class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500">
                    Fermer
                </button>
            </div>
        `;
    }

    showResult(result) {
        const modal = document.getElementById('resultModal');
        const modalContent = document.getElementById('modalContent');
        
        const resultColor = result.result === 'positive' ? 
            'bg-red-100 text-red-700' : 
            'bg-emerald-100 text-emerald-700';
        
        const iconPath = result.result === 'positive' ?
            '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>' :
            '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>';

        modalContent.innerHTML = `
            <div class="relative">
                <div class="relative rounded-t-xl overflow-hidden">
                    <img src="${result.image_url}" alt="Analysed image" class="w-full h-64 object-cover">
                    <div class="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
                </div>
                
                <div class="relative -mt-16 px-6">
                    <div class="mx-auto flex h-16 w-16 items-center justify-center rounded-full ${resultColor} ring-8 ring-white shadow-lg">
                        <svg class="h-8 w-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            ${iconPath}
                        </svg>
                    </div>
                    
                    <div class="mt-4 text-center">
                        <h3 class="text-2xl font-bold text-gray-900 mb-2">
                            ${result.result === 'positive' ? 'Malaria détectée' : 'Pas de malaria détectée'}
                        </h3>
                        
                        <div class="bg-gray-50 rounded-xl p-6 mb-6">
                            <div class="mb-4">
                                <div class="w-full bg-gray-200 rounded-full h-2">
                                    <div class="h-2 rounded-full ${
                                        result.result === 'positive' ? 'bg-red-500' : 'bg-emerald-500'
                                    } transition-all duration-1000" style="width: ${(result.confidence * 100).toFixed(1)}%"></div>
                                </div>
                                <p class="text-sm text-gray-600 mt-2">
                                    Confiance: ${(result.confidence * 100).toFixed(1)}%
                                </p>
                            </div>
                        </div>

                        <div class="flex justify-center space-x-3">
                            <button onclick="document.getElementById('resultModal').classList.add('hidden')"
                                class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-lg shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 transition-all duration-200">
                                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                                </svg>
                                Fermer
                            </button>
                            <a href="/history"
                                class="inline-flex items-center px-4 py-2 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-gradient-to-r from-emerald-500 to-emerald-600 hover:from-emerald-600 hover:to-emerald-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 transition-all duration-200">
                                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
                                </svg>
                                Voir l'historique
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        modal.classList.remove('hidden');
        modalContent.classList.add('modal-fade-in');
    }
}

// Gestionnaire de l'historique
class HistoryHandler {
    constructor() {
        this.historyGrid = document.getElementById('historyGrid');
        this.emptyState = document.getElementById('emptyState');
        this.currentPage = 1;
        this.itemsPerPage = 6;
        this.currentFilter = 'all';
        
        if (this.historyGrid) {
            this.initializeFilters();
            this.initializePagination();
            // Masquer initialement toutes les cartes
            gsap.set('.analysis-card', { 
                autoAlpha: 0,
                y: 30,
                scale: 0.95
            });
            this.updateDisplay();
        }
    }

    initializeFilters() {
        const filterButtons = document.querySelectorAll('.filter-btn');
        filterButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                filterButtons.forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');
                
                this.currentFilter = button.dataset.filter;
                this.currentPage = 1;
                this.updateDisplay();
            });
        });
    }

    getFilteredCards() {
        const cards = Array.from(document.querySelectorAll('.analysis-card'));
        return cards.filter(card => 
            this.currentFilter === 'all' || card.dataset.result === this.currentFilter
        );
    }

    initializePagination() {
        const prevBtn = document.querySelector('[data-action="prev"]');
        const nextBtn = document.querySelector('[data-action="next"]');
        
        if (prevBtn && nextBtn) {
            prevBtn.addEventListener('click', () => {
                this.currentPage--;
                this.updateDisplay();
            });
            nextBtn.addEventListener('click', () => {
                this.currentPage++;
                this.updateDisplay();
            });
        }
    }

    updateDisplay() {
        const filteredCards = this.getFilteredCards();
        const totalPages = Math.ceil(filteredCards.length / this.itemsPerPage);
        
        // Mettre à jour la pagination
        const prevBtn = document.querySelector('[data-action="prev"]');
        const nextBtn = document.querySelector('[data-action="next"]');
        const pageIndicator = document.getElementById('pageIndicator');

        prevBtn.disabled = this.currentPage <= 1;
        nextBtn.disabled = this.currentPage >= totalPages;
        
        if (pageIndicator) {
            pageIndicator.textContent = `Page ${this.currentPage} sur ${totalPages || 1}`;
        }

        // Créer une timeline principale
        const timeline = gsap.timeline({
            defaults: { ease: "power2.out" }
        });

        // Effet de sortie doux
        timeline.to('.analysis-card', {
            autoAlpha: 0,
            y: -10,
            scale: 0.98,
            stagger: {
                amount: 0.2,
                from: "start"
            },
            duration: 0.3
        });

        // Calculer les cartes à afficher
        const startIndex = (this.currentPage - 1) * this.itemsPerPage;
        const endIndex = startIndex + this.itemsPerPage;
        const visibleCards = filteredCards.slice(startIndex, endIndex);

        // Animation d'apparition séquentielle
        timeline.fromTo(visibleCards, 
            {
                autoAlpha: 0,
                y: 20,
                scale: 0.95,
                transformOrigin: "center center"
            },
            {
                autoAlpha: 1,
                y: 0,
                scale: 1,
                duration: 0.5,
                stagger: {
                    each: 0.1,
                    from: "start",
                    ease: "power1.inOut"
                },
                ease: "back.out(1.2)"
            },
            "-=0.1"
        )
        .fromTo(visibleCards.map(card => card.querySelector('img')),
            { 
                scale: 1.1
            },
            { 
                scale: 1,
                duration: 0.8,
                stagger: {
                    each: 0.1,
                    from: "start"
                }
            },
            "-=0.5"
        )
        .fromTo(visibleCards.map(card => card.querySelectorAll('.flex')),
            {
                autoAlpha: 0,
                y: 10
            },
            {
                autoAlpha: 1,
                y: 0,
                duration: 0.3,
                stagger: {
                    each: 0.05,
                    from: "start"
                }
            },
            "-=0.5"
        );

        // Gérer l'état vide
        if (filteredCards.length === 0) {
            this.historyGrid.style.display = 'none';
            this.emptyState.style.display = 'block';
            
            gsap.fromTo(this.emptyState,
                {
                    autoAlpha: 0,
                    y: 15
                },
                {
                    autoAlpha: 1,
                    y: 0,
                    duration: 0.4,
                    ease: "power2.out"
                }
            );
        } else {
            this.emptyState.style.display = 'none';
            this.historyGrid.style.display = 'grid';
        }
    }
}

// Initialisation conditionnelle selon la page
document.addEventListener('DOMContentLoaded', () => {
    // Initialiser AOS
    AOS.init({
        once: true,  // L'animation ne se joue qu'une fois
        offset: 50,  // Déclencher l'animation 50px avant que l'élément soit visible
        duration: 800,  // Durée de l'animation en ms
        easing: 'ease-out-cubic'  // Type d'easing
    });

    new FileHandler();
    new HistoryHandler();
});

// Gestion du menu mobile
document.addEventListener('DOMContentLoaded', () => {
    const menuButton = document.getElementById('menuButton');
    const mobileMenu = document.getElementById('mobileMenu');
    const menuIcon = document.getElementById('menuIcon');
    const closeIcon = document.getElementById('closeIcon');

    if (menuButton && mobileMenu) {
        menuButton.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
            menuIcon.classList.toggle('hidden');
            closeIcon.classList.toggle('hidden');
        });

        // Fermer le menu au clic sur un lien
        mobileMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.add('hidden');
                menuIcon.classList.remove('hidden');
                closeIcon.classList.add('hidden');
            });
        });

        // Fermer le menu au redimensionnement
        window.addEventListener('resize', () => {
            if (window.innerWidth >= 768) { // 768px est le breakpoint md de Tailwind
                mobileMenu.classList.add('hidden');
                menuIcon.classList.remove('hidden');
                closeIcon.classList.add('hidden');
            }
        });
    }
});