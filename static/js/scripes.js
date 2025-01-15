const RecipeManager = {
    async loadRecipes() {
        try {
            UI.showLoading();
            const recipes = await API.get('/api/recipes');
            this.displayRecipes(recipes);
        } catch (error) {
            UI.showError('Error loading recipes');
        } finally {
            UI.hideLoading();
        }
    },

    async loadFavorites() {
        try {
            UI.showLoading();
            const recipes = await API.get('/api/favorites');
            this.displayRecipes(recipes);
        } catch (error) {
            UI.showError('Error loading favorites');
        } finally {
            UI.hideLoading();
        }
    },

    async loadMyRecipes() {
        try {
            UI.showLoading();
            const recipes = await API.get('/api/my-recipes');
            this.displayRecipes(recipes);
        } catch (error) {
            UI.showError('Error loading my recipes');
        } finally {
            UI.hideLoading();
        }
    },

    displayRecipes: function(recipes) {
        const container = document.getElementById('recipe-container');
        container.innerHTML = '';
        recipes.forEach(recipe => RecipeCard.add(recipe));
    },

    async addRecipe(recipeData) {
        try {
            const recipe = await API.post('/api/recipe', recipeData);
            document.dispatchEvent(
                new CustomEvent('recipeAdded', { detail: recipe })
            );
            return recipe;
        } catch (error) {
            UI.showError('Error adding recipe');
            throw error;
        }
    },

    async updateRecipe(recipeId, recipeData) {
        try {
            const recipe = await API.put(`/api/recipe/${recipeId}`, recipeData);
            document.dispatchEvent(
                new CustomEvent('recipeUpdated', { detail: recipe })
            );
            return recipe;
        } catch (error) {
            UI.showError('Error updating recipe');
            throw error;
        }
    },

    async deleteRecipe(recipeId) {
        try {
            await API.delete(`/api/recipe/${recipeId}`);
            document.dispatchEvent(
                new CustomEvent('recipeDeleted', { detail: recipeId })
            );
        } catch (error) {
            UI.showError('Error deleting recipe');
            throw error;
        }
    },

    async toggleFavorite(recipeId) {
        try {
            const response = await API.post(`/api/recipe/${recipeId}/favorite`);
            return response.isFavorite;
        } catch (error) {
            UI.showError('Error updating favorite status');
            throw error;
        }
    }
}; 