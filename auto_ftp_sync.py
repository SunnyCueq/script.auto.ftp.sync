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

# Konfiguration
class Config:
    def __init__(self):
        self.enabled = ADDON.getSettingBool('enable_sync')
        self.is_main_system = ADDON.getSettingBool('is_main_system')
        self.overwrite_static = ADDON.getSettingBool('overwrite_static')
        self.ftp_base_path = ADDON.getSettingString('ftp_base_path')
        self.custom_folder = ADDON.getSettingString('custom_folder')
        self.specific_custom_folder = ADDON.getSettingString('specific_custom_folder')
        self.image_list_url = ADDON.getSettingString('image_list_url')
        self.ftp_host = ADDON.getSettingString('ftp_host')
        self.ftp_user = ADDON.getSettingString('ftp_user')
        self.ftp_pass = ADDON.getSettingString('ftp_pass')
        self.static_folders = [f.strip() for f in ADDON.getSettingString('static_folders').split(',') if f.strip()]
        self.enable_image_rotation = ADDON.getSettingBool('enable_image_rotation')
        
        # Pfade berechnen
        self.ftp_path = f"/{self.ftp_base_path}/auto_fav_sync/{self.custom_folder}/favourites.xml"
        self.local_favourites = os.path.join(xbmcvfs.translatePath('special://userdata'), 'favourites.xml')
        self.super_favourites_path = os.path.join(
            xbmcvfs.translatePath('special://userdata'), 
            'addon_data', 
            'plugin.program.super.favourites', 
            'Super Favourites'
        )
        self.local_image_path = os.path.join(xbmcvfs.translatePath('special://userdata'), 'marvel.jpg')
        self.addon_image_path = os.path.join(
            xbmcvfs.translatePath('special://home/addons/plugin.video.xstream'), 
            'fanart.jpg'
        )
        self.icon_path = os.path.join(ADDON.getAddonInfo('path'), 'resources', 'images', 'icon.png')
        
        # Validierung
        self._validate_config()
    
    def _validate_config(self):
        """Validiert die Konfiguration und gibt Warnungen aus"""
        if not self.custom_folder:
            xbmc.log("WARNING: Custom folder name is empty", xbmc.LOGWARNING)
        if not self.ftp_host:
            xbmc.log("WARNING: FTP host is not configured", xbmc.LOGWARNING)
        if not self.ftp_user:
            xbmc.log("WARNING: FTP user is not configured", xbmc.LOGWARNING)

# Globale Konfiguration
config = Config()
LANGUAGE = ADDON.getLocalizedString

# Rückwärtskompatibilität - Globale Variablen für bestehenden Code
ENABLED = config.enabled
IS_MAIN_SYSTEM = config.is_main_system
OVERWRITE_STATIC = config.overwrite_static
FTP_BASE_PATH = config.ftp_base_path
CUSTOM_FOLDER = config.custom_folder
SPECIFIC_CUSTOM_FOLDER = config.specific_custom_folder
IMAGE_LIST_URL = config.image_list_url
FTP_HOST = config.ftp_host
FTP_USER = config.ftp_user
FTP_PASS = config.ftp_pass
FTP_PATH = config.ftp_path
LOCAL_FAVOURITES = config.local_favourites
SUPER_FAVOURITES_PATH = config.super_favourites_path
LOCAL_IMAGE_PATH = config.local_image_path
ADDON_IMAGE_PATH = config.addon_image_path
STATIC_FOLDERS = config.static_folders
ENABLE_IMAGE_ROTATION = config.enable_image_rotation
ICON_PATH = config.icon_path
def show_notification(message_id: int, duration: int = 5000, **kwargs) -> None:
    """Zeigt eine Benachrichtigung an"""
    try:
        message = LANGUAGE(message_id).format(**kwargs)
        xbmc.executebuiltin(f'Notification({LANGUAGE(30001)}, {message}, {duration}, {config.icon_path})')
        time.sleep(duration / 1000)  # Warte, bis die Benachrichtigung abgeschlossen ist
    except Exception as e:
        xbmc.log(f"Error showing notification: {str(e)}", xbmc.LOGERROR)


class FTPManager:
    """Verwaltet FTP-Verbindungen mit Wiederverwendung"""
    
    def __init__(self, host: str, user: str, password: str):
        self.host = host
        self.user = user
        self.password = password
        self._connection: Optional[ftplib.FTP] = None
    
    @contextmanager
    def get_connection(self):
        """Kontextmanager für FTP-Verbindungen"""
        try:
            if self._connection is None:
                self._connection = ftplib.FTP(self.host)
                self._connection.login(self.user, self.password)
                xbmc.log("FTP connection established", xbmc.LOGINFO)
            yield self._connection
        except Exception as e:
            xbmc.log(f"FTP connection error: {str(e)}", xbmc.LOGERROR)
            if self._connection:
                try:
                    self._connection.quit()
                except:
                    pass
                self._connection = None
            raise
    
    def close(self):
        """Schließt die FTP-Verbindung"""
        if self._connection:
            try:
                self._connection.quit()
                xbmc.log("FTP connection closed", xbmc.LOGINFO)
            except Exception as e:
                xbmc.log(f"Error closing FTP connection: {str(e)}", xbmc.LOGERROR)
            finally:
                self._connection = Nonedef ftp_upload_legacy(local_path, remote_path):
    """Ursprüngliche FTP-Upload-Funktion für Rückwärtskompatibilität"""
    try:
        with ftplib.FTP(FTP_HOST) as ftp:
            ftp.login(FTP_USER, FTP_PASS)
            with open(local_path, 'rb') as file:
                ftp.storbinary(f'STOR {remote_path}', file)
        return True
    except Exception as e:
        xbmc.log(f"FTP upload failed: {str(e)}", xbmc.LOGERROR)
        return False

