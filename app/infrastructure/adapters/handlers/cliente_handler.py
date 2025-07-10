from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.application.services.cliente_servicio import ClienteServicio
from app.core.entities.cliente import Cliente
from app.infrastructure.adapters.dependency.dependencies import get_cliente_service
from app.infrastructure.adapters.schemas.cliente_esquema import ClienteCreate, ClienteUpdate

router = APIRouter()

@router.post("/clientes", response_model=Cliente, status_code=status.HTTP_201_CREATED)
async def create_cliente_handler(
    cliente_create: ClienteCreate,
    cliente_service: ClienteServicio = Depends(get_cliente_service)
):
    cliente = Cliente(**cliente_create.dict())
    return cliente_service.create_cliente(cliente)

@router.get("/clientes/{cliente_id}", response_model=Cliente)
async def get_cliente_handler(
    cliente_id: int,
    cliente_service: ClienteServicio = Depends(get_cliente_service)
):
    return cliente_service.get_cliente(cliente_id)

@router.get("/clientes", response_model=List[Cliente])
async def get_all_clientes_handler(
    skip: int = 0,
    limit: int = 100,
    cliente_service: ClienteServicio = Depends(get_cliente_service)
):
    return cliente_service.get_todos_los_clientes(skip=skip, limit=limit)

@router.patch("/clientes/{cliente_id}", response_model=Cliente)
async def update_cliente_handler(
    cliente_id: int,
    cliente_update: ClienteUpdate,
    cliente_service: ClienteServicio = Depends(get_cliente_service)
):
    cliente_data = cliente_update.dict(exclude_unset=True)
    existing_cliente = cliente_service.get_cliente(cliente_id) # Obtener para conservar datos no actualizados
    for key, value in cliente_data.items():
        setattr(existing_cliente, key, value)
    return cliente_service.update_cliente(cliente_id, existing_cliente)

@router.delete("/clientes/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cliente_handler(
    cliente_id: int,
    cliente_service: ClienteServicio = Depends(get_cliente_service)
):
    if not cliente_service.delete_cliente(cliente_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado.")
    return