#!/usr/bin/env python3
"""
PortDestroyer System Tray - Universal interface for macOS and Linux

Author: Jesus Posso
License: MIT
Version: 1.0.0
Repository: https://github.com/JohanPosso/Port-Destroyer

Description:
    System tray application that automatically detects the OS and uses
    the appropriate backend (pystray for macOS, AppIndicator3 for Linux).
"""

__author__ = "Jesus Posso"
__version__ = "1.0.0"
__license__ = "MIT"

import sys
import platform
import os
from threading import Thread, Event
import time
import signal
from io import BytesIO
from port_destroyer import PortDestroyer

# Detectar sistema operativo
IS_LINUX = platform.system() == "Linux"
IS_MACOS = platform.system() == "Darwin"

# Importar dependencias según el OS
if IS_LINUX:
    # Ubuntu/Linux - Usar AppIndicator3
    try:
        import gi
        gi.require_version('Gtk', '3.0')
        gi.require_version('AppIndicator3', '0.1')
        from gi.repository import Gtk, AppIndicator3, GLib
        from PIL import Image, ImageDraw
        import cairosvg
        HAS_DEPS = True
        print("[INFO] Backend: AppIndicator3 (Linux)")
    except (ImportError, ValueError) as e:
        HAS_DEPS = False
        print(f"[ERROR] {e}")
        print("Instala: sudo apt install gir1.2-appindicator3-0.1 python3-gi")
        sys.exit(1)
        
elif IS_MACOS:
    # macOS - Usar pystray
    try:
        import pystray
        from pystray import MenuItem as item
        from PIL import Image, ImageDraw, ImageFont
        import cairosvg
        from Foundation import NSBundle
        import AppKit
        HAS_DEPS = True
        print("[INFO] Backend: pystray (macOS)")
        
        # Configurar como agente de UI
        try:
            info = NSBundle.mainBundle().infoDictionary()
            info["LSUIElement"] = "1"
        except:
            pass
    except ImportError as e:
        HAS_DEPS = False
        print(f"[ERROR] {e}")
        print("Instala: pip install pystray pillow cairosvg")
        sys.exit(1)
else:
    print(f"[ERROR] Sistema operativo no soportado: {platform.system()}")
    sys.exit(1)


