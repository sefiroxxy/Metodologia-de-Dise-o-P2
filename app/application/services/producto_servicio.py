from typing import List, Optional
from fastapi import HTTPException, status
from app.core.entities.producto import Producto
from app.core.ports.repositories.producto_repositorio_base import ProductoRepositorioBase

class ProductoServicio:
    def __init__(self, producto_repo: ProductoRepositorioBase):
        self.producto_repo = producto_repo

    def get_producto(self, producto_id: int) -> Producto:
        producto = self.producto_repo.get_by_id(producto_id)
        if not producto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Producto con ID {producto_id} no encontrado.")
        return producto

    def get_todos_los_productos(self, skip: int = 0, limit: int = 100) -> List[Producto]:
        return self.producto_repo.get_all(skip, limit)

    def create_producto(self, producto: Producto) -> Producto:
        # Opcional: verificar si ya existe un producto con el mismo nombre
        if self.producto_repo.get_by_nombre(producto.nombre):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Ya existe un producto con el nombre '{producto.nombre}'.")
        return self.producto_repo.create(producto)

    def update_producto(self, producto_id: int, producto: Producto) -> Producto:
        if not self.producto_repo.get_by_id(producto_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Producto con ID {producto_id} no encontrado.")
        
        existing_producto = self.producto_repo.get_by_nombre(producto.nombre)
        if existing_producto and existing_producto.id != producto_id:
             raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Ya existe otro producto con el nombre '{producto.nombre}'.")

        updated_producto = self.producto_repo.update(producto_id, producto)
        if not updated_producto:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al actualizar el producto.")
        return updated_producto

    def delete_producto(self, producto_id: int) -> bool:
        if not self.producto_repo.get_by_id(producto_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Producto con ID {producto_id} no encontrado.")
        return self.producto_repo.delete(producto_id)