def ftp_download_legacy(remote_path, local_path):
    """Ursprüngliche FTP-Download-Funktion für Rückwärtskompatibilität"""
    try:
        with ftplib.FTP(FTP_HOST) as ftp:
            ftp.login(FTP_USER, FTP_PASS)
            with open(local_path, 'wb') as file:
                ftp.retrbinary(f'RETR {remote_path}', file.write)
        return True
    except Exception as e:
        xbmc.log(f"FTP download failed: {str(e)}", xbmc.LOGERROR)
        return False

def ftp_folder_exists_legacy(folder_path):
    """Ursprüngliche FTP-Ordner-Prüfung für Rückwärtskompatibilität"""
    try:
        with ftplib.FTP(FTP_HOST) as ftp:
            ftp.login(FTP_USER, FTP_PASS)
            ftp.cwd(folder_path)
        return True
    except ftplib.error_perm as e:
        if '550' in str(e):
            return False
        else:
            xbmc.log(f"FTP error: {str(e)}", xbmc.LOGERROR)
            return False

def ftp_upload(ftp_manager: FTPManager, local_path: str, remote_path: str) -> bool:
    """Lädt eine Datei zum FTP-Server hoch"""
    try:
        if not os.path.exists(local_path):
            xbmc.log(f"Local file does not exist: {local_path}", xbmc.LOGERROR)
            return False
            
        with ftp_manager.get_connection() as ftp:
            with open(local_path, 'rb') as file:
                ftp.storbinary(f'STOR {remote_path}', file)
        xbmc.log(f"Successfully uploaded: {local_path} -> {remote_path}", xbmc.LOGINFO)
        return True
    except Exception as e:
        xbmc.log(f"FTP upload failed: {str(e)}", xbmc.LOGERROR)
        return False

def ftp_download(ftp_manager: FTPManager, remote_path: str, local_path: str) -> bool:
    """Lädt eine Datei vom FTP-Server herunter"""
    try:
        # Stelle sicher, dass das Verzeichnis existiert
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        with ftp_manager.get_connection() as ftp:
            with open(local_path, 'wb') as file:
                ftp.retrbinary(f'RETR {remote_path}', file.write)
        xbmc.log(f"Successfully downloaded: {remote_path} -> {local_path}", xbmc.LOGINFO)
        return True
    except Exception as e:
        xbmc.log(f"FTP download failed: {str(e)}", xbmc.LOGERROR)
        return False

def ftp_folder_exists(ftp_manager: FTPManager, folder_path: str) -> bool:
    """Prüft, ob ein Ordner auf dem FTP-Server existiert"""
    try:
        with ftp_manager.get_connection() as ftp:
            ftp.cwd(folder_path)
        return True
    except ftplib.error_perm as e:
        if '550' in str(e):
            return False
        else:
            xbmc.log(f"FTP error checking folder: {str(e)}", xbmc.LOGERROR)
            return False
    except Exception as e:
        xbmc.log(f"Unexpected error checking folder: {str(e)}", xbmc.LOGERROR)
        return Falsedef sync_standard_favourites(ftp_manager: FTPManager) -> bool:
    """Synchronisiert Standard-Favoriten"""
    try:
        if config.is_main_system:
            return ftp_upload(ftp_manager, config.local_favourites, config.ftp_path)
        else:
            return ftp_download(ftp_manager, config.ftp_path, config.local_favourites)
    except Exception as e:
        xbmc.log(f"Error syncing standard favourites: {str(e)}", xbmc.LOGERROR)
        return False

