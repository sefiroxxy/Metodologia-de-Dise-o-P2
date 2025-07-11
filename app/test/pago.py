from abc import ABC, abstractmethod
from typing import Dict
from app.test.pedido import Pedido

class Factura(ABC):
    def __init__(self, total, descuento, impuesto):
        self.total = total
        self.descuento = descuento
        self.impuesto = impuesto
        self.pedido: Dict[str, Pedido] = {}  

class MetodoPago(ABC):
    def __init__(self, tipo='general'):
        self.tipo = tipo
        self.pedido: Dict[str, Pedido] = {}

    @abstractmethod
    def AgregarMetodoPago(self):
        pass

    @abstractmethod
    def ElimiarMetodoPago(self):
        pass


class GestorPagos:
    def __init__(self):
        self.metodos_disponibles = {}

    def agregar_metodo(self, nombre, metodo):
        self.metodos_disponibles[nombre] = metodo
        print(f"Se ha agregado el método de pago: {nombre}")

    def eliminar_metodo(self, nombre):
        if nombre in self.metodos_disponibles:
            del self.metodos_disponibles[nombre]
            print(f"Se ha eliminado el método de pago: {nombre}")
        else:
            print(f"El método de pago {nombre} no existe")

    def listar_metodos(self):
        print("Métodos de pago disponibles:")
        for nombre in self.metodos_disponibles:
            print(f"- {nombre}")

    def procesar_pago(self, metodo_nombre, pedido):
        if metodo_nombre in self.metodos_disponibles:
            metodo = self.metodos_disponibles[metodo_nombre]
            return metodo.procesar(pedido)
        else:
            print(f"El método de pago {metodo_nombre} no está disponible")
            return False


class PagoTarjeta(MetodoPago):
    def __init__(self):
        super().__init__(tipo="tarjeta")

    def AgregarMetodoPago(self):
        print("Método de pago con tarjeta agregado")

    def ElimiarMetodoPago(self):
        print("Método de pago con tarjeta eliminado")

    def procesar(self, pedido):
        print(f"Procesando pago con tarjeta para el pedido {pedido.id}")
        print("Pago con tarjeta realizado con éxito")
        pedido.estado = "pagado"
        return True


class PagoTransferencia(MetodoPago):
    def __init__(self):
        super().__init__(tipo="transferencia")

    def AgregarMetodoPago(self):
        print("Método de pago por transferencia agregado")

    def ElimiarMetodoPago(self):
        print("Método de pago por transferencia eliminado")

    def procesar(self, pedido):
        print(f"Procesando pago por transferencia para el pedido {pedido.id}")
        print("Pago por transferencia realizado con éxito")
        pedido.estado = "pagado"
        return True


class PagoCriptomoneda(MetodoPago):
    def __init__(self):
        super().__init__(tipo="criptomoneda")

    def AgregarMetodoPago(self):
        print("Método de pago con criptomoneda agregado")

    def ElimiarMetodoPago(self):
        print("Método de pago con criptomoneda eliminado")

    def procesar(self, pedido):
        print(f"Procesando pago con criptomoneda para el pedido {pedido.id}")
        print("Pago con criptomoneda realizado con éxito")
        pedido.estado = "pagado"
        return True


class PagoContraEntrega(MetodoPago):
    def __init__(self):
        super().__init__(tipo="contra_entrega")

    def AgregarMetodoPago(self):
        print("Método de pago contra entrega agregado")

    def ElimiarMetodoPago(self):
        print("Método de pago contra entrega eliminado")

    def procesar(self, pedido):
        print(f"Pedido {pedido.id} marcado para pago contra entrega")
        print("El pago se realizará en el momento de la entrega")
        return True


