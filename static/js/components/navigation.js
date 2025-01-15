const Navigation = {
    setup: function() {
        this.setupTabNavigation();
        this.setupUserMenu();
    },

    setupTabNavigation: function() {
        const tabs = document.querySelectorAll('.nav-button');
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                this.handleTabClick(tab);
            });
        });
    },

    setupUserMenu: function() {
        const userButton = document.getElementById('user-menu-button');
        if (userButton) {
            userButton.addEventListener('click', this.toggleUserMenu);
        }
    },

    handleTabClick: function(tab) {
        // Remove active class from all tabs
        document.querySelectorAll('.nav-button')
            .forEach(t => t.classList.remove('active'));
        
        // Add active class to clicked tab
        tab.classList.add('active');
        
        // Load content based on tab
        const page = tab.dataset.page;
        this.loadPageContent(page);
    },

    loadPageContent: function(page) {
        switch(page) {
            case 'dashboard':
                RecipeManager.loadRecipes();
                break;
            case 'favorites':
                RecipeManager.loadFavorites();
                break;
            case 'my-recipes':
                RecipeManager.loadMyRecipes();
                break;
            case 'shopping-list':
                ShoppingList.load();
                break;
        }
    },

    toggleUserMenu: function() {
        const menu = document.querySelector('.user-menu-dropdown');
        if (menu) {
            menu.style.display = 
                menu.style.display === 'none' ? 'block' : 'none';
        }
    }
}; 