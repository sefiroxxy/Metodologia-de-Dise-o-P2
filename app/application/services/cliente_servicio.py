from typing import List, Optional
from fastapi import HTTPException, status
from app.core.entities.cliente import Cliente
from app.core.ports.repositories.cliente_repositorio_base import ClienteRepositorioBase

class ClienteServicio:
    def __init__(self, cliente_repo: ClienteRepositorioBase):
        self.cliente_repo = cliente_repo

    def get_cliente(self, cliente_id: int) -> Cliente:
        cliente = self.cliente_repo.get_by_id(cliente_id)
        if not cliente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cliente con ID {cliente_id} no encontrado.")
        return cliente

    def get_cliente_by_email(self, email: str) -> Cliente:
        cliente = self.cliente_repo.get_by_email(email)
        if not cliente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cliente con email {email} no encontrado.")
        return cliente

    def get_todos_los_clientes(self, skip: int = 0, limit: int = 100) -> List[Cliente]:
        return self.cliente_repo.get_all(skip, limit)

    def create_cliente(self, cliente: Cliente) -> Cliente:
        if self.cliente_repo.get_by_email(cliente.email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Ya existe un cliente con el email {cliente.email}.")
        return self.cliente_repo.create(cliente)

    def update_cliente(self, cliente_id: int, cliente: Cliente) -> Cliente:
        existing_cliente = self.cliente_repo.get_by_id(cliente_id)
        if not existing_cliente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cliente con ID {cliente_id} no encontrado.")
        
        if cliente.email != existing_cliente.email and self.cliente_repo.get_by_email(cliente.email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Ya existe otro cliente con el email {cliente.email}.")
            
        updated_cliente = self.cliente_repo.update(cliente_id, cliente)
        if not updated_cliente:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al actualizar el cliente.")
        return updated_cliente

    def delete_cliente(self, cliente_id: int) -> bool:
        if not self.cliente_repo.get_by_id(cliente_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cliente con ID {cliente_id} no encontrado.")
        return self.cliente_repo.delete(cliente_id)