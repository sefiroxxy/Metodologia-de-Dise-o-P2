from app.test.cliente import (
    ClienteNuevo,
    ClienteFrecuente,
    ClienteVip,
    EnvioGratis,
    Cashback,
    DescuentoSimple,
)
from app.test.producto import Producto
from app.test.repositorio_cliente import RepositorioClientesProxy
from app.test.repositorio_producto import RepositorioProductos
from app.test.pedido import (
    PedidoBase,
    PedidoEstandarDecorator,
    PedidoExpresDecorator,
    PedidoProgramadoDecorator,
    PedidoInternacionalDecorator,
    GestorPedidos,
)
from app.test.pago import (
    GestorPagos,
    PagoTarjeta,
    PagoTransferencia,
    PagoCriptomoneda,
    PagoContraEntrega,
    GestorFacturacion,
    VerificarCliente,
    ControlFraude,
    RegistroAuditoria,
    PagoProxy,
    PasarelaQRExterna,
    PagoQR,
)
from app.test.repositorio_pedido import RepositorioPedidoProxy



print("===== DEMOSTRACIÓN DE SISTEMA DE PEDIDOS =====")
print("\n--- 1. Gestión de Productos ---")
gestor_productos = RepositorioProductos()

producto1 = Producto("Laptop Dell XPS", "LDX001", 1500.00, 10)
producto2 = Producto("Mouse Logitech MX", "MLM002", 75.50, 25)
producto3 = Producto("Teclado Mecánico", "TKM003", 120.00, 15)
producto4 = Producto("Monitor Ultrawide", "MUW004", 600.00, 8)
producto5 = Producto("Webcam HD", "WCH005", 50.00, 30)

gestor_productos.crear_producto(producto1)
gestor_productos.crear_producto(producto2)
gestor_productos.crear_producto(producto3)
gestor_productos.crear_producto(producto4)
gestor_productos.crear_producto(producto5)

print("\nProductos disponibles:")
for prod in gestor_productos.listar_productos():
    print(prod)

print("\n--- 2. Gestión de Clientes (con Proxy y Singleton) ---")
repo_clientes = RepositorioClientesProxy()
repo_clientes2 = RepositorioClientesProxy()
print(
    f"¿repo_clientes y repo_clientes2 son la misma instancia? {repo_clientes is repo_clientes2}"
)

cliente1 = ClienteNuevo("Ana García", "ana.garcia@example.com", "Calle Falsa 123")
cliente2 = ClienteFrecuente(
    "Luis Pérez", "luis.perez@example.com", "Avenida Siempre Viva 45"
)
cliente3 = ClienteVip("Sofía Ruiz", "sofia.ruiz@example.com", "Plaza Mayor 7")

repo_clientes.crear_cliente(cliente1)
repo_clientes.crear_cliente(cliente2)
repo_clientes.crear_cliente(cliente3)

repo_clientes.agregar_producto_a_cliente(cliente1.email, producto1)
repo_clientes.agregar_producto_a_cliente(cliente1.email, producto2)
repo_clientes.agregar_producto_a_cliente(cliente2.email, producto3)
repo_clientes.agregar_producto_a_cliente(cliente3.email, producto4)
repo_clientes.agregar_producto_a_cliente(cliente3.email, producto5)

print("\nListado de clientes y sus beneficios iniciales:")
for cliente in repo_clientes.listar_clientes():
    print(cliente)
    print(f"  Descuento base: {cliente.calcular_descuento()}%")
    cliente.aplicar_beneficios()
    print("  Beneficios:")
    for b in cliente.beneficios:
        print(f"  - {b.get_descripcion()}")
    if cliente.productos:
        print("  Productos asociados:")
        for prod_name, prod_obj in cliente.productos.items():
            print(f"    - {prod_obj.nombre}")

print("\n--- Cambio de tipo de cliente y re-evaluación de beneficios ---")
repo_clientes.cambiar_tipo_cliente("ana.garcia@example.com", "frecuente")
repo_clientes.cambiar_tipo_cliente("luis.perez@example.com", "VIP")

print("\nListado de clientes y sus beneficios después del cambio:")
for cliente in repo_clientes.listar_clientes():
    print(cliente)
    print(f"  Descuento base: {cliente.calcular_descuento()}%")
    cliente.aplicar_beneficios()
    print("  Beneficios:")
    for b in cliente.beneficios:
        print(f"  - {b.get_descripcion()}")


print("\n--- Prueba de Decorator en Cliente (añadiendo beneficios extra) ---")
cliente_ana = repo_clientes._repositorio_real.clientes[
    "ana.garcia@example.com"
]  
cliente_ana.beneficios.append(Cashback(2))
print(f"\nCliente Ana después de añadir Cashback:")
print(cliente_ana)
cliente_ana.aplicar_beneficios()
print("  Beneficios:")
for b in cliente_ana.beneficios:
    print(f"  - {b.get_descripcion()}")

