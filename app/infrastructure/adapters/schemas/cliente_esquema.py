from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class ClienteBase(BaseModel):
    nombre: str = Field(min_length=1)
    apellido: str = Field(min_length=1)
    email: EmailStr
    direccion: Optional[str] = None
    telefono: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(ClienteBase):
    nombre: Optional[str] = Field(None, min_length=1)
    apellido: Optional[str] = Field(None, min_length=1)
    email: Optional[EmailStr] = None
    fecha_registro: Optional[datetime] = None

# No se necesita un ClienteSchema aparte si Cliente (entidad) ya es un Pydantic BaseModel
# y se usa directamente como modelo de respuesta en los handlers.
# Sin embargo, si se quieren ocultar o transformar campos, se podría definir.
# class ClienteSchema(ClienteBase):
#     id: int
#     fecha_registro: datetime
#
#     class Config:
#         orm_mode = True # Para compatibilidad con ORMs, si se usara.