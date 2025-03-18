new Vue({
    el: '#app',
    data: {
        orders: [],
        socket: null,
        currentOrderIndex: 0,
        statistics: {
            dispatched: 0,
            pending: 0,
            boxesUsed: {
                'Caixa Pequena': 0,
                'Caixa Média': 0,
                'Caixa Grande': 0
            }
        },
        statisticsModal: null
    },
    computed: {
        finalStats() {
            return {
                total: this.orders.length,
                dispatched: this.orders.filter(o => o.status === 'dispatched').length,
                pending: this.orders.filter(o => !['dispatched', 'packed', 'no_box_available'].includes(o.status)).length,
                no_box: this.orders.filter(o => o.status === 'no_box_available').length,
                boxesUsed: this.statistics.boxesUsed
            };
        },
        currentOrder() {
            return this.orders.find(order => order.status === 'pending') || null;
        },
        hasActiveOrders() {
            return this.orders.some(order => order.status === 'pending');
        },
        completedOrders() {
            return this.orders.filter(o => o.status === 'dispatched' || o.status === 'packed').length;
        },
        totalOrders() {
            return this.orders.length;
        },
        progressPercentage() {
            return this.totalOrders ? (this.completedOrders / this.totalOrders) * 100 : 0;
        },
        pendingOrders() {
            return this.orders.filter(order => order.status === 'pending').length;
        },
        packedOrders() {
            return this.orders.filter(order => order.status === 'packed').length;
        },
        dispatchedOrders() {
            return this.orders.filter(order => order.status === 'dispatched').length;
        }
    },
    methods: {
        connectWebSocket() {
            this.socket = io('http://localhost:5001');
            
            this.socket.on('connect', () => {
                console.log('Conectado ao servidor');
            });
            
            this.socket.on('initial_orders', (orders) => {
                this.orders = orders;
            });
            
            this.socket.on('order_update', (updatedOrder) => {
                const index = this.orders.findIndex(o => o.id === updatedOrder.id);
                if (index !== -1) {
                    this.$set(this.orders, index, updatedOrder);
                } else {
                    this.orders.push(updatedOrder);
                }
            });
        },
        
        async generateOrders() {
            try {
                const response = await fetch('http://localhost:5001/api/orders/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ num_orders: 10 })
                });
                
                const data = await response.json();
                console.log('Pedidos gerados:', data);
                if (data.orders && data.orders.length > 0) {
                    console.log('Número de pedidos recebidos:', data.orders.length);
                    data.orders.forEach(order => {
                        if (!this.orders.find(o => o.id === order.id)) {
                            this.orders.push(order);
                        }
                    });
                }
            } catch (error) {
                console.error('Erro ao gerar pedidos:', error);
            }
        },
        
        async acceptRecommendation(orderId) {
            try {
                await fetch(`http://localhost:5001/api/orders/${orderId}/decision`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ accept: true })
                });
                
                const order = this.orders.find(o => o.id === orderId);
                if (order && order.recommended_box) {
                    this.statistics.boxesUsed[order.recommended_box.name]++;
                }
                
                if (!this.hasActiveOrders) {
                    this.showFinalStatistics();
                }
            } catch (error) {
                console.error('Erro ao aceitar recomendação:', error);
            }
        },
        
        async rejectRecommendation(orderId) {
            try {
                await fetch(`http://localhost:5001/api/orders/${orderId}/decision`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ accept: false })
                });
                
                if (!this.hasActiveOrders) {
                    this.showFinalStatistics();
                }
            } catch (error) {
                console.error('Erro ao rejeitar recomendação:', error);
            }
        },
        
        getStatusBadgeClass(status) {
            return `badge-${status}`;
        },
        
        getStatusText(status) {
            const statusMap = {
                'pending': 'Pendente',
                'packed': 'Empacotado',
                'dispatched': 'Despachado',
                'no_box_available': 'Sem caixa disponível'
            };
            return statusMap[status] || status;
        },
        
        getBoxPercentage(boxType) {
            const total = Object.values(this.finalStats.boxesUsed).reduce((a, b) => a + b, 0);
            return total ? (this.finalStats.boxesUsed[boxType] / total) * 100 : 0;
        },
        
        showFinalStatistics() {
            // Não precisa fazer nada, as estatísticas serão mostradas automaticamente
            // quando não houver mais pedidos ativos
        }
    },
    mounted() {
        this.connectWebSocket();
    }
}); 