def sync_static_favourites(ftp_manager: FTPManager) -> bool:
    """Synchronisiert statische Favoriten"""
    success = True
    try:
        for folder in config.static_folders:
            if not folder:  # Überspringe leere Ordner
                continue
                
            local_static_path = os.path.join(config.super_favourites_path, folder, 'favourites.xml')
            remote_static_path = f"/{config.ftp_base_path}/auto_fav_sync/{config.custom_folder}/{folder}/favourites.xml"
            
            if config.is_main_system:
                if not ftp_upload(ftp_manager, local_static_path, remote_static_path):
                    success = False
            else:
                if not ftp_download(ftp_manager, remote_static_path, local_static_path):
                    success = False
                    
                # Überschreiben falls aktiviert
                if config.overwrite_static and folder == config.specific_custom_folder:
                    specific_remote_static_path = f"/{config.ftp_base_path}/auto_fav_sync/{config.specific_custom_folder}/favourites.xml"
                    if not ftp_download(ftp_manager, specific_remote_static_path, local_static_path):
                        success = False
                        
        return success
    except Exception as e:
        xbmc.log(f"Error syncing static favourites: {str(e)}", xbmc.LOGERROR)
        return Falsedef clear_texture_cache() -> bool:
    """Löscht den Textur-Cache"""
    try:
        db_path = xbmcvfs.translatePath('special://database/Textures13.db')
        if not os.path.exists(db_path):
            xbmc.log("Texture database not found", xbmc.LOGWARNING)
            return False
            
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM texture")
            cursor.execute("DELETE FROM sizes")
            conn.commit()
        xbmc.log("Textures cache cleared successfully", xbmc.LOGINFO)
        return True
    except Exception as e:
        xbmc.log(f"Error clearing texture cache: {str(e)}", xbmc.LOGERROR)
        return Falsedef download_random_image() -> bool:
    """Lädt ein zufälliges Bild herunter und speichert es"""
    if not config.image_list_url or not config.enable_image_rotation:
        xbmc.log("Image rotation disabled or no URL provided", xbmc.LOGINFO)
        return False

    try:
        with urllib.request.urlopen(config.image_list_url, timeout=30) as response:
            content = response.read().decode('utf-8')
            image_urls = re.findall(r'\[img\](.*?)\[/img\]', content)
            if not image_urls:
                xbmc.log("No image URLs found in the list", xbmc.LOGERROR)
                return False
            random_image_url = random.choice(image_urls)
            xbmc.log(f"Selected random image URL: {random_image_url}", xbmc.LOGINFO)
            with urllib.request.urlopen(random_image_url, timeout=30) as img_response:
                img_data = img_response.read()
                
                # Speichere das Bild an beiden Orten
                for path in [config.local_image_path, config.addon_image_path]:
                    try:
                        os.makedirs(os.path.dirname(path), exist_ok=True)
                        with open(path, 'wb') as f:
                            f.write(img_data)
                        xbmc.log(f"Saved image to {path}", xbmc.LOGINFO)
                    except Exception as e:
                        xbmc.log(f"Error saving image to {path}: {str(e)}", xbmc.LOGERROR)
                        
        show_notification(30032, 5000)  # Zufallsbild heruntergeladen

        # Cache leeren und UI aktualisieren
        if clear_texture_cache():
            xbmc.executebuiltin('ReloadSkin()')
            xbmc.executebuiltin('Container.Refresh()')

    except urllib.error.HTTPError as e:
        xbmc.log(f"HTTPError downloading image: {e.code} - {e.reason}", xbmc.LOGERROR)
        try:
            xbmc.log(f"Response: {e.read().decode()}", xbmc.LOGERROR)
        except:
            pass
    except urllib.error.URLError as e:
        xbmc.log(f"URLError downloading image: {e.reason}", xbmc.LOGERROR)
    except Exception as e:
        xbmc.log(f"Failed to download random image: {str(e)}", xbmc.LOGERROR)
  def sync_favourites() -> bool:
    """Hauptfunktion für die Synchronisation der Favoriten"""
    try:
        if not config.custom_folder:
            show_notification(30023, 5000)  # Ein benutzerdefinierter Ordnername ist erforderlich
            return False

        # Erstelle FTP-Manager
        ftp_manager = FTPManager(config.ftp_host, config.ftp_user, config.ftp_pass)
        
        try:
            # Prüfe, ob der Ordner existiert
            if not ftp_folder_exists(ftp_manager, f"/{config.ftp_base_path}/auto_fav_sync/{config.custom_folder}"):
                show_notification(30024, 5000, folder=config.custom_folder)  # Benutzerdefinierter Ordner nicht gefunden
                return False

            # Synchronisiere Favoriten
            success = True
            if not sync_standard_favourites(ftp_manager):
                success = False
            if not sync_static_favourites(ftp_manager):
                success = False
                
            if success:
                show_notification(30028, 5000)  # Synchronisation abgeschlossen
                
            return success
            
        finally:
            ftp_manager.close()
            
    except Exception as e:
        xbmc.log(f"Error in sync_favourites: {str(e)}", xbmc.LOGERROR)
        return False

# Hauptausführung
if config.enabled:
    try:
        xbmc.log("Auto FTP Sync started", xbmc.LOGINFO)
        
        # Synchronisiere Favoriten
        if sync_favourites():
            xbmc.log("Favourites sync completed successfully", xbmc.LOGINFO)
        else:
            xbmc.log("Favourites sync failed", xbmc.LOGERROR)
            
        # Lade zufälliges Bild herunter
        if download_random_image():
            xbmc.log("Random image download completed successfully", xbmc.LOGINFO)
        else:
            xbmc.log("Random image download failed", xbmc.LOGWARNING)
            
        xbmc.log("Auto FTP Sync completed", xbmc.LOGINFO)
        
    except Exception as e:
        xbmc.log(f"Critical error in Auto FTP Sync: {str(e)}", xbmc.LOGERROR)
else:
    xbmc.log("Auto FTP Sync is disabled", xbmc.LOGINFO)
