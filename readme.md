# Auto FTP Sync

## Beschreibung

**Auto FTP Sync** ist ein praktisches Kodi-Addon, das Ihnen hilft, Ihre Favoriten und Hintergrundbilder automatisch zwischen mehreren Kodi-Installationen zu synchronisieren. Mit diesem Addon können Sie sicherstellen, dass Ihre Favoriten stets auf dem neuesten Stand sind und dass Ihre Hintergrundbilder regelmäßig rotieren, um für visuelle Abwechslung zu sorgen.gen.

## Hauptfunktionen

1. **Automatische Synchronisation der Favoriten**:
    - **Hauptsystem und Subsystem**: Definieren Sie Ihr Hauptsystem, das die Favoriten hochlädt, und Subsysteme, die die Favoriten herunterladen. Dies stellt sicher, dass alle Geräte synchronisiert bleiben.
    - **Benutzerdefinierte Ordner**: Legen Sie benutzerdefinierte Ordner für Ihre Favoriten fest, um eine organisierte Struktur zu gewährleisten.
    - **Statische Ordner**: Synchronisieren Sie spezifische statische Ordner wie Anime, Horror, Marvel und Goat, um eine konsistente Favoritenliste 2. **Rotation von Hintergrundbildern**:
    - **Bildlisten-URL**: Geben Sie eine URL zu einer Liste von Bildern an, die regelmäßig heruntergeladen und als Hintergrundbild festgelegt werden.
    - **Aktivieren/Deaktivieren der Bildrotation**: Entscheiden Sie, ob die Hintergrundbild-Rotation aktiviert oder deaktiviert werden soll.

3. **Favoriten-Kategorisierung mit Platzhaltern**:
    - **Kategorie-Platzhalter**: Fügen Sie leere Favoriten-Einträge hinzu, die als Trennzeichen zwischen Kategorien fungieren.
    - **Automatische Kategorisierung**: Lassen Sie das Addon Ihre Favoriten automatisch in Kategorien einteilen.
    - **Anpassbare Platzhalter-Formatierung**: Konfigurieren Sie Präfix und Suffix für Ihre Kategorie-Platzhalter.rt werden soll.

## Einstellungen

#### Allgemeine Einstellungen

- **Synchronisation aktivieren**: 
  - **Option**: Ein/Aus
  - **Beschreibung**: Schalten Sie die automatische Synchronisation der Favoriten ein oder aus.

- **Hauptsystem**:
  - **Option**: Ein/Aus
  - **Beschreibung**: Bestimmen Sie, ob das aktuelle Gerät das Hauptsystem ist, das die Favoriten hochlädt.

- **Benutzerdefinierter Ordnername**:
  - **Option**: Textfeld
  - **Beschreibung**: Geben Sie den Namen des benutzerdefinierten Ordners für die Favoriten an.

- **Spezifischer benutzerdefinierter Ordner zum Überschreiben**:
  - **Option**: Textfeld
  - **Beschreibung**: Geben Sie den Namen eines spezifischen benutzerdefinierten Ordners an, der im Subsystem überschrieben werden soll.

#### FTP-Einstellungen

- **FTP-Basispfad**:
  - **Option**: Textfeld
  - **Beschreibung**: Geben Sie den Basispfad für den FTP-Server an.

- **FTP-Host**:
  - **Option**: Textfeld
  - **Beschreibung**: Geben Sie die FTP-Serveradresse ein.

- **FTP-Benutzer**:
  - **Option**: Textfeld
  - **Beschreibung**: Geben Sie den Benutzernamen für den FTP-Server ein.

- **FTP-Passwort**:
  - **Option**: Textfeld (versteckt)
  - **Beschreibung**: Geben Sie das Passwort für den FTP-Server ein.

#### Synchronisationsoptionen

- **Statische Favoriten überschreiben**:
  - **Option**: Ein/Aus
  - **Beschreibung**: Entscheiden Sie, ob statische Favoriten überschrieben werden sollen.

- **Statische Ordner (durch Kommas getrennt)**:
  - **Option**: Textfeld
  - **Beschreibung**: Geben Sie die zu synchronisierenden statischen Ordner a#### Bildeinstellungen

- **Bildlisten-URL**:
  - **Option**: Textfeld
  - **Beschreibung**: Geben Sie die URL zu einer Liste von Bildern ein, die als Hintergrundbilder verwendet werden sollen.

- **Hintergrundbild-Rotation aktivieren**:
  - **Option**: Ein/Aus
  - **Beschreibung**: Schalten Sie die Rotation der Hintergrundbilder ein oder aus.

#### Kategorie-Einstellungen

- **Kategorien aktivieren**:
  - **Option**: Ein/Aus
  - **Beschreibung**: Aktivieren oder deaktivieren Sie die Kategorisierungsfunktion für Favoriten.

- **Kategorie-Platzhalter Präfix**:
  - **Option**: Textfeld
  - **Beschreibung**: Geben Sie das Präfix für Kategorie-Platzhalter ein (Standard: [KATEGORIE]).

