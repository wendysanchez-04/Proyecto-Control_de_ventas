class ErrorCRM(Exception): #---->Clase base para todos los errores del sistema CRM.
       pass
   
class InventarioInsuficienteError(ErrorCRM):
       pass
   
class EstadoPagoInvalidoError(ErrorCRM):
       pass
   
class EntidadDuplicadaError(ErrorCRM):
       pass
   
class DatoInvalidoError(ErrorCRM):
       pass