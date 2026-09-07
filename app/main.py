import traceback
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, Response, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.config import settings
from app.models.quiz import (
    GenerateQuizRequest,
    QuizQuestion,
    SubmitAnswerRequest,
    SubmitAnswerResponse,
)
from app.services.question_bank import EXACT_AGES, get_age_info
from app.services.ai_generator import ai_service

app = FastAPI(
    title="Ai Được Lì Xì",
    description="Ứng dụng đố vui trí tuệ AI chọn theo tuổi cụ thể từ 3 tuổi đến Đại học, nhận lì xì 50k (đúng) hoặc 5k (sai).",
    version="2.0.0"
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    err_trace = traceback.format_exc()
    print(f"FASTAPI ERROR on {request.url.path}:\n{err_trace}")
    return PlainTextResponse(f"FastAPI Exception:\n{err_trace}", status_code=500)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def vercel_path_middleware(request: Request, call_next):
    try:
        forwarded_uri = request.headers.get("x-forwarded-uri") or request.headers.get("x-matched-path")
        if forwarded_uri and not forwarded_uri.endswith(".py"):
            request.scope["path"] = forwarded_uri.split("?")[0]
        else:
            path = request.scope.get("path", "")
            for prefix in ["/api/index.py", "/api/index", "/app/main.py"]:
                if path == prefix:
                    request.scope["path"] = "/"
                    break
                elif path.startswith(prefix + "/"):
                    request.scope["path"] = path[len(prefix):]
                    break
    except Exception as e:
        print("[vercel_path_middleware] error:", e)
    return await call_next(request)

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

@app.get("/api/index.py", response_class=HTMLResponse)
@app.get("/app/main.py", response_class=HTMLResponse)
async def vercel_fallback(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "Ai Được Lì Xì",
        "exact_ages": EXACT_AGES
    })

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "Ai Được Lì Xì",
        "exact_ages": EXACT_AGES
    })

@app.get("/api/ages")
async def get_ages():
    return {
        "success": True,
        "data": EXACT_AGES
    }

@app.post("/api/quiz/generate", response_model=QuizQuestion)
async def generate_quiz(req: GenerateQuizRequest):
    try:
        question = await ai_service.generate_quiz(age=req.age)
        return question
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi tạo câu hỏi: {str(e)}")

@app.post("/api/quiz/submit", response_model=SubmitAnswerResponse)
async def submit_answer(req: SubmitAnswerRequest):
    is_correct = (req.selected_option.strip().upper() == req.correct_answer.strip().upper())
    
    # User requirement: Lì xì mặc định 50k nếu đúng / 5k nếu sai
    reward = 50000 if is_correct else 5000
    
    if is_correct:
        title = "🎉 CHÚC MỪNG BẠN ĐÃ ĐÚNG! 🧧"
        msg = f"Xuất sắc! Bạn đã chọn đúng đáp án {req.correct_answer} và nhận được 50k Lì Xì!"
    else:
        title = "🌸 TIẾC QUÁ, CHƯA CHÍNH XÁC! 🧧"
        msg = f"Đáp án đúng là {req.correct_answer}. Bạn nhận được 5k An Ủi nhé!"

    return SubmitAnswerResponse(
        is_correct=is_correct,
        correct_answer=req.correct_answer,
        selected_option=req.selected_option,
        explanation=req.explanation or "",
        reward_amount=reward,
        message=msg,
        congratulation_title=title
    )

class TTSRequest(BaseModel):
    text: str

@app.post("/api/quiz/tts")
async def text_to_speech(req: TTSRequest):
    text = req.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text is required")
    try:
        import io
        from gtts import gTTS
        from fastapi.responses import Response
        fp = io.BytesIO()
        tts = gTTS(text=text, lang="vi", slow=False)
        tts.write_to_fp(fp)
        fp.seek(0)
        return Response(content=fp.read(), media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS error: {str(e)}")

