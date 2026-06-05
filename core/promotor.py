from core.persona import Persona
from core.empresa import Empresa
   
class Promotor(Persona):
    def __init__(self, nombre: str, correo: str, telefono: str, codigo_promotor: str):
       super().__init__(nombre, correo, telefono)
       self.codigo_promotor = codigo_promotor
       self.empresas_asignadas = []  # Lista para almacenar objetos Empresa
   
    def obtener_rol(self) -> str:
           return "Promotor de Ventas"
   
    def asignar_empresa(self, empresa: Empresa):
       if empresa not in self.empresas_asignadas:
           self.empresas_asignadas.append(empresa)
   
    def mostrar_perfil(self) -> str:
        return f"Promotor: {self.nombre} | Código: {self.codigo_promotor} | Clientes: {len(self.empresas_asignadas)}"