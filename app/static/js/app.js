/**
 * TÊN WEBAPP: AI ĐƯỢC LÌ XÌ
 * 3 MÀN HÌNH:
 * 1. Màn hình chọn tuổi (từ 3 tuổi đến Đại học, không gom nhóm, chủ đề tự do)
 * 2. Màn hình quizz (câu hỏi + 4 đáp án A, B, C, D)
 * 3. Màn hình chúc mừng (thưởng lì xì 50k nếu đúng / 5k nếu sai + nút quay lại)
 */

// Global State
const state = {
  currentAge: 3,
  currentQuestion: null,
  totalLixi: parseInt(localStorage.getItem('lixi_balance') || '0', 10),
  soundEnabled: localStorage.getItem('lixi_sound') !== 'false',
  isAnswered: false,
};

// -----------------------------------------------------------
// 1. SOUND EFFECTS (Web Audio API Synthesizer)
// -----------------------------------------------------------
let audioCtx = null;

function getAudioContext() {
  if (!audioCtx) {
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    if (AudioContextClass) audioCtx = new AudioContextClass();
  }
  if (audioCtx && audioCtx.state === 'suspended') {
    audioCtx.resume();
  }
  return audioCtx;
}

function playSound(type) {
  if (!state.soundEnabled) return;
  try {
    const ctx = getAudioContext();
    if (!ctx) return;
    const now = ctx.currentTime;

    if (type === 'click') {
      // Cheerful pop
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.frequency.setValueAtTime(650, now);
      osc.frequency.exponentialRampToValueAtTime(880, now + 0.08);
      gain.gain.setValueAtTime(0.15, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(now);
      osc.stop(now + 0.08);
    } else if (type === 'correct') {
      // Celebratory cheerful fanfare
      [523.25, 659.25, 783.99, 1046.50].forEach((freq, idx) => {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(freq, now + idx * 0.1);
        gain.gain.setValueAtTime(0.2, now + idx * 0.1);
        gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.1 + 0.35);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now + idx * 0.1);
        osc.stop(now + idx * 0.1 + 0.35);
      });
    } else if (type === 'wrong') {
      // Gentle boing
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(320, now);
      osc.frequency.exponentialRampToValueAtTime(180, now + 0.25);
      gain.gain.setValueAtTime(0.12, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.25);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(now);
      osc.stop(now + 0.25);
    }
  } catch (e) {
    console.warn('Audio error:', e);
  }
}

// -----------------------------------------------------------
// 2. SCREEN NAVIGATION (3 SCREENS)
// -----------------------------------------------------------
function showScreen(screenId) {
  document.querySelectorAll('.screen-container').forEach(el => {
    el.classList.remove('active');
  });
  const target = document.getElementById(screenId);
  if (target) {
    target.classList.add('active');
  }
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function showLoading(show, message = 'AI đang chuẩn bị câu đố...') {
  const overlay = document.getElementById('loading-overlay');
  const desc = document.getElementById('loading-desc');
  if (desc) desc.textContent = message;
  if (overlay) overlay.style.display = show ? 'flex' : 'none';
}

// -----------------------------------------------------------
// 3. INITIALIZATION
// -----------------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
  updateBalanceDisplay();
  initSoundToggle();
  initKeyboardNav();
  if ('speechSynthesis' in window) {
    window.speechSynthesis.getVoices();
    window.speechSynthesis.onvoiceschanged = () => {
      window.speechSynthesis.getVoices();
    };
  }
});

function updateBalanceDisplay() {
  const el = document.getElementById('lixi-balance-text');
  if (el) {
    el.textContent = `${state.totalLixi.toLocaleString('vi-VN')} đ`;
  }
}

function initSoundToggle() {
  const btn = document.getElementById('btn-sound-toggle');
  if (!btn) return;
  btn.textContent = state.soundEnabled ? '🔊' : '🔇';
  btn.addEventListener('click', () => {
    state.soundEnabled = !state.soundEnabled;
    localStorage.setItem('lixi_sound', state.soundEnabled);
    btn.textContent = state.soundEnabled ? '🔊' : '🔇';
    if (state.soundEnabled) playSound('click');
  });
}

