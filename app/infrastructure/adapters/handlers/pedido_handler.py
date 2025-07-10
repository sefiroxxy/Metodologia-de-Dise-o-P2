from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.application.services.pedido_servicio import PedidoServicio
from app.core.entities.pedido import Pedido
from app.infrastructure.adapters.dependency.dependencies import get_pedido_service
from app.infrastructure.adapters.schemas.pedido_esquema import PedidoCreate, PedidoUpdate

router = APIRouter()

@router.post("/pedidos", response_model=Pedido, status_code=status.HTTP_201_CREATED)
async def create_pedido_handler(
    pedido_create: PedidoCreate,
    pedido_service: PedidoServicio = Depends(get_pedido_service)
):
    pedido = Pedido(**pedido_create.dict())
    return pedido_service.create_pedido(pedido)

@router.get("/pedidos/{pedido_id}", response_model=Pedido)
async def get_pedido_handler(
    pedido_id: int,
    pedido_service: PedidoServicio = Depends(get_pedido_service)
):
    return pedido_service.get_pedido(pedido_id)

@router.get("/pedidos", response_model=List[Pedido])
async def get_all_pedidos_handler(
    skip: int = 0,
    limit: int = 100,
    pedido_service: PedidoServicio = Depends(get_pedido_service)
):
    return pedido_service.get_todos_los_pedidos(skip=skip, limit=limit)

@router.put("/pedidos/{pedido_id}", response_model=Pedido)
async def update_pedido_handler(
    pedido_id: int,
    pedido_update: PedidoUpdate,
    pedido_service: PedidoServicio = Depends(get_pedido_service)
):
    pedido_data = pedido_update.dict(exclude_unset=True)
    existing_pedido = pedido_service.get_pedido(pedido_id)
    for key, value in pedido_data.items():
        setattr(existing_pedido, key, value)
    return pedido_service.update_pedido(pedido_id, existing_pedido)

@router.delete("/pedidos/{pedido_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pedido_handler(
    pedido_id: int,
    pedido_service: PedidoServicio = Depends(get_pedido_service)
):
    if not pedido_service.delete_pedido(pedido_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido no encontrado.")
    return