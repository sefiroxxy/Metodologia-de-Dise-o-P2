from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Pedido(BaseModel):
    id: Optional[int] = None
    cliente_id: int
    productos_ids: List[int] = Field(min_items=1)
    fecha_pedido: datetime = Field(default_factory=datetime.now)
    estado_pedido: str = Field(min_length=1)
    total: float = Field(gt=0)