print("\n--- 3. Gestión de Pedidos (con Decorator y Repositorio Proxy/Singleton) ---")
gestor_pedidos = GestorPedidos()
gestor_pedidos.agregar_tipo_pedido(
    "estandar", lambda pedido_base: PedidoEstandarDecorator(pedido_base)
)
gestor_pedidos.agregar_tipo_pedido(
    "expres_instantaneo", lambda pedido_base: PedidoExpresDecorator(pedido_base)
)
gestor_pedidos.agregar_tipo_pedido(
    "expres_dia_siguiente",
    lambda pedido_base: PedidoExpresDecorator(pedido_base, "dia_siguiente"),
)
gestor_pedidos.agregar_tipo_pedido(
    "programado",
    lambda pedido_base, fecha_entrega: PedidoProgramadoDecorator(
        pedido_base, fecha_entrega
    ),
)
gestor_pedidos.agregar_tipo_pedido(
    "internacional",
    lambda pedido_base: PedidoInternacionalDecorator(pedido_base),
)

pedido_base_simple = PedidoBase("PED001", costo_base=20.0)
pedido_estandar = gestor_pedidos.crear_pedido_con_tipo(pedido_base_simple, "estandar")
pedido_estandar.clientes[cliente1.email] = cliente1
pedido_estandar.productos = {
    producto1.codigo: (producto1, 1),
    producto2.codigo: (producto2, 2),
}

pedido_expres = gestor_pedidos.crear_pedido_con_tipo(
    PedidoBase("PED002", costo_base=25.0), "expres_instantaneo"
)
pedido_expres.clientes[cliente2.email] = cliente2
pedido_expres.productos = {producto3.codigo: (producto3, 1)}

pedido_programado = gestor_pedidos.crear_pedido_con_tipo(
    PedidoBase("PED003", costo_base=18.0), "programado", fecha_entrega="2025-07-20"
)
pedido_programado.clientes[cliente3.email] = cliente3
pedido_programado.productos = {
    producto4.codigo: (producto4, 1),
    producto5.codigo: (producto5, 1),
}

pedido_internacional = gestor_pedidos.crear_pedido_con_tipo(
    PedidoBase("PED004", costo_base=50.0), "internacional"
)
pedido_internacional.clientes[cliente1.email] = cliente1
pedido_internacional.productos = {producto1.codigo: (producto1, 1)}

print("\nDescripción y costo de los pedidos creados:")
for pedido in [
    pedido_estandar,
    pedido_expres,
    pedido_programado,
    pedido_internacional,
]:
    print(f"- {pedido.get_descripcion()}")
    print(f"  Costo total: ${pedido.get_costo():.2f}")
    pedido.calcular_entrega()

repo_pedidos = RepositorioPedidoProxy()
repo_pedidos.crear(pedido_estandar)
repo_pedidos.crear(pedido_expres)
repo_pedidos.crear(pedido_programado)
repo_pedidos.crear(pedido_internacional)

print("\n--- Recuperando pedidos del repositorio (demostración de caché del Proxy) ---")
rec_pedido_estandar = repo_pedidos.recuperar("PED001")
rec_pedido_estandar_cached = repo_pedidos.recuperar(
    "PED001"
)
print(f"Estado de PED001: {rec_pedido_estandar.estado}")

print("\n--- Modificando estado de pedido (invalida caché del Proxy) ---")
repo_pedidos.modificar(rec_pedido_estandar)  
rec_pedido_estandar_after_mod = repo_pedidos.recuperar(
    "PED001"
)  
print(f"Nuevo estado de PED001: {rec_pedido_estandar_after_mod.estado}")

print("\n--- 4. Gestión de Pagos (con Chain of Responsibility, Proxy y Adapter) ---")
gestor_pagos = GestorPagos()

gestor_pagos.agregar_metodo("tarjeta", PagoTarjeta())
gestor_pagos.agregar_metodo("transferencia", PagoTransferencia())
gestor_pagos.agregar_metodo("criptomoneda", PagoCriptomoneda())
gestor_pagos.agregar_metodo("contra_entrega", PagoContraEntrega())

verificar_cliente = VerificarCliente()
control_fraude = ControlFraude()
registro_auditoria = RegistroAuditoria()

verificar_cliente.enlazar(control_fraude).enlazar(registro_auditoria)

pago_tarjeta_seguro = PagoProxy(PagoTarjeta(), verificar_cliente)
gestor_pagos.agregar_metodo("tarjeta_segura", pago_tarjeta_seguro)

pasarela_qr_externa = PasarelaQRExterna()
pago_qr_adapter = PagoQR(pasarela_qr_externa)
gestor_pagos.agregar_metodo("qr", pago_qr_adapter)

gestor_pagos.listar_metodos()

