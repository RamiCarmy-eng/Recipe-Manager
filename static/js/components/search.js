const Search = {
    initialize: function() {
        this.searchInput = document.getElementById('search-input');
        this.categoryFilter = document.getElementById('category-filter');
        this.setupEventListeners();
        this.loadCategories();
    },

    setupEventListeners: function() {
        this.searchInput.addEventListener('input', 
            Utils.debounce(this.performSearch.bind(this), 300));
        this.categoryFilter.addEventListener('change', 
            this.performSearch.bind(this));
    },

    async loadCategories() {
        try {
            const categories = await API.get('/categories');
            this.updateCategoryFilter(categories);
        } catch (error) {
            UI.showError('Error loading categories');
        }
    },

    updateCategoryFilter: function(categories) {
        this.categoryFilter.innerHTML = `
            <option value="">All Categories</option>
            ${categories.map(cat => 
                `<option value="${cat}">${cat}</option>`
            ).join('')}
        `;
    },

    async performSearch() {
        const query = this.searchInput.value;
        const category = this.categoryFilter.value;
        
        try {
            UI.showLoading();
            const recipes = await API.get(
                `/search?q=${query}&category=${category}`
            );
            this.updateResults(recipes);
        } catch (error) {
            UI.showError('Error performing search');
        } finally {
            UI.hideLoading();
        }
    },

    updateResults: function(recipes) {
        const container = document.getElementById('recipe-container');
        container.innerHTML = '';
        recipes.forEach(recipe => RecipeCard.add(recipe));
    }
}; 