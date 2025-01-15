const Auth = {
    initialize: function() {
        this.setupLoginForm();
        this.setupLogoutButton();
    },

    setupLoginForm: function() {
        const form = document.querySelector('.login-form');
        if (form) {
            form.addEventListener('submit', this.handleLogin.bind(this));
        }
    },

    setupLogoutButton: function() {
        const logoutBtn = document.getElementById('logout-button');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', this.handleLogout.bind(this));
        }
    },

    async handleLogin(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        
        try {
            const response = await API.post('/login', {
                username: formData.get('username'),
                password: formData.get('password')
            });
            
            if (response.success) {
                window.location.href = '/dashboard';
            } else {
                UI.showError('Invalid credentials');
            }
        } catch (error) {
            UI.showError('Login failed');
        }
    },

    async handleLogout() {
        try {
            await API.post('/logout');
            window.location.href = '/login';
        } catch (error) {
            UI.showError('Logout failed');
        }
    },

    isLoggedIn: function() {
        return !!localStorage.getItem('user');
    },

    getCurrentUser: function() {
        return localStorage.getItem('user');
    },

    setCurrentUser: function(username) {
        localStorage.setItem('user', username);
    },

    clearCurrentUser: function() {
        localStorage.removeItem('user');
    }
}; 