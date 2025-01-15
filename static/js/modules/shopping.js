const ShoppingList = {
    async load() {
        try {
            UI.showLoading();
            const items = await API.get('/api/shopping-list');
            this.displayItems(items);
        } catch (error) {
            UI.showError('Error loading shopping list');
        } finally {
            UI.hideLoading();
        }
    },

    displayItems: function(items) {
        const container = document.getElementById('shopping-list-container');
        if (!container) return;

        container.innerHTML = items.map(item => `
            <div class="shopping-item" data-id="${item.id}">
                <input type="checkbox" 
                       ${item.checked ? 'checked' : ''} 
                       onchange="ShoppingList.toggleItem(${item.id})">
                <span>${item.name} - ${item.amount} ${item.unit}</span>
                <button onclick="ShoppingList.removeItem(${item.id})">
                    Remove
                </button>
            </div>
        `).join('');
    },

    async addItem(item) {
        try {
            const newItem = await API.post('/api/shopping-list', item);
            this.load(); // Reload the list
            return newItem;
        } catch (error) {
            UI.showError('Error adding item to shopping list');
            throw error;
        }
    },

    async removeItem(itemId) {
        try {
            await API.delete(`/api/shopping-list/${itemId}`);
            document.querySelector(`.shopping-item[data-id="${itemId}"]`).remove();
        } catch (error) {
            UI.showError('Error removing item from shopping list');
            throw error;
        }
    },

    async toggleItem(itemId) {
        try {
            await API.put(`/api/shopping-list/${itemId}/toggle`);
        } catch (error) {
            UI.showError('Error updating item status');
            // Revert checkbox state on error
            const checkbox = document
                .querySelector(`.shopping-item[data-id="${itemId}"] input`);
            if (checkbox) checkbox.checked = !checkbox.checked;
        }
    },

    async addRecipeIngredients(recipeId) {
        try {
            await API.post(`/api/shopping-list/recipe/${recipeId}`);
            UI.showError('Recipe ingredients added to shopping list', 'success');
        } catch (error) {
            UI.showError('Error adding recipe ingredients to shopping list');
            throw error;
        }
    },

    async clearCompleted() {
        try {
            await API.delete('/api/shopping-list/completed');
            this.load(); // Reload the list
        } catch (error) {
            UI.showError('Error clearing completed items');
            throw error;
        }
    }
}; 