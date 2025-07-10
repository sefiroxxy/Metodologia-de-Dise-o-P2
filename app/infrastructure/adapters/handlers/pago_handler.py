from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.application.services.pago_servicio import PagoServicio
from app.core.entities.pago import Pago
from app.infrastructure.adapters.dependency.dependencies import get_pago_service
from app.infrastructure.adapters.schemas.pago_esquema import PagoCreate, PagoUpdate

router = APIRouter()

@router.post("/pagos", response_model=Pago, status_code=status.HTTP_201_CREATED)
async def create_pago_handler(
    pago_create: PagoCreate,
    pago_service: PagoServicio = Depends(get_pago_service)
):
    pago = Pago(**pago_create.dict())
    return pago_service.create_pago(pago)

@router.get("/pagos/{pago_id}", response_model=Pago)
async def get_pago_handler(
    pago_id: int,
    pago_service: PagoServicio = Depends(get_pago_service)
):
    return pago_service.get_pago(pago_id)

@router.get("/pagos", response_model=List[Pago])
async def get_all_pagos_handler(
    skip: int = 0,
    limit: int = 100,
    pago_service: PagoServicio = Depends(get_pago_service)
):
    return pago_service.get_todos_los_pagos(skip=skip, limit=limit)

@router.put("/pagos/{pago_id}", response_model=Pago)
async def update_pago_handler(
    pago_id: int,
    pago_update: PagoUpdate,
    pago_service: PagoServicio = Depends(get_pago_service)
):
    pago_data = pago_update.dict(exclude_unset=True)
    existing_pago = pago_service.get_pago(pago_id)
    for key, value in pago_data.items():
        setattr(existing_pago, key, value)
    return pago_service.update_pago(pago_id, existing_pago)

@router.delete("/pagos/{pago_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pago_handler(
    pago_id: int,
    pago_service: PagoServicio = Depends(get_pago_service)
):
    if not pago_service.delete_pago(pago_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado.")
    return
