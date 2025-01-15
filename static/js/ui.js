const UI = {
    initialize: function() {
        this.setupEventListeners();
        this.updateUserInterface();
    },

    setupEventListeners: function() {
        document.addEventListener('recipeAdded', this.handleRecipeAdded.bind(this));
        document.addEventListener('recipeUpdated', this.handleRecipeUpdated.bind(this));
        document.addEventListener('recipeDeleted', this.handleRecipeDeleted.bind(this));
    },

    updateUserInterface: function() {
        if (Auth.isLoggedIn()) {
            this.showUserMenu();
            this.updateUsername();
        } else {
            this.hideUserMenu();
        }
    },

    showUserMenu: function() {
        const userMenu = document.querySelector('.user-menu');
        if (userMenu) userMenu.style.display = 'block';
    },

    hideUserMenu: function() {
        const userMenu = document.querySelector('.user-menu');
        if (userMenu) userMenu.style.display = 'none';
    },

    updateUsername: function() {
        const usernameDisplay = document.getElementById('username-display');
        if (usernameDisplay) {
            usernameDisplay.textContent = Auth.getCurrentUser();
        }
    },

    showLoading: function() {
        // Add loading indicator
        const loader = document.createElement('div');
        loader.className = 'loader';
        document.body.appendChild(loader);
    },

    hideLoading: function() {
        // Remove loading indicator
        const loader = document.querySelector('.loader');
        if (loader) loader.remove();
    },

    showError: function(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        document.body.appendChild(errorDiv);
        setTimeout(() => errorDiv.remove(), 3000);
    },

    handleRecipeAdded: function(event) {
        const recipe = event.detail;
        RecipeCard.add(recipe);
    },

    handleRecipeUpdated: function(event) {
        const recipe = event.detail;
        RecipeCard.update(recipe);
    },

    handleRecipeDeleted: function(event) {
        const recipeId = event.detail;
        RecipeCard.remove(recipeId);
    }
};



