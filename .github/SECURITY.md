# Security Policy

## Supported Versions

We take security seriously. The following versions of PortDestroyer are currently being supported with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability within PortDestroyer, please follow these steps:

### 1. Do Not Open a Public Issue

Please **do not** open a public GitHub issue for security vulnerabilities.

### 2. Send a Private Report

Send an email to: **security@jesusposso.dev** (or open a private security advisory on GitHub)

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### 3. Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Release**: Within 30 days (depending on severity)

### 4. Disclosure Policy

- We will acknowledge receipt of your vulnerability report
- We will provide regular updates about our progress
- We will credit you in the security advisory (unless you prefer to remain anonymous)
- We will publicly disclose the vulnerability only after a fix is released

## Security Best Practices

When using PortDestroyer:

1. **Keep Updated**: Always use the latest version
2. **Virtual Environment**: Run in a virtual environment
3. **Permissions**: Be cautious when running with elevated privileges
4. **Source**: Only download from official sources (GitHub, PyPI)

## Known Security Considerations

- **Elevated Privileges**: Some operations may require sudo/admin rights
- **Process Termination**: Killing processes can affect system stability
- **Port Scanning**: Port enumeration is visible to system administrators

## Security Features

PortDestroyer implements:
- No external network connections
- Minimal privilege escalation
- Safe process termination
- Input validation and sanitization

## Contact

For security concerns: security@jesusposso.dev  
For general issues: [GitHub Issues](https://github.com/jesusposso/port-destroyer/issues)

---

**Author**: Jesus Posso  
**Last Updated**: January 2025


