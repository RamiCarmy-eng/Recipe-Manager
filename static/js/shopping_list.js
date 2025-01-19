class ShoppingListManager {
    constructor(listId) {
        this.listId = listId;
        this.filters = {
            category: null,
            checked: null,
            sortBy: 'category'
        };
        this.initializeFilters();
        this.initializeEventListeners();
    }

    initializeFilters() {
        // Category filter
        const categorySelect = document.getElementById('category-filter');
        if (categorySelect) {
            categorySelect.addEventListener('change', (e) => {
                this.filters.category = e.target.value || null;
                this.updateList();
            });
        }

        // Sort options
        const sortSelect = document.getElementById('sort-by');
        if (sortSelect) {
            sortSelect.addEventListener('change', (e) => {
                this.filters.sortBy = e.target.value;
                this.updateList();
            });
        }

        // Show/hide checked items
        const checkedFilter = document.getElementById('show-checked');
        if (checkedFilter) {
            checkedFilter.addEventListener('change', (e) => {
                this.filters.checked = e.target.checked ? null : false;
                this.updateList();
            });
        }
    }

    initializeEventListeners() {
        // Item checkboxes
        document.querySelectorAll('.item-checkbox').forEach(checkbox => {
            checkbox.addEventListener('change', (e) => this.toggleItem(e.target));
        });

        // Remove buttons
        document.querySelectorAll('.remove-item').forEach(button => {
            button.addEventListener('click', (e) => this.removeItem(e.target));
        });
    }

    async updateList() {
        try {
            const queryParams = new URLSearchParams({
                category_id: this.filters.category || '',
                sort_by: this.filters.sortBy,
                checked: this.filters.checked || ''
            });

            const response = await fetch(
                `/shopping/list/${this.listId}/filter?${queryParams}`
            );
            const data = await response.json();
            this.renderList(data);
        } catch (error) {
            console.error('Failed to update list:', error);
        }
    }

    renderList(categorizedItems) {
        const container = document.querySelector('.shopping-list');
        container.innerHTML = '';

        Object.entries(categorizedItems).forEach(([category, items]) => {
            const categorySection = document.createElement('div');
            categorySection.className = 'category-section mb-4';
            categorySection.innerHTML = `
                <h4 class="category-header">${category}</h4>
                <div class="list-group">
                    ${items.map(item => this.renderItem(item)).join('')}
                </div>
            `;
            container.appendChild(categorySection);
        });

        this.initializeEventListeners();
    }

    renderItem(item) {
        return `
            <div class="list-group-item d-flex justify-content-between align-items-center">
                <div class="form-check">
                    <input type="checkbox" 
                           class="form-check-input item-checkbox" 
                           data-item-id="${item.id}"
                           ${item.checked ? 'checked' : ''}>
                    <label class="form-check-label ${item.checked ? 'text-muted' : ''}">
                        ${item.name} - ${item.quantity} ${item.unit}
                    </label>
                </div>
                <button class="btn btn-sm btn-outline-danger remove-item" 
                        data-item-id="${item.id}">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
    }

    async toggleItem(checkbox) {
        const itemId = checkbox.dataset.itemId;
        try {
            await fetch(`/shopping/item/${itemId}/toggle`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ checked: checkbox.checked })
            });
            
            const label = checkbox.nextElementSibling;
            if (checkbox.checked) {
                label.classList.add('text-muted');
            } else {
                label.classList.remove('text-muted');
            }
        } catch (error) {
            console.error('Failed to toggle item:', error);
            checkbox.checked = !checkbox.checked;
        }
    }

    async removeItem(button) {
        if (!confirm('Remove this item from the list?')) return;

        const itemId = button.dataset.itemId;
        try {
            const response = await fetch(`/shopping/item/${itemId}/remove`, {
                method: 'POST'
            });
            if (response.ok) {
                button.closest('.list-group-item').remove();
            }
        } catch (error) {
            console.error('Failed to remove item:', error);
        }
    }
} 