from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Pago(BaseModel):
    id: Optional[int] = None
    pedido_id: int
    monto: float = Field(gt=0)
    metodo_pago: str = Field(min_length=1)
    estado_pago: str = Field(min_length=1) # Ej: "pendiente", "completado", "fallido"
    fecha_pago: datetime = Field(default_factory=datetime.now)