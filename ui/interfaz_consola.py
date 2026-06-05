# ui/interfaz_consola.py
import sys
import os

# Añadir el directorio raíz al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.promotor import Promotor
from core.empresa import Empresa
from core.negociacion import Negociacion
from core.despacho import Despacho
from core.producto import Producto
from persistence.manejador_json import ManejadorJSON
from exceptions.errores_crm import (
    ErrorCRM, InventarioInsuficienteError, EstadoPagoInvalidoError,
    EntidadDuplicadaError, DatoInvalidoError
)


class InterfazConsola:
    """Interfaz de consola para el sistema CRM B2B."""
    
    def __init__(self):
        self.promotor_actual = None
        self.productos = []
        self.negociaciones = []  # Lista de objetos Negociacion
        self.despachos = []      # Lista de objetos Despacho
        
        # Cargar inventario desde JSON
        self._cargar_inventario()
        
    def _cargar_inventario(self):
        """Carga el inventario desde el archivo JSON."""
        self.productos = ManejadorJSON.cargar_inventario()
        if not self.productos:
            # Inventario por defecto si no hay datos
            self.productos = [
                Producto("P001", "Laptop Pro", 1200.00, 10),
                Producto("P002", "Mouse Inalámbrico", 25.50, 50),
                Producto("P003", "Teclado Mecánico", 85.00, 30),
                Producto("P004", "Monitor 24\"", 300.00, 15),
                Producto("P005", "SSD 1TB", 150.00, 25),
            ]
            self._guardar_inventario()
    
    def _guardar_inventario(self):
        """Guarda el inventario en el archivo JSON."""
        try:
            ManejadorJSON.guardar_inventario(self.productos)
        except Exception as e:
            print(f"[ADVERTENCIA] No se pudo guardar el inventario: {e}")
    
    def _mostrar_titulo(self, titulo: str):
        """Muestra un título formateado."""
        print("\n" + "=" * 60)
        print(f" {titulo}")
        print("=" * 60)
    
    def _mostrar_error(self, mensaje: str):
        """Muestra un mensaje de error de forma amigable."""
        print(f"\n❌ ERROR: {mensaje}")
    
    def _mostrar_exito(self, mensaje: str):
        """Muestra un mensaje de éxito."""
        print(f"\n✅ {mensaje}")
    
    def _mostrar_info(self, mensaje: str):
        """Muestra un mensaje informativo."""
        print(f"\nℹ️ {mensaje}")
    
    def _pausar(self):
        """Pausa la ejecución hasta que el usuario presione Enter."""
        input("\nPresione Enter para continuar...")
    
    def _obtener_entrada(self, mensaje: str, obligatorio: bool = True) -> str:
        """Obtiene una entrada del usuario con validación básica."""
        while True:
            valor = input(mensaje).strip()
            if not obligatorio and not valor:
                return ""
            if obligatorio and not valor:
                print("Este campo es obligatorio. Intente nuevamente.")
                continue
            return valor
    
    def _obtener_entrada_numerica(self, mensaje: str, positivo: bool = True) -> float:
        """Obtiene un valor numérico del usuario."""
        while True:
            try:
                valor = float(input(mensaje))
                if positivo and valor <= 0:
                    print("El valor debe ser mayor a cero.")
                    continue
                return valor
            except ValueError:
                print("Por favor, ingrese un número válido.")
    
    def _obtener_entrada_entera(self, mensaje: str, positivo: bool = True) -> int:
        """Obtiene un valor entero del usuario."""
        while True:
            try:
                valor = int(input(mensaje))
                if positivo and valor <= 0:
                    print("El valor debe ser mayor a cero.")
                    continue
                return valor
            except ValueError:
                print("Por favor, ingrese un número entero válido.")
    
    def ejecutar(self):
        """Ejecuta el menú principal del sistema."""
        try:
            self._login_promotor()
        except ErrorCRM as e:
            self._mostrar_error(str(e))
            return
        
        while True:
            self._mostrar_menu_principal()
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "1":
                self._registrar_empresa()
            elif opcion == "2":
                self._ver_inventario()
            elif opcion == "3":
                self._agregar_oportunidad_venta()
            elif opcion == "4":
                self._ver_ventas()
            elif opcion == "5":
                self._gestionar_despacho()
            elif opcion == "6":
                self._salir()
                break
            else:
                self._mostrar_error("Opción no válida. Intente nuevamente.")
            
            self._pausar()
    
    def _login_promotor(self):
        """Login del promotor (simulado)."""
        self._mostrar_titulo("INICIAR SESIÓN - PROMOTOR")
        
        nombre = self._obtener_entrada("Nombre del promotor: ")
        correo = self._obtener_entrada("Correo electrónico: ")
        telefono = self._obtener_entrada("Teléfono: ")
        codigo = self._obtener_entrada("Código de promotor: ")
        
        self.promotor_actual = Promotor(nombre, correo, telefono, codigo)
        self._mostrar_exito(f"Bienvenido, {self.promotor_actual.nombre}!")
    
    def _mostrar_menu_principal(self):
        """Muestra el menú principal del sistema."""
        self._mostrar_titulo(f"MENÚ PRINCIPAL - {self.promotor_actual.nombre}")
        print("1. Registrar Empresa")
        print("2. Ver Inventario")
        print("3. Agregar Oportunidad de Venta")
        print("4. Ver Ventas")
        print("5. Gestionar Despacho")
        print("6. Salir")
    
    def _registrar_empresa(self):
        """Registra una nueva empresa y la asigna al promotor."""
        self._mostrar_titulo("REGISTRO DE EMPRESA")
        
        try:
            rif = self._obtener_entrada("RIF (ID Fiscal): ")
            razon_social = self._obtener_entrada("Razón Social: ")
            direccion = self._obtener_entrada("Dirección de Despacho: ")
            
            # Verificar si ya existe una empresa con el mismo RIF
            for empresa in self.promotor_actual.empresas_asignadas:
                if empresa.rif == rif:
                    raise EntidadDuplicadaError(f"Ya existe una empresa con RIF {rif}")
            
            nueva_empresa = Empresa(rif, razon_social, direccion)
            self.promotor_actual.asignar_empresa(nueva_empresa)
            
            self._mostrar_exito(f"Empresa '{razon_social}' registrada exitosamente!")
            
        except EntidadDuplicadaError as e:
            self._mostrar_error(str(e))
        except DatoInvalidoError as e:
            self._mostrar_error(str(e))
        except Exception as e:
            self._mostrar_error(f"Error inesperado: {e}")
    
    def _ver_inventario(self):
        """Muestra el inventario actual de productos."""
        self._mostrar_titulo("INVENTARIO DE PRODUCTOS")
        
        if not self.productos:
            self._mostrar_info("No hay productos en el inventario.")
            return
        
        print(f"{'ID':<12} {'Nombre':<25} {'Precio':<12} {'Stock':<8}")
        print("-" * 60)
        for p in self.productos:
            print(f"{p.id_producto:<12} {p.nombre:<25} ${p.precio_unitario:<11.2f} {p.stock:<8}")
    
    def _agregar_oportunidad_venta(self):
        """Crea una nueva negociación (oportunidad de venta)."""
        self._mostrar_titulo("NUEVA OPORTUNIDAD DE VENTA")
        
        try:
            # Verificar que haya empresas registradas
            if not self.promotor_actual.empresas_asignadas:
                self._mostrar_error("No hay empresas registradas. Registre una empresa primero.")
                return
            
            # Mostrar empresas disponibles
            print("\nEmpresas registradas:")
            for i, empresa in enumerate(self.promotor_actual.empresas_asignadas, 1):
                print(f"  {i}. {empresa.razon_social} (RIF: {empresa.rif})")
            
            opcion = self._obtener_entrada_entera("\nSeleccione la empresa: ")
            if opcion < 1 or opcion > len(self.promotor_actual.empresas_asignadas):
                self._mostrar_error("Opción inválida.")
                return
            
            empresa_seleccionada = self.promotor_actual.empresas_asignadas[opcion - 1]
            
            # Crear ID de negociación
            id_negociacion = f"NEG-{len(self.negociaciones) + 1:04d}"
            
            # Crear negociación
            negociacion = Negociacion(id_negociacion, self.promotor_actual, empresa_seleccionada)
            
            # Agregar productos
            print("\n--- AGREGAR PRODUCTOS ---")
            while True:
                self._ver_inventario()
                print(f"\nProductos actuales en la negociación:")
                if negociacion.productos_solicitados:
                    for id_prod, cant in negociacion.productos_solicitados.items():
                        prod = next((p for p in self.productos if p.id_producto == id_prod), None)
                        if prod:
                            print(f"  - {prod.nombre}: {cant} unidades")
                else:
                    print("  (Sin productos agregados)")
                
                print("\nOpciones:")
                print("  1. Agregar producto")
                print("  2. Finalizar negociación")
                
                sub_opcion = input("Seleccione: ").strip()
                
                if sub_opcion == "1":
                    id_producto = self._obtener_entrada("ID del producto: ")
                    cantidad = self._obtener_entrada_entera("Cantidad: ")
                    
                    # Verificar stock
                    producto = next((p for p in self.productos if p.id_producto == id_producto), None)
                    if producto:
                        if producto.stock < cantidad:
                            self._mostrar_error(f"Stock insuficiente. Disponible: {producto.stock}")
                            continue
                    
                    negociacion.agregar_producto(id_producto, cantidad, self.productos)
                    self._mostrar_exito(f"Producto agregado. Total actual: ${negociacion.monto_total:.2f}")
                    
                elif sub_opcion == "2":
                    if not negociacion.productos_solicitados:
                        self._mostrar_error("Debe agregar al menos un producto.")
                        continue
                    break
                else:
                    self._mostrar_error("Opción inválida.")
            
            # Actualizar stock
            for id_prod, cantidad in negociacion.productos_solicitados.items():
                producto = next((p for p in self.productos if p.id_producto == id_prod), None)
                if producto:
                    producto.stock -= cantidad
            
            self._guardar_inventario()
            self.negociaciones.append(negociacion)
            
            self._mostrar_exito(f"¡Negociación creada exitosamente!")
            self._mostrar_info(f"ID: {id_negociacion} | Total: ${negociacion.monto_total:.2f} | Estado Pago: {negociacion.estado_pago}")
            
            # Preguntar si desea actualizar el pago
            actualizar = input("\n¿Desea actualizar el estado de pago? (s/n): ").strip().lower()
            if actualizar == 's':
                self._actualizar_estado_pago(negociacion)
            
        except DatoInvalidoError as e:
            self._mostrar_error(str(e))
        except Exception as e:
            self._mostrar_error(f"Error inesperado: {e}")
    
    def _actualizar_estado_pago(self, negociacion: Negociacion):
        """Actualiza el estado de pago de una negociación."""
        self._mostrar_titulo("ACTUALIZAR ESTADO DE PAGO")
        
        print(f"Negociación: {negociacion.id_negociacion}")
        print(f"Empresa: {negociacion.empresa.razon_social}")
        print(f"Monto Total: ${negociacion.monto_total:.2f}")
        print(f"Estado actual: {negociacion.estado_pago}")
        
        print("\nEstados disponibles:")
        print("  1. PENDIENTE")
        print("  2. ABONADO")
        print("  3. PAGADO")
        
        opcion = input("Seleccione nuevo estado: ").strip()
        estados = {"1": "PENDIENTE", "2": "ABONADO", "3": "PAGADO"}
        
        if opcion in estados:
            try:
                negociacion.actualizar_pago(estados[opcion])
                self._mostrar_exito(f"Estado de pago actualizado a: {estados[opcion]}")
            except DatoInvalidoError as e:
                self._mostrar_error(str(e))
        else:
            self._mostrar_error("Opción inválida.")
    
    def _ver_ventas(self):
        """Muestra todas las ventas (negociaciones) registradas."""
        self._mostrar_titulo("VENTAS REGISTRADAS")
        
        if not self.negociaciones:
            self._mostrar_info("No hay ventas registradas.")
            return
        
        print(f"{'ID':<12} {'Empresa':<25} {'Total':<12} {'Estado Pago':<12} {'Despacho':<12}")
        print("-" * 80)
        
        for n in self.negociaciones:
            # Buscar estado de despacho
            estado_despacho = "NO INICIADO"
            for d in self.despachos:
                if d.negociacion == n:
                    estado_despacho = d.estado_envio
                    break
            
            print(f"{n.id_negociacion:<12} {n.empresa.razon_social[:25]:<25} "
                  f"${n.monto_total:<11.2f} {n.estado_pago:<12} {estado_despacho:<12}")
    
    def _gestionar_despacho(self):
        """Gestiona el despacho de una negociación."""
        self._mostrar_titulo("GESTIÓN DE DESPACHO")
        
        # Filtrar negociaciones que pueden ser despachadas
        negociaciones_despachables = [n for n in self.negociaciones 
                                       if n.estado_pago != "PENDIENTE"]
        
        if not negociaciones_despachables:
            self._mostrar_info("No hay negociaciones disponibles para despachar "
                               "(todas tienen estado de pago PENDIENTE).")
            return
        
        print("\nNegociaciones disponibles para despachar:")
        for i, n in enumerate(negociaciones_despachables, 1):
            # Verificar si ya tiene despacho
            tiene_despacho = any(d.negociacion == n for d in self.despachos)
            estado_actual = ""
            for d in self.despachos:
                if d.negociacion == n:
                    estado_actual = f" [{d.estado_envio}]"
                    break
            print(f"  {i}. {n.id_negociacion} - {n.empresa.razon_social} "
                  f"(${n.monto_total:.2f}) - Pago: {n.estado_pago}{estado_actual}")
        
        opcion = self._obtener_entrada_entera("\nSeleccione una negociación: ")
        if opcion < 1 or opcion > len(negociaciones_despachables):
            self._mostrar_error("Opción inválida.")
            return
        
        negociacion = negociaciones_despachables[opcion - 1]
        
        # Verificar si ya existe un despacho
        despacho_existente = None
        for d in self.despachos:
            if d.negociacion == negociacion:
                despacho_existente = d
                break
        
        if despacho_existente:
            self._mostrar_info(f"Estado actual del despacho: {despacho_existente.estado_envio}")
            if despacho_existente.estado_envio == "DESPACHADO":
                print("\nOpciones:")
                print("  1. Confirmar entrega")
                print("  2. Volver al menú")
                
                sub_opcion = input("Seleccione: ").strip()
                if sub_opcion == "1" and despacho_existente.estado_envio == "DESPACHADO":
                    despacho_existente.estado_envio = "ENTREGADO"
                    self._mostrar_exito("¡Entrega confirmada!")
                return
            elif despacho_existente.estado_envio == "ENTREGADO":
                self._mostrar_info("Este pedido ya fue entregado.")
                return
            elif despacho_existente.estado_envio == "EN_PREPARACION":
                # Confirmar despacho
                try:
                    despacho_existente.confirmar_despacho()
                    self._mostrar_exito(f"Despacho confirmado para {negociacion.id_negociacion}")
                except EstadoPagoInvalidoError as e:
                    self._mostrar_error(str(e))
                return
        else:
            # Crear nuevo despacho
            try:
                fecha = self._obtener_entrada("Fecha de despacho (YYYY-MM-DD): ")
                nuevo_despacho = Despacho(f"DESP-{len(self.despachos) + 1:04d}", 
                                          negociacion, fecha)
                nuevo_despacho.confirmar_despacho()
                self.despachos.append(nuevo_despacho)
                self._mostrar_exito(f"Despacho creado y confirmado para {negociacion.id_negociacion}")
            except EstadoPagoInvalidoError as e:
                self._mostrar_error(str(e))
            except Exception as e:
                self._mostrar_error(f"Error al crear despacho: {e}")
    
    def _salir(self):
        """Sale del sistema guardando datos."""
        self._mostrar_titulo("SALIR DEL SISTEMA")
        self._guardar_inventario()
        self._mostrar_exito("¡Gracias por usar el Sistema CRM B2B!")