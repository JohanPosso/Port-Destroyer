#!/usr/bin/env python3
"""
PortDestroyer System Tray - Professional system tray interface

Author: Jesus Posso
License: MIT
Version: 1.0.0
Repository: https://github.com/JohanPosso/port-destroyer

Description:
    System tray application for PortDestroyer with real-time updates,
    professional SVG icon, and optimized performance for macOS and Linux.
"""

__author__ = "Jesus Posso"
__version__ = "1.0.0"
__license__ = "MIT"

import sys
import platform
import os
from threading import Thread, Event
import time
from io import BytesIO
from port_destroyer import PortDestroyer

# Configurar para que la aplicación siempre esté en primer plano en macOS
if platform.system() == "Darwin":
    try:
        import AppKit
        from Foundation import NSBundle
        # Configurar la aplicación como agente de UI (aparece en la barra pero no en el dock)
        info = NSBundle.mainBundle().infoDictionary()
        info["LSUIElement"] = "1"
    except ImportError:
        pass

# Intentar importar pystray (multiplataforma)
try:
    import pystray
    from pystray import MenuItem as item
    from PIL import Image, ImageDraw, ImageFont, ImageEnhance
    import cairosvg
    HAS_PYSTRAY = True
    HAS_CAIROSVG = True
except ImportError as e:
    HAS_PYSTRAY = False
    HAS_CAIROSVG = False
    print(f"[ADVERTENCIA] Dependencias no instaladas: {e}")
    print("Instálalo con: pip3 install pystray pillow cairosvg")


