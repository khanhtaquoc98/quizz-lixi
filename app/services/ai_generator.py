import json
import re
import uuid
import random
import logging
from collections import deque
from typing import Optional, Dict, Any, List
from groq import Groq

from app.config import settings
from app.models.quiz import QuizQuestion, QuestionOption
from app.services.question_bank import EXACT_AGES, get_age_info, get_fallback_question

logger = logging.getLogger("ai_generator")

# Topic seeds for guaranteed variety on every generation
TOPICS_BY_AGE = {
    "toddler": [
        "Đố thơ có vần điệu về con vật nuôi trong nhà",
        "Đố thơ về các loài chim líu lo bay lượn",
        "Đố vui về các loại quả ngọt mùa hè",
        "Đố về màu sắc cầu vồng và đồ chơi bé yêu",
        "Đố về xe đạp, xe buýt, máy bay, tàu hỏa",
        "Đố về các bạn cá, tôm, cua dưới nước",
        "Đố về đồ dùng quen thuộc trong nhà bé",
        "Đố về ông mặt trời, chị hằng, mưa và gió",
        "Đố thơ về bé ngoan rửa tay và đánh răng",
        "Đố về bông hoa cúc, hoa hồng, hoa đào xinh xắn"
    ],
    "school": [
        "Toán nhanh tính nhẩm đố mẹo thông minh",
        "Đố chữ Tiếng Việt, dấu câu và ghép từ dí dỏm",
        "Câu đố dân gian Việt Nam truyền thống",
        "Thế giới côn trùng và muông thú kỳ thú",
        "Kỹ năng sống và thói quen sinh hoạt hàng ngày",
        "Địa danh sông núi danh thắng Việt Nam",
        "Đố mẹo suy luận nhanh không lối mòn",
        "Đồ dùng học tập và những câu chuyện trường lớp vui",
        "Hiện tượng tự nhiên sấm chớp, mây mưa, cầu vồng"
    ],
    "teen": [
        "Khoa học tự nhiên & bí ẩn Hệ Mặt Trời",
        "Hiện tượng vật lý - hóa học kỳ thú trong đời sống",
        "Danh nhân hào kiệt và lịch sử Việt Nam",
        "Toán logic suy luận IQ bất ngờ",
        "Thành ngữ tục ngữ và tinh hoa văn hóa",
        "Địa lý thế giới và những kỳ quan thiên nhiên",
        "Bí mật cơ thể người và tiến hóa sinh học",
        "Công nghệ số và những phát minh làm thay đổi thế giới"
    ],
    "adult": [
        "Nghịch lý logic và tư duy phản biện sắc bén",
        "Tâm lý học hành vi và kinh tế học ứng dụng",
        "Triết học vui và nghệ thuật ứng xử cuộc sống",
        "Đố mẹo tình huống thực tiễn và chỉ số EQ",
        "Khoa học công nghệ và bước tiến của trí tuệ nhân tạo",
        "Văn hóa, lịch sử và các nền văn minh nhân loại",
        "Ca dao tục ngữ và trí tuệ thâm sâu dân gian",
        "Sức khỏe, dinh dưỡng và khoa học cân bằng cuộc sống",
        "Quản lý tài chính cá nhân và tư duy chiến lược",
        "Nghệ thuật, điện ảnh và văn học kinh điển"
    ]
}

# Keep history of recently shown questions to NEVER repeat
recent_questions = deque(maxlen=80)

