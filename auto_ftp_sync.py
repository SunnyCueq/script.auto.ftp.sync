import os
import ftplib
import random
import urllib.request
import re
import xbmc
import xbmcaddon
import xbmcvfs
import sqlite3
import time
from contextlib import contextmanager
from typing import Optional, List, Tuple

# Einstellungen laden
ADDON = xbmcaddon.Addon()
ENABLED = ADDON.getSettingBool('enable_sync')
IS_MAIN_SYSTEM = ADDON.getSettingBool('is_main_system')
OVERWRITE_STATIC = ADDON.getSettingBool('overwrite_static')
FTP_BASE_PATH = ADDON.getSettingString('ftp_base_path')
CUSTOM_FOLDER = ADDON.getSettingString('custom_folder')
SPECIFIC_CUSTOM_FOLDER = ADDON.getSettingString('specific_custom_folder')
IMAGE_LIST_URL = ADDON.getSettingString('image_list_url')
FTP_HOST = ADDON.getSettingString('ftp_host')
FTP_USER = ADDON.getSettingString('ftp_user')
FTP_PASS = ADDON.getSettingString('ftp_pass')
FTP_PATH = f"/{FTP_BASE_PATH}/auto_fav_sync/{CUSTOM_FOLDER}/favourites.xml"
LOCAL_FAVOURITES = os.path.join(xbmcvfs.translatePath('special://userdata'), 'favourites.xml')
SUPER_FAVOURITES_PATH = os.path.join(xbmcvfs.translatePath('special://userdata'), 'addon_data', 'plugin.program.super.favourites', 'Super Favourites')
LOCAL_IMAGE_PATH = os.path.join(xbmcvfs.translatePath('special://userdata'), 'marvel.jpg')
ADDON_IMAGE_PATH = os.path.join(xbmcvfs.translatePath('special://home/addons/plugin.video.xstream'), 'fanart.jpg')
STATIC_FOLDERS = [folder.strip() for folder in ADDON.getSettingString('static_folders').split(',') if folder.strip()]
ENABLE_IMAGE_ROTATION = ADDON.getSettingBool('enable_image_rotation')

# Mehrsprachigkeit
LANGUAGE = ADDON.getLocalizedString

# Pfad zum Icon
ICON_PATH = os.path.join(ADDON.getAddonInfo('path'), 'resources', 'images', 'icon.png')

