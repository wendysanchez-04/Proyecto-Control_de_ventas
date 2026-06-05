from core.negociacion import Negociacion
from exceptions.errores_crm import EstadoPagoInvalidoError
   
class Despacho:
    def __init__(self, id_despacho: str, negociacion: Negociacion, fecha_despacho: str):
        self.id_despacho = id_despacho
        self.negociacion = negociacion
        self.fecha_despacho = fecha_despacho
        self.estado_envio = "EN_PREPARACION"  # Estados: EN_PREPARACION, DESPACHADO, ENTREGADO
   
    def confirmar_despacho(self):
        # Regla de negocio: No se puede despachar si el pago es 'PENDIENTE'
        if self.negociacion.estado_pago == "PENDIENTE":
            raise EstadoPagoInvalidoError(
                f"No se puede despachar. La negociación {self.negociacion.id_negociacion} se encuentra PENDIENTE de pago."
            )
        self.estado_envio = "DESPACHADO"