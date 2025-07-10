from typing import List, Optional, Dict, Any, Callable
from app.core.entities.pago import Pago
from app.core.ports.repositories.pago_repositorio_base import PagoRepositorioBase

class PagoRepositorio(PagoRepositorioBase):
    def __init__(self, db: Dict[int, Dict[str, Any]], id_generator: Callable[[], int]):
        self.db = db
        self.id_generator = id_generator

    def get_by_id(self, pago_id: int) -> Optional[Pago]:
        data = self.db.get(pago_id)
        return Pago(**data) if data else None

    def get_pagos_by_pedido_id(self, pedido_id: int) -> List[Pago]:
        return [Pago(**data) for data in self.db.values() if data.get("pedido_id") == pedido_id]

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Pago]:
        return [Pago(**data) for data in list(self.db.values())[skip : skip + limit]]

    def create(self, pago: Pago) -> Pago:
        new_id = self.id_generator()
        pago.id = new_id
        self.db[new_id] = pago.dict()
        return pago

    def update(self, pago_id: int, pago: Pago) -> Optional[Pago]:
        if pago_id in self.db:
            pago.id = pago_id
            self.db[pago_id] = pago.dict()
            return pago
        return None

    def delete(self, pago_id: int) -> bool:
        if pago_id in self.db:
            del self.db[pago_id]
            return True
        return False