class PortDestroyerTray:
    """Aplicación de bandeja del sistema para PortDestroyer"""
    
    def __init__(self, start_port=3000, end_port=9000):
        self.destroyer = PortDestroyer(port_range=(start_port, end_port))
        self.start_port = start_port
        self.end_port = end_port
        self.icon = None
        self.processes = []
        self.processes_dict = {}  # Cache para comparación rápida
        self.update_interval = 1.5  # Actualizar cada 1.5 segundos para mejor respuesta
        self.stop_event = Event()
        self.base_icon = None  # Cache del icono base
        self._load_base_icon()
        
    def _load_base_icon(self):
        """Carga el icono SVG y lo convierte a PNG"""
        try:
            # Obtener la ruta del directorio del script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            svg_path = os.path.join(script_dir, 'assets', 'icon.svg')
            
            if not os.path.exists(svg_path):
                print(f"[ADVERTENCIA] No se encontró el icono en {svg_path}")
                self.base_icon = None
                return
            
            # En Linux, usar tamaño más pequeño para mejor calidad
            icon_size = 64 if platform.system() == "Linux" else 128
            
            # Convertir SVG a PNG en memoria
            png_data = cairosvg.svg2png(url=svg_path, output_width=icon_size, output_height=icon_size)
            self.base_icon = Image.open(BytesIO(png_data))
            
            print(f"[INFO] Icono cargado correctamente ({icon_size}x{icon_size})")
            
        except Exception as e:
            print(f"[ERROR] No se pudo cargar el icono SVG: {e}")
            self.base_icon = None
    
    def create_icon_image(self, has_processes=False):
        """Crea un ícono profesional coloreado según el estado"""
        if self.base_icon is None:
            # Fallback a icono simple si no se puede cargar el SVG
            return self._create_fallback_icon(has_processes)
        
        # Crear una copia del icono base
        icon = self.base_icon.copy()
        
        # Aplicar tinte de color según el estado
        if has_processes:
            # Tinte rojo para procesos activos
            icon = self._apply_color_tint(icon, (220, 53, 69))
        else:
            # Tinte verde para estado limpio
            icon = self._apply_color_tint(icon, (40, 167, 69))
        
        return icon
    
    def _apply_color_tint(self, image, color):
        """Aplica un tinte de color a la imagen"""
        # Convertir a RGBA si no lo está
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        # Crear una capa de color
        color_layer = Image.new('RGBA', image.size, color + (0,))
        
        # Obtener los datos de la imagen
        img_data = image.copy()
        
        # Aplicar el tinte manteniendo el canal alfa
        pixels = img_data.load()
        color_pixels = color_layer.load()
        
        for y in range(image.size[1]):
            for x in range(image.size[0]):
                r, g, b, a = pixels[x, y]
                
                # Si el pixel tiene transparencia completa, dejarlo así
                if a == 0:
                    continue
                
                # Mezclar el color con el tinte (50% mezcla)
                new_r = int((r * 0.3) + (color[0] * 0.7))
                new_g = int((g * 0.3) + (color[1] * 0.7))
                new_b = int((b * 0.3) + (color[2] * 0.7))
                
                pixels[x, y] = (new_r, new_g, new_b, a)
        
        return img_data
    
    def _create_fallback_icon(self, has_processes=False):
        """Crea un icono simple como fallback"""
        width = 64
        height = 64
        image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        dc = ImageDraw.Draw(image)
        
        # Colores según estado
        if has_processes:
            color = (220, 53, 69)  # Rojo
        else:
            color = (40, 167, 69)  # Verde
        
        # Círculo simple
        padding = 8
        dc.ellipse(
            [padding, padding, width - padding, height - padding],
            fill=color,
            outline=(255, 255, 255),
            width=3
        )
        
        # Letra P
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
        except:
            font = ImageFont.load_default()
        
        dc.text((18, 10), "P", fill=(255, 255, 255), font=font)
        
        return image
    
    def update_processes(self):
        """Actualiza la lista de procesos en segundo plano con optimización"""
        while not self.stop_event.is_set():
            try:
                new_processes = self.destroyer.get_processes_on_ports()
                
                # Crear diccionario para comparación rápida
                new_dict = {(p['port'], p['pid']): p for p in new_processes}
                
                # Solo actualizar si hay cambios
                if new_dict != self.processes_dict:
                    self.processes = new_processes
                    self.processes_dict = new_dict
                    
                    print(f"[DEBUG] Procesos actualizados: {len(self.processes)}")
                    
                    # Actualizar ícono y menú
                    if self.icon:
                        try:
                            has_processes = len(self.processes) > 0
                            self.icon.icon = self.create_icon_image(has_processes)
                            count = len(self.processes)
                            self.icon.title = f"PortDestroyer - {count} proceso{'s' if count != 1 else ''}"
                            # Actualizar menú dinámicamente
                            self.icon.menu = pystray.Menu(self.create_menu)
                        except Exception as e:
                            print(f"[ERROR] Actualizando UI: {e}")
                    
            except Exception as e:
                print(f"[ERROR] Actualizando procesos: {e}")
                import traceback
                traceback.print_exc()
            
            # Esperar antes de la próxima actualización
            self.stop_event.wait(self.update_interval)
    
    def on_list_processes(self, icon, item):
        """Muestra la lista de procesos en consola"""
        self._bring_to_front()
        print("\n" + "="*80)
        self.destroyer.list_processes()
        print("="*80 + "\n")
    
    def on_kill_all(self, icon, item):
        """Mata todos los procesos"""
        self._bring_to_front()
        count = self.destroyer.kill_all()
        print(f"\n[OK] Se eliminaron {count} proceso(s)\n")
        # Forzar actualización inmediata
        self._force_update()
    
    def on_kill_port(self, port):
        """Crea una función para matar un proceso en un puerto específico"""
        def kill(icon, item):
            self._bring_to_front()
            count = self.destroyer.kill_port(port)
            if count > 0:
                print(f"\n[OK] Proceso eliminado en puerto {port}\n")
            # Forzar actualización inmediata
            self._force_update()
        return kill
    
    def _force_update(self):
        """Fuerza una actualización inmediata de los procesos"""
        try:
            self.processes = self.destroyer.get_processes_on_ports()
            self.processes_dict = {(p['port'], p['pid']): p for p in self.processes}
            if self.icon:
                has_processes = len(self.processes) > 0
                self.icon.icon = self.create_icon_image(has_processes)
                count = len(self.processes)
                self.icon.title = f"PortDestroyer - {count} proceso{'s' if count != 1 else ''}"
                self.icon.menu = pystray.Menu(self.create_menu)
        except Exception as e:
            print(f"[ERROR] Actualizando: {e}")
    
    def on_quit(self, icon, item):
        """Cierra la aplicación"""
        print("\n[INFO] Cerrando PortDestroyer...\n")
        self.stop_event.set()
        icon.stop()
    
    def create_menu(self):
        """Crea el menú dinámico"""
        try:
            menu_items = []
            
            # Título con información
            processes_count = len(self.processes)
            status = f'{processes_count} proceso{"s" if processes_count != 1 else ""} activo{"s" if processes_count != 1 else ""}'
            menu_items.append(item(status, lambda: None, enabled=False))
            menu_items.append(item('-', lambda: None))
            
            # Listar procesos individuales
            if self.processes:
                for proc in sorted(self.processes, key=lambda x: x['port']):
                    label = f"Puerto {proc['port']}: {proc['name']} (PID: {proc['pid']})"
                    menu_items.append(item(label, self.on_kill_port(proc['port'])))
                
                menu_items.append(item('-', lambda: None))
                menu_items.append(item('Eliminar Todos', self.on_kill_all))
            else:
                menu_items.append(item('No hay procesos activos', lambda: None, enabled=False))
            
            menu_items.append(item('-', lambda: None))
            
            # Opciones generales
            menu_items.append(item('Listar en Consola', self.on_list_processes))
            menu_items.append(item(f'Rango: {self.start_port}-{self.end_port}', lambda: None, enabled=False))
            menu_items.append(item('-', lambda: None))
            menu_items.append(item('Salir', self.on_quit))
            
            return tuple(menu_items)
        except Exception as e:
            print(f"[ERROR] Creando menú: {e}")
            import traceback
            traceback.print_exc()
            # Retornar menú mínimo en caso de error
            return (item('Error en menú', lambda: None, enabled=False),
                    item('Salir', self.on_quit))
    
    def _bring_to_front(self):
        """Trae la aplicación al frente en macOS"""
        if platform.system() == "Darwin":
            try:
                import AppKit
                # Activar la aplicación para que aparezca al frente
                app = AppKit.NSApplication.sharedApplication()
                app.activateIgnoringOtherApps_(True)
            except Exception as e:
                print(f"[DEBUG] No se pudo traer al frente: {e}")
    
    def setup(self, icon):
        """Configuración inicial del ícono"""
        icon.visible = True
        
        # Configurar para que siempre aparezca al frente en macOS
        if platform.system() == "Darwin":
            try:
                import AppKit
                # Configurar nivel de activación alto
                app = AppKit.NSApplication.sharedApplication()
                app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyAccessory)
            except Exception as e:
                print(f"[DEBUG] No se pudo configurar prioridad: {e}")
        
        print(f"""
╔══════════════════════════════════════════════════════════╗
║              PortDestroyer - System Tray                 ║
║                                                           ║
║  Rango de puertos: {self.start_port}-{self.end_port}                             ║
║  Sistema: {platform.system()}                                      ║
║  Actualización: Tiempo real (1.5s)                       ║
║                                                           ║
║  Indicador en barra superior:                            ║
║  • Verde = Sin procesos                                  ║
║  • Rojo = Procesos activos                              ║
╚══════════════════════════════════════════════════════════╝
        """)
    
    def run(self):
        """Inicia la aplicación de bandeja"""
        if not HAS_PYSTRAY:
            print("\n[ERROR] pystray no está instalado")
            print("Instálalo con: pip3 install pystray pillow\n")
            return
        
        # Configurar macOS para que la app siempre esté al frente
        if platform.system() == "Darwin":
            try:
                import AppKit
                from PyObjCTools import AppHelper
                
                # Obtener la aplicación NSApplication
                app = AppKit.NSApplication.sharedApplication()
                
                # Configurar como agente con política de presentación que permite estar siempre visible
                app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyAccessory)
                
                # Activar la aplicación ignorando otras apps
                app.activateIgnoringOtherApps_(True)
                
            except Exception as e:
                print(f"[DEBUG] Configuración de macOS: {e}")
        
        # Cargar procesos iniciales antes de crear el icono
        print("[INFO] Cargando procesos iniciales...")
        self.processes = self.destroyer.get_processes_on_ports()
        self.processes_dict = {(p['port'], p['pid']): p for p in self.processes}
        print(f"[INFO] {len(self.processes)} proceso(s) encontrado(s)")
        
        # Crear ícono
        image = self.create_icon_image(len(self.processes) > 0)
        self.icon = pystray.Icon(
            "PortDestroyer",
            image,
            f"PortDestroyer - {len(self.processes)} proceso(s)",
            menu=pystray.Menu(self.create_menu)
        )
        
        # Iniciar thread de actualización
        update_thread = Thread(target=self.update_processes, daemon=True)
        update_thread.start()
        
        # Configurar y ejecutar
        try:
            self.icon.run(setup=self.setup)
        except Exception as e:
            if "SystemExit" not in str(type(e).__name__):
                raise