# FTP-Verbindungsklasse für bessere Performance
class FTPManager:
    """Verwaltet FTP-Verbindungen für bessere Performance und Fehlerbehandlung"""
    
    def __init__(self, host: str, user: str, password: str, timeout: int = 30):
        self.host = host
        self.user = user
        self.password = password
        self.timeout = timeout
        self._connection: Optional[ftplib.FTP] = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def connect(self) -> bool:
        """Stellt eine FTP-Verbindung her"""
        try:
            if self._connection:
                self.close()
            
            self._connection = ftplib.FTP()
            self._connection.connect(self.host, timeout=self.timeout)
            self._connection.login(self.user, self.password)
            xbmc.log("FTP-Verbindung erfolgreich hergestellt", xbmc.LOGINFO)
            return True
        except ftplib.all_errors as e:
            xbmc.log(f"FTP-Verbindungsfehler: {str(e)}", xbmc.LOGERROR)
            self.close()
            return False
    
    def close(self):
        """Schließt die FTP-Verbindung"""
        if self._connection:
            try:
                self._connection.quit()
            except:
                pass
            finally:
                self._connection = None
    
    def upload_file(self, local_path: str, remote_path: str) -> bool:
        """Lädt eine Datei hoch"""
        if not self._connection:
            if not self.connect():
                return False
        
        try:
            # Stelle sicher, dass das Verzeichnis existiert
            remote_dir = os.path.dirname(remote_path)
            if remote_dir and remote_dir != '/':
                self._create_remote_directory(remote_dir)
            
            with open(local_path, 'rb') as file:
                self._connection.storbinary(f'STOR {remote_path}', file)
            xbmc.log(f"Datei erfolgreich hochgeladen: {remote_path}", xbmc.LOGINFO)
            return True
        except ftplib.all_errors as e:
            xbmc.log(f"FTP Upload-Fehler: {str(e)}", xbmc.LOGERROR)
            return False
        except IOError as e:
            xbmc.log(f"Datei-Lesefehler: {str(e)}", xbmc.LOGERROR)
            return False
    
    def download_file(self, remote_path: str, local_path: str) -> bool:
        """Lädt eine Datei herunter"""
        if not self._connection:
            if not self.connect():
                return False
        
        try:
            # Stelle sicher, dass das lokale Verzeichnis existiert
            local_dir = os.path.dirname(local_path)
            if local_dir and not os.path.exists(local_dir):
                os.makedirs(local_dir, exist_ok=True)
            
            with open(local_path, 'wb') as file:
                self._connection.retrbinary(f'RETR {remote_path}', file.write)
            xbmc.log(f"Datei erfolgreich heruntergeladen: {local_path}", xbmc.LOGINFO)
            return True
        except ftplib.all_errors as e:
            xbmc.log(f"FTP Download-Fehler: {str(e)}", xbmc.LOGERROR)
            return False
        except IOError as e:
            xbmc.log(f"Datei-Schreibfehler: {str(e)}", xbmc.LOGERROR)
            return False
    
    def folder_exists(self, folder_path: str) -> bool:
        """Prüft, ob ein Ordner existiert"""
        if not self._connection:
            if not self.connect():
                return False
        
        try:
            current_dir = self._connection.pwd()
            self._connection.cwd(folder_path)
            self._connection.cwd(current_dir)  # Zurück zum ursprünglichen Verzeichnis
            return True
        except ftplib.error_perm as e:
            if '550' in str(e):
                return False
            else:
                xbmc.log(f"FTP-Ordnerprüfung fehlgeschlagen: {str(e)}", xbmc.LOGERROR)
                return False
    
    def _create_remote_directory(self, remote_dir: str):
        """Erstellt ein Remote-Verzeichnis rekursiv"""
        if not remote_dir or remote_dir == '/':
            return
        
        try:
            current_dir = self._connection.pwd()
            parts = remote_dir.strip('/').split('/')
            path = ''
            
            for part in parts:
                path += '/' + part
                try:
                    self._connection.cwd(path)
                except ftplib.error_perm:
                    self._connection.mkd(path)
                    self._connection.cwd(path)
            
            self._connection.cwd(current_dir)  # Zurück zum ursprünglichen Verzeichnis
        except ftplib.all_errors as e:
            xbmc.log(f"Fehler beim Erstellen des Remote-Verzeichnisses {remote_dir}: {str(e)}", xbmc.LOGERROR)

def show_notification(message_id, duration=5000, **kwargs):
    """Zeigt eine Benachrichtigung an"""
    try:
        message = LANGUAGE(message_id).format(**kwargs)
        xbmc.executebuiltin(f'Notification({LANGUAGE(30001)}, {message}, {duration}, {ICON_PATH})')
        # Reduzierte Wartezeit für bessere Performance
        time.sleep(min(duration / 2000, 1))  # Maximal 1 Sekunde warten
    except Exception as e:
        xbmc.log(f"Benachrichtigungsfehler: {str(e)}", xbmc.LOGERROR)

def validate_configuration() -> bool:
    """Validiert die Konfiguration vor der Ausführung"""
    if not FTP_HOST or not FTP_USER or not FTP_PASS:
        xbmc.log("FTP-Konfiguration unvollständig", xbmc.LOGERROR)
        return False
    
    if not CUSTOM_FOLDER:
        xbmc.log("Benutzerdefinierter Ordnername fehlt", xbmc.LOGERROR)
        return False
    
    if not FTP_BASE_PATH:
        xbmc.log("FTP-Basispfad fehlt", xbmc.LOGERROR)
        return False
    
    return True

