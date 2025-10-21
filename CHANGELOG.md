# Changelog

All notable changes to PortDestroyer will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-21

### Added
- Professional system tray application with real-time updates
- Custom SVG icon with dynamic color tinting (green/red status)
- Intelligent caching system for optimal performance
- Automatic port deduplication to prevent duplicates
- macOS optimization for always-on-top menu display
- Support for custom port ranges
- CLI interface for command-line usage
- Cross-platform support (macOS and Linux)

### Features
- Real-time port monitoring (1.5s update interval)
- One-click process termination
- Professional UI without emojis
- SVG-based scalable icon
- Background process management
- Virtual environment support

### Technical
- Built with Python 3.7+
- Uses pystray for system tray integration
- CairoSVG for SVG rendering
- AppKit integration for macOS optimization
- Efficient process detection using lsof (macOS) and ss/netstat (Linux)

### Author
- Jesus Posso

## Future Roadmap

### [1.1.0] - Planned
- [ ] Multi-language support (Spanish, English)
- [ ] Dark mode icon variants
- [ ] Process filtering by name
- [ ] Export port usage reports
- [ ] Notification system for new processes

### [1.2.0] - Planned
- [ ] Windows support
- [ ] Process auto-kill rules
- [ ] System startup integration
- [ ] Web dashboard
- [ ] API for programmatic access

---

For more information, visit: https://github.com/JohanPosso/port-destroyer


