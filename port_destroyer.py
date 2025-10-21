#!/usr/bin/env python3
"""
PortDestroyer - Professional port management tool for macOS and Linux

Author: Jesus Posso
License: MIT
Version: 1.0.0
Repository: https://github.com/JohanPosso/port-destroyer

Description:
    A fast, professional tool to manage and free up ports on macOS and Linux.
    Supports both CLI and GUI (system tray) interfaces.
"""

__author__ = "Jesus Posso"
__version__ = "1.0.0"
__license__ = "MIT"

import subprocess
import platform
import signal
import sys
from typing import List, Dict, Optional


class PortDestroyer:
    """Gestor de puertos multiplataforma"""
    
    def __init__(self, port_range: tuple = (3000, 9000)):
        self.start_port = port_range[0]
        self.end_port = port_range[1]
        self.os_type = platform.system()
        
    def get_processes_on_ports(self) -> List[Dict]:
        """
        Obtiene todos los procesos usando puertos en el rango especificado.
        
        Los procesos se deduplican automáticamente usando la combinación (puerto, PID).
        Esto evita mostrar el mismo proceso múltiples veces cuando escucha en 
        múltiples interfaces (ej: IPv4 e IPv6).
        
        Returns:
            Lista de diccionarios con información de procesos únicos
        """
        processes = []
        
        if self.os_type == "Darwin":  # macOS
            processes = self._get_processes_macos()
        elif self.os_type == "Linux":  # Ubuntu/Linux
            processes = self._get_processes_linux()
        else:
            print(f"Sistema operativo no soportado: {self.os_type}")
            
        return processes
    
    def _get_processes_macos(self) -> List[Dict]:
        """Obtiene procesos en macOS usando lsof"""
        # Usar diccionario para evitar duplicados (mismo puerto + PID)
        processes_dict = {}
        
        try:
            # Usar lsof para obtener procesos en puertos TCP
            cmd = "lsof -iTCP -sTCP:LISTEN -n -P"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            for line in result.stdout.split('\n')[1:]:  # Saltar header
                if not line.strip():
                    continue
                    
                parts = line.split()
                if len(parts) >= 9:
                    try:
                        # Extraer puerto de la columna NAME (ej: *:3000)
                        port_info = parts[8]
                        if ':' in port_info:
                            port = int(port_info.split(':')[-1])
                            
                            # Filtrar por rango
                            if self.start_port <= port <= self.end_port:
                                pid = int(parts[1])
                                # Usar (puerto, pid) como clave única para evitar duplicados
                                key = (port, pid)
                                
                                if key not in processes_dict:
                                    processes_dict[key] = {
                                        'name': parts[0],
                                        'pid': pid,
                                        'port': port,
                                        'user': parts[2]
                                    }
                    except (ValueError, IndexError):
                        continue
                        
        except Exception as e:
            print(f"Error obteniendo procesos en macOS: {e}")
            
        return list(processes_dict.values())
    
    def _get_processes_linux(self) -> List[Dict]:
        """Obtiene procesos en Linux usando ss o netstat"""
        # Usar diccionario para evitar duplicados (mismo puerto + PID)
        processes_dict = {}
        
        try:
            # Intentar con ss primero (más moderno)
            cmd = "ss -tlnp"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode != 0:
                # Fallback a netstat
                cmd = "netstat -tlnp"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            for line in result.stdout.split('\n')[1:]:
                if not line.strip():
                    continue
                    
                parts = line.split()
                if len(parts) >= 4:
                    try:
                        # Extraer puerto de la columna Local Address (ej: 0.0.0.0:3000)
                        local_addr = parts[3]
                        if ':' in local_addr:
                            port = int(local_addr.split(':')[-1])
                            
                            # Filtrar por rango
                            if self.start_port <= port <= self.end_port:
                                # Extraer PID del formato users:(("proceso",pid=1234,fd=3))
                                pid_info = parts[-1] if len(parts) >= 6 else ''
                                pid = self._extract_pid_linux(pid_info)
                                
                                if pid:
                                    # Usar (puerto, pid) como clave única para evitar duplicados
                                    key = (port, pid)
                                    
                                    if key not in processes_dict:
                                        process_name = self._get_process_name(pid)
                                        processes_dict[key] = {
                                            'name': process_name,
                                            'pid': pid,
                                            'port': port,
                                            'user': ''
                                        }
                    except (ValueError, IndexError):
                        continue
                        
        except Exception as e:
            print(f"Error obteniendo procesos en Linux: {e}")
            
        return list(processes_dict.values())
    
    def _extract_pid_linux(self, pid_info: str) -> Optional[int]:
        """Extrae el PID del formato de ss/netstat"""
        try:
            if 'pid=' in pid_info:
                pid_str = pid_info.split('pid=')[1].split(',')[0]
                return int(pid_str)
        except:
            pass
        return None
    
    def _get_process_name(self, pid: int) -> str:
        """Obtiene el nombre del proceso dado su PID"""
        try:
            cmd = f"ps -p {pid} -o comm="
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.stdout.strip() or f"PID-{pid}"
        except:
            return f"PID-{pid}"
    
    def kill_process(self, pid: int) -> bool:
        """Mata un proceso dado su PID"""
        try:
            if self.os_type in ["Darwin", "Linux"]:
                # Usar kill -9 para forzar el cierre
                subprocess.run(f"kill -9 {pid}", shell=True, check=True)
                return True
            return False
        except subprocess.CalledProcessError:
            return False
        except Exception as e:
            print(f"Error matando proceso {pid}: {e}")
            return False
    
    def kill_port(self, port: int) -> int:
        """Mata todos los procesos en un puerto específico"""
        killed_count = 0
        processes = self.get_processes_on_ports()
        
        for proc in processes:
            if proc['port'] == port:
                print(f"Matando proceso {proc['name']} (PID: {proc['pid']}) en puerto {port}")
                if self.kill_process(proc['pid']):
                    killed_count += 1
                    
        return killed_count
    
    def kill_all(self) -> int:
        """Mata todos los procesos en el rango de puertos"""
        killed_count = 0
        processes = self.get_processes_on_ports()
        
        for proc in processes:
            print(f"Matando proceso {proc['name']} (PID: {proc['pid']}) en puerto {proc['port']}")
            if self.kill_process(proc['pid']):
                killed_count += 1
                
        return killed_count
    
    def list_processes(self) -> None:
        """Lista todos los procesos en el rango de puertos"""
        processes = self.get_processes_on_ports()
        
        if not processes:
            print(f"\n[OK] No hay procesos en el rango de puertos {self.start_port}-{self.end_port}")
            return
        
        print(f"\nProcesos encontrados en rango {self.start_port}-{self.end_port}:\n")
        print(f"{'Puerto':<10} {'PID':<10} {'Proceso':<30} {'Usuario':<15}")
        print("-" * 70)
        
        for proc in sorted(processes, key=lambda x: x['port']):
            print(f"{proc['port']:<10} {proc['pid']:<10} {proc['name']:<30} {proc['user']:<15}")


