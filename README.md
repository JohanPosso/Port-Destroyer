# PortDestroyer

**Professional Port Management Tool for macOS and Linux**

A fast, efficient, and user-friendly system tray application to monitor and manage network ports on your development machine. Built with performance and user experience in mind.

[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux-blue)](https://github.com/JohanPosso/port-destroyer)
[![Python](https://img.shields.io/badge/python-3.7+-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-blue)](CHANGELOG.md)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**Author:** [Jesus Posso](https://github.com/JohanPosso)  
**Website:** [johanposso.com](https://johanposso.com)  
**Status:** Production Ready

---

## Features

### Core Capabilities
- **High Performance** - Optimized with intelligent caching system
- **Cross-Platform** - Native support for macOS and Linux
- **Professional UI** - Clean system tray interface with SVG icons
- **Real-Time Updates** - 1.5s refresh rate with change detection
- **Smart Filtering** - Automatic deduplication, no repeated entries
- **Always Visible** - macOS optimized menus stay on top
- **Highly Configurable** - Custom port ranges and settings

### User Experience
- **Visual Status Indicator**: Green (idle) / Red (active processes)
- **One-Click Actions**: Terminate processes instantly
- **Professional Design**: Clean interface without emojis
- **CLI Available**: Full command-line interface for automation
- **Minimal Dependencies**: Only 3 required packages

## Requisitos

- Python 3.7 o superior
- macOS o Ubuntu/Linux
- Cairo (para renderizado de iconos SVG)

## Instalación

**UN SOLO COMANDO para macOS y Ubuntu:**

```bash
# 1. Clonar el proyecto
git clone https://github.com/JohanPosso/Port-Destroyer.git
cd Port-Destroyer

# 2. Instalar (detecta automáticamente el OS)
chmod +x port-destroyer
./port-destroyer --install

# 3. Listo! Ya puedes ejecutar
./port-destroyer
```

### Inicio Automático (Opcional)

```bash
# Configurar para que inicie al arrancar el sistema
./port-destroyer --autostart

# Desactivar inicio automático
./port-destroyer --uninstall-autostart
```

## Uso

### Interfaz Gráfica (Recomendado)

```bash
# Ejecutar (activa venv automáticamente, detecta el OS)
./port-destroyer

# Con rango personalizado de puertos
./port-destroyer --start 5000 --end 8000

# Ver ayuda
./port-destroyer --help
```

**Características del icono:**
- **Verde** - No hay procesos activos
- **Rojo** - Hay procesos activos
- **Icono profesional** - Diseño SVG escalable
- **Actualización en tiempo real** - Cada 1.5 segundos
- Click en el icono para ver el menú
- Selecciona un proceso para eliminarlo
- "Eliminar Todos" para liberar todos los puertos

**Se ejecuta en segundo plano** - No necesitas mantener la terminal abierta.

### CLI (Línea de Comandos)

```bash
# Activar venv primero
source venv/bin/activate

# Listar procesos
python3 port_destroyer.py --list

# Eliminar proceso en puerto específico
python3 port_destroyer.py --kill 3000

# Eliminar todos
python3 port_destroyer.py --kill-all
```

### Ejemplos Prácticos

```bash
# Ver qué está usando tus puertos de desarrollo
port-destroyer --list --start 3000 --end 5000

# Liberar puerto 3000 (React, Vite, etc.)
port-destroyer --kill 3000

# Liberar puerto 8080 (servidores web)
port-destroyer --kill 8080

# Limpiar todos los puertos de desarrollo
port-destroyer --kill-all --start 3000 --end 9000
```

## 📖 Opciones de Línea de Comandos

```
port-destroyer [opciones]

Opciones:
  --list              Listar todos los procesos en el rango
  --kill PORT         Matar proceso en puerto específico
  --kill-all          Matar todos los procesos en el rango
  --start PORT        Puerto inicial del rango (default: 3000)
  --end PORT          Puerto final del rango (default: 9000)
  -h, --help          Mostrar ayuda
```

## 🎯 Casos de Uso Comunes

### Desarrollo Web

```bash
# Puertos comunes de desarrollo web (React, Vue, Next.js, Vite)
port-destroyer --list --start 3000 --end 5000
```

### Servidores de Desarrollo

```bash
# Node.js, Python, Ruby servers
port-destroyer --list --start 8000 --end 9000
```

### Bases de Datos

```bash
# PostgreSQL (5432), MongoDB (27017), Redis (6379)
port-destroyer --list --start 5000 --end 30000
```

## 🔄 Inicio Automático (Opcional)

### macOS (LaunchAgent)

Crear archivo `~/Library/LaunchAgents/com.portdestroyer.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.portdestroyer</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/ruta/completa/a/port_destroyer_tray.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

Activar:
```bash
launchctl load ~/Library/LaunchAgents/com.portdestroyer.plist
```

### Ubuntu (Autostart)

Crear archivo `~/.config/autostart/portdestroyer.desktop`:

```ini
[Desktop Entry]
Type=Application
Name=PortDestroyer
Exec=/usr/bin/python3 /ruta/completa/a/port_destroyer_tray.py
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
```

## Desarrollo

### Estructura del Proyecto

```
Port-Destroyer/
├── assets/icon.svg           # Icono profesional SVG
├── port_destroyer.py         # Motor + CLI (multiplataforma)
├── port_destroyer_tray.py    # GUI (detecta macOS/Linux automáticamente)
├── port-destroyer             # Script universal (hace todo)
├── requirements.txt          # Dependencias
├── LICENSE                   # MIT License
└── README.md                 # Documentación
```

### Arquitectura

**port_destroyer.py** - Motor principal
- Detecta procesos con `lsof` (macOS) o `ss`/`netstat` (Linux)
- Deduplicación automática
- CLI completo

**port_destroyer_tray.py** - GUI unificada
- Detecta automáticamente el OS
- macOS: Usa `pystray` con optimizaciones AppKit
- Linux: Usa `AppIndicator3` (nativo GNOME)
- Actualización en tiempo real (1.5s)
- Cache inteligente
- Iconos dinámicos (verde/rojo)

## Solución de Problemas

### "No se puede importar pystray" o "No se puede importar cairosvg"

```bash
# Con entorno virtual (recomendado)
source venv/bin/activate
pip install -r requirements.txt

# Sin entorno virtual
pip3 install --user pystray pillow cairosvg
```

### "Permission denied"

Algunos procesos pueden requerir permisos de administrador:

```bash
# macOS/Linux
sudo python3 port_destroyer.py --kill-all
```

### El icono no aparece en la barra

**macOS:**
- Busca en el área de la derecha de la barra superior
- Si tienes muchos iconos, puede estar oculto en el menú de desbordamiento

**Ubuntu:**
- Asegúrate de tener soporte para system tray en tu escritorio
- En GNOME, instala la extensión "AppIndicator Support"

### "command not found: port-destroyer"

Asegúrate de que `~/.local/bin` esté en tu PATH:

```bash
# Agregar a ~/.zshrc o ~/.bashrc
export PATH="$PATH:$HOME/.local/bin"

# Recargar
source ~/.zshrc  # o source ~/.bashrc
```

## Comparación con port-kill

| Característica | PortDestroyer | port-kill original |
|----------------|---------------|-------------------|
| Tamaño | ~400 líneas Python | ~5000+ líneas Rust |
| Instalación | 1 comando | Compilación compleja |
| Personalización | Fácil (Python) | Difícil (Rust) |
| Rendimiento | Rápido + optimizado | Muy rápido |
| Dependencias | 3 (pystray, Pillow, cairosvg) | Muchas (Rust crates) |
| Mantenimiento | Simple | Complejo |
| Icono | SVG profesional | Generado |
| Actualización | Tiempo real (1.5s) | Por intervalo |

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting pull requests.

### Ways to Contribute
- Report bugs and issues
- Suggest new features
- Improve documentation
- Submit pull requests
- Share with the community

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License - Copyright (c) 2025 Jesus Posso
```

## Author

**Jesus Posso**
- GitHub: [@JohanPosso](https://github.com/JohanPosso)
- Website: [johanposso.com](https://johanposso.com)
- LinkedIn: [in/jesusposso](https://linkedin.com/in/jesusposso)
- Project: [port-destroyer](https://github.com/JohanPosso/port-destroyer)

## Acknowledgments

- Built for developers who need efficient port management
- Inspired by the need for a lightweight alternative to complex tools
- Icon designed to represent network connections professionally

## Project Stats

- **Version:** 1.0.0 (Production Ready)
- **Language:** Python 3.7+
- **Dependencies:** 3 (minimal)
- **Size:** ~500 lines of optimized code
- **Performance:** 1.5s update cycle with caching

## Star History

If you find this project useful, please consider giving it a star

## Support

- **Issues:** [GitHub Issues](https://github.com/JohanPosso/port-destroyer/issues)
- **Discussions:** [GitHub Discussions](https://github.com/JohanPosso/port-destroyer/discussions)
- **Changelog:** [CHANGELOG.md](CHANGELOG.md)

---

**Built by Jesus Posso**

*Professional tools for professional developers*

