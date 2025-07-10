from typing import Dict, Any

clientes_db: Dict[int, Dict[str, Any]] = {}
pagos_db: Dict[int, Dict[str, Any]] = {}
pedidos_db: Dict[int, Dict[str, Any]] = {}
productos_db: Dict[int, Dict[str, Any]] = {}

cliente_id_counter = 0
pago_id_counter = 0
pedido_id_counter = 0
producto_id_counter = 0

def get_next_cliente_id() -> int:
    global cliente_id_counter
    cliente_id_counter += 1
    return cliente_id_counter

def get_next_pago_id() -> int:
    global pago_id_counter
    pago_id_counter += 1
    return pago_id_counter

def get_next_pedido_id() -> int:
    global pedido_id_counter
    pedido_id_counter += 1
    return pedido_id_counter

def get_next_producto_id() -> int:
    global producto_id_counter
    producto_id_counter += 1
    return producto_id_counter
