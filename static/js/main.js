// Main application initialization
document.addEventListener('DOMContentLoaded', function() {
    Auth.initialize();
    UI.initialize();
    Navigation.setup();
    
    if (document.querySelector('.dashboard')) {
        RecipeManager.loadRecipes();
        Search.initialize();
        Modals.initialize();
    }
});
 