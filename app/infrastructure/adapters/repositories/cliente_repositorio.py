from typing import List, Optional, Dict, Any, Callable
from app.core.entities.cliente import Cliente
from app.core.ports.repositories.cliente_repositorio_base import ClienteRepositorioBase

class ClienteRepositorio(ClienteRepositorioBase):
    def __init__(self, db: Dict[int, Dict[str, Any]], id_generator: Callable[[], int]):
        self.db = db
        self.id_generator = id_generator

    def get_by_id(self, cliente_id: int) -> Optional[Cliente]:
        data = self.db.get(cliente_id)
        return Cliente(**data) if data else None

    def get_by_email(self, email: str) -> Optional[Cliente]:
        for cliente_data in self.db.values():
            if cliente_data.get("email") == email:
                return Cliente(**cliente_data)
        return None

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Cliente]:
        return [Cliente(**data) for data in list(self.db.values())[skip : skip + limit]]

    def create(self, cliente: Cliente) -> Cliente:
        new_id = self.id_generator()
        cliente.id = new_id
        self.db[new_id] = cliente.dict()
        return cliente

    def update(self, cliente_id: int, cliente: Cliente) -> Optional[Cliente]:
        if cliente_id in self.db:
            cliente.id = cliente_id
            self.db[cliente_id] = cliente.dict()
            return cliente
        return None

    def delete(self, cliente_id: int) -> bool:
        if cliente_id in self.db:
            del self.db[cliente_id]
            return True
        return False