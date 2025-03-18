from dataclasses import dataclass
from typing import List
from .item import Item
from .box import Box

@dataclass
class Order:
    id: str
    items: List[Item]
    recommended_box: Box = None
    status: str = "pending"  # pending, packed, dispatched
    
    def total_weight(self) -> float:
        """Calcula o peso total do pedido"""
        return sum(item.weight for item in self.items)
    
    def total_volume(self) -> float:
        """Calcula o volume total dos itens"""
        return sum(item.volume() for item in self.items)
    
    def to_dict(self) -> dict:
        """Converte o pedido para dicionário"""
        print(f"Convertendo pedido {self.id} para dicionário")
        return {
            'id': self.id,
            'items': [item.to_dict() for item in self.items],
            'recommended_box': self.recommended_box.to_dict() if self.recommended_box else None,
            'status': self.status,
            'total_weight': self.total_weight(),
            'total_volume': self.total_volume()
        } 