class GestorFacturacion:
    def generar_factura(self, pedido, descuento=0, impuesto=0):
        total = sum(producto.precio_unitario * cantidad 
                    for producto, cantidad in pedido.productos.values())

        total_con_descuento = total * (1 - descuento / 100)

        total_final = total_con_descuento * (1 + impuesto / 100)

        factura = FacturaConcreta(total_final, descuento, impuesto)
        factura.pedido[pedido.id] = pedido

        self.mostrar_factura(factura, pedido)

        return factura

    def mostrar_factura(self, factura, pedido):
        print("\n===== FACTURA =====")
        print(f"Pedido ID: {pedido.id}")
        print(f"Estado: {pedido.estado}")
        print("\nProductos:")

        subtotal = 0
        for producto, cantidad in pedido.productos.values():
            precio_total = producto.precio_unitario * cantidad
            subtotal += precio_total
            print(f"- {producto.nombre}: {cantidad} x ${producto.precio_unitario} = ${precio_total}")

        print(f"\nSubtotal: ${subtotal}")

        if factura.descuento > 0:
            descuento_valor = subtotal * (factura.descuento / 100)
            print(f"Descuento ({factura.descuento}%): -${descuento_valor}")

        if factura.impuesto > 0:
            print(f"Impuesto ({factura.impuesto}%): ${subtotal * (factura.impuesto / 100)}")

        print(f"Total: ${factura.total}")
        print("===================\n")


class FacturaConcreta(Factura):
    def __init__(self, total, descuento, impuesto):
        super().__init__(total, descuento, impuesto)

class Validador(ABC):
    def __init__(self):
        self.siguiente = None

    def enlazar(self, siguiente):
        self.siguiente = siguiente
        return siguiente

    def ejecutar(self, pedido):
        if self.validar(pedido):
            if self.siguiente:
                return self.siguiente.ejecutar(pedido)
            return True
        return False

    @abstractmethod
    def validar(self, pedido):
        pass


class VerificarCliente(Validador):
    def validar(self, pedido):
        if pedido.clientes and isinstance(pedido.clientes, dict):
            print("[✔] Cliente verificado.")
            return True
        print("[✖] Cliente no válido.")
        return False


class ControlFraude(Validador):
    def validar(self, pedido):
        print("[✔] Control de fraude: aprobado.")
        return True


class RegistroAuditoria(Validador):
    def validar(self, pedido):
        print(f"[✔] Auditoría registrada para el pedido {pedido.id}")
        return True
    

class PagoProxy(MetodoPago):
    def __init__(self, metodo_real: MetodoPago, validador: Validador):
        super().__init__(tipo=metodo_real.tipo)
        self.metodo_real = metodo_real
        self.validador = validador

    def AgregarMetodoPago(self):
        self.metodo_real.AgregarMetodoPago()

    def ElimiarMetodoPago(self):
        self.metodo_real.ElimiarMetodoPago()

    def procesar(self, pedido):
        print(f"[Proxy] Validando el pago del pedido {pedido.id}...")
        if self.validador.ejecutar(pedido):
            print("[Proxy] Validaciones superadas.")
            return self.metodo_real.procesar(pedido)
        print("[Proxy] Pago cancelado por validación fallida.")
        return False
    

class PasarelaQRExterna:
    def autenticar(self):
        print("[QR] Autenticando token temporal...")

    def validar_ubicacion(self):
        print("[QR] Validando geolocalización e IP segura...")

    def registrar_transaccion(self, exito=True):
        estado = "éxito" if exito else "fallo"
        print(f"[QR] Transacción registrada con {estado}.")


class PagoQR(MetodoPago):
    def __init__(self, pasarela: PasarelaQRExterna):
        super().__init__(tipo="qr")
        self.pasarela = pasarela

    def AgregarMetodoPago(self):
        print("[QR] Método de pago QR agregado.")

    def ElimiarMetodoPago(self):
        print("[QR] Método de pago QR eliminado.")

    def procesar(self, pedido):
        self.pasarela.autenticar()
        self.pasarela.validar_ubicacion()
        self.pasarela.registrar_transaccion(exito=True)
        pedido.estado = "pagado"
        print(f"[QR] Pago exitoso para el pedido {pedido.id}")
        return True