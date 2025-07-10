from typing import List, Optional, Dict, Any, Callable
from app.core.entities.pedido import Pedido
from app.core.ports.repositories.pedido_repositorio_base import PedidoRepositorioBase

class PedidoRepositorio(PedidoRepositorioBase):
    def __init__(self, db: Dict[int, Dict[str, Any]], id_generator: Callable[[], int]):
        self.db = db
        self.id_generator = id_generator

    def get_by_id(self, pedido_id: int) -> Optional[Pedido]:
        data = self.db.get(pedido_id)
        return Pedido(**data) if data else None

    def get_pedidos_by_cliente_id(self, cliente_id: int) -> List[Pedido]:
        return [Pedido(**data) for data in self.db.values() if data.get("cliente_id") == cliente_id]

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Pedido]:
        return [Pedido(**data) for data in list(self.db.values())[skip : skip + limit]]

    def create(self, pedido: Pedido) -> Pedido:
        new_id = self.id_generator()
        pedido.id = new_id
        self.db[new_id] = pedido.dict()
        return pedido

    def update(self, pedido_id: int, pedido: Pedido) -> Optional[Pedido]:
        if pedido_id in self.db:
            pedido.id = pedido_id
            self.db[pedido_id] = pedido.dict()
            return pedido
        return None

    def delete(self, pedido_id: int) -> bool:
        if pedido_id in self.db:
            del self.db[pedido_id]
            return True
        return False