def main():
    """Función principal para uso por línea de comandos"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='PortDestroyer - Gestor de puertos rápido para Mac y Ubuntu',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  # Listar procesos en el rango por defecto (3000-9000)
  python3 port_destroyer.py --list
  
  # Matar proceso en puerto específico
  python3 port_destroyer.py --kill 3000
  
  # Matar todos los procesos en el rango
  python3 port_destroyer.py --kill-all
  
  # Usar rango personalizado
  python3 port_destroyer.py --list --start 5000 --end 8000
        """
    )
    
    parser.add_argument('--start', type=int, default=3000, 
                       help='Puerto inicial del rango (default: 3000)')
    parser.add_argument('--end', type=int, default=9000, 
                       help='Puerto final del rango (default: 9000)')
    parser.add_argument('--list', action='store_true', 
                       help='Listar procesos en el rango de puertos')
    parser.add_argument('--kill', type=int, metavar='PORT', 
                       help='Matar proceso en puerto específico')
    parser.add_argument('--kill-all', action='store_true', 
                       help='Matar todos los procesos en el rango')
    
    args = parser.parse_args()
    
    # Validar rango
    if args.start >= args.end:
        print("[ERROR] El puerto inicial debe ser menor que el puerto final")
        sys.exit(1)
    
    destroyer = PortDestroyer(port_range=(args.start, args.end))
    
    if args.list:
        destroyer.list_processes()
    elif args.kill:
        count = destroyer.kill_port(args.kill)
        if count > 0:
            print(f"\n[OK] Se eliminaron {count} proceso(s) en puerto {args.kill}")
        else:
            print(f"\n[INFO] No se encontraron procesos en puerto {args.kill}")
    elif args.kill_all:
        count = destroyer.kill_all()
        if count > 0:
            print(f"\n[OK] Se eliminaron {count} proceso(s) en total")
        else:
            print(f"\n[INFO] No se encontraron procesos para eliminar")
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

