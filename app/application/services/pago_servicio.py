from typing import List, Optional
from fastapi import HTTPException, status
from app.core.entities.pago import Pago
from app.core.ports.repositories.pago_repositorio_base import PagoRepositorioBase

class PagoServicio:
    def __init__(self, pago_repo: PagoRepositorioBase):
        self.pago_repo = pago_repo

    def get_pago(self, pago_id: int) -> Pago:
        pago = self.pago_repo.get_by_id(pago_id)
        if not pago:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pago con ID {pago_id} no encontrado.")
        return pago

    def get_pagos_by_pedido_id(self, pedido_id: int) -> List[Pago]:
        return self.pago_repo.get_pagos_by_pedido_id(pedido_id)

    def get_todos_los_pagos(self, skip: int = 0, limit: int = 100) -> List[Pago]:
        return self.pago_repo.get_all(skip, limit)

    def create_pago(self, pago: Pago) -> Pago:
        return self.pago_repo.create(pago)

    def update_pago(self, pago_id: int, pago: Pago) -> Pago:
        if not self.pago_repo.get_by_id(pago_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pago con ID {pago_id} no encontrado.")
        updated_pago = self.pago_repo.update(pago_id, pago)
        if not updated_pago:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al actualizar el pago.")
        return updated_pago

    def delete_pago(self, pago_id: int) -> bool:
        if not self.pago_repo.get_by_id(pago_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pago con ID {pago_id} no encontrado.")
        return self.pago_repo.delete(pago_id)
