# Kali Linux - Security Desktop

**URL**: https://kali.cbass.space | **Container**: kali | **Port**: 6901

## Overview

Kali Linux is a Debian-based distribution for security testing, running in a browser-accessible desktop via KasmWeb. Use it for learning security fundamentals, CTF challenges, and authorized penetration testing.

## Quick Access

| Environment | URL |
|-------------|-----|
| Production | https://kali.cbass.space |
| Local | https://localhost:6901 |

Note: Uses HTTPS even locally (self-signed cert).

## First-Time Setup

1. Navigate to Kali URL (`https://localhost:6901` locally)
2. Accept self-signed certificate warning in browser
3. Login with KasmWeb credentials:
   - Username: `kasm_user`
   - Password: `KALI_VNC_PW` value from `.env`

## Interface

KasmWeb provides:
- Full Kali desktop in browser
- Clipboard sharing
- File upload/download
- Resolution auto-scaling

## Common Tasks

### Open Terminal

Click terminal icon in taskbar or right-click desktop > "Open Terminal Here"

### Update Tools

```bash
sudo apt update && sudo apt upgrade -y
```

### Install Additional Tools

```bash
sudo apt install <tool-name>
```

### Access Host Network

From Kali, other CBass services are accessible via container names:
- `http://n8n:5678`
- `http://ollama:11434`
- `http://supabase-db:5432`

## Pre-installed Tools

Kali includes hundreds of security tools:

| Category | Tools |
|----------|-------|
| Information Gathering | nmap, recon-ng, maltego |
| Vulnerability Analysis | nikto, sqlmap, wpscan |
| Web Applications | burpsuite, zap, gobuster |
| Password Attacks | john, hashcat, hydra |
| Wireless | aircrack-ng, wifite |
| Exploitation | metasploit, searchsploit |
| Forensics | autopsy, binwalk, volatility |
| Reverse Engineering | ghidra, radare2 |

## Troubleshooting

### Problem: Cannot connect
**Solution**:
- Accept self-signed certificate
- Verify VNC_PW is set in .env
- Check container is running

### Problem: Black screen
**Solution**:
- Refresh browser
- Clear browser cache
- Restart container: `docker compose -p localai restart kali`

### Problem: Clipboard not working
**Solution**:
- Use Kasm's clipboard panel (left sidebar)
- Copy to Kasm clipboard, then paste

### Problem: Slow performance
**Solution**:
- Reduce browser window size
- Close unused applications
- Increase container resources

## Educational Applications

| Use Case | Tools to Learn |
|----------|----------------|
| Network basics | nmap, wireshark |
| Web security | burpsuite, sqlmap |
| CTF challenges | All categories |
| Scripting | Python, Bash in Kali |
| Forensics | Autopsy, binwalk |

## Security Notes

**Use responsibly:**
- Only test systems you own or have permission to test
- CBass Kali is for learning and authorized testing
- Keep container updated for security patches
- Don't expose to public internet without authentication

## Environment Variables

```bash
# In .env
KALI_VNC_PW=yourpassword        # Required for login (user: kasm_user)
KALI_HOSTNAME=kali.cbass.space  # Production hostname
```

## Resource Usage

Kali desktop uses significant resources:
- Memory: 2-4 GB
- CPU: Variable based on tools
- Disk: Base image + installed tools

Monitor with:
```bash
docker stats kali
```

## Persistence

Work files persist in container. For important files:

1. **Download**: Use KasmWeb file download
2. **Volume mount**: Map local directory to container
3. **Git**: Push code to repositories

## Resources

- [Kali Linux Documentation](https://www.kali.org/docs/)
- [Kali Tools](https://www.kali.org/tools/)
- [KasmWeb Documentation](https://kasmweb.com/docs/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
