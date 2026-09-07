import logging
from typing import Optional
import httpx
from app.config import settings

logger = logging.getLogger("notifier")

class TelegramNotifier:
    def __init__(self):
        self.bot_token = settings.TELEGRAM_BOT_TOKEN
        self.chat_id = settings.NOTI_CHAT_ID
        self.noti_topic_id = settings.NOTI_TOPIC_ID
        self.summary_topic_id = settings.SUMMARY_TOPIC_ID

    async def send_message(
        self,
        text: str,
        topic_id: Optional[str] = None,
        parse_mode: str = "HTML"
    ) -> bool:
        if not self.bot_token:
            logger.info(f"[TELEGRAM SIMULATION] ChatID={self.chat_id} TopicID={topic_id}: {text}")
            return True

        target_topic = topic_id or self.noti_topic_id
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": parse_mode
        }
        if target_topic:
            payload["message_thread_id"] = int(target_topic)

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(url, json=payload)
                if res.status_code == 200:
                    logger.info("Telegram notification sent successfully.")
                    return True
                else:
                    logger.warning(f"Telegram API response {res.status_code}: {res.text}")
                    return False
        except Exception as e:
            logger.error(f"Failed to send Telegram notification: {e}")
            return False

    async def send_congratulation_notice(self, player_name: str, age: int, tier_title: str, prize: int, question: str):
        message = (
            f"🎉 <b>AI ĐƯỢC LÌ XÌ - CHÚC MỪNG CHIẾN THẮNG!</b> 🧧\n\n"
            f"👤 Người chơi: <b>{player_name}</b> ({age} tuổi - {tier_title})\n"
            f"🎁 Thưởng lì xì: <b>+{prize:,} VNĐ</b>\n"
            f"❓ Câu hỏi vừa giải: <i>{question[:100]}...</i>\n"
            f"✨ Xuất sắc vượt qua thử thách trí tuệ AI!"
        )
        return await self.send_message(message, topic_id=self.noti_topic_id)

notifier = TelegramNotifier()
