from exceptions.errores_crm import DatoInvalidoError
   
class Producto:
    def __init__(self, id_producto: str, nombre: str, precio_unitario: float, stock: int):
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio_unitario = precio_unitario
        self.stock = stock

    @property
    def id_producto(self): return self._id_producto

    @id_producto.setter
    def id_producto(self, valor):
       if not valor: raise DatoInvalidoError("El ID del producto no puede estar vacío.")
       self._id_producto = valor
   
    @property
    def precio_unitario(self): return self._precio_unitario
   
    @precio_unitario.setter
    def precio_unitario(self, valor):
       if valor <= 0: raise DatoInvalidoError("El precio debe ser un número positivo.")
       self._precio_unitario = valor
   
    @property
    def stock(self): return self._stock
   
    @stock.setter
    def stock(self, valor):
        if valor < 0: raise DatoInvalidoError("El stock disponible no puede ser negativo.")
        self._stock = valor
