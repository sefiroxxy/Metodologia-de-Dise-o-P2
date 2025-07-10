# Directorio: app/main.py
from fastapi import FastAPI, HTTPException, status, Request, Depends
import logging

from app.infrastructure.adapters.web.fastapi_adapter import router as api_router

from app.application.services.producto_servicio import ProductoServicio
from app.infrastructure.adapters.dependency.dependencies import get_producto_service
from app.core.entities.producto import Producto

# Configura el logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="PayTrack API",
    description="API para la gestión de pagos con Arquitectura Hexagonal",
    version="1.0.0",
)

# Base de datos en memoria para productos (ejemplo)
products_db = {}
product_id_counter = 0

@app.on_event("startup")
async def startup_event():
    global product_id_counter
    # Productos predefinidos
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

# Endpoint de logeo y deslogeo (ejemplo con correo)
# NOTA: Esto es una implementación simplificada para el ejemplo.
# En un sistema real, implicaría JWT, sesiones, etc.
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