// -----------------------------------------------------------
// 4. MÀN HÌNH 1 -> MÀN HÌNH 2: CHỌN ĐÚNG TUỔI & TẠO QUIZZ
// -----------------------------------------------------------
async function selectExactAge(age) {
  playSound('click');
  state.isAnswered = false;
  stopReadQuiz();
  if ('speechSynthesis' in window) {
    window.speechSynthesis.resume();
  }
  state.currentAge = parseInt(age, 10);
  
  // Wipe previous question content so the new question is always fresh
  const questionEl = document.getElementById('quiz-question-text');
  const optionsEl = document.getElementById('quiz-options-wrapper');
  if (questionEl) questionEl.textContent = 'Đang tải câu đố mới...';
  if (optionsEl) optionsEl.innerHTML = '';

  showLoading(true, 'Đang chuẩn bị câu đố mới cho bạn...');

  try {
    const res = await fetch('/api/quiz/generate?_t=' + Date.now(), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      cache: 'no-store',
      body: JSON.stringify({ age: state.currentAge })
    });

    if (!res.ok) throw new Error('API error');
    const question = await res.json();
    state.currentQuestion = question;

    renderQuizScreen(question);
    showLoading(false);
    showScreen('screen-quiz');
  } catch (err) {
    showLoading(false);
    console.error('Quiz generation error:', err);
    alert('Không thể tải câu đố lúc này, vui lòng thử lại nhé!');
    showScreen('screen-age');
  }
}

// -----------------------------------------------------------
// 5. MÀN HÌNH 2: RENDER CÂU HỎI + 4 ĐÁP ÁN A, B, C, D
// -----------------------------------------------------------
function renderQuizScreen(q) {
  state.isAnswered = false;
  document.getElementById('quiz-age-pill-text').textContent = `🎈 ${q.age_label || (q.age + ' Tuổi')}`;
  document.getElementById('quiz-question-text').textContent = q.question;

  const container = document.getElementById('quiz-options-wrapper');
  container.innerHTML = '';

  q.options.forEach(opt => {
    const btn = document.createElement('button');
    btn.className = 'quiz-opt-btn';
    btn.dataset.key = opt.key;
    btn.innerHTML = `
      <div class="opt-letter">${opt.key}</div>
      <div class="opt-text">${escapeHtml(opt.text)}</div>
    `;
    btn.addEventListener('click', () => handleSelectOption(opt.key, btn));
    container.appendChild(btn);
  });

  // Tự động đọc to câu hỏi và 4 đáp án ngay khi load câu hỏi (chỉ đọc nếu người dùng chưa chọn đáp án)
  if (autoReadTimer) {
    clearTimeout(autoReadTimer);
    autoReadTimer = null;
  }
  autoReadTimer = setTimeout(() => {
    if (!state.isAnswered && state.currentQuestion === q) {
      readQuizAloud();
    }
  }, 200);
}

// -----------------------------------------------------------
// 6. XỬ LÝ ĐÁP ÁN -> CHUYỂN QUA MÀN HÌNH 3 (CHÚC MỪNG)
// -----------------------------------------------------------
async function handleSelectOption(selectedKey, clickedBtn) {
  const q = state.currentQuestion;
  if (!q || state.isAnswered) return;
  state.isAnswered = true;

  // NGƯNG ĐỌC NGAY LẬP TỨC KHI CHỌN ĐÁP ÁN
  stopReadQuiz();
  setTimeout(stopReadQuiz, 50);
  setTimeout(stopReadQuiz, 150);

  // Disable all options
  document.querySelectorAll('.quiz-opt-btn').forEach(b => b.disabled = true);

  const isCorrect = (selectedKey.toUpperCase() === q.answer.toUpperCase());
  const reward = isCorrect ? 50000 : 5000; // 50k nếu đúng, 5k nếu sai

  if (isCorrect) {
    clickedBtn.classList.add('is-correct');
    playSound('correct');
    triggerConfetti();
  } else {
    clickedBtn.classList.add('is-wrong');
    playSound('wrong');
    // Highlight correct answer
    document.querySelectorAll('.quiz-opt-btn').forEach(b => {
      if (b.dataset.key === q.answer) b.classList.add('is-correct');
    });
  }

  // Update total money
  state.totalLixi += reward;
  localStorage.setItem('lixi_balance', state.totalLixi);
  updateBalanceDisplay();

  // Transition to Screen 3 after 600ms
  setTimeout(() => {
    renderCongratScreen(isCorrect, q, reward);
    showScreen('screen-congrat');
  }, 650);
}

