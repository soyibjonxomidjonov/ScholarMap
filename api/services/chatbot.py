"""
ScholarMap LangChain + Groq Chatbot Service
=============================================
Groq (ultra-tez inference) + LangChain Groq yordamida yaratilgan aqlli chatbot.
- Llama-3.3-70b modeli (bepul va eng tez)
- 6 ta API key — limit tugaganda avtomatik navbatdagiga o'tadi
- Bazadagi universitetlar va grantlar haqida savollarga javob beradi
- Har bir foydalanuvchi uchun alohida session xotirasi (thread-safe)

Faqat langchain-groq va langchain-core ishlatiladi — qo'shimcha paket shart emas.
"""
import os
import logging
import threading
from typing import List, Dict

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

load_dotenv()
logger = logging.getLogger(__name__)


# ─── Minimal in-memory chat history ──────────────────────────────────────────
class InMemoryChatHistory(BaseChatMessageHistory):
    """
    Oddiy, yengil in-memory suhbat tarixi.
    langchain_community'ga bog'liq emas.
    """
    def __init__(self):
        self._messages: List[BaseMessage] = []

    @property
    def messages(self) -> List[BaseMessage]:
        return self._messages

    def add_message(self, message: BaseMessage) -> None:
        self._messages.append(message)

    def clear(self) -> None:
        self._messages.clear()


# ─── Session store (thread-safe) ─────────────────────────────────────────────
_session_store: Dict[str, InMemoryChatHistory] = {}
_session_lock = threading.Lock()


def _get_session_history(session_id: str) -> InMemoryChatHistory:
    """Session ID bo'yicha suhbat tarixini olish yoki yangi yaratish."""
    with _session_lock:
        if session_id not in _session_store:
            _session_store[session_id] = InMemoryChatHistory()
        return _session_store[session_id]


def chatbot_clear_history(session_id: str) -> None:
    """Foydalanuvchi sessiyasini tozalash."""
    with _session_lock:
        if session_id in _session_store:
            del _session_store[session_id]
    logger.info(f"Session tozalandi: {session_id}")


def get_history_messages(session_id: str) -> List[Dict]:
    """Suhbat tarixini JSON-ready formatda qaytarish."""
    history = _get_session_history(session_id)
    result = []
    for msg in history.messages:
        if isinstance(msg, HumanMessage):
            role = "user"
        elif isinstance(msg, AIMessage):
            role = "assistant"
        else:
            role = "system"
        result.append({"role": role, "content": msg.content})
    return result


# ─── Groq API Key Rotation (thread-safe) ─────────────────────────────────────
_GROQ_KEYS: List[str] = [
    k for k in [
        os.environ.get("GROQ_API_KEY"),
        os.environ.get("GROQ_API_KEY_2"),
        os.environ.get("GROQ_API_KEY_3"),
        os.environ.get("GROQ_API_KEY_4"),
        os.environ.get("GROQ_API_KEY_5"),
        os.environ.get("GROQ_API_KEY_6"),
    ] if k
]

_key_index = 0
_key_lock = threading.Lock()
GROQ_MODEL = "qwen/qwen3.8-27b"


def _current_key() -> str:
    with _key_lock:
        if not _GROQ_KEYS:
            raise RuntimeError(
                "Hech qanday GROQ_API_KEY topilmadi. "
                "Iltimos .env faylida GROQ_API_KEY=gsk_... mavjudligini tekshiring."
            )
        return _GROQ_KEYS[_key_index]


def _rotate_key() -> bool:
    global _key_index
    with _key_lock:
        next_idx = _key_index + 1
        if next_idx >= len(_GROQ_KEYS):
            logger.error("Barcha Groq API key limitlari tugadi!")
            return False
        _key_index = next_idx
        logger.warning(f"Groq API key {_key_index + 1}-ga o'tildi.")
        return True


# ─── Prompt va kontekst ───────────────────────────────────────────────────────

