import random
from typing import List
from uuid import uuid4
from ..models.item import Item
from ..models.order import Order

class OrderGenerator:
    def __init__(self):
        # Catálogo de produtos (peças de computador)
        self.catalog = [
            Item(
                id="CPU001",
                name="Processador Intel i7",
                width=3.7,
                height=3.7,
                depth=0.5,
                weight=70,
                image_url="https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=400"
            ),
            Item(
                id="GPU001",
                name="Placa de Vídeo RTX 3080",
                width=28.5,
                height=11.2,
                depth=4,
                weight=1400,
                image_url="https://images.unsplash.com/photo-1591488320449-011701bb6704?w=400"
            ),
            Item(
                id="RAM001",
                name="Memória RAM 16GB",
                width=13.3,
                height=3.1,
                depth=0.7,
                weight=45,
                image_url="https://images.unsplash.com/photo-1562976540-1502c2145186?w=400"
            ),
            Item(
                id="SSD001",
                name="SSD 1TB",
                width=10,
                height=7,
                depth=0.7,
                weight=150,
                image_url="https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=400"
            ),
            Item(
                id="MB001",
                name="Placa-mãe ATX",
                width=30.5,
                height=24.4,
                depth=0.5,
                weight=800,
                image_url="https://images.unsplash.com/photo-1518770660439-4636190af475?w=400"
            )
        ]
    
    def generate_order(self, min_items: int = 1, max_items: int = 5) -> Order:
        """
        Gera um pedido aleatório com itens do catálogo
        
        Args:
            min_items: Número mínimo de itens no pedido
            max_items: Número máximo de itens no pedido
        
        Returns:
            Order: Novo pedido gerado
        """
        # Determina quantos itens terá o pedido
        num_items = random.randint(min_items, max_items)
        
        # Seleciona itens aleatórios do catálogo
        selected_items = random.choices(self.catalog, k=num_items)
        
        # Cria um novo pedido com ID único
        order = Order(
            id=str(uuid4()),
            items=selected_items
        )
        
        return order
    
    def generate_orders(self, num_orders: int) -> List[Order]:
        """
        Gera múltiplos pedidos
        
        Args:
            num_orders: Número de pedidos a serem gerados
        
        Returns:
            List[Order]: Lista de pedidos gerados
        """
        print(f"Gerando {num_orders} pedidos...")
        orders = [self.generate_order() for _ in range(num_orders)]
        print(f"Pedidos gerados: {[order.id for order in orders]}")
        return orders 