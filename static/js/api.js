const API = {
    get: async function(endpoint) {
        try {
            const response = await fetch(endpoint);
            return await response.json();
        } catch (error) {
            console.error('API Get Error:', error);
            throw error;
        }
    },

    post: async function(endpoint, data) {
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            return await response.json();
        } catch (error) {
            console.error('API Post Error:', error);
            throw error;
        }
    },

    put: async function(endpoint, data) {
        try {
            const response = await fetch(endpoint, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            return await response.json();
        } catch (error) {
            console.error('API Put Error:', error);
            throw error;
        }
    },

    delete: async function(endpoint) {
        try {
            const response = await fetch(endpoint, {
                method: 'DELETE'
            });
            return await response.json();
        } catch (error) {
            console.error('API Delete Error:', error);
            throw error;
        }
    }
};






