from abc import ABC, abstractmethod
from typing import Dict
from app.test.cliente import (
    Cliente,
    ClienteNuevo,
    ClienteFrecuente,
    ClienteVip
)
from app.test.producto import Producto

class ClienteBD(ABC):
    @abstractmethod
    def crear_cliente(self, cliente: Cliente):
        pass

    @abstractmethod
    def cambiar_tipo_cliente(self, email: str, nuevo_tipo: str):
        pass

    @abstractmethod
    def listar_clientes(self):
        pass

    @abstractmethod
    def agregar_producto_a_cliente(self, email: str, producto: Producto):
        pass


class _RepositorioClientesReal(ClienteBD):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(_RepositorioClientesReal, cls).__new__(cls)
            cls._instance.clientes: Dict[str, Cliente] = {}
            print("Inicializando RepositorioClientesReal.")
        return cls._instance

    def crear_cliente(self, cliente: Cliente):
        if cliente.email in self.clientes:
            print(f"[ERROR] Ya existe un usuario con ese correo: {cliente.email}.")
        else:
            self.clientes[cliente.email] = cliente
            print(f"Cliente '{cliente.nombre}' insertado.")

    def cambiar_tipo_cliente(self, email: str, nuevo_tipo: str):
        if email not in self.clientes:
            print(f"[ERROR] Cliente con email '{email}' no encontrado.")
            return

        cliente_antiguo = self.clientes[email]
        nombre = cliente_antiguo.nombre
        direccion = cliente_antiguo.direccion
        productos_antiguos = cliente_antiguo.productos

        nuevo_cliente = None
        if nuevo_tipo == 'nuevo':
            nuevo_cliente = ClienteNuevo(nombre, email, direccion)
        elif nuevo_tipo == 'frecuente':
            nuevo_cliente = ClienteFrecuente(nombre, email, direccion)
        elif nuevo_tipo == 'VIP':
            nuevo_cliente = ClienteVip(nombre, email, direccion)
        else:
            print(f"[ERROR] Tipo de cliente '{nuevo_tipo}' no reconocido.")
            return

        nuevo_cliente.productos = productos_antiguos
        self.clientes[email] = nuevo_cliente
        print(f"Cliente '{nombre}' cambiado a tipo '{nuevo_tipo}'.")


    def agregar_producto_a_cliente(self, email: str, producto: Producto):
        cliente = self.clientes.get(email)
        if cliente:
            cliente.productos[producto.nombre] = producto
            print(f"Producto '{producto.nombre}' agregado al cliente '{cliente.nombre}'.")
        else:
            print(f"[ERROR] Cliente con email '{email}' no encontrado.")

    def listar_clientes(self):
        return list(self.clientes.values())


class RepositorioClientesProxy(ClienteBD):
    _instance = None 

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RepositorioClientesProxy, cls).__new__(cls)
            cls._instance._repositorio_real = _RepositorioClientesReal() 
        return cls._instance

    def _log_acceso(self, accion):
        print(f"[Proxy Log] Acceso a la operación: {accion}")

    def crear_cliente(self, cliente: Cliente):
        self._log_acceso(f"crear_cliente para {cliente.email}")
        self._repositorio_real.crear_cliente(cliente)

    def cambiar_tipo_cliente(self, email: str, nuevo_tipo: str):
        self._log_acceso(f"cambiar_tipo_cliente para {email} a {nuevo_tipo}")
        self._repositorio_real.cambiar_tipo_cliente(email, nuevo_tipo)

    def listar_clientes(self):
        self._log_acceso("listar_clientes")
        return self._repositorio_real.listar_clientes()

    def agregar_producto_a_cliente(self, email: str, producto: Producto):
        self._log_acceso(f"agregar_producto_a_cliente para {email}")
        self._repositorio_real.agregar_producto_a_cliente(email, producto)
