from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.application.services.producto_servicio import ProductoServicio
from app.core.entities.producto import Producto
from app.infrastructure.adapters.dependency.dependencies import get_producto_service
from app.infrastructure.adapters.schemas.producto_esquema import ProductoCreate, ProductoUpdate

router = APIRouter()

@router.post("/productos", response_model=Producto, status_code=status.HTTP_201_CREATED)
async def create_producto_handler(
    producto_create: ProductoCreate,
    producto_service: ProductoServicio = Depends(get_producto_service)
):
    producto = Producto(**producto_create.dict())
    return producto_service.create_producto(producto)

@router.get("/productos/{producto_id}", response_model=Producto)
async def get_producto_handler(
    producto_id: int,
    producto_service: ProductoServicio = Depends(get_producto_service)
):
    return producto_service.get_producto(producto_id)

@router.get("/productos", response_model=List[Producto])
async def get_all_productos_handler(
    skip: int = 0,
    limit: int = 100,
    producto_service: ProductoServicio = Depends(get_producto_service)
):
    return producto_service.get_todos_los_productos(skip=skip, limit=limit)

@router.put("/productos/{producto_id}", response_model=Producto)
async def update_producto_handler(
    producto_id: int,
    producto_update: ProductoUpdate,
    producto_service: ProductoServicio = Depends(get_producto_service)
):
    producto_data = producto_update.dict(exclude_unset=True)
    existing_producto = producto_service.get_producto(producto_id)
    for key, value in producto_data.items():
        setattr(existing_producto, key, value)
    return producto_service.update_producto(producto_id, existing_producto)

@router.delete("/productos/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_producto_handler(
    producto_id: int,
    producto_service: ProductoServicio = Depends(get_producto_service)
):
    if not producto_service.delete_producto(producto_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado.")
    return