from aiogram import Router, F
from aiogram.types import Message

from bot.services.ai_service import ask
from bot.database import get_chat_history, add_chat_message

router = Router()


@router.message(F.text)
async def handle_text(message: Message):
    await message.bot.send_chat_action(message.chat.id, "typing")

    history_records = await get_chat_history(message.from_user.id, limit=10)
    history = [{"role": r.role, "content": r.content} for r in history_records]

    answer = await ask(message.text, history)

    await add_chat_message(message.from_user.id, "user", message.text)
    await add_chat_message(message.from_user.id, "assistant", answer)

    await message.answer(answer)
