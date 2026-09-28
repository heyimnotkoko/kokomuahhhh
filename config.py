import base64
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DOWNLOADS_DIR = BASE_DIR / "downloads"
CACHE_DIR = BASE_DIR / "cache"
COOKIES_FILE = BASE_DIR / os.getenv("YTDLP_COOKIES_FILE", "cookies.txt")
DB_PATH = BASE_DIR / os.getenv("DB_PATH", "kromusic.db")


def _required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def _int_required(name: str) -> int:
    value = _required(name)
    try:
        return int(value)
    except ValueError as exc:
        raise RuntimeError(f"Environment variable {name} must be an integer.") from exc


def _int_list(value: str) -> list[int]:
    if not value.strip():
        return []
    result = []
    for item in value.replace(",", " ").split():
        try:
            result.append(int(item))
        except ValueError as exc:
            raise RuntimeError(f"SUDO_USERS contains an invalid Telegram user ID: {item}") from exc
    return result


API_ID = _int_required("API_ID")
API_HASH = _required("API_HASH")
BOT_TOKEN = _required("BOT_TOKEN")
OWNER_ID = _int_required("OWNER_ID")
# Optional: if empty, the owner can add the assistant account from the bot.
SESSION = os.getenv("SESSION", "").strip()

BOT_NAME = "KroMusic"
DEVELOPER_USERNAME = os.getenv("DEVELOPER_USERNAME", "krofullpower").lstrip("@")
DEVELOPER_CHANNEL = os.getenv("DEVELOPER_CHANNEL", "dlxfullpower").lstrip("@")

DURATION_LIMIT = int(os.getenv("DURATION_LIMIT", "90"))
PING_IMG = os.getenv("PING_IMG", "").strip()
START_IMG = os.getenv("START_IMG", "").strip()
FAILED = os.getenv("FAILED_IMG", "").strip()

SUPPORT_CHAT = os.getenv("SUPPORT_CHAT", f"https://t.me/{DEVELOPER_CHANNEL}").strip()
SUPPORT_CHANNEL = os.getenv("SUPPORT_CHANNEL", f"https://t.me/{DEVELOPER_CHANNEL}").strip()
SUDO_USERS = _int_list(os.getenv("SUDO_USERS", ""))
AUTO_JOIN_CHATS = [
    item.lstrip("@").strip()
    for item in os.getenv("AUTO_JOIN_CHATS", "").replace(",", " ").split()
    if item.strip()
]

YTDLP_COOKIES_B64 = os.getenv("YTDLP_COOKIES_B64", "").strip()
if YTDLP_COOKIES_B64:
    try:
        COOKIES_FILE.write_bytes(base64.b64decode(YTDLP_COOKIES_B64, validate=True))
        try:
            COOKIES_FILE.chmod(0o600)
        except OSError:
            pass
    except Exception as exc:
        raise RuntimeError("YTDLP_COOKIES_B64 is not valid base64.") from exc

DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)
