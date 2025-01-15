const Favorites = {
    async load() {
        try {
            UI.showLoading();
            const recipes = await API.get('/api/favorites');
            RecipeManager.displayRecipes(recipes);
        } catch (error) {
            UI.showError('Error loading favorites');
        } finally {
            UI.hideLoading();
        }
    },

    async toggle(recipeId) {
        try {
            const isFavorite = await RecipeManager.toggleFavorite(recipeId);
            this.updateFavoriteButton(recipeId, isFavorite);
            return isFavorite;
        } catch (error) {
            UI.showError('Error updating favorite status');
            throw error;
        }
    },

    updateFavoriteButton: function(recipeId, isFavorite) {
        const button = document
            .querySelector(`.recipe-card[data-id="${recipeId}"] .favorite-btn`);
        
        if (button) {
            button.classList.toggle('active', isFavorite);
            button.title = isFavorite ? 'Remove from favorites' : 'Add to favorites';
        }
    }
}; 