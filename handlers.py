import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

import config
from utils import save_log_group, load_log_group

logger = logging.getLogger(__name__)
router = Router()

def is_admin(user_id: int) -> bool:
    """Проверяет, входит ли пользователь в список ADMINS."""
    return user_id in config.ADMINS

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Используй /help."
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    text = (
        "Список команд:\n"
        "/start — приветствие\n"
        "/help — показать это сообщение\n"
        "/bind — привязать текущий чат как лог-группу (только для админов)\n"
        "/get_info — узнать chat_id и message_thread_id (в форуме)\n"
    )
    await message.answer(text)

@router.message(Command("bind"))
async def cmd_bind(message: Message):
    """
    Привязывает текущий чат как лог-группу.
    Доступно только для админов.
    """
    if not message.from_user or not is_admin(message.from_user.id):
        await message.answer("У вас нет прав для выполнения этой команды.")
        return

    chat_id = message.chat.id
    save_log_group(chat_id)
    await message.answer(f"Лог-группа привязана! ID: {chat_id}")
    logger.info(f"Лог-группа привязана админом {message.from_user.id} => {chat_id}")

@router.message(Command("get_info"))
async def cmd_get_info(message: Message):
    """
    Показывает chat_id и message_thread_id (если есть),
    чтобы понять, где находимся.
    """
    await message.answer(
        f"chat_id: {message.chat.id}\n"
        f"message_thread_id: {message.message_thread_id}"
    )

#
# Логика пересылки сообщений
#
@router.message(F.chat.id == config.SOURCE_CHAT_ID)
async def forward_leads(message: Message):
    """
    Пересылает сообщения, если:
    1. Пришли из SOURCE_CHAT_ID,
    2. Если SOURCE_TOPIC_ID != 0, то message_thread_id совпадает,
    3. Лог-группа привязана.
    """
    # Проверка темы (forum topic)
    if config.SOURCE_TOPIC_ID != 0:
        if message.message_thread_id != config.SOURCE_TOPIC_ID:
            return

    log_group_id = load_log_group()
    if not log_group_id:
        # Лог-группа не привязана — пересылать некуда
        return

    try:
        await message.forward(log_group_id)
        logger.info(
            f"Переслал сообщение {message.message_id} "
            f"из {config.SOURCE_CHAT_ID} в {log_group_id}"
        )
    except Exception as e:
        logger.error(f"Ошибка при пересылке: {e}")
