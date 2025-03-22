import os
import logging
from config import LOG_GROUP_FILE

logger = logging.getLogger(__name__)

def save_log_group(chat_id: int):
    """Сохраняет ID лог-группы в файл."""
    try:
        with open(LOG_GROUP_FILE, "w", encoding="utf-8") as f:
            f.write(str(chat_id))
        logger.info(f"Сохранил ID лог-группы {chat_id} в {LOG_GROUP_FILE}")
    except Exception as e:
        logger.error(f"Ошибка при сохранении ID лог-группы: {e}")

def load_log_group():
    """Загружает ID лог-группы из файла (или None, если нет файла)."""
    if not os.path.exists(LOG_GROUP_FILE):
        logger.warning(f"Файл {LOG_GROUP_FILE} не найден. Лог-группа не привязана.")
        return None

    try:
        with open(LOG_GROUP_FILE, "r", encoding="utf-8") as f:
            return int(f.read().strip())
    except Exception as e:
        logger.error(f"Ошибка при загрузке ID лог-группы: {e}")
        return None
