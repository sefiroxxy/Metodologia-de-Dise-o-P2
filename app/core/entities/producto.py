from pydantic import BaseModel, Field
from typing import Optional

class Producto(BaseModel):
    id: Optional[int] = None
    nombre: str = Field(min_length=1)
    descripcion: Optional[str] = None
    precio: float = Field(gt=0)
    stock: int = Field(ge=0)