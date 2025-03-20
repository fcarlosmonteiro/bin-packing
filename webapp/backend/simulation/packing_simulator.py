import simpy
from typing import List, Optional, Callable
from backend.models.box import Box
from backend.models.order import Order

class PackingSimulator:
    # Tempos de processamento em minutos
    RECOMMENDATION_TIME = 1
    PACKING_TIME = 5
    DISPATCH_TIME = 2

    def __init__(self):
        self.on_order_update: Optional[Callable[[Order], None]] = None
        self.waiting_decision = {}  # Armazena pedidos aguardando decisão
        # Catálogo de caixas disponíveis
        self.available_boxes = [
            Box(
                id="BOX_P",
                name="Caixa Pequena",
                width=30,
                height=20,
                depth=15,
                max_weight=2000,
                cost=5.0,
                image_url="https://img.freepik.com/fotos-gratis/caixa-vazia-aberta_1101-94.jpg"
            ),
            Box(
                id="BOX_M",
                name="Caixa Média",
                width=40,
                height=30,
                depth=25,
                max_weight=5000,
                cost=8.0,
                image_url="https://img.freepik.com/fotos-gratis/caixa-vazia-aberta_1101-94.jpg"
            ),
            Box(
                id="BOX_G",
                name="Caixa Grande",
                width=60,
                height=40,
                depth=35,
                max_weight=10000,
                cost=12.0,
                image_url="https://img.freepik.com/fotos-gratis/caixa-vazia-aberta_1101-94.jpg"
            )
        ]
    
    def recommend_box(self, order: Order) -> Optional[Box]:
        """
        Recomenda a menor caixa adequada para o pedido
        """
        order_volume = order.total_volume()
        order_weight = order.total_weight()
        
        # Se já teve uma recomendação rejeitada, tenta uma caixa maior
        if hasattr(order, 'last_rejected_box'):
            suitable_boxes = [
                box for box in self.available_boxes 
                if box.volume() > order.last_rejected_box.volume() 
                and box.max_weight >= order_weight
            ]
        else:
            suitable_boxes = [
                box for box in self.available_boxes 
                if box.volume() >= order_volume 
                and box.max_weight >= order_weight
            ]
        
        # Ordena as caixas por volume
        suitable_boxes.sort(key=lambda box: box.volume())
        
        return suitable_boxes[0] if suitable_boxes else None
    
    def process_order(self, order: Order):
        """
        Processa um pedido na simulação
        """
        print(f"Iniciando processamento do pedido {order.id}")
        
        try:
            # Recomenda uma caixa
            yield self.env.timeout(self.RECOMMENDATION_TIME)
            order.recommended_box = self.recommend_box(order)
            print(f"Caixa recomendada para pedido {order.id}: {order.recommended_box.name if order.recommended_box else 'Nenhuma'}")
            if self.on_order_update:
                self.on_order_update(order)
            
            # Pausa aqui e aguarda decisão do usuário
            self.waiting_decision[order.id] = order
            return
            
            # Aguarda a estação de empacotamento
            with self.packing_station.request() as request:
                yield request
                
                # Empacota o pedido
                yield self.env.timeout(self.PACKING_TIME)
                order.status = "packed"
                if self.on_order_update:
                    self.on_order_update(order)
                
                # Despacha o pedido
                yield self.env.timeout(self.DISPATCH_TIME)
                order.status = "dispatched"
                if self.on_order_update:
                    self.on_order_update(order)
        except Exception as e:
            print(f"Erro no processamento do pedido {order.id}: {str(e)}")
            raise
    
    def start_simulation(self, orders: List[Order]):
        """
        Inicia a simulação com uma lista de pedidos
        """
        # Cria um novo ambiente de simulação
        self.env = simpy.Environment()
        self.packing_station = simpy.Resource(self.env, capacity=1)
        
        print(f"Iniciando simulação com {len(orders)} pedidos")
        for order in orders:
            self.env.process(self.process_order(order))
            print(f"Processo iniciado para pedido {order.id}")
            
        # Executa a simulação por um tempo determinado
        print("Executando simulação")
        self.env.run(until=100)  # Executa por 100 unidades de tempo 

    def continue_processing(self, order_id: str, accepted: bool):
        """
        Continua o processamento após decisão do usuário
        """
        order = self.waiting_decision.get(order_id)
        if not order:
            return
            
        if accepted:
            # Cria novo ambiente para continuar o processamento
            self.env = simpy.Environment()
            self.packing_station = simpy.Resource(self.env, capacity=1)
            
            def finish_processing():
                with self.packing_station.request() as request:
                    yield request
                    
                    # Empacota o pedido
                    yield self.env.timeout(self.PACKING_TIME)
                    order.status = "packed"
                    if self.on_order_update:
                        self.on_order_update(order)
                    
                    # Despacha o pedido
                    yield self.env.timeout(self.DISPATCH_TIME)
                    order.status = "dispatched"
                    if self.on_order_update:
                        self.on_order_update(order)
            
            self.env.process(finish_processing())
            self.env.run(until=100)
        else:
            # Guarda a caixa rejeitada para tentar uma maior na próxima
            order.last_rejected_box = order.recommended_box
            # Remove a recomendação atual
            order.recommended_box = None
            
            # Tenta recomendar uma nova caixa
            new_box = self.recommend_box(order)
            if new_box:
                order.recommended_box = new_box
                if self.on_order_update:
                    self.on_order_update(order)
            else:
                # Se não há caixa maior disponível, marca como sem recomendação
                order.status = "no_box_available"
                if self.on_order_update:
                    self.on_order_update(order)
        
        # Remove o pedido da lista de espera apenas se não houver nova recomendação
        if not order.recommended_box:
            del self.waiting_decision[order_id] 