def _build_universities_context(universities: List[Dict]) -> str:
    if not universities:
        return "Hozircha ma'lumotlar bazasida universitetlar mavjud emas."

    lines = ["MAVJUD UNIVERSITETLAR VA GRANT DASTURLARI:\n"]
    for i, u in enumerate(universities[:80], 1):
        lines.append(
            f"{i}. {u.get('university_name', 'N/A')} | {u.get('state', 'N/A')}\n"
            f"   Daraja: {u.get('level', 'N/A')} | Yo'nalish: {u.get('directions', 'N/A')}\n"
            f"   Grant: {u.get('grant_name', 'N/A')} — {u.get('grand_amount', 'N/A')} ({u.get('grand_turi', 'N/A')})\n"
            f"   Qabul: {u.get('reception_start', 'N/A')} dan {u.get('reception_end', 'N/A')} gacha\n"
        )
    return "\n".join(lines)


SYSTEM_TEMPLATE = (
    "Siz ScholarMap platformasining aqlli AI yordamchisisiz.\n\n"
    "Asosiy vazifalaringiz:\n"
    "1. Xorijda o'qish imkoniyatlari haqida aniq va foydali maslahat berish\n"
    "2. Foydalanuvchi profili asosida eng mos universitetlarni tavsiya etish\n"
    "3. Grant ariza jarayoni, hujjatlar va muddat haqida yo'l ko'rsatish\n"
    "4. Har bir talaba muvaffaqiyatga erisha olishiga ishontirish\n\n"
    "Muloqot qoidalari:\n"
    "- Do'stona, iliq va professional bo'ling\n"
    "- Foydalanuvchi qaysi tilda yozsa, shu tilda javob bering (O'zbek, Rus, Ingliz)\n"
    "- Javoblar aniq, qisqa va amaliy bo'lsin\n"
    "- Markdown belgilari (**, ##, - kabi) ISHLATMANG — faqat oddiy matn\n"
    "- Noma'lum narsani bilmasangiz, ochiq tan oling\n\n"
    "{universities_context}\n\n"
    "Universitetni tavsiya qilayotganda nima uchun mos ekanini tushuntiring, "
    "qabul muddatlari va keyingi qadamlarni ham ayting."
)


def _build_chain(universities_context: str):
    llm = ChatGroq(
        model=GROQ_MODEL,
        api_key=_current_key(),
        temperature=0.65,
        max_tokens=2048,
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_TEMPLATE),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ])

    chain = prompt | llm

    return RunnableWithMessageHistory(
        chain,
        _get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )


# ─── Asosiy funksiya ──────────────────────────────────────────────────────────

def chatbot_respond(
    session_id: str,
    user_message: str,
    universities_data: List[Dict] = None,
) -> str:
    """
    Chatbot'ga so'rov yuborish va javob olish.

    Args:
        session_id       : Foydalanuvchi unikal identifikatori (masalan "user_42")
        user_message     : Foydalanuvchi xabari
        universities_data: DB'dan olingan universitetlar ro'yxati

    Returns:
        AI javobi (str)
    """
    universities_context = _build_universities_context(universities_data or [])
    max_retries = len(_GROQ_KEYS) if _GROQ_KEYS else 1

    for attempt in range(max_retries):
        try:
            chain = _build_chain(universities_context)
            response = chain.invoke(
                {
                    "input": user_message,
                    "universities_context": universities_context,
                },
                config={"configurable": {"session_id": session_id}},
            )
            return response.content if hasattr(response, "content") else str(response)

        except Exception as e:
            err = str(e).lower()
            if any(kw in err for kw in ["rate_limit", "429", "401", "quota", "exceeded"]):
                logger.warning(f"API limit (urinish {attempt + 1}): {e}")
                if not _rotate_key():
                    return "Kechirasiz, barcha AI limitlarimiz tugadi. Bir oz kuting."
                continue
            logger.exception(f"Chatbot xatolik (session={session_id}): {e}")
            raise RuntimeError(f"AI javob berishda xatolik: {e}") from e

    return "Kechirasiz, hozir muammo yuz berdi. Keyinroq urinib ko'ring."
