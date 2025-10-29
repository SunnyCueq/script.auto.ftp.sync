import os
import xbmc
import xbmcvfs
from contextlib import contextmanager


class VFSManager:
    """Connection-like Manager, der Kodi VFS-URLs (ftp/sftp/smb) über xbmcvfs nutzt.

    Diese Klasse spiegelt das Interface der bestehenden ConnectionManager-Unterklassen,
    nutzt intern jedoch ausschließlich Kodi-VFS (kein paramiko/smbclient nötig).
    """

    def __init__(self, protocol: str, host: str, user: str, password: str, base_path: str = "", port: int | None = None, share: str | None = None):
        self.protocol = protocol.lower().strip()  # "ftp", "sftp", "smb"
        self.host = host or ""
        self.user = user or ""
        self.password = password or ""
        self.base_path = base_path.strip("/") if base_path else ""
        self.port = port
        self.share = share.strip("/\\") if share else None

    @contextmanager
    def get_connection(self):
        """Dummy-Context, um kompatibel zum bestehenden Interface zu bleiben."""
        yield None

    def close(self):
        return None

    # Public API – kompatibel zu ConnectionManager
    def upload_file(self, local_path: str, remote_path: str) -> bool:
        try:
            src = xbmcvfs.translatePath(local_path) if local_path.startswith("special://") else local_path
            dst = self._build_remote_url(remote_path)
            self._ensure_remote_dirs(dst)
            ok = xbmcvfs.copy(src, dst)
            if ok:
                xbmc.log(f"VFS upload OK: {src} -> {dst}", xbmc.LOGINFO)
            else:
                xbmc.log(f"VFS upload FAILED: {src} -> {dst}", xbmc.LOGERROR)
            return bool(ok)
        except Exception as e:
            xbmc.log(f"VFS upload error: {str(e)}", xbmc.LOGERROR)
            return False

    def download_file(self, remote_path: str, local_path: str) -> bool:
        try:
            src = self._build_remote_url(remote_path)
            dst = xbmcvfs.translatePath(local_path) if local_path.startswith("special://") else local_path
            # Lokalen Ordner sicherstellen
            local_dir = os.path.dirname(dst)
            if local_dir and not xbmcvfs.exists(local_dir):
                xbmcvfs.mkdirs(local_dir)
            ok = xbmcvfs.copy(src, dst)
            if ok:
                xbmc.log(f"VFS download OK: {src} -> {dst}", xbmc.LOGINFO)
            else:
                xbmc.log(f"VFS download FAILED: {src} -> {dst}", xbmc.LOGERROR)
            return bool(ok)
        except Exception as e:
            xbmc.log(f"VFS download error: {str(e)}", xbmc.LOGERROR)
            return False

    def folder_exists(self, folder_path: str) -> bool:
        try:
            url = self._build_remote_url(folder_path, as_dir=True)
            exists = xbmcvfs.exists(url)
            return bool(exists)
        except Exception as e:
            xbmc.log(f"VFS folder_exists error: {str(e)}", xbmc.LOGERROR)
            return False

    # Internals
    def _build_remote_url(self, remote_path: str, as_dir: bool = False) -> str:
        remote_path = remote_path.replace("\\", "/")
        remote_path = remote_path.lstrip("/")

        # FTP/SFTP: scheme://user:pass@host[:port]/path
        # SMB: smb://user:pass@host/share/path
        auth = ""
        if self.user or self.password:
            auth = f"{self.user}:{self.password}@"

        if self.protocol == "smb":
            share_part = f"/{self.share}" if self.share else ""
            path_part = f"/{self.base_path}" if self.base_path else ""
            full = f"smb://{auth}{self.host}{share_part}{path_part}/{remote_path}"
        else:
            port_part = f":{self.port}" if self.port else ""
            path_part = f"/{self.base_path}" if self.base_path else ""
            full = f"{self.protocol}://{auth}{self.host}{port_part}{path_part}/{remote_path}"

        # Falls als Ordner angefragt, sicherstellen, dass ein trailing slash vorhanden ist
        if as_dir and not full.endswith("/"):
            full = full + "/"
        return full

    def _ensure_remote_dirs(self, remote_url: str) -> None:
        try:
            # xbmcvfs.mkdirs akzeptiert Pfade/URLs; wir entfernen den Dateinamen
            url_dir = remote_url
            if "/" in remote_url:
                url_dir = remote_url.rsplit("/", 1)[0] + "/"
            if not xbmcvfs.exists(url_dir):
                xbmcvfs.mkdirs(url_dir)
        except Exception as e:
            xbmc.log(f"VFS ensure dirs error: {str(e)}", xbmc.LOGERROR)


