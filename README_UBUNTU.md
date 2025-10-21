# Instalación y Uso en Ubuntu

## Problema con pystray en Ubuntu

Si el menú no se despliega usando `port_destroyer_tray.py`, usa la versión específica para Linux que utiliza AppIndicator3 (más confiable en GNOME).

## Instalación Ubuntu

```bash
# 1. Instalar dependencias del sistema
sudo apt update
sudo apt install -y python3-gi gir1.2-appindicator3-0.1 libcairo2-dev pkg-config python3-dev

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependencias Python
pip install Pillow cairosvg

# 4. Dar permisos
chmod +x port_destroyer_tray_linux.py
```

## Uso

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar versión para Linux (con sudo si es necesario)
sudo $(which python3) port_destroyer_tray_linux.py

# O sin sudo si tus puertos no requieren privilegios
python3 port_destroyer_tray_linux.py
```

## Diferencias entre versiones

- `port_destroyer_tray.py` - Usa pystray (funciona mejor en macOS)
- `port_destroyer_tray_linux.py` - Usa AppIndicator3 (funciona mejor en Ubuntu/GNOME)

## Si el icono no aparece

1. Verifica que AppIndicator esté instalado:
```bash
dpkg -l | grep appindicator
```

2. Habilita la extensión de GNOME:
```bash
gnome-extensions enable ubuntu-appindicators@ubuntu.com
```

3. Reinicia GNOME Shell:
- Presiona Alt+F2
- Escribe `r`
- Presiona Enter

Author: Jesus Posso

