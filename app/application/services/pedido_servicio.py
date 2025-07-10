from typing import List, Optional
from fastapi import HTTPException, status
from app.core.entities.pedido import Pedido
from app.core.ports.repositories.pedido_repositorio_base import PedidoRepositorioBase

class PedidoServicio:
    def __init__(self, pedido_repo: PedidoRepositorioBase):
        self.pedido_repo = pedido_repo

    def get_pedido(self, pedido_id: int) -> Pedido:
        pedido = self.pedido_repo.get_by_id(pedido_id)
        if not pedido:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pedido con ID {pedido_id} no encontrado.")
        return pedido

    def get_pedidos_by_cliente_id(self, cliente_id: int) -> List[Pedido]:
        return self.pedido_repo.get_pedidos_by_cliente_id(cliente_id)

    def get_todos_los_pedidos(self, skip: int = 0, limit: int = 100) -> List[Pedido]:
        return self.pedido_repo.get_all(skip, limit)

    def create_pedido(self, pedido: Pedido) -> Pedido:
        # Aquí se podrían añadir validaciones adicionales, como verificar si cliente_id y productos_ids existen
        return self.pedido_repo.create(pedido)

    def update_pedido(self, pedido_id: int, pedido: Pedido) -> Pedido:
        if not self.pedido_repo.get_by_id(pedido_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pedido con ID {pedido_id} no encontrado.")
        updated_pedido = self.pedido_repo.update(pedido_id, pedido)
        if not updated_pedido:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al actualizar el pedido.")
        return updated_pedido

    def delete_pedido(self, pedido_id: int) -> bool:
        if not self.pedido_repo.get_by_id(pedido_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pedido con ID {pedido_id} no encontrado.")
        return self.pedido_repo.delete(pedido_id)