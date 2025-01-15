const RecipeCard = {
    create: function(recipe) {
        const card = document.createElement('div');
        card.className = 'recipe-card';
        card.dataset.id = recipe.id;
        
        card.innerHTML = `
            <img src="${recipe.image || '/static/images/default-recipe.jpg'}" 
                 alt="${recipe.name}"
                 onerror="this.src='/static/images/default-recipe.jpg'">
            <h3>${recipe.name}</h3>
            <p>${recipe.description || ''}</p>
            <div class="recipe-actions">
                <button onclick="RecipeCard.view(${recipe.id})">View Details</button>
                <button onclick="RecipeCard.edit(${recipe.id})">Edit</button>
                <button onclick="RecipeCard.delete(${recipe.id})">Delete</button>
            </div>
        `;
        
        return card;
    },

    add: function(recipe) {
        const container = document.getElementById('recipe-container');
        const card = this.create(recipe);
        container.appendChild(card);
    },

    update: function(recipe) {
        const card = document.querySelector(`.recipe-card[data-id="${recipe.id}"]`);
        if (card) {
            const newCard = this.create(recipe);
            card.replaceWith(newCard);
        }
    },

    remove: function(recipeId) {
        const card = document.querySelector(`.recipe-card[data-id="${recipeId}"]`);
        if (card) card.remove();
    },

    view: function(recipeId) {
        window.location.href = `/recipe/details/${recipeId}`;
    },

    edit: function(recipeId) {
        Modals.openEditRecipe(recipeId);
    },

    delete: async function(recipeId) {
        if (confirm('Are you sure you want to delete this recipe?')) {
            try {
                await API.delete(`/api/recipe/${recipeId}`);
                this.remove(recipeId);
            } catch (error) {
                UI.showError('Error deleting recipe');
            }
        }
    }
}; 