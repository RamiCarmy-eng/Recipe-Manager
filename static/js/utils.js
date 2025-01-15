const Utils = {
    formatDate: function(date) {
        return new Date(date).toLocaleDateString();
    },

    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    validateForm: function(formData) {
        const errors = [];
        for (const [key, value] of formData.entries()) {
            if (!value) {
                errors.push(`${key} is required`);
            }
        }
        return errors;
    },

    createSlug: function(text) {
        return text
            .toLowerCase()
            .replace(/[^a-z0-9]+/g, '-')
            .replace(/(^-|-$)+/g, '');
    },

    sanitizeHTML: function(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    },

    getFormData: function(form) {
        const formData = new FormData(form);
        const data = {};
        for (const [key, value] of formData.entries()) {
            data[key] = value;
        }
        return data;
    }
}; 