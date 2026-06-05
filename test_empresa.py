import unittest
# Importamos tu clase Empresa y la excepción personalizada
from core.empresa import Empresa
from exceptions.errores_crm import DatoInvalidoError

class TestEmpresa(unittest.TestCase):

    def test_creacion_empresa_exitosa(self):
        """Verifica que una empresa se cree correctamente con todos sus datos válidos."""
        empresa = Empresa("J-12345678-9", "Tech Solutions C.A.", "Av. Principal #123, Caracas")
        self.assertEqual(empresa.rif, "J-12345678-9")
        self.assertEqual(empresa.razon_social, "Tech Solutions C.A.")
        self.assertEqual(empresa.direccion_despacho, "Av. Principal #123, Caracas")

    def test_rif_vacio_en_constructor_lanza_excepcion(self):
        """Verifica que el constructor bloquee un RIF vacío con DatoInvalidoError."""
        with self.assertRaises(DatoInvalidoError):
            Empresa("", "Empresa XYZ", "Calle Falsa 123")

    def test_rif_solo_espacios_en_constructor_lanza_excepcion(self):
        """Verifica que el constructor bloquee un RIF que contiene solo espacios."""
        with self.assertRaises(DatoInvalidoError):
            Empresa("   ", "Empresa XYZ", "Calle Falsa 123")

    def test_razon_social_vacia_en_constructor_lanza_excepcion(self):
        """Verifica que el constructor bloquee una razón social vacía."""
        with self.assertRaises(DatoInvalidoError):
            Empresa("J-12345678-9", "", "Calle Falsa 123")

    def test_razon_social_solo_espacios_en_constructor_lanza_excepcion(self):
        """Verifica que el constructor bloquee una razón social que contiene solo espacios."""
        with self.assertRaises(DatoInvalidoError):
            Empresa("J-12345678-9", "   ", "Calle Falsa 123")

    def test_direccion_vacia_en_constructor_lanza_excepcion(self):
        """Verifica que el constructor bloquee una dirección vacía."""
        with self.assertRaises(DatoInvalidoError):
            Empresa("J-12345678-9", "Empresa XYZ", "")

    def test_direccion_solo_espacios_en_constructor_lanza_excepcion(self):
        """Verifica que el constructor bloquee una dirección que contiene solo espacios."""
        with self.assertRaises(DatoInvalidoError):
            Empresa("J-12345678-9", "Empresa XYZ", "   ")

    def test_modificacion_rif_vacio_lanza_excepcion(self):
        """Verifica que el setter de rif bloquee valores vacíos posteriormente."""
        empresa = Empresa("J-12345678-9", "Empresa XYZ", "Dirección 123")
        with self.assertRaises(DatoInvalidoError):
            empresa.rif = ""
        with self.assertRaises(DatoInvalidoError):
            empresa.rif = "   "

    def test_modificacion_razon_social_vacia_lanza_excepcion(self):
        """Verifica que el setter de razon_social bloquee valores vacíos posteriormente."""
        empresa = Empresa("J-12345678-9", "Empresa XYZ", "Dirección 123")
        with self.assertRaises(DatoInvalidoError):
            empresa.razon_social = ""
        with self.assertRaises(DatoInvalidoError):
            empresa.razon_social = "   "

    def test_modificacion_direccion_vacia_lanza_excepcion(self):
        """Verifica que el setter de direccion_despacho bloquee valores vacíos posteriormente."""
        empresa = Empresa("J-12345678-9", "Empresa XYZ", "Dirección 123")
        with self.assertRaises(DatoInvalidoError):
            empresa.direccion_despacho = ""
        with self.assertRaises(DatoInvalidoError):
            empresa.direccion_despacho = "   "

    def test_rif_con_espacios_es_trimmeado(self):
        """Verifica que el RIF se almacene sin espacios al inicio o final."""
        empresa = Empresa("  J-12345678-9  ", "Empresa XYZ", "Dirección 123")
        self.assertEqual(empresa.rif, "J-12345678-9")

    def test_razon_social_con_espacios_es_trimmeada(self):
        """Verifica que la razón social se almacene sin espacios al inicio o final."""
        empresa = Empresa("J-12345678-9", "  Empresa XYZ  ", "Dirección 123")
        self.assertEqual(empresa.razon_social, "Empresa XYZ")

    def test_direccion_con_espacios_es_trimmeada(self):
        """Verifica que la dirección se almacene sin espacios al inicio o final."""
        empresa = Empresa("J-12345678-9", "Empresa XYZ", "  Dirección 123  ")
        self.assertEqual(empresa.direccion_despacho, "Dirección 123")

    def test_empresa_permite_caracteres_especiales_en_rif(self):
        """Verifica que el RIF pueda contener letras, números y guiones."""
        empresa = Empresa("E-98765432-1", "Otra Empresa", "Otra Dirección")
        self.assertEqual(empresa.rif, "E-98765432-1")

    def test_empresa_permite_direcciones_largas(self):
        """Verifica que se puedan almacenar direcciones extensas."""
        direccion_larga = "Av. Siempre Viva #742, Urbanización Las Mercedes, Municipio Baruta, Caracas 1080"
        empresa = Empresa("J-12345678-9", "Empresa XYZ", direccion_larga)
        self.assertEqual(empresa.direccion_despacho, direccion_larga)

if __name__ == '__main__':
    unittest.main()