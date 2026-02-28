// API Service with better error handling
const API = {
    async request(endpoint, options = {}) {
        try {
            const response = await fetch(endpoint, {
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                }
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || `HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error(`API Error (${endpoint}):`, error);
            throw error;
        }
    },
    
    // Users
    async getUsers() {
        return this.request('/api/users');
    },
    
    async getUser(id) {
        return this.request(`/api/users/${id}`);
    },
    
    async createUser(userData) {
        return this.request('/api/users', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    },
    
    async updateUser(id, userData) {
        return this.request(`/api/users/${id}`, {
            method: 'PUT',
            body: JSON.stringify(userData)
        });
    },
    
    async deleteUser(id) {
        return this.request(`/api/users/${id}`, {
            method: 'DELETE'
        });
    },
    
    // Products
    async getProducts() {
        return this.request('/api/products');
    },
    
    async createProduct(productData) {
        return this.request('/api/products', {
            method: 'POST',
            body: JSON.stringify(productData)
        });
    },
    
    async updateProduct(id, productData) {
        return this.request(`/api/products/${id}`, {
            method: 'PUT',
            body: JSON.stringify(productData)
        });
    },
    
    async deleteProduct(id) {
        return this.request(`/api/products/${id}`, {
            method: 'DELETE'
        });
    },
    
    // Orders
    async getOrders() {
        return this.request('/api/orders');
    },
    
    async getOrderDetails(id) {
        return this.request(`/api/orders/${id}`);
    },
    
    async createOrder(orderData) {
        return this.request('/api/orders', {
            method: 'POST',
            body: JSON.stringify(orderData)
        });
    },
    
    // Inventory
    async getInventory() {
        return this.request('/api/inventory');
    },
    
    async updateInventory(productId, inventoryData) {
        return this.request(`/api/inventory/${productId}`, {
            method: 'PUT',
            body: JSON.stringify(inventoryData)
        });
    },
    
    // Logs
    async getLogs(filters = {}) {
        const params = new URLSearchParams(filters);
        return this.request(`/api/logs?${params}`);
    },
    
    async createLog(logData) {
        return this.request('/api/logs', {
            method: 'POST',
            body: JSON.stringify(logData)
        });
    },
    
    async getLogStats() {
        return this.request('/api/logs/stats');
    },
    
    // Test connection
    async testConnection() {
        return this.request('/api/test');
    }
};

// Utility Functions
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleString();
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function showAlert(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    alertDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background-color: ${type === 'success' ? '#4CAF50' : '#f44336'};
        color: white;
        border-radius: 5px;
        z-index: 9999;
        animation: slideIn 0.5s;
    `;
    
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.style.animation = 'slideOut 0.5s';
        setTimeout(() => alertDiv.remove(), 500);
    }, 3000);
}

// Modal Management
const Modal = {
    open(modalId) {
        document.getElementById(modalId).style.display = 'block';
    },
    
    close(modalId) {
        document.getElementById(modalId).style.display = 'none';
    }
};

// Close modals when clicking outside
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
};

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);