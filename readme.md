# Auto FTP Sync

## Überblick

Auto FTP Sync ist ein Kodi‑Addon für Kodi 21 (Omega), das Favoriten und optionale statische Ordner zwischen mehreren Geräten synchronisiert, Hintergrundbilder rotieren kann und einfache Kategorien für Favoriten unterstützt.

## Features

- Protokolle: FTP, SFTP, SMB – standardmäßig über Kodi‑VFS (kein externes Python nötig)
- Multi‑Master‑Sync: Neueste Änderung gewinnt (keine Haupt/Sub‑Unterscheidung)
- Statische Ordner: z. B. `Anime,Horror,Marvel,Goat`
- Kategorien: Platzhalter‑basierte Kategorisierung, Dialoge zum Anlegen und Verschieben
- Hintergrundbilder: Rotation per Bildlisten‑URL
- Ersteinrichtung: Dialog geführte Einrichtung beim ersten Start

## Voraussetzungen

- Kodi 21 (Omega)
- Für SFTP: Kodi‑Addon `vfs.sftp` (wird als optionale Abhängigkeit deklariert)

## Installation & Ersteinrichtung

1) Addon installieren und starten
2) Ersteinrichtungsdialog ausfüllen:
   - Protokoll (FTP/SFTP/SMB)
   - Host (+ SFTP‑Port oder SMB Share, falls nötig)
   - Basis‑Pfad und `custom_folder`
   - Benutzername/Passwort
3) Optional: `Einstellungen → Verbindung → Kodi VFS bevorzugen` aktiv lassen (empfohlen)

## Nutzung

- Synchronisieren: Bei aktivierter Synchronisation läuft der Multi‑Master‑Sync automatisch. Änderungen an `favourites.xml` werden hochgeladen bzw. vom Server bezogen.
- Statische Ordner: Werden pro Eintrag unter `Super Favourites/<Ordner>/favourites.xml` synchronisiert.
- Kategorien:
  - Anlegen per Dialog (Platzhalter wird erzeugt)
  - Favorit in Kategorie verschieben (Favorit und Ziel‑Kategorie wählen)
  - Automatisches Kategorisieren optional aktivierbar
- Hintergrundbildrotation: Lädt per Bildlisten‑URL ein zufälliges Bild und aktualisiert Skin/Cache.

## Einstellungen (Auszug)

- Allgemein: Synchronisation aktivieren, `custom_folder`, statische Ordner
- Verbindung: Protokoll, Host, Zugangsdaten, optional `prefer_vfs`
- Kategorien: aktivieren, Präfix/Suffix, Auto‑Kategorisieren
- Bilder: Bildlisten‑URL, Rotation aktivieren

## Hinweise

- SFTP erfordert das Kodi‑Addon `vfs.sftp`. Bei installierter Abhängigkeit funktioniert SFTP ohne zusätzliche Python‑Module.
- Wenn `prefer_vfs` deaktiviert wird, können externe Module erforderlich sein (paramiko/smbclient). Standard ist VFS.

## Lizenz / Support

Siehe Repository. Bei Fragen bitte ein Issue im GitHub‑Repository eröffnen.
