// DOM Elements
const recipeForm = document.getElementById('recipe-form');
const ingredientList = document.getElementById('ingredient-list');
const addIngredientBtn = document.getElementById('add-ingredient');
const searchInput = document.getElementById('search');
const recipeContainer = document.getElementById('recipe-container');

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    loadRecipes();
    setupEventListeners();
});

function setupEventListeners() {
    // Add ingredient button
    if (addIngredientBtn) {
        addIngredientBtn.addEventListener('click', addIngredientField);
    }

    // Recipe form submission
    if (recipeForm) {
        recipeForm.addEventListener('submit', handleRecipeSubmit);
    }

    // Search functionality
    if (searchInput) {
        searchInput.addEventListener('input', debounce(handleSearch, 300));
    }
}

// Recipe Functions
async function loadRecipes() {
    try {
        const response = await fetch('/user/recipes');
        const recipes = await response.json();
        displayRecipes(recipes);
    } catch (error) {
        console.error('Error loading recipes:', error);
        showAlert('Error loading recipes', 'error');
    }
}

function displayRecipes(recipes) {
    if (!recipeContainer) return;

    recipeContainer.innerHTML = recipes.map(recipe => `
        <div class="recipe-card" data-id="${recipe.id}">
            <h3>${recipe.name}</h3>
            <p>${recipe.description || ''}</p>
            <div class="recipe-actions">
                <button onclick="editRecipe(${recipe.id})" class="btn-edit">Edit</button>
                <button onclick="deleteRecipe(${recipe.id})" class="btn-delete">Delete</button>
            </div>
        </div>
    `).join('');
}

async function handleRecipeSubmit(e) {
    e.preventDefault();
    const formData = new FormData(recipeForm);

    try {
        const response = await fetch('/recipe/add', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            showAlert('Recipe saved successfully', 'success');
            loadRecipes();
            recipeForm.reset();
        } else {
            throw new Error('Failed to save recipe');
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('Error saving recipe', 'error');
    }
}

// Ingredient Functions
function addIngredientField() {
    const newRow = document.createElement('div');
    newRow.className = 'ingredient-row';
    newRow.innerHTML = `
        <input type="text" name="ingredients[]" placeholder="Ingredient name" required>
        <input type="number" name="quantities[]" placeholder="Amount" required>
        <input type="text" name="units[]" placeholder="Unit">
        <button type="button" class="remove-ingredient" onclick="removeIngredient(this)">Remove</button>
    `;
    ingredientList.appendChild(newRow);
}

function removeIngredient(button) {
    button.parentElement.remove();
}

// Utility Functions
function showAlert(message, type) {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    document.body.appendChild(alert);
    setTimeout(() => alert.remove(), 3000);
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function handleSearch(e) {
    const searchTerm = e.target.value.toLowerCase();
    const recipes = document.querySelectorAll('.recipe-card');

    recipes.forEach(recipe => {
        const title = recipe.querySelector('h3').textContent.toLowerCase();
        const description = recipe.querySelector('p').textContent.toLowerCase();
        const visible = title.includes(searchTerm) || description.includes(searchTerm);
        recipe.style.display = visible ? 'block' : 'none';
    });
}