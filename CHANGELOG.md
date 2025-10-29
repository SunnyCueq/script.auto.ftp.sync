# Changelog - KODi Auto FTP Sync Plugin

## Version 2.0.0 - Multi-Protocol Support

### 🆕 Neue Features

#### Protokoll-Unterstützung
- **FTP**: Weiterhin vollständig unterstützt (Standard)
- **SFTP**: Neue sichere SSH-basierte Dateiübertragung
- **SMB**: Neue Windows-Freigaben-Unterstützung

#### Verbesserte Architektur
- **ConnectionManager**: Abstrakte Basisklasse für alle Protokolle
- **Factory Pattern**: Automatische Protokoll-Auswahl
- **Fallback-System**: Automatischer Fallback auf FTP bei fehlenden Bibliotheken

#### Neue Einstellungen
- **Protokoll-Auswahl**: Dropdown-Menü für FTP/SFTP/SMB
- **SFTP-Einstellungen**: Port, Schlüsseldatei
- **SMB-Einstellungen**: Freigabe, Domäne

#### Verbesserte Benutzerfreundlichkeit
- **Protokoll-Status-Logging**: Zeigt verfügbare Protokolle an
- **Test-Funktion**: `test_connection()` zum Testen der Verbindung
- **Bessere Fehlermeldungen**: Detaillierte Installationsanweisungen

### 🔧 Technische Verbesserungen

#### Code-Refactoring
- Alle FTP-spezifischen Funktionen durch universelle Funktionen ersetzt
- Rückwärtskompatibilität vollständig erhalten
- Konsistente Fehlerbehandlung für alle Protokolle

#### Neue Manager-Klassen
- **SFTPManager**: Vollständige SFTP-Implementierung mit paramiko
- **SMBManager**: Vollständige SMB-Implementierung mit smbprotocol
- **FTPManager**: Erweitert um neue Methoden

#### Automatische Ordner-Erstellung
- Alle Protokolle erstellen automatisch benötigte Ordner
- Rekursive Ordner-Erstellung für verschachtelte Pfade

### 📦 Abhängigkeiten

#### Neue Abhängigkeiten
- `paramiko>=2.7.0` für SFTP-Unterstützung
- `smbprotocol>=1.0.0` für SMB-Unterstützung

#### Installation
```bash
pip install paramiko smbprotocol
```

### 🌐 Internationalisierung
- Deutsche und englische Sprachdateien erweitert
- Neue String-IDs für Protokoll-Einstellungen

### 📚 Dokumentation
- **PROTOCOL_SETUP.md**: Detaillierte Setup-Anleitung
- **requirements.txt**: Abhängigkeitsliste
- **CHANGELOG.md**: Diese Änderungsliste

### 🔄 Migration
- **Automatisch**: Bestehende FTP-Konfigurationen funktionieren unverändert
- **Keine Datenverluste**: Alle bestehenden Einstellungen bleiben erhalten
- **Erweiterte Optionen**: Neue Protokolle als zusätzliche Optionen verfügbar

### 🐛 Fehlerbehandlung
- Graceful Fallback bei fehlenden Bibliotheken
- Detaillierte Fehlermeldungen mit Installationsanweisungen
- Umfassende Protokollierung für alle Protokolle

### ⚡ Performance
- Verbindungs-Wiederverwendung für alle Protokolle
- Optimierte Ordner-Erstellung
- Effiziente Fehlerbehandlung

---

## Verwendung

### Protokoll wechseln
1. Einstellungen öffnen
2. "Verbindungseinstellungen" → "Protokoll" auswählen
3. Entsprechende Einstellungen konfigurieren
4. Verbindung testen mit `test_connection()`

### SFTP einrichten
1. Protokoll auf "SFTP" setzen
2. Host, Port, Benutzer, Passwort eingeben
3. Optional: Schlüsseldatei-Pfad angeben

### SMB einrichten
1. Protokoll auf "SMB" setzen
2. Host, Benutzer, Passwort eingeben
3. Freigabe-Name eingeben
4. Optional: Domäne eingeben

Das Plugin ist jetzt vollständig multi-protokoll-fähig! 🎉