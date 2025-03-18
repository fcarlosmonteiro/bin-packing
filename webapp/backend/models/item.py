from dataclasses import dataclass

@dataclass
class Item:
    id: str
    name: str
    width: float  # em centímetros
    height: float
    depth: float
    weight: float  # em gramas
    image_url: str
    
    def volume(self) -> float:
        """Calcula o volume do item em centímetros cúbicos"""
        return self.width * self.height * self.depth
    
    def to_dict(self) -> dict:
        """Converte o item para dicionário"""
        return {
            'id': self.id,
            'name': self.name,
            'width': self.width,
            'height': self.height,
            'depth': self.depth,
            'weight': self.weight,
            'image_url': self.image_url,
            'volume': self.volume()
        } 