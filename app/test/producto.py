from abc import ABC

class Producto(ABC):
    def __init__(self, nombre, codigo, precio_unitario, cant_stock):
        self.nombre = nombre
        self.codigo = codigo
        self.precio_unitario = precio_unitario
        self.cant_stock = cant_stock

    def __str__(self):
        return f"{self.nombre} ({self.codigo}) - ${self.precio_unitario} | Stock: {self.cant_stock}"
