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

**Mismo proceso para macOS y Ubuntu/Linux:**

```bash
# 1. Clonar o descargar el proyecto
cd port-destroy

# 2. Crear entorno virtual
python3 -m venv venv

# 3. Activar entorno virtual
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Dar permisos
chmod +x start_tray.sh port_destroyer.py
```

### Dependencias del sistema (solo Ubuntu/Debian)

```bash
# Si estás en Ubuntu, instala Cairo primero:
sudo apt install libcairo2-dev pkg-config python3-dev

# Para bandeja del sistema en GNOME:
sudo apt install gnome-shell-extension-appindicator
```

Listo! El mismo proyecto funciona en ambos sistemas.

## Uso

### Interfaz Gráfica (Barra Superior)

La forma más cómoda de usar PortDestroyer:

```bash
# Usando el script de inicio (activa automáticamente el entorno virtual)
./start_tray.sh

# O manualmente activando el entorno virtual:
source venv/bin/activate
python3 port_destroyer_tray.py

# Con rango personalizado
./start_tray.sh  # Edita el script para personalizar el rango
```

**Características del icono:**
- **Verde** - No hay procesos activos en el rango
- **Rojo** - Hay procesos activos
- **Icono de red profesional** - Diseño SVG escalable que representa puertos/conexiones
- **Actualización en tiempo real** - Responde inmediatamente a cambios
- **Menú siempre visible** - Aparece por encima de todas las ventanas en macOS
- Haz clic en el icono para ver el menú
- Selecciona un proceso para eliminarlo
- Usa "Eliminar Todos" para liberar todos los puertos

**Nota para macOS:** La aplicación está optimizada para que el menú siempre aparezca al frente de todas las ventanas.

### Línea de Comandos (CLI)

Para uso rápido desde la terminal:

```bash
# Listar procesos en el rango por defecto (3000-9000)
port-destroyer --list

# Listar con rango personalizado
port-destroyer --list --start 5000 --end 8000

# Matar proceso en puerto específico
port-destroyer --kill 3000

# Matar todos los procesos en el rango
port-destroyer --kill-all
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
port-destroy/
├── assets/
│   └── icon.svg              # Icono SVG profesional
├── port_destroyer.py         # Lógica principal y CLI
├── port_destroyer_tray.py    # Interfaz de barra superior
├── start_tray.sh             # Script de inicio
├── requirements.txt          # Dependencias Python
└── README.md                 # Documentación
```

### Arquitectura

- **port_destroyer.py**: Clase `PortDestroyer` con lógica multiplataforma
  - Usa `lsof` en macOS
  - Usa `ss` o `netstat` en Linux
  - Métodos optimizados para listar y eliminar procesos

- **port_destroyer_tray.py**: Clase `PortDestroyerTray` con interfaz gráfica
  - Usa `pystray` para sistema de bandeja
  - Renderizado SVG a PNG con `cairosvg`
  - Thread para actualización automática en tiempo real
  - Cache inteligente que solo actualiza cuando detecta cambios
  - Menú dinámico con procesos actuales
  - Tintado dinámico del icono según estado (verde/rojo)

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

