from core.promotor import Promotor
from core.empresa import Empresa
from exceptions.errores_crm import DatoInvalidoError
   
class Negociacion:
    def __init__(self, id_negociacion: str, promotor: Promotor, empresa: Empresa):
       self.id_negociacion = id_negociacion
       self.promotor = promotor
       self.empresa = empresa
       self.productos_solicitados = {}  # Formato: {id_producto: cantidad}
       self.estado_pago = "PENDIENTE"   # Estados: PENDIENTE, ABONADO, PAGADO
       self.monto_total = 0.0
   
    def agregar_producto(self, id_producto: str, cantidad: int, lista_productos: list):
        if cantidad <= 0:
            raise DatoInvalidoError("La cantidad debe ser mayor a cero.")
   
           # Buscar si el producto existe en el catálogo para validar
        producto_existente = next((p for p in lista_productos if p.id_producto == id_producto), None)
        if not producto_existente:
            raise DatoInvalidoError(f"El producto con ID {id_producto} no existe.")
   
        self.productos_solicitados[id_producto] = self.productos_solicitados.get(id_producto, 0) + cantidad
        self.calcular_total(lista_productos)
   
    def calcular_total(self, lista_productos: list):
        total = 0.0
        for id_prod, cant in self.productos_solicitados.items():
            producto = next((p for p in lista_productos if p.id_producto == id_prod), None)
            if producto:
                total += producto.precio_unitario * cant
        self.monto_total = total
   
    def actualizar_pago(self, nuevo_estado: str):
        estados_validos = ["PENDIENTE", "ABONADO", "PAGADO"]
        if nuevo_estado not in estados_validos:
            raise DatoInvalidoError(f"Estado de pago inválido. Opciones: {estados_validos}")
        self.estado_pago = nuevo_estado