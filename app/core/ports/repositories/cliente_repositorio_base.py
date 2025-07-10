from abc import ABC, abstractmethod
from typing import List, Optional
from app.core.entities.cliente import Cliente

class ClienteRepositorioBase(ABC):
    @abstractmethod
    def get_by_id(self, cliente_id: int) -> Optional[Cliente]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Cliente]:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Cliente]:
        pass

    @abstractmethod
    def create(self, cliente: Cliente) -> Cliente:
        pass

    @abstractmethod
    def update(self, cliente_id: int, cliente: Cliente) -> Optional[Cliente]:
        pass

    @abstractmethod
    def delete(self, cliente_id: int) -> bool:
        pass