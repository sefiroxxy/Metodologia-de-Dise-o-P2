from abc import ABC, abstractmethod
from typing import Dict, List
from app.test.pedido import Pedido
import time


class PedidoBD(ABC):
    @abstractmethod
    def crear(self, pedido: Pedido):
        pass

    @abstractmethod
    def modificar(self, pedido: Pedido):
        pass

    @abstractmethod
    def cancelar(self, pedido: Pedido):
        pass

    @abstractmethod
    def recuperar(self, pedido_id: str):
        pass

    @abstractmethod
    def listar_pagado(self) -> List[Pedido]:
        pass

    @abstractmethod
    def listar_enpreparacion(self) -> List[Pedido]:
        pass

    @abstractmethod
    def listar_pedidos(self) -> List[Pedido]:
        pass


class RealRepositorioPedido(PedidoBD):
    def __init__(self):
        self.pedidos: Dict[str, Pedido] = {}
        print("RealRepositorioPedido: Inicializando conexión con la 'base de datos' de pedidos.")

    def crear(self, pedido: Pedido):
        self.pedidos[pedido.id] = pedido
        print(f"RealRepositorioPedido: Se creó su Pedido con ID: {pedido.id}. Estado inicial: {pedido.estado}.")

    def modificar(self, pedido: Pedido):
        transiciones = {
            'pendiente': 'pagado',
            'pagado': 'en preparacion',
            'en preparacion': 'enviado'
        }

        estado_actual = pedido.estado
        if estado_actual in transiciones:
            nuevo_estado = transiciones[estado_actual]
            pedido.estado = nuevo_estado
            print(f"RealRepositorioPedido: El estado del pedido '{pedido.id}' ha sido cambiado de '{estado_actual}' a '{nuevo_estado}'.")
        else:
            print(f"[ERROR] RealRepositorioPedido: No se puede modificar el estado del pedido '{pedido.id}' desde '{estado_actual}'.")

    def cancelar(self, pedido: Pedido):
        if pedido.estado not in ['entregado', 'cancelado']:
            pedido.estado = 'cancelado'
            print(f"RealRepositorioPedido: El estado del pedido {pedido.id} ha sido cambiado a 'cancelado'.")
        else:
            print(f"RealRepositorioPedido: No se puede cancelar el pedido {pedido.id} en estado '{pedido.estado}'.")

    def recuperar(self, pedido_id: str):
        print(f"RealRepositorioPedido: Consultando pedido {pedido_id} en la 'base de datos' (simulado)...")
        time.sleep(0.5) 
        encontrado = self.pedidos.get(pedido_id)
        if encontrado:
            print(f"RealRepositorioPedido: Pedido recuperado: ID={encontrado.id}, Estado={encontrado.estado}")
            return encontrado
        else:
            print(f"RealRepositorioPedido: No se encontró ningún pedido con ID {pedido_id}.")
            return None

    def listar_pagado(self) -> List[Pedido]:
        print("RealRepositorioPedido: Listando pedidos pagados.")
        return [p for p in self.pedidos.values() if p.estado == 'pagado']

    def listar_enpreparacion(self) -> List[Pedido]:
        print("RealRepositorioPedido: Listando pedidos en preparación.")
        return [p for p in self.pedidos.values() if p.estado == 'en preparacion']

    def listar_pedidos(self) -> List[Pedido]:
        print("RealRepositorioPedido: Listando todos los pedidos activos.")
        return [p for p in self.pedidos.values() if p.estado in {'pendiente', 'pagado', 'en preparacion'}]

class RepositorioPedidoProxy(PedidoBD):
    _instancia = None 
    _real_repositorio = None 

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._real_repositorio = RealRepositorioPedido()
            cls._instancia.cache = {} 
            print("RepositorioPedidoProxy: Instancia Singleton creada.")
        return cls._instancia

    def __init__(self):
        if not hasattr(self, 'cache'):
            self.cache = {}

    def crear(self, pedido: Pedido):
        if pedido.id in self.cache:
            del self.cache[pedido.id]
            print(f"RepositorioPedidoProxy: Caché invalidado para el pedido {pedido.id} debido a una nueva creación.")
        self._real_repositorio.crear(pedido)

    def modificar(self, pedido: Pedido):
        if pedido.id in self.cache:
            del self.cache[pedido.id]
            print(f"RepositorioPedidoProxy: Caché invalidado para el pedido {pedido.id} debido a una modificación.")
        self._real_repositorio.modificar(pedido)

    def cancelar(self, pedido: Pedido):
        if pedido.id in self.cache:
            del self.cache[pedido.id]
            print(f"RepositorioPedidoProxy: Caché invalidado para el pedido {pedido.id} debido a una cancelación.")
        self._real_repositorio.cancelar(pedido)

    def recuperar(self, pedido_id: str):
        if pedido_id in self.cache:
            print(f"RepositorioPedidoProxy: Devolviendo datos cacheados para el pedido {pedido_id}.")
            return self.cache[pedido_id]
        else:
            print(f"RepositorioPedidoProxy: Obteniendo datos reales para el pedido {pedido_id}.")
            pedido = self._real_repositorio.recuperar(pedido_id)
            if pedido:
                self.cache[pedido_id] = pedido
            return pedido

    def listar_pagado(self) -> List[Pedido]:
        return self._real_repositorio.listar_pagado()

    def listar_enpreparacion(self) -> List[Pedido]:
        return self._real_repositorio.listar_enpreparacion()

    def listar_pedidos(self) -> List[Pedido]:
        return self._real_repositorio.listar_pedidos()