// -----------------------------------------------------------
// 7. MÀN HÌNH 3: CHÚC MỪNG & LÌ XÌ + NÚT QUAY LẠI
// -----------------------------------------------------------
function renderCongratScreen(isCorrect, q, reward) {
  const iconBox = document.getElementById('congrat-icon-box');
  const titleEl = document.getElementById('congrat-title-text');
  const prizeEl = document.getElementById('congrat-prize-text');
  const detailEl = document.getElementById('congrat-detail-text');

  // Find correct option text
  const correctOpt = (q.options || []).find(o => o.key.toUpperCase() === q.answer.toUpperCase());
  const correctText = correctOpt ? correctOpt.text : '';

  // Display question header block at top of explanation card
  const questionHeaderHtml = `
    <div style="margin-bottom: 12px; padding-bottom: 10px; border-bottom: 1.5px dashed #cbd5e1; text-align: left;">
      <div style="font-size: 0.8rem; font-weight: 800; color: #64748b; text-transform: uppercase; margin-bottom: 4px;">❓ Câu hỏi:</div>
      <div style="font-size: 1.15rem; font-weight: 800; color: #1e293b; line-height: 1.45; white-space: pre-line;">${escapeHtml(q.question)}</div>
    </div>
  `;

  if (isCorrect) {
    iconBox.innerHTML = `
      <div class="lixi-coin-badge">🧧</div>
      <div class="lixi-tag-name">CHÍNH XÁC</div>
    `;
    titleEl.textContent = '🎉 CHÚC MỪNG BẠN ĐÃ TRẢ LỜI ĐÚNG!';
    titleEl.style.color = '#dc2626';
    prizeEl.textContent = '50k Lì Xì';
    detailEl.innerHTML = `
      ${questionHeaderHtml}
      <div style="margin-bottom: 8px; text-align: left;">
        <strong>🎯 Đáp án đúng:</strong> <span style="color: #059669; font-weight: 800;">${q.answer}. ${escapeHtml(correctText)}</span>
      </div>
      <div style="text-align: left;">
        <strong>💡 Lời giải:</strong> ${escapeHtml(q.explanation || 'Bạn đã chọn đáp án vô cùng chính xác!')}
      </div>
      ${q.fun_fact ? `<div style="margin-top: 8px; text-align: left; color: #b45309;"><strong>✨ Điều thú vị:</strong> ${escapeHtml(q.fun_fact)}</div>` : ''}
    `;
  } else {
    iconBox.innerHTML = `
      <div class="lixi-coin-badge">🌸</div>
      <div class="lixi-tag-name">LÌ XÌ AN ỦI</div>
    `;
    titleEl.textContent = 'TIẾC QUÁ, CHƯA CHÍNH XÁC!';
    titleEl.style.color = '#e11d48';
    prizeEl.textContent = '5k An Ủi';
    detailEl.innerHTML = `
      ${questionHeaderHtml}
      <div style="margin-bottom: 8px; text-align: left;">
        <strong>🎯 Đáp án đúng:</strong> <span style="color: #dc2626; font-weight: 800;">${q.answer}. ${escapeHtml(correctText)}</span>
      </div>
      <div style="text-align: left;">
        <strong>💡 Lời giải:</strong> ${escapeHtml(q.explanation || 'Đừng nản lòng nhé, hãy thử lại ở câu tiếp theo!')}
      </div>
    `;
  }
}

// Nút "Quay Lại Chọn Tuổi" (trở lại Màn hình 1)
function returnToAgeScreen() {
  playSound('click');
  stopReadQuiz();
  state.currentQuestion = null;
  showScreen('screen-age');
}

// -----------------------------------------------------------
// 8. TEXT-TO-SPEECH (TTS): ĐỌC CÂU HỎI KÈM ĐÁP ÁN A, B, C, D
// -----------------------------------------------------------
let autoReadTimer = null;
let ttsAbortController = null;
let currentTTSAudio = null;
let isSpeaking = false;
let currentTTSId = 0;

function buildQuizSpeechText(q) {
  let text = `${q.question}. `;
  (q.options || []).forEach(opt => {
    text += `${opt.key}, ${opt.text}. `;
  });
  return text;
}

function updateReadButtonUI(speaking) {
  isSpeaking = speaking;
  const btn = document.getElementById('btn-read-quiz');
  const icon = document.getElementById('read-icon');
  const label = document.getElementById('read-label');
  if (!btn) return;
  if (speaking) {
    btn.classList.add('is-reading');
    if (icon) icon.textContent = '⏹';
    if (label) label.textContent = 'Dừng đọc';
  } else {
    btn.classList.remove('is-reading');
    if (icon) icon.textContent = '🔊';
    if (label) label.textContent = 'Đọc câu hỏi';
  }
}

function stopReadQuiz() {
  currentTTSId++; // Vô hiệu hoá mọi tác vụ async TTS đang chờ
  if (autoReadTimer) {
    clearTimeout(autoReadTimer);
    autoReadTimer = null;
  }
  if (ttsAbortController) {
    try { ttsAbortController.abort(); } catch (e) {}
    ttsAbortController = null;
  }
  if ('speechSynthesis' in window) {
    try {
      window.speechSynthesis.pause();
      window.speechSynthesis.cancel();
    } catch (e) {}
  }
  if (currentTTSAudio) {
    try {
      currentTTSAudio.pause();
      currentTTSAudio.currentTime = 0;
      currentTTSAudio.src = '';
    } catch (e) {}
    currentTTSAudio = null;
  }
  updateReadButtonUI(false);
}

