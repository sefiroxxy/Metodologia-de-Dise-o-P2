from abc import ABC, abstractmethod
from typing import Dict
from app.test.producto import Producto

class ProductoBD(ABC):
    @abstractmethod
    def crear_producto(self, producto: Producto):
        pass

    @abstractmethod
    def listar_productos(self):
        pass

class RepositorioProductos(ProductoBD):
    def __init__(self):
        self.productos: Dict[str, Producto] = {}

    def crear_producto(self, producto: Producto):
        self.productos[producto.codigo] = producto
        print(f"Producto '{producto.nombre}' insertado.")

    def listar_productos(self):
        return list(self.productos.values())