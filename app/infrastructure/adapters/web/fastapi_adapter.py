from fastapi import APIRouter
from app.infrastructure.adapters.handlers import cliente_handler, pago_handler, pedido_handler, producto_handler, handler_health_check

# Este es el router principal que incluirá todos los routers de los handlers.
router = APIRouter(prefix="/api/v1")

# Incluye los routers de cada handler
router.include_router(cliente_handler.router, tags=["Clientes"])
router.include_router(pago_handler.router, tags=["Pagos"])
router.include_router(pedido_handler.router, tags=["Pedidos"])
router.include_router(producto_handler.router, tags=["Productos"])
router.include_router(handler_health_check.router, tags=["Health Check"])