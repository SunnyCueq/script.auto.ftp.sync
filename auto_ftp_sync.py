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
STATIC_FOLDERS = ADDON.getSettingString('static_folders').split(',')
ENABLE_IMAGE_ROTATION = ADDON.getSettingBool('enable_image_rotation')

# Mehrsprachigkeit
LANGUAGE = ADDON.getLocalizedString

# Pfad zum Icon
ICON_PATH = os.path.join(ADDON.getAddonInfo('path'), 'resources', 'images', 'icon.png')

def show_notification(message_id, duration=5000, **kwargs):
    message = LANGUAGE(message_id).format(**kwargs)
    xbmc.executebuiltin(f'Notification({LANGUAGE(30001)}, {message}, {duration}, {ICON_PATH})')
    time.sleep(duration / 1000)  # Warte, bis die Benachrichtigung abgeschlossen ist

def ftp_upload(local_path, remote_path):
    try:
        with ftplib.FTP(FTP_HOST) as ftp:
            ftp.login(FTP_USER, FTP_PASS)
            with open(local_path, 'rb') as file:
                ftp.storbinary(f'STOR {remote_path}', file)
        return True
    except Exception as e:
        xbmc.log(f"FTP upload failed: {str(e)}", xbmc.LOGERROR)
        return False

def ftp_download(remote_path, local_path):
    try:
        with ftplib.FTP(FTP_HOST) as ftp:
            ftp.login(FTP_USER, FTP_PASS)
            with open(local_path, 'wb') as file:
                ftp.retrbinary(f'RETR {remote_path}', file.write)
        return True
    except Exception as e:
        xbmc.log(f"FTP download failed: {str(e)}", xbmc.LOGERROR)
        return False

def ftp_folder_exists(folder_path):
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

def sync_standard_favourites():
    if IS_MAIN_SYSTEM:
        ftp_upload(LOCAL_FAVOURITES, FTP_PATH)
    else:
        ftp_download(FTP_PATH, LOCAL_FAVOURITES)

def sync_static_favourites():
    for folder in STATIC_FOLDERS:
        local_static_path = os.path.join(SUPER_FAVOURITES_PATH, folder, 'favourites.xml')
        remote_static_path = f"/{FTP_BASE_PATH}/auto_fav_sync/{CUSTOM_FOLDER}/{folder}/favourites.xml"
        if IS_MAIN_SYSTEM:
            ftp_upload(local_static_path, remote_static_path)
        else:
            ftp_download(remote_static_path, local_static_path)
            if OVERWRITE_STATIC and folder == SPECIFIC_CUSTOM_FOLDER:
                specific_remote_static_path = f"/{FTP_BASE_PATH}/auto_fav_sync/{SPECIFIC_CUSTOM_FOLDER}/favourites.xml"
                ftp_download(specific_remote_static_path, local_static_path)

def clear_texture_cache():
    db_path = xbmcvfs.translatePath('special://database/Textures13.db')
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM texture")
        cursor.execute("DELETE FROM sizes")
        conn.commit()
        conn.close()
        xbmc.log("Textures cache cleared", xbmc.LOGINFO)

def download_random_image():
    if not IMAGE_LIST_URL or not ENABLE_IMAGE_ROTATION:
        return False

    try:
        with urllib.request.urlopen(IMAGE_LIST_URL) as response:
            content = response.read().decode('utf-8')
            image_urls = re.findall(r'\[img\](.*?)\[/img\]', content)
            if not image_urls:
                xbmc.log("No image URLs found in the list", xbmc.LOGERROR)
                return False
            random_image_url = random.choice(image_urls)
            xbmc.log(f"Selected random image URL: {random_image_url}", xbmc.LOGINFO)
            with urllib.request.urlopen(random_image_url) as img_response:
                img_data = img_response.read()
                with open(LOCAL_IMAGE_PATH, 'wb') as f:
                    f.write(img_data)
                    xbmc.log(f"Saved image to {LOCAL_IMAGE_PATH}", xbmc.LOGINFO)
                with open(ADDON_IMAGE_PATH, 'wb') as f:
                    f.write(img_data)
                    xbmc.log(f"Saved image to {ADDON_IMAGE_PATH}", xbmc.LOGINFO)
        show_notification(30032, 5000)  # Zufallsbild heruntergeladen

        # Clear texture cache and refresh UI
        clear_texture_cache()
        xbmc.executebuiltin('ReloadSkin()')
        xbmc.executebuiltin('Container.Refresh()')

        return True
    except urllib.error.HTTPError as e:
        xbmc.log(f"HTTPError: {e.code} - {e.reason}", xbmc.LOGERROR)
        xbmc.log(f"Response: {e.read().decode()}", xbmc.LOGERROR)
    except urllib.error.URLError as e:
        xbmc.log(f"URLError: {e.reason}", xbmc.LOGERROR)
    except Exception as e:
        xbmc.log(f"Failed to download random image: {str(e)}", xbmc.LOGERROR)
    return False

def sync_favourites():
    if not CUSTOM_FOLDER:
        show_notification(30023, 5000)  # Ein benutzerdefinierter Ordnername ist erforderlich
        return

    if not ftp_folder_exists(f"/{FTP_BASE_PATH}/auto_fav_sync/{CUSTOM_FOLDER}"):
        show_notification(30024, 5000, folder=CUSTOM_FOLDER)  # Benutzerdefinierter Ordner nicht gefunden
        return

    sync_standard_favourites()
    sync_static_favourites()

if ENABLED:
    sync_favourites()
    download_random_image()
