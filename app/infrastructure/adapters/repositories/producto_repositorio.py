from typing import List, Optional, Dict, Any, Callable
from app.core.entities.producto import Producto
from app.core.ports.repositories.producto_repositorio_base import ProductoRepositorioBase

class ProductoRepositorio(ProductoRepositorioBase):
    def __init__(self, db: Dict[int, Dict[str, Any]], id_generator: Callable[[], int]):
        self.db = db
        self.id_generator = id_generator

    def get_by_id(self, producto_id: int) -> Optional[Producto]:
        data = self.db.get(producto_id)
        return Producto(**data) if data else None

    def get_by_nombre(self, nombre: str) -> Optional[Producto]:
        for producto_data in self.db.values():
            if producto_data.get("nombre") == nombre:
                return Producto(**producto_data)
        return None

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Producto]:
        return [Producto(**data) for data in list(self.db.values())[skip : skip + limit]]

    def create(self, producto: Producto) -> Producto:
        new_id = self.id_generator()
        producto.id = new_id
        self.db[new_id] = producto.dict()
        return producto

    def update(self, producto_id: int, producto: Producto) -> Optional[Producto]:
        if producto_id in self.db:
            producto.id = producto_id
            self.db[producto_id] = producto.dict()
            return producto
        return None

    def delete(self, producto_id: int) -> bool:
        if producto_id in self.db:
            del self.db[producto_id]
            return True
        return False