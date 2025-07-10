from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class PedidoBase(BaseModel):
    cliente_id: int
    productos_ids: List[int] = Field(min_items=1)
    estado_pedido: str = Field(min_length=1)
    total: float = Field(gt=0)

class PedidoCreate(PedidoBase):
    pass

class PedidoUpdate(PedidoBase):
    cliente_id: Optional[int] = None
    productos_ids: Optional[List[int]] = Field(None, min_items=1)
    fecha_pedido: Optional[datetime] = None
    estado_pedido: Optional[str] = Field(None, min_length=1)
    total: Optional[float] = Field(None, gt=0)