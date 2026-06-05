from exceptions.errores_crm import DatoInvalidoError

class Empresa:
    def __init__(self, rif: str, razon_social: str, direccion_despacho: str):
        # El constructor invoca a los setters automáticos para validar los datos iniciales
        self.rif = rif
        self.razon_social = razon_social
        self.direccion_despacho = direccion_despacho

    @property
    def rif(self) -> str:
        return self._rif

    @rif.setter
    def rif(self, valor: str):
        if not valor or not valor.strip():
            raise DatoInvalidoError("El RIF (ID Fiscal) no puede estar vacío.")
        self._rif = valor.strip()

    @property
    def razon_social(self) -> str:
        return self._razon_social

    @razon_social.setter
    def razon_social(self, valor: str):
        if not valor or not valor.strip():
            raise DatoInvalidoError("La razón social no puede estar vacía.")
        self._razon_social = valor.strip()

    @property
    def direccion_despacho(self) -> str:
        return self._direccion_despacho

    @direccion_despacho.setter
    def direccion_despacho(self, valor: str):
        if not valor or not valor.strip():
            raise DatoInvalidoError("La dirección de despacho no puede estar vacía.")
        self._direccion_despacho = valor.strip()
