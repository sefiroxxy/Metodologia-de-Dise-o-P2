from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class Cliente(BaseModel):
    id: Optional[int] = None
    nombre: str = Field(min_length=1)
    apellido: str = Field(min_length=1)
    email: EmailStr
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    fecha_registro: datetime = Field(default_factory=datetime.now)