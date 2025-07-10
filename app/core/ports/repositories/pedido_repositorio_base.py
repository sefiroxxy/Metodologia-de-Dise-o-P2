from abc import ABC, abstractmethod
from typing import List, Optional
from app.core.entities.pedido import Pedido

class PedidoRepositorioBase(ABC):
    @abstractmethod
    def get_by_id(self, pedido_id: int) -> Optional[Pedido]:
        pass

    @abstractmethod
    def get_pedidos_by_cliente_id(self, cliente_id: int) -> List[Pedido]:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Pedido]:
        pass

    @abstractmethod
    def create(self, pedido: Pedido) -> Pedido:
        pass

    @abstractmethod
    def update(self, pedido_id: int, pedido: Pedido) -> Optional[Pedido]:
        pass

    @abstractmethod
    def delete(self, pedido_id: int) -> bool:
        pass