def ftp_upload(local_path: str, remote_path: str) -> bool:
    """Lädt eine Datei über FTP hoch (Legacy-Funktion für Kompatibilität)"""
    if not os.path.exists(local_path):
        xbmc.log(f"Lokale Datei existiert nicht: {local_path}", xbmc.LOGERROR)
        return False
    
    with FTPManager(FTP_HOST, FTP_USER, FTP_PASS) as ftp:
        return ftp.upload_file(local_path, remote_path)

def ftp_download(remote_path: str, local_path: str) -> bool:
    """Lädt eine Datei über FTP herunter (Legacy-Funktion für Kompatibilität)"""
    with FTPManager(FTP_HOST, FTP_USER, FTP_PASS) as ftp:
        return ftp.download_file(remote_path, local_path)

def ftp_folder_exists(folder_path: str) -> bool:
    """Prüft, ob ein FTP-Ordner existiert (Legacy-Funktion für Kompatibilität)"""
    with FTPManager(FTP_HOST, FTP_USER, FTP_PASS) as ftp:
        return ftp.folder_exists(folder_path)

def sync_standard_favourites() -> bool:
    """Synchronisiert Standard-Favoriten"""
    try:
        if IS_MAIN_SYSTEM:
            if not os.path.exists(LOCAL_FAVOURITES):
                xbmc.log("Lokale Favoriten-Datei existiert nicht", xbmc.LOGWARNING)
                return False
            success = ftp_upload(LOCAL_FAVOURITES, FTP_PATH)
            if success:
                xbmc.log("Standard-Favoriten erfolgreich hochgeladen", xbmc.LOGINFO)
            return success
        else:
            success = ftp_download(FTP_PATH, LOCAL_FAVOURITES)
            if success:
                xbmc.log("Standard-Favoriten erfolgreich heruntergeladen", xbmc.LOGINFO)
            return success
    except Exception as e:
        xbmc.log(f"Fehler bei der Standard-Favoriten-Synchronisation: {str(e)}", xbmc.LOGERROR)
        return False

def sync_static_favourites() -> bool:
    """Synchronisiert statische Favoriten"""
    if not STATIC_FOLDERS:
        xbmc.log("Keine statischen Ordner konfiguriert", xbmc.LOGINFO)
        return True
    
    success_count = 0
    total_folders = len(STATIC_FOLDERS)
    
    try:
        with FTPManager(FTP_HOST, FTP_USER, FTP_PASS) as ftp:
            for folder in STATIC_FOLDERS:
                if not folder.strip():  # Überspringe leere Ordner
                    continue
                    
                local_static_path = os.path.join(SUPER_FAVOURITES_PATH, folder, 'favourites.xml')
                remote_static_path = f"/{FTP_BASE_PATH}/auto_fav_sync/{CUSTOM_FOLDER}/{folder}/favourites.xml"
                
                try:
                    if IS_MAIN_SYSTEM:
                        if os.path.exists(local_static_path):
                            if ftp.upload_file(local_static_path, remote_static_path):
                                xbmc.log(f"Statische Favoriten hochgeladen: {folder}", xbmc.LOGINFO)
                                success_count += 1
                            else:
                                xbmc.log(f"Fehler beim Hochladen der statischen Favoriten: {folder}", xbmc.LOGERROR)
                        else:
                            xbmc.log(f"Lokale statische Favoriten-Datei existiert nicht: {folder}", xbmc.LOGWARNING)
                    else:
                        if ftp.download_file(remote_static_path, local_static_path):
                            xbmc.log(f"Statische Favoriten heruntergeladen: {folder}", xbmc.LOGINFO)
                            success_count += 1
                            
                            # Überschreiben-Funktion für spezifischen Ordner
                            if OVERWRITE_STATIC and folder == SPECIFIC_CUSTOM_FOLDER:
                                specific_remote_static_path = f"/{FTP_BASE_PATH}/auto_fav_sync/{SPECIFIC_CUSTOM_FOLDER}/favourites.xml"
                                if ftp.download_file(specific_remote_static_path, local_static_path):
                                    xbmc.log(f"Spezifische Favoriten überschrieben: {folder}", xbmc.LOGINFO)
                        else:
                            xbmc.log(f"Fehler beim Herunterladen der statischen Favoriten: {folder}", xbmc.LOGERROR)
                except Exception as e:
                    xbmc.log(f"Fehler bei der Synchronisation des Ordners {folder}: {str(e)}", xbmc.LOGERROR)
        
        xbmc.log(f"Statische Favoriten-Synchronisation abgeschlossen: {success_count}/{total_folders} erfolgreich", xbmc.LOGINFO)
        return success_count > 0
        
    except Exception as e:
        xbmc.log(f"Kritischer Fehler bei der statischen Favoriten-Synchronisation: {str(e)}", xbmc.LOGERROR)
        return False

