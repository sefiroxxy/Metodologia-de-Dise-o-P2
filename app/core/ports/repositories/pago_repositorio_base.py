from abc import ABC, abstractmethod
from typing import List, Optional
from app.core.entities.pago import Pago

class PagoRepositorioBase(ABC):
    @abstractmethod
    def get_by_id(self, pago_id: int) -> Optional[Pago]:
        pass

    @abstractmethod
    def get_pagos_by_pedido_id(self, pedido_id: int) -> List[Pago]:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Pago]:
        pass

    @abstractmethod
    def create(self, pago: Pago) -> Pago:
        pass

    @abstractmethod
    def update(self, pago_id: int, pago: Pago) -> Optional[Pago]:
        pass

    @abstractmethod
    def delete(self, pago_id: int) -> bool:
        pass