from exceptions.errores_crm import DatoInvalidoError
   
class Producto:
    def __init__(self, id_producto: str, nombre: str, precio_unitario: float, stock: int):
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio_unitario = precio_unitario
        self.stock = stock
   