class AIGeneratorService:
    def __init__(self):
        self.primary_api_key = settings.GROQ_API_KEY
        self.backup_api_key = settings.GROQ_API_KEY_CHAT_BOT
        self.model_name = settings.GROQ_MODEL or "qwen/qwen3.8-27b"
        
        self.primary_client = Groq(api_key=self.primary_api_key) if self.primary_api_key else None
        self.backup_client = Groq(api_key=self.backup_api_key) if self.backup_api_key else None

    def _get_active_client(self, use_backup: bool = False) -> Optional[Groq]:
        if use_backup and self.backup_client:
            return self.backup_client
        if self.primary_client:
            return self.primary_client
        if self.backup_client:
            return self.backup_client
        return None

    def _build_prompt(self, age: int, age_info: Dict[str, Any]) -> str:
        # Determine topic category pool
        if age <= 5:
            topic_pool = TOPICS_BY_AGE["toddler"]
            group_key = "toddler"
        elif age <= 10:
            topic_pool = TOPICS_BY_AGE["school"]
            group_key = "school"
        elif age <= 17:
            topic_pool = TOPICS_BY_AGE["teen"]
            group_key = "teen"
        else:
            topic_pool = TOPICS_BY_AGE["adult"]
            group_key = "adult"

        selected_topic = random.choice(topic_pool)
        seed_nonce = uuid.uuid4().hex[:6]

        # Specific prompt instructions per age bracket
        if age <= 5:
            tone = f"""
ĐỐI TƯỢNG: Bé {age_info['label']} ({age_info['sublabel']}).
- Chủ đề ngẫu nhiên BẮT BUỘC: '{selected_topic}'.
- Dạng câu: Câu thơ đố 4 câu có vần điệu ngân vang dễ thương HOẶC câu hỏi siêu ngộ nghĩnh.
- 4 đáp án A, B, C, D: Cực kỳ ngắn gọn (1-3 từ), KÈM EMOJI đáng yêu (ví dụ: 'Con Thỏ 🐰', 'Quả Cam 🍊').
- Lời giải thích: Khen ngợi bé ngọt ngào, dịu dàng."""
        elif age <= 10:
            tone = f"""
ĐỐI TƯỢNG: Học sinh {age_info['label']} ({age_info['sublabel']}).
- Chủ đề ngẫu nhiên BẮT BUỘC: '{selected_topic}'.
- Dạng câu: Câu đố mẹo, toán nhanh hoặc kiến thức tự nhiên, không cliché, tươi vui.
- 4 đáp án A, B, C, D: Ngắn gọn (dưới 6 từ mỗi đáp án).
- Lời giải thích: Vui vẻ, chỉ rõ mẹo hay hoặc kiến thức bổ ích."""
        elif age <= 17:
            tone = f"""
ĐỐI TƯỢNG: Học sinh {age_info['label']} ({age_info['sublabel']}).
- Chủ đề ngẫu nhiên BẮT BUỘC: '{selected_topic}'.
- Dạng câu: Thử thách tư duy phân tích, logic sắc bén, thông tin bất ngờ.
- 4 đáp án A, B, C, D: Chuẩn xác, súc tích (dưới 10 từ mỗi đáp án).
- Lời giải thích: Rõ ràng, thuyết phục, mở rộng hiểu biết."""
        elif age == 18:
            tone = f"""
ĐỐI TƯỢNG: Thanh niên & Sinh viên 18+ ({age_info['sublabel']}).
- Chủ đề ngẫu nhiên BẮT BUỘC: '{selected_topic}'.
- Dạng câu: Tư duy phản biện, nghịch lý logic, kinh tế học hành vi hoặc câu đố trí tuệ hiện đại.
- 4 đáp án A, B, C, D: Ngắn gọn (dưới 12 từ mỗi đáp án).
- Lời giải thích: Sâu sắc, súc tích."""
        elif age == 30:
            tone = f"""
ĐỐI TƯỢNG: Người trưởng thành 30+ ({age_info['sublabel']}).
- Chủ đề ngẫu nhiên BẮT BUỘC: '{selected_topic}'.
- Dạng câu: Đố vui trí tuệ về tư duy tài chính, tâm lý học, mẹo cuộc sống gia đình và sự nghiệp.
- 4 đáp án A, B, C, D: Ngắn gọn, thực tế."""
        elif age == 40:
            tone = f"""
ĐỐI TƯỢNG: Độ tuổi 40+ ({age_info['sublabel']}).
- Chủ đề ngẫu nhiên BẮT BUỘC: '{selected_topic}'.
- Dạng câu: Nghệ thuật sống, văn hóa lịch sử, sức khỏe thể chất & tinh thần, câu đố ứng xử sâu sắc.
- 4 đáp án A, B, C, D: Tinh tế, rõ ràng."""
        elif age == 50:
            tone = f"""
ĐỐI TƯỢNG: Độ tuổi 50+ ({age_info['sublabel']}).
- Chủ đề ngẫu nhiên BẮT BUỘC: '{selected_topic}'.
- Dạng câu: Ca dao tục ngữ thâm thúy, tinh hoa danh nhân, kiến thức bách khoa đời sống trường thọ.
- 4 đáp án A, B, C, D: Súc tích, đậm đà vốn sống."""
        else: # 60+
            tone = f"""
ĐỐI TƯỢNG: Độ tuổi 60+ ({age_info['sublabel']}).
- Chủ đề ngẫu nhiên BẮT BUỘC: '{selected_topic}'.
- Dạng câu: Minh triết phương Đông, y học cổ truyền và lối sống an lạc, kỷ niệm lịch sử thiêng liêng.
- 4 đáp án A, B, C, D: Trang trọng, súc tích, ý nghĩa."""

        prompt = f"""Bạn là Chuyên gia Đố Vui Hàng Đầu Việt Nam của chương trình 'Ai Được Lì Xì'.
Nhiệm vụ: Sáng tạo 1 câu đố trắc nghiệm 4 lựa chọn (A, B, C, D) hoàn toàn ĐỘC BẢN, MỚI LẠ dành cho người chơi {age_info['label']}.

{tone}

QUY TẮC BẮT BUỘC:
1. TUYỆT ĐỐI KHÔNG lặp lại các câu đố cũ phổ biến (như 'con gì biết bay nhưng không cánh'). Hãy sáng tạo câu đố mới mẻ.
2. Mã phiên ngẫu nhiên (Session ID): {seed_nonce}.
3. Đúng 4 lựa chọn A, B, C, D ngắn gọn, không giải thích trong options.
4. Chỉ có DUY NHẤT 1 đáp án đúng. `answer` là một trong các chữ cái: "A", "B", "C", hoặc "D".
5. Định dạng trả về BẮT BUỘC là JSON duy nhất:
{{
  "question": "Nội dung câu hỏi hoặc câu thơ đố",
  "options": [
    {{"key": "A", "text": "Lựa chọn A"}},
    {{"key": "B", "text": "Lựa chọn B"}},
    {{"key": "C", "text": "Lựa chọn C"}},
    {{"key": "D", "text": "Lựa chọn D"}}
  ],
  "answer": "A",
  "explanation": "Lời giải thích ngắn gọn, hay và khen ngợi người chơi",
  "fun_fact": "Một điều thú vị mở rộng ngắn gọn"
}}
Chỉ xuất ra JSON thuần túy, không thêm bất kỳ văn bản nào bên ngoài.
"""
        return prompt

    def _extract_json(self, raw_text: str) -> Optional[Dict[str, Any]]:
        raw_text = raw_text.strip()
        if raw_text.startswith("```"):
            raw_text = re.sub(r"^```(?:json)?\s*", "", raw_text)
            raw_text = re.sub(r"\s*```$", "", raw_text)
        try:
            return json.loads(raw_text)
        except Exception:
            pass
        match = re.search(r"\{[\s\S]*\}", raw_text)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                pass
        return None

    def _sanitize_options(self, options_data: Any) -> List[QuestionOption]:
        clean_opts: List[QuestionOption] = []
        if isinstance(options_data, list):
            for i, opt in enumerate(options_data[:4]):
                key = ["A", "B", "C", "D"][i]
                if isinstance(opt, dict):
                    k = str(opt.get("key", key)).strip().upper()
                    if k not in ["A", "B", "C", "D"]:
                        k = key
                    t = str(opt.get("text", "")).strip()
                    t = re.sub(r"^[A-D][.:\-–]\s*", "", t)
                    clean_opts.append(QuestionOption(key=k, text=t))
                elif isinstance(opt, str):
                    t = opt.strip()
                    t = re.sub(r"^[A-D][.:\-–]\s*", "", t)
                    clean_opts.append(QuestionOption(key=key, text=t))
        while len(clean_opts) < 4:
            idx = len(clean_opts)
            key = ["A", "B", "C", "D"][idx]
            clean_opts.append(QuestionOption(key=key, text=f"Lựa chọn {key}"))
        return clean_opts[:4]

    async def generate_quiz(self, age: int) -> QuizQuestion:
        info = get_age_info(age)
        age_label = f"{info['label']} ({info['sublabel']})"

        clients = [
            ("primary", self._get_active_client(use_backup=False)),
            ("backup", self._get_active_client(use_backup=True)),
        ]

        # Try up to 2 attempts with AI to ensure freshness
        for attempt in range(2):
            prompt = self._build_prompt(age=age, age_info=info)

            for client_name, client in clients:
                if not client:
                    continue
                try:
                    logger.info(f"Generating quiz for {info['label']} via AI ({client_name}, attempt {attempt+1})...")
                    response = client.chat.completions.create(
                        model=self.model_name,
                        messages=[
                            {
                                "role": "system",
                                "content": "Bạn là chuyên gia đố vui hàng đầu của game 'Ai Được Lì Xì'. Bạn luôn tạo ra câu hỏi hoàn toàn mới lạ và xuất ra JSON thuần túy theo yêu cầu."
                            },
                            {"role": "user", "content": prompt}
                        ],
                        response_format={"type": "json_object"},
                        temperature=0.88,
                        max_tokens=600,
                    )
                    data = self._extract_json(response.choices[0].message.content)
                    if data and "question" in data and "options" in data and "answer" in data:
                        q_text = str(data["question"]).strip()
                        
                        # Deduplication check: if question was seen in last 80 queries, retry
                        q_hash = q_text[:40].lower()
                        if q_hash in recent_questions and attempt == 0:
                            logger.info(f"Duplicate question detected: '{q_text[:30]}...'. Regenerating...")
                            continue
                        
                        recent_questions.append(q_hash)

                        raw_ans = str(data.get("answer", "A")).strip().upper()
                        ans_match = re.search(r"[A-D]", raw_ans)
                        valid_ans = ans_match.group(0) if ans_match else "A"
                        options = self._sanitize_options(data.get("options"))

                        return QuizQuestion(
                            id=str(uuid.uuid4()),
                            age=age,
                            age_label=age_label,
                            question=q_text,
                            options=options,
                            answer=valid_ans,
                            explanation=str(data.get("explanation", "Chúc mừng bạn đã trả lời chính xác!")).strip(),
                            fun_fact=data.get("fun_fact"),
                            reward_correct=50000,
                            reward_wrong=5000
                        )
                except Exception as e:
                    logger.warning(f"AI generation error ({client_name}): {e}")

        # Fallback to local question bank (ensuring unseen question)
        logger.info(f"Using rich fallback question for age {age}")
        fallback = get_fallback_question(age)
        options = [QuestionOption(key=o["key"], text=o["text"]) for o in fallback["options"]]
        return QuizQuestion(
            id=str(uuid.uuid4()),
            age=age,
            age_label=age_label,
            question=fallback["question"],
            options=options,
            answer=fallback["answer"],
            explanation=fallback["explanation"],
            fun_fact=fallback.get("fun_fact"),
            reward_correct=50000,
            reward_wrong=5000
        )

ai_service = AIGeneratorService()
