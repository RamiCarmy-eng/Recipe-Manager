class IngredientSearch {
    constructor(inputElement, resultsContainer) {
        this.input = inputElement;
        this.resultsContainer = resultsContainer;
        this.selectedIngredients = new Set();
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Debounce search input
        let timeout = null;
        this.input.addEventListener('input', () => {
            clearTimeout(timeout);
            timeout = setTimeout(() => this.performSearch(), 300);
        });

        // Close results when clicking outside
        document.addEventListener('click', (e) => {
            if (!this.resultsContainer.contains(e.target) && 
                !this.input.contains(e.target)) {
                this.clearResults();
            }
        });
    }

    async performSearch() {
        const query = this.input.value.trim();
        if (query.length < 2) {
            this.clearResults();
            return;
        }

        try {
            const response = await fetch(`/ingredients/search?q=${encodeURIComponent(query)}`);
            const ingredients = await response.json();
            this.displayResults(ingredients);
        } catch (error) {
            console.error('Search failed:', error);
        }
    }

    displayResults(ingredients) {
        this.clearResults();
        
        if (ingredients.length === 0) {
            this.resultsContainer.innerHTML = '<div class="no-results">No ingredients found</div>';
            return;
        }

        const ul = document.createElement('ul');
        ul.className = 'ingredient-results';

        ingredients.forEach(ingredient => {
            if (!this.selectedIngredients.has(ingredient.id)) {
                const li = document.createElement('li');
                li.className = 'ingredient-item';
                li.innerHTML = `
                    <span class="ingredient-name">${ingredient.name}</span>
                    <span class="ingredient-category">${ingredient.category}</span>
                `;
                li.addEventListener('click', () => this.selectIngredient(ingredient));
                ul.appendChild(li);
            }
        });

        this.resultsContainer.appendChild(ul);
    }

    selectIngredient(ingredient) {
        this.selectedIngredients.add(ingredient.id);
        this.addIngredientToForm(ingredient);
        this.clearResults();
        this.input.value = '';
    }

    addIngredientToForm(ingredient) {
        const ingredientList = document.getElementById('selected-ingredients');
        const ingredientItem = document.createElement('div');
        ingredientItem.className = 'selected-ingredient';
        ingredientItem.dataset.ingredientId = ingredient.id;
        
        ingredientItem.innerHTML = `
            <div class="ingredient-info">
                <span class="name">${ingredient.name}</span>
                <span class="category">${ingredient.category}</span>
            </div>
            <div class="ingredient-controls">
                <input type="number" name="quantities[]" step="0.1" min="0" 
                       value="1" class="quantity-input">
                <select name="units[]" class="unit-select">
                    <option value="g">grams</option>
                    <option value="kg">kilograms</option>
                    <option value="ml">milliliters</option>
                    <option value="l">liters</option>
                    <option value="pcs">pieces</option>
                    <option value="tbsp">tablespoons</option>
                    <option value="tsp">teaspoons</option>
                </select>
                <button type="button" class="remove-ingredient">×</button>
            </div>
            <input type="hidden" name="ingredients[]" value="${ingredient.id}">
        `;

        // Set default unit if available
        if (ingredient.default_unit) {
            ingredientItem.querySelector('.unit-select').value = ingredient.default_unit;
        }

        // Add remove functionality
        ingredientItem.querySelector('.remove-ingredient').addEventListener('click', () => {
            this.selectedIngredients.delete(ingredient.id);
            ingredientItem.remove();
        });

        ingredientList.appendChild(ingredientItem);
    }

    clearResults() {
        this.resultsContainer.innerHTML = '';
    }
} 