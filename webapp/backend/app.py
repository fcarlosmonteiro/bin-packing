from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from threading import Thread
from .simulation.order_generator import OrderGenerator
from .simulation.packing_simulator import PackingSimulator
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'packing-simulation-secret'
socketio = SocketIO(app, cors_allowed_origins="*")

# Instancia os componentes principais
order_generator = OrderGenerator()
packing_simulator = PackingSimulator()

# Lista de pedidos em processamento
active_orders = []

def on_order_update(order):
    """Callback para atualização de status dos pedidos"""
    socketio.emit('order_update', order.to_dict())

# Configura o callback no simulador
packing_simulator.on_order_update = on_order_update

@app.route('/api/orders', methods=['GET'])
def get_orders():
    """Retorna todos os pedidos ativos"""
    return jsonify([order.to_dict() for order in active_orders])

@app.route('/api/orders/generate', methods=['POST'])
def generate_orders():
    """Gera novos pedidos e inicia sua simulação"""
    try:
        data = request.get_json()
        num_orders = data.get('num_orders', 1)
        
        print(f"Recebida requisição para gerar {num_orders} pedidos")
        
        # Gera novos pedidos
        new_orders = order_generator.generate_orders(num_orders)
        active_orders.extend(new_orders)
        
        # Inicia a simulação para os novos pedidos
        print("Iniciando simulação dos novos pedidos")
        try:
            packing_simulator.start_simulation(new_orders)
        except Exception as sim_error:
            print(f"Erro na simulação: {str(sim_error)}")
            import traceback
            print(traceback.format_exc())
        
        print("Enviando resposta com pedidos gerados")
        return jsonify({
            'message': f'{num_orders} pedidos gerados com sucesso',
            'orders': [order.to_dict() for order in new_orders]
        })
    
    except Exception as e:
        print(f"Erro ao gerar pedidos: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 400

@app.route('/api/orders/<order_id>/decision', methods=['POST'])
def process_decision(order_id):
    """Processa a decisão do usuário sobre a recomendação de caixa"""
    try:
        data = request.get_json()
        decision = data.get('accept', False)
        
        # Encontra o pedido
        order = next((o for o in active_orders if o.id == order_id), None)
        if not order:
            return jsonify({'error': 'Pedido não encontrado'}), 404
        
        # Continua o processamento do pedido com base na decisão
        packing_simulator.continue_processing(order_id, decision)
        
        return jsonify({'message': 'Decisão processada com sucesso'})
    
    except Exception as e:
        print(f"Erro ao processar decisão: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 400

@socketio.on('connect')
def handle_connect():
    """Manipula nova conexão WebSocket"""
    print('Cliente conectado')
    # Envia os pedidos ativos para o novo cliente
    emit('initial_orders', [order.to_dict() for order in active_orders])

@socketio.on('disconnect')
def handle_disconnect():
    """Manipula desconexão WebSocket"""
    print('Cliente desconectado')

def start_server():
    """Inicia o servidor Flask com WebSocket"""
    # Inicia o servidor
    socketio.run(app, debug=True, host='0.0.0.0', port=5001)

if __name__ == '__main__':
    start_server() 