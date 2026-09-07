from typing import List, Optional
from pydantic import BaseModel, Field

class QuestionOption(BaseModel):
    key: str = Field(..., description="A, B, C, hoặc D")
    text: str = Field(..., description="Nội dung lựa chọn")

class QuizQuestion(BaseModel):
    id: str
    age: int
    age_label: str
    question: str
    options: List[QuestionOption]
    answer: str
    explanation: str
    fun_fact: Optional[str] = None
    reward_correct: int = 50000
    reward_wrong: int = 5000

class GenerateQuizRequest(BaseModel):
    age: int = Field(..., ge=3, le=120, description="Độ tuổi cụ thể từ U3 đến 60+")

class SubmitAnswerRequest(BaseModel):
    question_id: str
    age: int
    selected_option: str
    correct_answer: str
    explanation: Optional[str] = ""

class SubmitAnswerResponse(BaseModel):
    is_correct: bool
    correct_answer: str
    selected_option: str
    explanation: str
    reward_amount: int  # 50000 if correct, 5000 if wrong
    message: str
    congratulation_title: str

class ExactAgeItem(BaseModel):
    age: int
    label: str
    sublabel: str
    icon: str
    color: str