def main():
    """Función principal"""
    import argparse
    import signal
    
    parser = argparse.ArgumentParser(
        description='PortDestroyer System Tray - Interfaz de bandeja del sistema'
    )
    
    parser.add_argument('--start', type=int, default=3000,
                       help='Puerto inicial del rango (default: 3000)')
    parser.add_argument('--end', type=int, default=9000,
                       help='Puerto final del rango (default: 9000)')
    parser.add_argument('--debug', action='store_true',
                       help='Modo debug con información adicional')
    
    args = parser.parse_args()
    
    # Validar rango
    if args.start >= args.end:
        print("[ERROR] El puerto inicial debe ser menor que el puerto final")
        sys.exit(1)
    
    # Crear aplicación
    app = PortDestroyerTray(start_port=args.start, end_port=args.end)
    
    # Manejar señales de cierre correctamente
    def signal_handler(sig, frame):
        print("\n[INFO] Cerrando PortDestroyer...")
        app.stop_event.set()
        if app.icon:
            try:
                app.icon.stop()
            except:
                pass  # Ignorar errores de Xlib al cerrar
        # No llamar sys.exit() aquí para evitar error de Xlib
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n[INFO] Cerrando PortDestroyer...")
        app.stop_event.set()
    except SystemExit:
        # Salida normal, no mostrar error
        pass
    except Exception as e:
        print(f"\n[ERROR] Error fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

