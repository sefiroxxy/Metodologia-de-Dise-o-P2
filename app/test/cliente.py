from abc import ABC, abstractmethod
from typing import Dict, List
from app.test.producto import Producto

class Cliente(ABC):
    def __init__(self, nombre, email, direccion, tipo_cliente='nuevo'):
        self.nombre = nombre
        self.email = email
        self.direccion = direccion
        self.tipo_cliente = tipo_cliente
        self.productos: Dict[str, 'Producto'] = {}
        self.beneficios: List[Beneficio] = [] 

    def __str__(self):
        return f" {self.nombre} - {self.email} - {self.direccion} - {self.tipo_cliente}"

    def aplicar_beneficios(self):
        for beneficio in self.beneficios:
            beneficio.aplicar(self)

    @abstractmethod
    def calcular_descuento(self):
        pass

class Beneficio(ABC):
    @abstractmethod
    def aplicar(self, cliente: Cliente):
        pass

    @abstractmethod
    def get_descripcion(self):
        pass

class ClienteBeneficioDecorator(Cliente):
    def __init__(self, cliente: Cliente):
        self._cliente = cliente
        super().__init__(cliente.nombre, cliente.email, cliente.direccion, cliente.tipo_cliente)
        self.productos = cliente.productos
        self.beneficios = cliente.beneficios

    def __getattr__(self, name):
        return getattr(self._cliente, name)

    def calcular_descuento(self):
        return self._cliente.calcular_descuento()

class DescuentoSimple(Beneficio):
    def __init__(self, porcentaje):
        self.porcentaje = porcentaje

    def aplicar(self, cliente: Cliente):
        pass

    def get_descripcion(self):
        return f"Descuento del {self.porcentaje}%"

class EnvioGratis(Beneficio):
    def aplicar(self, cliente: Cliente):
        print(f"[{cliente.nombre}] Beneficio: Envío gratis activado.")

    def get_descripcion(self):
        return "Envío gratis"

class Cashback(Beneficio):
    def __init__(self, porcentaje):
        self.porcentaje = porcentaje

    def aplicar(self, cliente: Cliente):
        print(f"[{cliente.nombre}] Beneficio: {self.porcentaje}% de cashback en próximas compras.")

    def get_descripcion(self):
        return f"Cashback del {self.porcentaje}%"


class ClienteNuevo(Cliente):
    def __init__(self, nombre, email, direccion):
        super().__init__(nombre, email, direccion, tipo_cliente='nuevo')
        self.beneficios.append(DescuentoSimple(5))

    def calcular_descuento(self):
        return 5

class ClienteFrecuente(Cliente):
    def __init__(self, nombre, email, direccion):
        super().__init__(nombre, email, direccion, tipo_cliente='frecuente')
        self.beneficios.append(DescuentoSimple(10))

    def calcular_descuento(self):
        return 10

class ClienteVip(Cliente):
    def __init__(self, nombre, email, direccion):
        super().__init__(nombre, email, direccion, tipo_cliente='VIP')
        self.beneficios.append(DescuentoSimple(15))
        self.beneficios.append(EnvioGratis())

    def calcular_descuento(self):
        return 15