def clear_texture_cache() -> bool:
    """Löscht den Textur-Cache für bessere Performance"""
    try:
        db_path = xbmcvfs.translatePath('special://database/Textures13.db')
        if not os.path.exists(db_path):
            xbmc.log("Textur-Datenbank nicht gefunden", xbmc.LOGWARNING)
            return False
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Lösche Texturen und Größen
        cursor.execute("DELETE FROM texture")
        cursor.execute("DELETE FROM sizes")
        
        # Optional: VACUUM für bessere Performance
        cursor.execute("VACUUM")
        
        conn.commit()
        conn.close()
        
        xbmc.log("Textur-Cache erfolgreich geleert", xbmc.LOGINFO)
        return True
        
    except sqlite3.Error as e:
        xbmc.log(f"SQLite-Fehler beim Leeren des Caches: {str(e)}", xbmc.LOGERROR)
        return False
    except Exception as e:
        xbmc.log(f"Unerwarteter Fehler beim Leeren des Caches: {str(e)}", xbmc.LOGERROR)
        return False

def download_random_image() -> bool:
    """Lädt ein zufälliges Bild herunter und speichert es"""
    if not IMAGE_LIST_URL or not ENABLE_IMAGE_ROTATION:
        xbmc.log("Bildrotation deaktiviert oder URL nicht konfiguriert", xbmc.LOGINFO)
        return False

    try:
        # Erstelle Request mit Timeout und User-Agent
        request = urllib.request.Request(
            IMAGE_LIST_URL,
            headers={'User-Agent': 'Kodi Auto FTP Sync Addon/1.0.1'}
        )
        
        with urllib.request.urlopen(request, timeout=30) as response:
            if response.status != 200:
                xbmc.log(f"HTTP-Fehler beim Laden der Bildliste: {response.status}", xbmc.LOGERROR)
                return False
                
            content = response.read().decode('utf-8')
            image_urls = re.findall(r'\[img\](.*?)\[/img\]', content)
            
            if not image_urls:
                xbmc.log("Keine Bild-URLs in der Liste gefunden", xbmc.LOGERROR)
                return False
            
            # Wähle zufälliges Bild aus
            random_image_url = random.choice(image_urls).strip()
            if not random_image_url:
                xbmc.log("Leere Bild-URL gefunden", xbmc.LOGERROR)
                return False
                
            xbmc.log(f"Zufälliges Bild ausgewählt: {random_image_url}", xbmc.LOGINFO)
            
            # Lade das Bild herunter
            img_request = urllib.request.Request(
                random_image_url,
                headers={'User-Agent': 'Kodi Auto FTP Sync Addon/1.0.1'}
            )
            
            with urllib.request.urlopen(img_request, timeout=60) as img_response:
                if img_response.status != 200:
                    xbmc.log(f"HTTP-Fehler beim Laden des Bildes: {img_response.status}", xbmc.LOGERROR)
                    return False
                    
                img_data = img_response.read()
                
                # Validiere Bildgröße (max 10MB)
                if len(img_data) > 10 * 1024 * 1024:
                    xbmc.log("Bild zu groß (>10MB), überspringe", xbmc.LOGWARNING)
                    return False
                
                # Speichere Bild an beiden Orten
                success = True
                for path in [LOCAL_IMAGE_PATH, ADDON_IMAGE_PATH]:
                    try:
                        # Stelle sicher, dass das Verzeichnis existiert
                        os.makedirs(os.path.dirname(path), exist_ok=True)
                        
                        with open(path, 'wb') as f:
                            f.write(img_data)
                        xbmc.log(f"Bild gespeichert: {path}", xbmc.LOGINFO)
                    except IOError as e:
                        xbmc.log(f"Fehler beim Speichern des Bildes nach {path}: {str(e)}", xbmc.LOGERROR)
                        success = False
                
                if success:
                    show_notification(30032, 3000)  # Zufallsbild heruntergeladen
                    
                    # Cache leeren und UI aktualisieren
                    if clear_texture_cache():
                        xbmc.executebuiltin('ReloadSkin()')
                        xbmc.executebuiltin('Container.Refresh()')
                    
                    return True
                else:
                    return False
                    
    except urllib.error.HTTPError as e:
        xbmc.log(f"HTTP-Fehler: {e.code} - {e.reason}", xbmc.LOGERROR)
        try:
            error_response = e.read().decode('utf-8')
            xbmc.log(f"Server-Antwort: {error_response[:200]}...", xbmc.LOGERROR)
        except:
            pass
    except urllib.error.URLError as e:
        xbmc.log(f"URL-Fehler: {e.reason}", xbmc.LOGERROR)
    except Exception as e:
        xbmc.log(f"Unerwarteter Fehler beim Herunterladen des Bildes: {str(e)}", xbmc.LOGERROR)
    
    return False

