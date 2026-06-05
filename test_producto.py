import unittest
# Importamos tu clase y tu excepción personalizada
from core.producto import Producto
from exceptions.errores_crm import DatoInvalidoError

class TestProducto(unittest.TestCase):

    def test_creacion_producto_exitoso(self):
        prod = Producto("PROD-001", "Laptop", 1200.50, 10)
        self.assertEqual(prod.id_producto, "PROD-001")
        self.assertEqual(prod.nombre, "Laptop")
        self.assertEqual(prod.precio_unitario, 1200.50)
        self.assertEqual(prod.stock, 10)

    def test_id_vacio_en_constructor_lanza_excepcion(self):
        with self.assertRaises(DatoInvalidoError):
            Producto("", "Celular", 500.0, 5)

    def test_precio_cero_en_constructor_lanza_excepcion(self):
        with self.assertRaises(DatoInvalidoError):
            Producto("PROD-002", "Teclado", 0.0, 15)

    def test_precio_negativo_en_constructor_lanza_excepcion(self):
        with self.assertRaises(DatoInvalidoError):
            Producto("PROD-003", "Mouse", -10.0, 15)

    def test_stock_negativo_en_constructor_lanza_excepcion(self):
        with self.assertRaises(DatoInvalidoError):
            Producto("PROD-004", "Monitor", 300.0, -1)

    def test_modificacion_id_vacio_lanza_excepcion(self):
        prod = Producto("PROD-005", "Audífonos", 50.0, 20)
        with self.assertRaises(DatoInvalidoError):
            prod.id_producto = ""

    def test_modificacion_precio_invalido_lanza_excepcion(self):
        prod = Producto("PROD-006", "Cargador", 25.0, 30)
        with self.assertRaises(DatoInvalidoError):
            prod.precio_unitario = 0
        with self.assertRaises(DatoInvalidoError):
            prod.precio_unitario = -5.50

    def test_modificacion_stock_negativo_lanza_excepcion(self):
        prod = Producto("PROD-007", "Cable HDMI", 12.0, 40)
        with self.assertRaises(DatoInvalidoError):
            prod.stock = -10

    def test_stock_permite_cero(self):
        prod = Producto("PROD-008", "Adaptador", 15.0, 5)
        prod.stock = 0
        self.assertEqual(prod.stock, 0)

if __name__ == '__main__':
    unittest.main()