print("\n--- Procesando pagos ---")
print("\nIntentando pago con Tarjeta Segura (con validaciones):")
gestor_pagos.procesar_pago("tarjeta_segura", pedido_estandar)
print(f"Estado final de PED001 después de intento de pago: {pedido_estandar.estado}")

pedido_prueba_sin_cliente_info = PedidoBase("PED999")
print("\nIntentando pago con Tarjeta Segura para un pedido sin información de cliente:")
gestor_pagos.procesar_pago("tarjeta_segura", pedido_prueba_sin_cliente_info)
print(f"Estado final de PED999: {pedido_prueba_sin_cliente_info.estado}")

print("\nProcesando pago con Transferencia para PED002:")
gestor_pagos.procesar_pago("transferencia", pedido_expres)
print(f"Estado final de PED002: {pedido_expres.estado}")

print("\nProcesando pago Contra Entrega para PED003:")
gestor_pagos.procesar_pago("contra_entrega", pedido_programado)
print(f"Estado final de PED003: {pedido_programado.estado}")

print("\nProcesando pago con QR para PED004:")
gestor_pagos.procesar_pago("qr", pedido_internacional)
print(f"Estado final de PED004: {pedido_internacional.estado}")

print("\n--- 5. Generación de Facturas ---")
gestor_facturacion = GestorFacturacion()

print("\nGenerando factura para PED001 (Estandar):")
gestor_facturacion.generar_factura(pedido_estandar, descuento=cliente_ana.calcular_descuento())

print("\nGenerando factura para PED002 (Express):")
gestor_facturacion.generar_factura(pedido_expres, descuento=cliente2.calcular_descuento())

print("\nGenerando factura para PED003 (Programado):")
gestor_facturacion.generar_factura(pedido_programado, descuento=cliente3.calcular_descuento())

print("\nGenerando factura para PED004 (Internacional con impuesto):")
gestor_facturacion.generar_factura(pedido_internacional, impuesto=10) 


print("\n===== FIN DE LA DEMOSTRACIÓN =====")    


from fastapi import FastAPI, HTTPException, status, Request, Depends
import logging

from app.infrastructure.adapters.web.fastapi_adapter import router as api_router

from app.application.services.producto_servicio import ProductoServicio
from app.infrastructure.adapters.dependency.dependencies import get_producto_service
from app.core.entities.producto import Producto

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="PayTrack API",
    description="API para la gestión de pagos con Arquitectura Hexagonal",
    version="1.0.0",
)

products_db = {}
product_id_counter = 0

@app.on_event("startup")
async def startup_event():
    global product_id_counter
    products_to_add = [
        {"nombre": "Laptop", "descripcion": "Potente laptop para trabajo y juegos", "precio": 1200.00, "stock": 50},
        {"nombre": "Mouse", "descripcion": "Mouse ergonómico inalámbrico", "precio": 25.00, "stock": 200},
        {"nombre": "Teclado Mecánico", "descripcion": "Teclado con switches Cherry MX", "precio": 90.00, "stock": 100},
        {"nombre": "Monitor Curvo", "descripcion": "Monitor de 27 pulgadas 144Hz", "precio": 300.00, "stock": 75},
    ]

    for product_data in products_to_add:
        product_id_counter += 1
        product = Producto(id=product_id_counter, **product_data)
        products_db[product.id] = product
        logger.info(f"Producto precargado: {product.nombre} con ID: {product.id}")

app.include_router(api_router)

@app.get("/")
async def root():
    logger.info("Endpoint raíz accedido.")
    return {"message": "Welcome to PayTrack API"}


logged_in_users = set()

@app.get("/login")
async def login(email: str):
    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El correo electrónico es requerido para el login.")
    if email in logged_in_users:
        return {"message": f"El usuario {email} ya está logeado."}
    logged_in_users.add(email)
    logger.info(f"Usuario {email} ha iniciado sesión.")
    return {"message": f"Usuario {email} logeado exitosamente."}

@app.get("/logout")
async def logout(email: str):
    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El correo electrónico es requerido para el logout.")
    if email not in logged_in_users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El usuario {email} no está logeado.")
    logged_in_users.remove(email)
    logger.info(f"Usuario {email} ha cerrado sesión.")
    return {"message": f"Usuario {email} deslogeado exitosamente."}

@app.post("/productos")
async def create_product(
    request: Request,
    nombre: str,
    descripcion: str,
    precio: float,
    stock: int,
    producto_service: ProductoServicio = Depends(get_producto_service)
):
    global product_id_counter
    product_id_counter += 1
    new_product_data = {
        "id": product_id_counter,
        "nombre": nombre,
        "descripcion": descripcion,
        "precio": precio,
        "stock": stock
    }
    try:
        new_product = Producto(**new_product_data)
        created_product = producto_service.create_producto(new_product)
        return created_product
    except HTTPException as e:
        logger.error(f"Error al crear producto: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Error inesperado al crear producto: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")
