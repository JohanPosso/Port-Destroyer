#!/usr/bin/env python3
"""
PortDestroyer System Tray - Linux/Ubuntu version with AppIndicator3

Author: Jesus Posso
License: MIT
Version: 1.0.0
Repository: https://github.com/JohanPosso/Port-Destroyer

This is a Linux-specific version that uses AppIndicator3 for better
compatibility with GNOME desktop environment.
"""

__author__ = "Jesus Posso"
__version__ = "1.0.0"
__license__ = "MIT"

import sys
import os
from threading import Thread, Event
import time
import signal
from io import BytesIO

# Importar GTK y AppIndicator
try:
    import gi
    gi.require_version('Gtk', '3.0')
    gi.require_version('AppIndicator3', '0.1')
    from gi.repository import Gtk, AppIndicator3, GLib
    from PIL import Image
    import cairosvg
except ImportError as e:
    print(f"[ERROR] Dependencias faltantes: {e}")
    print("Instala con:")
    print("  sudo apt install gir1.2-appindicator3-0.1 python3-gi")
    print("  pip install Pillow cairosvg")
    sys.exit(1)

from port_destroyer import PortDestroyer


class PortDestroyerTrayLinux:
    """Aplicación de bandeja del sistema para Linux usando AppIndicator3"""
    
    def __init__(self, start_port=3000, end_port=9000):
        self.destroyer = PortDestroyer(port_range=(start_port, end_port))
        self.start_port = start_port
        self.end_port = end_port
        self.processes = []
        self.processes_dict = {}
        self.update_interval = 1.5
        self.stop_event = Event()
        
        # Crear directorio temporal para iconos
        self.temp_dir = "/tmp/port-destroyer"
        os.makedirs(self.temp_dir, exist_ok=True)
        self.icon_path_green = os.path.join(self.temp_dir, "icon_green.png")
        self.icon_path_red = os.path.join(self.temp_dir, "icon_red.png")
        
        # Generar iconos
        self._create_icons()
        
        # Crear indicador
        self.indicator = AppIndicator3.Indicator.new(
            "port-destroyer",
            self.icon_path_green,
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_title("PortDestroyer")
        
        # Crear menú
        self.menu = Gtk.Menu()
        self.update_menu()
        self.indicator.set_menu(self.menu)
        
        print("""
╔══════════════════════════════════════════════════════════╗
║         PortDestroyer - Ubuntu/Linux (AppIndicator)      ║
║                                                           ║
║  Rango de puertos: {}-{}                             ║
║  Actualización: Tiempo real (1.5s)                       ║
║                                                           ║
║  Busca el icono en tu bandeja del sistema                ║
║  • Verde = Sin procesos                                  ║
║  • Rojo = Procesos activos                              ║
╚══════════════════════════════════════════════════════════╝
        """.format(self.start_port, self.end_port))
    
    def _create_icons(self):
        """Crea iconos verde y rojo"""
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            svg_path = os.path.join(script_dir, 'assets', 'icon.svg')
            
            if os.path.exists(svg_path):
                # Convertir SVG a PNG
                png_data_green = cairosvg.svg2png(url=svg_path, output_width=64, output_height=64)
                png_data_red = cairosvg.svg2png(url=svg_path, output_width=64, output_height=64)
                
                # Guardar iconos con tinte
                img_green = Image.open(BytesIO(png_data_green)).convert('RGBA')
                img_red = Image.open(BytesIO(png_data_red)).convert('RGBA')
                
                # Aplicar tintes
                img_green = self._tint_image(img_green, (40, 167, 69))
                img_red = self._tint_image(img_red, (220, 53, 69))
                
                img_green.save(self.icon_path_green, 'PNG')
                img_red.save(self.icon_path_red, 'PNG')
                
                print("[INFO] Iconos creados correctamente")
            else:
                print(f"[ADVERTENCIA] SVG no encontrado, usando iconos simples")
                self._create_simple_icons()
                
        except Exception as e:
            print(f"[ERROR] Creando iconos: {e}")
            self._create_simple_icons()
    
    def _create_simple_icons(self):
        """Crea iconos simples de respaldo"""
        for color, path in [(40, 167, 69, self.icon_path_green), 
                            (220, 53, 69, self.icon_path_red)]:
            img = Image.new('RGBA', (64, 64), (color[0], color[1], color[2], 255))
            img.save(path, 'PNG')
    
    def _tint_image(self, image, color):
        """Aplica tinte a la imagen"""
        pixels = image.load()
        for y in range(image.size[1]):
            for x in range(image.size[0]):
                r, g, b, a = pixels[x, y]
                if a > 0:
                    new_r = int((r * 0.3) + (color[0] * 0.7))
                    new_g = int((g * 0.3) + (color[1] * 0.7))
                    new_b = int((b * 0.3) + (color[2] * 0.7))
                    pixels[x, y] = (new_r, new_g, new_b, a)
        return image
    
    def update_menu(self):
        """Actualiza el menú con los procesos actuales"""
        # Limpiar menú actual
        for item in self.menu.get_children():
            self.menu.remove(item)
        
        # Título
        count = len(self.processes)
        title = Gtk.MenuItem(label=f"{count} proceso{'s' if count != 1 else ''} activo{'s' if count != 1 else ''}")
        title.set_sensitive(False)
        self.menu.append(title)
        
        self.menu.append(Gtk.SeparatorMenuItem())
        
        # Listar procesos
        if self.processes:
            for proc in sorted(self.processes, key=lambda x: x['port']):
                label = f"Puerto {proc['port']}: {proc['name']} (PID: {proc['pid']})"
                item = Gtk.MenuItem(label=label)
                item.connect('activate', self.on_kill_port, proc['port'])
                self.menu.append(item)
            
            self.menu.append(Gtk.SeparatorMenuItem())
            
            # Eliminar todos
            kill_all = Gtk.MenuItem(label="Eliminar Todos")
            kill_all.connect('activate', self.on_kill_all)
            self.menu.append(kill_all)
        else:
            no_proc = Gtk.MenuItem(label="No hay procesos activos")
            no_proc.set_sensitive(False)
            self.menu.append(no_proc)
        
        self.menu.append(Gtk.SeparatorMenuItem())
        
        # Opciones
        list_item = Gtk.MenuItem(label="Listar en Consola")
        list_item.connect('activate', self.on_list_processes)
        self.menu.append(list_item)
        
        range_item = Gtk.MenuItem(label=f"Rango: {self.start_port}-{self.end_port}")
        range_item.set_sensitive(False)
        self.menu.append(range_item)
        
        self.menu.append(Gtk.SeparatorMenuItem())
        
        # Salir
        quit_item = Gtk.MenuItem(label="Salir")
        quit_item.connect('activate', self.on_quit)
        self.menu.append(quit_item)
        
        self.menu.show_all()
    
    def update_processes(self):
        """Actualiza la lista de procesos periódicamente"""
        while not self.stop_event.is_set():
            try:
                new_processes = self.destroyer.get_processes_on_ports()
                new_dict = {(p['port'], p['pid']): p for p in new_processes}
                
                if new_dict != self.processes_dict:
                    self.processes = new_processes
                    self.processes_dict = new_dict
                    
                    # Actualizar en el hilo principal de GTK
                    GLib.idle_add(self._update_ui)
                    
            except Exception as e:
                print(f"[ERROR] Actualizando procesos: {e}")
            
            time.sleep(self.update_interval)
    
    def _update_ui(self):
        """Actualiza la UI (debe ejecutarse en hilo principal de GTK)"""
        # Cambiar icono según estado
        has_processes = len(self.processes) > 0
        icon_path = self.icon_path_red if has_processes else self.icon_path_green
        self.indicator.set_icon_full(icon_path, "PortDestroyer")
        
        # Actualizar menú
        self.update_menu()
        
        print(f"[DEBUG] UI actualizada: {len(self.processes)} procesos")
        return False  # No repetir
    
    def on_kill_port(self, widget, port):
        """Elimina proceso en puerto específico"""
        count = self.destroyer.kill_port(port)
        if count > 0:
            print(f"\n[OK] Proceso eliminado en puerto {port}")
        GLib.idle_add(self._update_ui)
    
    def on_kill_all(self, widget):
        """Elimina todos los procesos"""
        count = self.destroyer.kill_all()
        print(f"\n[OK] Se eliminaron {count} proceso(s)")
        GLib.idle_add(self._update_ui)
    
    def on_list_processes(self, widget):
        """Lista procesos en consola"""
        print("\n" + "="*80)
        self.destroyer.list_processes()
        print("="*80 + "\n")
    
    def on_quit(self, widget):
        """Cierra la aplicación"""
        print("\n[INFO] Cerrando PortDestroyer...")
        self.stop_event.set()
        Gtk.main_quit()
    
    def run(self):
        """Inicia la aplicación"""
        # Cargar procesos iniciales
        print("[INFO] Cargando procesos iniciales...")
        self.processes = self.destroyer.get_processes_on_ports()
        self.processes_dict = {(p['port'], p['pid']): p for p in self.processes}
        print(f"[INFO] {len(self.processes)} proceso(s) encontrado(s)")
        
        # Actualizar UI inicial
        self._update_ui()
        
        # Iniciar thread de actualización
        update_thread = Thread(target=self.update_processes, daemon=True)
        update_thread.start()
        
        # Iniciar GTK main loop
        try:
            Gtk.main()
        except KeyboardInterrupt:
            print("\n[INFO] Cerrando PortDestroyer...")
            self.stop_event.set()


def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='PortDestroyer System Tray - Linux/Ubuntu con AppIndicator3'
    )
    
    parser.add_argument('--start', type=int, default=3000,
                       help='Puerto inicial del rango (default: 3000)')
    parser.add_argument('--end', type=int, default=9000,
                       help='Puerto final del rango (default: 9000)')
    
    args = parser.parse_args()
    
    if args.start >= args.end:
        print("[ERROR] El puerto inicial debe ser menor que el puerto final")
        sys.exit(1)
    
    app = PortDestroyerTrayLinux(start_port=args.start, end_port=args.end)
    
    # Manejar señales
    def signal_handler(sig, frame):
        print("\n[INFO] Cerrando PortDestroyer...")
        app.stop_event.set()
        Gtk.main_quit()
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    app.run()


if __name__ == '__main__':
    main()

