# Protokoll-Setup Anleitung

## Übersicht
Das KODi Plugin unterstützt jetzt drei verschiedene Protokolle für die Synchronisation:
- **FTP** (Standard, keine zusätzlichen Abhängigkeiten)
- **SFTP** (SSH File Transfer Protocol, sicher)
- **SMB** (Server Message Block, Windows-Freigaben)

## SFTP-Setup

### Abhängigkeiten installieren
```bash
pip install paramiko
```

### Konfiguration
1. **Protokoll**: Wähle "SFTP" in den Einstellungen
2. **Host**: IP-Adresse oder Hostname des SFTP-Servers
3. **Port**: Standardmäßig 22 (kann geändert werden)
4. **Benutzer**: SFTP-Benutzername
5. **Passwort**: SFTP-Passwort
6. **Schlüsseldatei** (optional): Pfad zur privaten SSH-Schlüsseldatei

### Authentifizierung
- **Passwort**: Einfach Benutzername und Passwort eingeben
- **Schlüssel**: Privaten SSH-Schlüssel in eine Datei speichern und Pfad angeben

## SMB-Setup

### Abhängigkeiten installieren
```bash
pip install smbprotocol
```

### Konfiguration
1. **Protokoll**: Wähle "SMB" in den Einstellungen
2. **Host**: IP-Adresse oder Hostname des SMB-Servers
3. **Benutzer**: SMB-Benutzername
4. **Passwort**: SMB-Passwort
5. **Freigabe**: Name der SMB-Freigabe (z.B. "shared")
6. **Domäne** (optional): Windows-Domäne falls erforderlich

### SMB-Pfad-Struktur
Der Remote-Pfad wird automatisch als `\\HOST\SHARE\pfad` konstruiert.

## Fallback-Verhalten
- Falls SFTP/SMB-Bibliotheken nicht verfügbar sind, fällt das Plugin automatisch auf FTP zurück
- Eine Warnung wird in den KODi-Logs ausgegeben

## Troubleshooting

### SFTP-Probleme
- Prüfe SSH-Verbindung: `ssh user@host -p port`
- Prüfe Schlüsselberechtigungen: `chmod 600 keyfile`
- Prüfe Server-Logs für Authentifizierungsfehler

### SMB-Probleme
- Prüfe SMB-Verbindung: `smbclient -L //host -U user`
- Prüfe Firewall-Einstellungen (Port 445)
- Prüfe SMB-Version-Kompatibilität

### Allgemeine Probleme
- Alle Protokolle verwenden dieselben Basis-Pfad-Einstellungen
- Ordner werden automatisch erstellt falls sie nicht existieren
- Fehler werden in den KODi-Logs protokolliert