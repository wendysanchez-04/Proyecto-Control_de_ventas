import json
import os
from core.producto import Producto
from core.empresa import Empresa
   
class ManejadorJSON:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data")
   
    @classmethod
    def _obtener_ruta(cls, archivo: str) -> str:
        return os.path.join(cls.DATA_DIR, archivo)
   
    @classmethod
    def guardar_inventario(cls, productos: list[Producto]):
        ruta = cls._obtener_ruta("inventario.json")
        datos = [
            {
                "id_producto": p.id_producto,
                "nombre": p.nombre,
                "precio_unitario": p.precio_unitario,
                "stock": p.stock
            } for p in productos
        ]
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
   
    @classmethod
    def cargar_inventario(cls) -> list[Producto]:
        ruta = cls._obtener_ruta("inventario.json")
        if not os.path.exists(ruta):
            return []
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            return [Producto(d["id_producto"], d["nombre"], d["precio_unitario"], d["stock"]) for d in datos]
        except Exception:
            return []