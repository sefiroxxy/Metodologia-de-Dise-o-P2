from abc import ABC, abstractmethod
from typing import Dict
from app.test.cliente import Cliente

class Pedido(ABC):
    def __init__(self, id: str, estado: str = 'pendiente'):
        self.id = id
        self.estado = estado
        self.clientes: Dict[str, Cliente] = {}
        self.productos: Dict[str, tuple] = {}

    @abstractmethod
    def get_descripcion(self) -> str:
        pass

    @abstractmethod
    def calcular_entrega(self):
        pass

    @abstractmethod
    def get_costo(self) -> float:
        pass

class PedidoBase(Pedido):
    def __init__(self, id: str, estado: str = 'pendiente', costo_base: float = 10.0):
        super().__init__(id, estado)
        self._costo_base = costo_base 

    def get_descripcion(self) -> str:
        return f"Pedido Base (ID: {self.id}, Estado: {self.estado})"

    def calcular_entrega(self):
        print("Cálculo de entrega: El pedido base no tiene reglas de entrega especiales.")

    def get_costo(self) -> float:
        return self._costo_base

class PedidoDecorator(Pedido, ABC):
    def __init__(self, wrapped_pedido: Pedido):
        super().__init__(wrapped_pedido.id, wrapped_pedido.estado)
        self._wrapped_pedido = wrapped_pedido

    def get_descripcion(self) -> str:
        return self._wrapped_pedido.get_descripcion()

    def calcular_entrega(self):
        self._wrapped_pedido.calcular_entrega()

    def get_costo(self) -> float:
        return self._wrapped_pedido.get_costo()


class PedidoEstandarDecorator(PedidoDecorator):
    def __init__(self, wrapped_pedido: Pedido):
        super().__init__(wrapped_pedido)
        self.nombre_servicio = "Servicio Estándar"

    def get_descripcion(self) -> str:
        return f"{self._wrapped_pedido.get_descripcion()}, con {self.nombre_servicio}"

    def calcular_entrega(self):
        self._wrapped_pedido.calcular_entrega()
        print("Regla Estándar: Su pedido será entregado en 3-5 días hábiles.")

    def get_costo(self) -> float:
        return self._wrapped_pedido.get_costo() + 0.0 

class PedidoExpresDecorator(PedidoDecorator):
    def __init__(self, wrapped_pedido: Pedido, tipo_entrega: str = 'instantaneo'):
        super().__init__(wrapped_pedido)
        if tipo_entrega == 'dia_siguiente':
            self.tipo_entrega = 'dia_siguiente'
            self.nombre_servicio = "Servicio Exprés Día Siguiente"
            self.costo_extra = 8.0
        else: # Default or invalid input
            self.tipo_entrega = 'instantaneo'
            self.nombre_servicio = "Servicio Exprés Instantáneo"
            self.costo_extra = 15.0

    def get_descripcion(self) -> str:
        return f"{self._wrapped_pedido.get_descripcion()}, con {self.nombre_servicio}"

    def calcular_entrega(self):
        self._wrapped_pedido.calcular_entrega()
        if self.tipo_entrega == 'instantaneo':
            print("Regla Exprés Instantáneo: Su pedido se entregará hoy mismo (dentro de 2-4 horas).")
        elif self.tipo_entrega == 'dia_siguiente':
            print("Regla Exprés Día Siguiente: Su pedido se entregará el día siguiente con cargo extra.")

    def get_costo(self) -> float:
        return self._wrapped_pedido.get_costo() + self.costo_extra

class PedidoProgramadoDecorator(PedidoDecorator):
    def __init__(self, wrapped_pedido: Pedido, fecha_entrega: str):
        super().__init__(wrapped_pedido)
        self.nombre_servicio = "Servicio Programado"
        self.fecha_entrega = fecha_entrega
        self.costo_extra = 5.0

    def get_descripcion(self) -> str:
        return f"{self._wrapped_pedido.get_descripcion()}, con {self.nombre_servicio} para {self.fecha_entrega}"

    def calcular_entrega(self):
        self._wrapped_pedido.calcular_entrega()
        print(f"Regla Programado: Su pedido se entregará el día {self.fecha_entrega}.")

    def get_costo(self) -> float:
        return self._wrapped_pedido.get_costo() + self.costo_extra

class PedidoInternacionalDecorator(PedidoDecorator):
    def __init__(self, wrapped_pedido: Pedido, impuesto_porcentaje: float = 0.1):
        super().__init__(wrapped_pedido)
        self.nombre_servicio = "Servicio Internacional"
        self.impuesto_porcentaje = impuesto_porcentaje

    def get_descripcion(self) -> str:
        return f"{self._wrapped_pedido.get_descripcion()}, con {self.nombre_servicio} (impuesto aduanero)"

    def calcular_entrega(self):
        self._wrapped_pedido.calcular_entrega()
        print("Regla Internacional: Se aplican regulaciones aduaneras. La entrega puede tardar más.")

    def get_costo(self) -> float:
        base_cost = self._wrapped_pedido.get_costo()
        return base_cost * (1 + self.impuesto_porcentaje)

class GestorPedidos:
    def __init__(self):
        self.tipos_pedido_disponibles = {}

    def agregar_tipo_pedido(self, nombre: str, constructor_func):
        self.tipos_pedido_disponibles[nombre] = constructor_func
        print(f"Se ha agregado el tipo de pedido: {nombre}")

    def crear_pedido_con_tipo(self, pedido_base: PedidoBase, tipo_nombre: str, **kwargs) -> Pedido:
        if tipo_nombre in self.tipos_pedido_disponibles:
            constructor = self.tipos_pedido_disponibles[tipo_nombre]
            return constructor(pedido_base, **kwargs)
        else:
            print(f"El tipo de pedido '{tipo_nombre}' no está disponible. Devolviendo pedido base.")
            return pedido_base

    def listar_tipos_pedido(self):
        print("Tipos de pedido disponibles:")
        for nombre in self.tipos_pedido_disponibles:
            print(f"- {nombre}")