class PortDestroyerTray:
    """Aplicación de bandeja del sistema (unificada para macOS y Linux)"""
    
    def __init__(self, start_port=3000, end_port=9000):
        self.destroyer = PortDestroyer(port_range=(start_port, end_port))
        self.start_port = start_port
        self.end_port = end_port
        self.processes = []
        self.processes_dict = {}
        self.update_interval = 1.5
        self.stop_event = Event()
        
        if IS_LINUX:
            self._init_linux()
        else:
            self._init_macos()
    
    def _init_linux(self):
        """Inicialización específica para Linux"""
        # Crear directorio temporal para iconos
        self.temp_dir = "/tmp/port-destroyer"
        os.makedirs(self.temp_dir, exist_ok=True)
        self.icon_path_green = os.path.join(self.temp_dir, "icon_green.png")
        self.icon_path_red = os.path.join(self.temp_dir, "icon_red.png")
        
        # Generar iconos PNG desde SVG
        self._create_linux_icons()
        
        # Crear indicador AppIndicator3
        self.indicator = AppIndicator3.Indicator.new(
            "port-destroyer",
            self.icon_path_green,
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_title("PortDestroyer")
        
        # Crear menú GTK
        self.menu = Gtk.Menu()
        self.indicator.set_menu(self.menu)
    
    def _init_macos(self):
        """Inicialización específica para macOS"""
        self.icon = None
        self.base_icon = None
        self._load_macos_icon()
    
    def _create_linux_icons(self):
        """Create Linux system tray icons with status badges"""
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            svg_path = os.path.join(script_dir, 'assets', 'icon.svg')
            
            if os.path.exists(svg_path):
                # Convert SVG to PNG (64x64 for Linux) - no tinting
                png_data = cairosvg.svg2png(url=svg_path, output_width=64, output_height=64)
                base_img = Image.open(BytesIO(png_data))
                
                # Create icons with status badges
                img_green = self._add_status_badge(base_img, False)  # Green = no processes
                img_red = self._add_status_badge(base_img, True)     # Red = with processes
                
                img_green.save(self.icon_path_green, 'PNG')
                img_red.save(self.icon_path_red, 'PNG')
                print("[INFO] Icons created (64x64) with status badges")
            else:
                # Fallback: simple icons with badges
                base_img = Image.new('RGBA', (64, 64), (100, 100, 100, 255))
                img_green = self._add_status_badge(base_img, False)
                img_red = self._add_status_badge(base_img, True)
                img_green.save(self.icon_path_green, 'PNG')
                img_red.save(self.icon_path_red, 'PNG')
        except Exception as e:
            print(f"[ERROR] Creating icons: {e}")
    
    def _load_macos_icon(self):
        """Carga icono para macOS"""
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            svg_path = os.path.join(script_dir, 'assets', 'icon.svg')
            
            if os.path.exists(svg_path):
                png_data = cairosvg.svg2png(url=svg_path, output_width=128, output_height=128)
                self.base_icon = Image.open(BytesIO(png_data))
                print("[INFO] Icono cargado (128x128)")
        except Exception as e:
            print(f"[ERROR] Cargando icono: {e}")
            self.base_icon = None
    
    def _add_status_badge(self, image, has_processes=False):
        """Add status badge to icon"""
        img_with_badge = image.copy()
        draw = ImageDraw.Draw(img_with_badge)
        
        # Calculate badge position (top-right corner)
        width, height = img_with_badge.size
        badge_size = max(8, width // 8)
        badge_x = width - badge_size - 2
        badge_y = 2
        
        # Badge color based on process status
        badge_color = (220, 53, 69) if has_processes else (40, 167, 69)
        
        # Draw badge circle
        draw.ellipse([badge_x, badge_y, badge_x + badge_size, badge_y + badge_size], 
                    fill=badge_color, outline=(255, 255, 255), width=1)
        
        return img_with_badge
    
    def create_macos_icon(self, has_processes=False):
        """Create macOS icon with status badge"""
        if self.base_icon:
            return self._add_status_badge(self.base_icon, has_processes)
        
        # Fallback: simple icon with badge
        width = 64
        img = Image.new('RGBA', (width, width), (100, 100, 100, 255))
        return self._add_status_badge(img, has_processes)
    
    # ==================== LINUX (AppIndicator3) ====================
    
    def update_linux_menu(self):
        """Actualiza menú GTK (Linux)"""
        for item in self.menu.get_children():
            self.menu.remove(item)
        
        count = len(self.processes)
        title = Gtk.MenuItem(label=f"{count} proceso{'s' if count != 1 else ''} activo{'s' if count != 1 else ''}")
        title.set_sensitive(False)
        self.menu.append(title)
        self.menu.append(Gtk.SeparatorMenuItem())
        
        if self.processes:
            for proc in sorted(self.processes, key=lambda x: x['port']):
                label = f"Puerto {proc['port']}: {proc['name']} (PID: {proc['pid']})"
                item = Gtk.MenuItem(label=label)
                item.connect('activate', lambda w, p=proc['port']: self.on_kill_port_linux(w, p))
                self.menu.append(item)
            
            self.menu.append(Gtk.SeparatorMenuItem())
            kill_all = Gtk.MenuItem(label="Eliminar Todos")
            kill_all.connect('activate', self.on_kill_all_linux)
            self.menu.append(kill_all)
        else:
            no_proc = Gtk.MenuItem(label="No hay procesos activos")
            no_proc.set_sensitive(False)
            self.menu.append(no_proc)
        
        self.menu.append(Gtk.SeparatorMenuItem())
        list_item = Gtk.MenuItem(label="Listar en Consola")
        list_item.connect('activate', self.on_list_processes_linux)
        self.menu.append(list_item)
        
        range_item = Gtk.MenuItem(label=f"Rango: {self.start_port}-{self.end_port}")
        range_item.set_sensitive(False)
        self.menu.append(range_item)
        
        self.menu.append(Gtk.SeparatorMenuItem())
        quit_item = Gtk.MenuItem(label="Salir")
        quit_item.connect('activate', self.on_quit_linux)
        self.menu.append(quit_item)
        
        self.menu.show_all()
    
    def on_kill_port_linux(self, widget, port):
        count = self.destroyer.kill_port(port)
        if count > 0:
            print(f"\n[OK] Proceso eliminado en puerto {port}")
        GLib.idle_add(self._update_ui_linux)
    
    def on_kill_all_linux(self, widget):
        count = self.destroyer.kill_all()
        print(f"\n[OK] Se eliminaron {count} proceso(s)")
        GLib.idle_add(self._update_ui_linux)
    
    def on_list_processes_linux(self, widget):
        print("\n" + "="*80)
        self.destroyer.list_processes()
        print("="*80 + "\n")
    
    def on_quit_linux(self, widget):
        print("\n[INFO] Cerrando PortDestroyer...")
        self.stop_event.set()
        Gtk.main_quit()
    
    def _update_ui_linux(self):
        """Actualiza UI de Linux"""
        has_processes = len(self.processes) > 0
        icon_path = self.icon_path_red if has_processes else self.icon_path_green
        self.indicator.set_icon_full(icon_path, "PortDestroyer")
        self.update_linux_menu()
        print(f"[DEBUG] UI actualizada: {len(self.processes)} procesos")
        return False
    
    # ==================== MACOS (pystray) ====================
    
    def create_macos_menu(self):
        """Crea menú pystray (macOS)"""
        try:
            menu_items = []
            count = len(self.processes)
            status = f'{count} proceso{"s" if count != 1 else ""} activo{"s" if count != 1 else ""}'
            menu_items.append(item(status, lambda: None, enabled=False))
            menu_items.append(item('-', lambda: None))
            
            if self.processes:
                for proc in sorted(self.processes, key=lambda x: x['port']):
                    label = f"Puerto {proc['port']}: {proc['name']} (PID: {proc['pid']})"
                    menu_items.append(item(label, self.on_kill_port_macos(proc['port'])))
                menu_items.append(item('-', lambda: None))
                menu_items.append(item('Eliminar Todos', self.on_kill_all_macos))
            else:
                menu_items.append(item('No hay procesos activos', lambda: None, enabled=False))
            
            menu_items.append(item('-', lambda: None))
            menu_items.append(item('Listar en Consola', self.on_list_processes_macos))
            menu_items.append(item(f'Rango: {self.start_port}-{self.end_port}', lambda: None, enabled=False))
            menu_items.append(item('-', lambda: None))
            menu_items.append(item('Salir', self.on_quit_macos))
            
            return tuple(menu_items)
        except Exception as e:
            print(f"[ERROR] Creando menú: {e}")
            return (item('Error', lambda: None, enabled=False), item('Salir', self.on_quit_macos))
    
    def on_kill_port_macos(self, port):
        def kill(icon, item):
            count = self.destroyer.kill_port(port)
            if count > 0:
                print(f"\n[OK] Proceso eliminado en puerto {port}")
            self._update_ui_macos()
        return kill
    
    def on_kill_all_macos(self, icon, item):
        count = self.destroyer.kill_all()
        print(f"\n[OK] Se eliminaron {count} proceso(s)")
        self._update_ui_macos()
    
    def on_list_processes_macos(self, icon, item):
        print("\n" + "="*80)
        self.destroyer.list_processes()
        print("="*80 + "\n")
    
    def on_quit_macos(self, icon, item):
        print("\n[INFO] Cerrando PortDestroyer...")
        self.stop_event.set()
        self.icon.stop()
    
    def _update_ui_macos(self):
        """Actualiza UI de macOS"""
        self.processes = self.destroyer.get_processes_on_ports()
        self.processes_dict = {(p['port'], p['pid']): p for p in self.processes}
        if self.icon:
            has_processes = len(self.processes) > 0
            self.icon.icon = self.create_macos_icon(has_processes)
            count = len(self.processes)
            self.icon.title = f"PortDestroyer - {count} proceso{'s' if count != 1 else ''}"
            self.icon.menu = pystray.Menu(self.create_macos_menu)
    
    # ==================== COMÚN ====================
    
    def update_processes(self):
        """Thread de actualización (común para ambos OS)"""
        while not self.stop_event.is_set():
            try:
                new_processes = self.destroyer.get_processes_on_ports()
                new_dict = {(p['port'], p['pid']): p for p in new_processes}
                
                if new_dict != self.processes_dict:
                    self.processes = new_processes
                    self.processes_dict = new_dict
                    print(f"[DEBUG] Procesos actualizados: {len(self.processes)}")
                    
                    # Actualizar UI según el OS
                    if IS_LINUX:
                        GLib.idle_add(self._update_ui_linux)
                    else:
                        self._update_ui_macos()
                        
            except Exception as e:
                print(f"[ERROR] Actualizando: {e}")
            
            time.sleep(self.update_interval)
    
    def run(self):
        """Ejecuta la aplicación según el OS"""
        # Cargar procesos iniciales
        print("[INFO] Cargando procesos iniciales...")
        self.processes = self.destroyer.get_processes_on_ports()
        self.processes_dict = {(p['port'], p['pid']): p for p in self.processes}
        print(f"[INFO] {len(self.processes)} proceso(s) encontrado(s)")
        
        # Mostrar banner
        print(f"""
╔══════════════════════════════════════════════════════════╗
║              PortDestroyer - System Tray                 ║
║  OS: {platform.system():<52} ║
║  Rango: {self.start_port}-{self.end_port:<47} ║
║  Actualización: Tiempo real (1.5s)                       ║
╚══════════════════════════════════════════════════════════╝
        """)
        
        # Iniciar thread de actualización
        update_thread = Thread(target=self.update_processes, daemon=True)
        update_thread.start()
        
        if IS_LINUX:
            # Actualizar menú inicial
            self.update_linux_menu()
            self._update_ui_linux()
            # Ejecutar GTK main loop
            try:
                Gtk.main()
            except KeyboardInterrupt:
                print("\n[INFO] Cerrando...")
                self.stop_event.set()
        else:
            # macOS
            try:
                app = AppKit.NSApplication.sharedApplication()
                app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyAccessory)
                app.activateIgnoringOtherApps_(True)
            except:
                pass
            
            # Crear icono pystray
            image = self.create_macos_icon(len(self.processes) > 0)
            self.icon = pystray.Icon(
                "PortDestroyer",
                image,
                f"PortDestroyer - {len(self.processes)} proceso(s)",
                menu=pystray.Menu(self.create_macos_menu)
            )
            
            try:
                self.icon.run()
            except SystemExit:
                pass


def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='PortDestroyer System Tray')
    parser.add_argument('--start', type=int, default=3000, help='Puerto inicial (default: 3000)')
    parser.add_argument('--end', type=int, default=9000, help='Puerto final (default: 9000)')
    args = parser.parse_args()
    
    if args.start >= args.end:
        print("[ERROR] El puerto inicial debe ser menor que el final")
        sys.exit(1)
    
    app = PortDestroyerTray(start_port=args.start, end_port=args.end)
    
    # Manejar señales
    def signal_handler(sig, frame):
        print("\n[INFO] Cerrando...")
        app.stop_event.set()
        if IS_LINUX:
            Gtk.main_quit()
        elif app.icon:
            try:
                app.icon.stop()
            except:
                pass
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        app.run()
    except KeyboardInterrupt:
        app.stop_event.set()
    except SystemExit:
        pass


if __name__ == '__main__':
    main()