- **Kategorie-Platzhalter Suffix**:
  - **Option**: Textfeld
  - **Beschreibung**: Geben Sie das Suffix für Kategorie-Platzhalter ein (Standard: leer).

- **Favoriten automatisch kategorisieren**:
  - **Option**: Ein/Aus
  - **Beschreibung**: Lassen Sie das Addon Ihre Favoriten automatisch in Kategorien einteilen.bung**: Schalten Sie die Rotation der Hintergrundbilder ein oder aus.

## Nutzungshinweise

#### Erstkonfiguration

1. **Öffnen Sie die Einstellungen des Addons**:
    - Navigieren Sie zu den Addon-Einstellungen und konfigurieren Sie die FTP-Einstellungen. Geben Sie die FTP-Serveradresse, den Benutzernamen und das Passwort ein.

2. **Hauptsystem oder Subsystem bestimmen**:
    - Aktivieren Sie die Option "Hauptsystem", wenn das aktuelle Gerät das Hauptsystem ist, das die Favoriten hochlädt. Deaktivieren Sie diese Option, wenn es sich um ein Subsystem handelt, das die Favoriten herunterlädt.

3. **Benutzerdefinierte Ordnernamen festlegen**:
    - Geben Sie den Namen des benutzerdefinierten Ordners an, der für die Favoriten verwendet werden soll. Dies hilft, Ihre Favoriten organisiert zu halten.

4. **Statische Ordner angeben**:
    - Listen Sie die statischen Ordner auf, die synchronisiert werden sollen, getrennt durch Kommas (z.B. Anime,Horror,Marvel,Goat).

5. **Bildlisten-URL festlegen**:
    - Geben Sie die URL zu einer Bildliste an, die für die Rotation der Hintergrundbilder verwendet werden soll. Diese Liste muss in folgendem Format vorliegen:
      ```
      [img]https://example.6. **Hintergrundbild-Rotation aktivieren/deaktivieren**:
    - Schalten Sie die Hintergrundbild-Rotation ein oder aus, je nach Bedarf.

7. **Kategorisierungsoptionen konfigurieren**:
    - Aktivieren Sie die Kategorisierungsfunktion, wenn Sie Ihre Favoriten in Kategorien organisieren möchten.
    - Konfigurieren Sie das Präfix und Suffix für Ihre Kategorie-Platzhalter.
    - Aktivieren Sie die automatische Kategorisierung für eine einfache Organisation.ren**:#### Automatische Synchronisation

- Sobald das Addon aktiviert ist, synchronisiert es automatisch Ihre Favoriten basierend auf den festgelegten Einstellungen. Falls die Hintergrundbild-Rotation aktiviert ist, werden die Bilder regelmäßig aktualisiert und angezeigt.

#### Kategorisierungsfunktionen

**Manuelle Kategorisierung:**
- Fügen Sie Kategorie-Platzhalter manuell zu Ihren Favoriten hinzu, indem Sie das Addon mit dem entsprechenden Kategorie-Namen aufrufen.
- Die Platzhalter erscheinen als leere Favoriten-Einträge mit dem konfigurierten Präfix und Suffix.

**Automatische Kategorisierung:**
- Das Addon kann Ihre bestehenden Favoriten automatisch in Kategorien einteilen.
- Kategorie-Platzhalter werden automatisch zwischen verschiedenen Favoriten-Gruppen eingefügt.

**Beispiel einer kategorisierten Favoriten-Liste:**
```
[KATEGORIE] Filme
- Netflix
- Amazon Prime
- Disney+

[KATEGORIE] Serien
- Breaking Bad
- Game of Thrones
- Stranger Things

[KATEGORIE] Musik
- Spotify
- YouTube Music
```bild-Ro## Vorteile

- **Konsistente Favoriten**: Ihre Favoriten werden automatisch über alle Ihre Geräte hinweg synchronisiert, ohne dass Sie manuell eingreifen müssen.
- **Visuelle Abwechslung**: Die regelmäßige Rotation der Hintergrundbilder sorgt für eine frische und abwechslungsreiche Benutzeroberfläche.
- **Organisierte Favoriten**: Kategorisieren Sie Ihre Favoriten mit Platzhaltern für eine bessere Übersicht und Organisation.
- **Automatische Kategorisierung**: Lassen Sie das Addon Ihre Favoriten automatisch in logische Kategorien einteilen.
- **Einfach zu konfigurieren**: Mit benutzerfreundlichen Einstellungen können Sie das Addon nach Ihren Bedürfnissen anpassen.utzerfreundlichen Einstellungen können Sie das Addon nach Ihren Bedürfnissen anpassen.

## Support

Bei Fragen oder Problemen mit dem Addon wenden Sie sich bitte an den Support unter [Support-Kontakt]. Wir sind stets bemüht, Ihnen zu helfen und Ihre Erfahrung mit unserem Addon so angenehm wie möglich zu gestalten.
