from dataclasses import dataclass

@dataclass
class Box:
    id: str
    name: str
    width: float
    height: float
    depth: float
    max_weight: float
    cost: float  # custo da caixa
    image_url: str
    
    def volume(self) -> float:
        """Calcula o volume da caixa em centímetros cúbicos"""
        return self.width * self.height * self.depth
    
    def to_dict(self) -> dict:
        """Converte a caixa para dicionário"""
        return {
            'id': self.id,
            'name': self.name,
            'width': self.width,
            'height': self.height,
            'depth': self.depth,
            'max_weight': self.max_weight,
            'cost': self.cost,
            'image_url': self.image_url,
            'volume': self.volume()
        } 