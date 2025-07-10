from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PagoBase(BaseModel):
    pedido_id: int
    monto: float = Field(gt=0)
    metodo_pago: str = Field(min_length=1)
    estado_pago: str = Field(min_length=1)

class PagoCreate(PagoBase):
    pass

class PagoUpdate(PagoBase):
    pedido_id: Optional[int] = None
    monto: Optional[float] = Field(None, gt=0)
    metodo_pago: Optional[str] = Field(None, min_length=1)
    estado_pago: Optional[str] = Field(None, min_length=1)
    fecha_pago: Optional[datetime] = None
