const Modals = {
    initialize: function() {
        this.setupModalListeners();
    },

    setupModalListeners: function() {
        // Close modal when clicking outside
        window.addEventListener('click', (event) => {
            if (event.target.classList.contains('modal')) {
                this.closeAll();
            }
        });

        // Close modal when clicking close button
        document.querySelectorAll('.close-modal').forEach(button => {
            button.addEventListener('click', () => this.closeAll());
        });
    },

    openAddRecipe: function() {
        this.loadModalContent('/static/html/modals/add-recipe.html', 'add-recipe-modal')
            .then(() => {
                const modal = document.getElementById('add-recipe-modal');
                modal.style.display = 'block';
                this.setupAddRecipeForm();
            });
    },

    openEditRecipe: function(recipeId) {
        this.loadModalContent('/static/html/modals/edit-recipe.html', 'edit-recipe-modal')
            .then(() => {
                const modal = document.getElementById('edit-recipe-modal');
                modal.style.display = 'block';
                this.loadRecipeData(recipeId);
            });
    },

    async loadModalContent(url, modalId) {
        try {
            const response = await fetch(url);
            const html = await response.text();
            
            let modal = document.getElementById(modalId);
            if (!modal) {
                modal = document.createElement('div');
                modal.id = modalId;
                modal.className = 'modal';
                document.body.appendChild(modal);
            }
            
            modal.innerHTML = html;
        } catch (error) {
            console.error('Error loading modal content:', error);
        }
    },

    async loadRecipeData(recipeId) {
        try {
            const recipe = await API.get(`/api/recipe/${recipeId}/details`);
            const form = document.getElementById('edit-recipe-form');
            
            form.elements['name'].value = recipe.name;
            form.elements['category'].value = recipe.category;
            form.elements['description'].value = recipe.description;
            form.elements['instructions'].value = recipe.instructions;
            
            this.populateIngredients(recipe.ingredients);
        } catch (error) {
            UI.showError('Error loading recipe details');
        }
    },

    setupAddRecipeForm: function() {
        const form = document.getElementById('add-recipe-form');
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = Utils.getFormData(form);
            
            try {
                const recipe = await API.post('/api/recipe', formData);
                document.dispatchEvent(
                    new CustomEvent('recipeAdded', { detail: recipe })
                );
                this.closeAll();
            } catch (error) {
                UI.showError('Error adding recipe');
            }
        });
    },

    populateIngredients: function(ingredients) {
        const container = document.getElementById('edit-ingredients-list');
        container.innerHTML = ingredients.map(ing => `
            <div class="ingredient-item">
                <input type="text" value="${ing.name}" class="ing-name">
                <input type="number" value="${ing.amount}" class="ing-amount">
                <input type="text" value="${ing.unit}" class="ing-unit">
                <button type="button" onclick="this.parentElement.remove()">
                    Remove
                </button>
            </div>
        `).join('');
    },

    closeAll: function() {
        document.querySelectorAll('.modal').forEach(modal => {
            modal.style.display = 'none';
        });
    }
}; 