function startReadQuiz() {
  if (state.isAnswered) return; // Đã trả lời thì tuyệt đối không phát âm thanh
  stopReadQuiz();
  if (state.isAnswered) return;

  const q = state.currentQuestion;
  if (!q) return;

  const thisTTSId = currentTTSId;
  const speechText = buildQuizSpeechText(q);
  updateReadButtonUI(true);

  // Strategy 1: Web Speech API (vi-VN)
  if ('speechSynthesis' in window) {
    try {
      window.speechSynthesis.cancel();
      window.speechSynthesis.resume();
      const utterance = new SpeechSynthesisUtterance(speechText);
      utterance.lang = 'vi-VN';
      const voices = window.speechSynthesis.getVoices() || [];
      const viVoice = voices.find(v => v.lang && (v.lang.startsWith('vi') || v.lang.includes('VIE')));
      if (viVoice) utterance.voice = viVoice;
      utterance.rate = 1.18; // Tốc độ đọc nhanh hơn, dứt khoát
      utterance.pitch = 1.0;

      utterance.onend = () => updateReadButtonUI(false);
      utterance.onerror = (e) => {
        if (state.isAnswered || thisTTSId !== currentTTSId) return;
        console.warn('SpeechSynthesis error, falling back to server TTS:', e);
        playServerTTS(speechText, thisTTSId);
      };
      window.speechSynthesis.speak(utterance);
      return;
    } catch (e) {
      console.warn('SpeechSynthesis exception:', e);
    }
  }

  // Strategy 2: Server-side gTTS fallback
  playServerTTS(speechText, thisTTSId);
}

function readQuizAloud() {
  startReadQuiz();
}

async function toggleReadQuiz() {
  if (isSpeaking) {
    stopReadQuiz();
  } else {
    startReadQuiz();
  }
}

async function playServerTTS(text, thisTTSId) {
  if (state.isAnswered || (thisTTSId !== undefined && thisTTSId !== currentTTSId)) return;
  try {
    ttsAbortController = new AbortController();
    const res = await fetch('/api/quiz/tts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
      signal: ttsAbortController.signal
    });
    if (!res.ok) throw new Error('TTS server error');
    if (state.isAnswered || (thisTTSId !== undefined && thisTTSId !== currentTTSId)) return;

    const blob = await res.blob();
    if (state.isAnswered || (thisTTSId !== undefined && thisTTSId !== currentTTSId)) return;

    const audioUrl = URL.createObjectURL(blob);
    currentTTSAudio = new Audio(audioUrl);
    currentTTSAudio.playbackRate = 1.18;
    currentTTSAudio.onended = () => updateReadButtonUI(false);
    currentTTSAudio.onerror = () => updateReadButtonUI(false);
    await currentTTSAudio.play();
  } catch (err) {
    if (err.name !== 'AbortError') {
      console.warn('TTS playback error:', err);
    }
    updateReadButtonUI(false);
  }
}

// -----------------------------------------------------------
// 8. PHÁO HOA CONFETTI
// -----------------------------------------------------------
function triggerConfetti() {
  if (typeof confetti === 'function') {
    confetti({
      particleCount: 70,
      spread: 70,
      origin: { y: 0.6 },
      colors: ['#ef4444', '#f59e0b', '#10b981', '#3b82f6', '#ec4899']
    });
    setTimeout(() => {
      confetti({
        particleCount: 40,
        angle: 60,
        spread: 50,
        origin: { x: 0 },
        colors: ['#f59e0b', '#ef4444']
      });
      confetti({
        particleCount: 40,
        angle: 120,
        spread: 50,
        origin: { x: 1 },
        colors: ['#10b981', '#3b82f6']
      });
    }, 180);
  }
}

// -----------------------------------------------------------
// 9. BÀN PHÍM TẮT (A, B, C, D)
// -----------------------------------------------------------
function initKeyboardNav() {
  document.addEventListener('keydown', (e) => {
    const key = e.key.toUpperCase();
    const quizScreen = document.getElementById('screen-quiz');
    if (quizScreen && quizScreen.classList.contains('active')) {
      if (['A', 'B', 'C', 'D'].includes(key)) {
        const btn = document.querySelector(`.quiz-opt-btn[data-key="${key}"]:not(:disabled)`);
        if (btn) btn.click();
      }
    }
  });
}

function escapeHtml(str) {
  if (!str) return '';
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
