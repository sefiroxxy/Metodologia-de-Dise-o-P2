from app.infrastructure.adapters.database.database import (
    clientes_db, pagos_db, pedidos_db, productos_db,
    get_next_cliente_id, get_next_pago_id, get_next_pedido_id, get_next_producto_id
)
from app.infrastructure.adapters.repositories.cliente_repositorio import ClienteRepositorio
from app.infrastructure.adapters.repositories.pago_repositorio import PagoRepositorio
from app.infrastructure.adapters.repositories.pedido_repositorio import PedidoRepositorio
from app.infrastructure.adapters.repositories.producto_repositorio import ProductoRepositorio

from app.application.services.cliente_servicio import ClienteServicio
from app.application.services.pago_servicio import PagoServicio
from app.application.services.pedido_servicio import PedidoServicio
from app.application.services.producto_servicio import ProductoServicio

# Dependencias para los repositorios
def get_cliente_repository() -> ClienteRepositorio:
    return ClienteRepositorio(clientes_db, get_next_cliente_id)

def get_pago_repository() -> PagoRepositorio:
    return PagoRepositorio(pagos_db, get_next_pago_id)

def get_pedido_repository() -> PedidoRepositorio:
    return PedidoRepositorio(pedidos_db, get_next_pedido_id)

def get_producto_repository() -> ProductoRepositorio:
    return ProductoRepositorio(productos_db, get_next_producto_id)

# Dependencias para los servicios (usando los repositorios)
def get_cliente_service() -> ClienteServicio:
    return ClienteServicio(get_cliente_repository())

def get_pago_service() -> PagoServicio:
    return PagoServicio(get_pago_repository())

def get_pedido_service() -> PedidoServicio:
    return PedidoServicio(get_pedido_repository())

def get_producto_service() -> ProductoServicio:
    return ProductoServicio(get_producto_repository())