def sync_favourites() -> bool:
    """Hauptfunktion für die Favoriten-Synchronisation"""
    try:
        # Validiere Konfiguration
        if not validate_configuration():
            show_notification(30023, 5000)  # Ein benutzerdefinierter Ordnername ist erforderlich
            return False

        # Prüfe FTP-Ordner
        if not ftp_folder_exists(f"/{FTP_BASE_PATH}/auto_fav_sync/{CUSTOM_FOLDER}"):
            show_notification(30024, 5000, folder=CUSTOM_FOLDER)  # Benutzerdefinierter Ordner nicht gefunden
            return False

        # Synchronisiere Favoriten
        standard_success = sync_standard_favourites()
        static_success = sync_static_favourites()
        
        # Zeige Erfolgsmeldung
        if standard_success or static_success:
            show_notification(30028, 3000)  # Synchronisation abgeschlossen
            return True
        else:
            xbmc.log("Keine Favoriten erfolgreich synchronisiert", xbmc.LOGWARNING)
            return False
            
    except Exception as e:
        xbmc.log(f"Kritischer Fehler bei der Favoriten-Synchronisation: {str(e)}", xbmc.LOGERROR)
        return False

def main():
    """Hauptfunktion des Addons"""
    try:
        if not ENABLED:
            xbmc.log("Auto FTP Sync ist deaktiviert", xbmc.LOGINFO)
            return
        
        xbmc.log("Auto FTP Sync gestartet", xbmc.LOGINFO)
        
        # Synchronisiere Favoriten
        sync_success = sync_favourites()
        
        # Lade zufälliges Bild herunter (unabhängig von Favoriten-Sync)
        image_success = download_random_image()
        
        # Logge Gesamtergebnis
        if sync_success or image_success:
            xbmc.log("Auto FTP Sync erfolgreich abgeschlossen", xbmc.LOGINFO)
        else:
            xbmc.log("Auto FTP Sync abgeschlossen mit Fehlern", xbmc.LOGWARNING)
            
    except Exception as e:
        xbmc.log(f"Kritischer Fehler in der Hauptfunktion: {str(e)}", xbmc.LOGERROR)

# Starte das Addon
if __name__ == "__main__":
    main()