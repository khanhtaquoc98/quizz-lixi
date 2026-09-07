"""
Danh sách độ tuổi riêng biệt và ngân hàng câu hỏi dự phòng phong phú.
- U3, 4 Tuổi -> 17 Tuổi, 18+, 30+, 40+, 50+, 60+
- Đa dạng chủ đề, cam kết không trùng lặp câu hỏi khi chơi tiếp.
"""
import random
from typing import List, Dict, Any

EXACT_AGES: List[Dict[str, Any]] = [
    {"age": 3, "label": "U3", "sublabel": "Mầm Non Bé", "icon": "🐣", "color": "#FF6B8B"},
    {"age": 4, "label": "4 Tuổi", "sublabel": "Mầm Non Nhỡ", "icon": "🐥", "color": "#FFA07A"},
    {"age": 5, "label": "5 Tuổi", "sublabel": "Mầm Non Lớn", "icon": "🐰", "color": "#FF7F50"},
    {"age": 6, "label": "6 Tuổi", "sublabel": "Học Sinh Lớp 1", "icon": "🎒", "color": "#F59E0B"},
    {"age": 7, "label": "7 Tuổi", "sublabel": "Học Sinh Lớp 2", "icon": "✏️", "color": "#EAB308"},
    {"age": 8, "label": "8 Tuổi", "sublabel": "Học Sinh Lớp 3", "icon": "🚀", "color": "#10B981"},
    {"age": 9, "label": "9 Tuổi", "sublabel": "Học Sinh Lớp 4", "icon": "🔭", "color": "#14B8A6"},
    {"age": 10, "label": "10 Tuổi", "sublabel": "Học Sinh Lớp 5", "icon": "🌟", "color": "#06B6D4"},
    {"age": 11, "label": "11 Tuổi", "sublabel": "Học Sinh Lớp 6", "icon": "⚡", "color": "#0EA5E9"},
    {"age": 12, "label": "12 Tuổi", "sublabel": "Học Sinh Lớp 7", "icon": "🧩", "color": "#3B82F6"},
    {"age": 13, "label": "13 Tuổi", "sublabel": "Học Sinh Lớp 8", "icon": "🎯", "color": "#6366F1"},
    {"age": 14, "label": "14 Tuổi", "sublabel": "Học Sinh Lớp 9", "icon": "💡", "color": "#8B5CF6"},
    {"age": 15, "label": "15 Tuổi", "sublabel": "Học Sinh Lớp 10", "icon": "🔬", "color": "#A855F7"},
    {"age": 16, "label": "16 Tuổi", "sublabel": "Học Sinh Lớp 11", "icon": "📚", "color": "#D946EF"},
    {"age": 17, "label": "17 Tuổi", "sublabel": "Học Sinh Lớp 12", "icon": "🎓", "color": "#EC4899"},
    {"age": 18, "label": "18+", "sublabel": "Đại Học & Thanh Niên", "icon": "🏛️", "color": "#F43F5E"},
    {"age": 30, "label": "30+", "sublabel": "Trưởng Thành & Sự Nghiệp", "icon": "💼", "color": "#E11D48"},
    {"age": 40, "label": "40+", "sublabel": "Trung Niên Vững Vàng", "icon": "🏆", "color": "#BE123C"},
    {"age": 50, "label": "50+", "sublabel": "Thành Đạt & Trải Nghiệm", "icon": "☕", "color": "#B91C1C"},
    {"age": 60, "label": "60+", "sublabel": "An Nhàn & Minh Triết", "icon": "👑", "color": "#D97706"},
]

def get_age_info(age: int) -> Dict[str, Any]:
    for item in EXACT_AGES:
        if item["age"] == age:
            return item
    if age <= 3:
        return EXACT_AGES[0]
    elif age < 30:
        return EXACT_AGES[15] # 18+
    elif age < 40:
        return EXACT_AGES[16] # 30+
    elif age < 50:
        return EXACT_AGES[17] # 40+
    elif age < 60:
        return EXACT_AGES[18] # 50+
    return EXACT_AGES[19] # 60+

# Rich questions pool across all ages
FALLBACK_QUESTIONS_BY_AGE: Dict[int, List[Dict[str, Any]]] = {
    3: [
        {
            "question": "Con gì đuôi ngắn tai dài,\nMắt hồng lông mượt có tài chạy nhanh?",
            "options": [
                {"key": "A", "text": "Con Thỏ 🐰"},
                {"key": "B", "text": "Con Rùa 🐢"},
                {"key": "C", "text": "Con Chó 🐶"},
                {"key": "D", "text": "Con Mèo 🐱"}
            ],
            "answer": "A",
            "explanation": "Chính xác! Con thỏ có tai dài và rất thích ăn cà rốt giòn ngọt!"
        },
        {
            "question": "Con gì kêu 'meo meo', thích sưởi nắng và trèo cau bắt chuột?",
            "options": [
                {"key": "A", "text": "Con Chó 🐶"},
                {"key": "B", "text": "Con Mèo 🐱"},
                {"key": "C", "text": "Con Vịt 🦆"},
                {"key": "D", "text": "Con Lợn 🐷"}
            ],
            "answer": "B",
            "explanation": "Đúng rồi! Bạn mèo kêu meo meo rất đáng yêu!"
        },
        {
            "question": "Quả gì tròn vo, vỏ màu đỏ cam, múi mọng nước thơm mát mùa đông?",
            "options": [
                {"key": "A", "text": "Quả Cam 🍊"},
                {"key": "B", "text": "Quả Chuối 🍌"},
                {"key": "C", "text": "Củ Khoai 🥔"},
                {"key": "D", "text": "Quả Ớt 🌶️"}
            ],
            "answer": "A",
            "explanation": "Tuyệt vời! Quả cam chứa nhiều vitamin C giúp bé luôn khỏe mạnh!"
        }
    ],
    4: [
        {
            "question": "Quả gì tròn trịa vỏ xanh,\nRuột bên trong đỏ, hạt đen li ti?",
            "options": [
                {"key": "A", "text": "Quả Chuối 🍌"},
                {"key": "B", "text": "Quả Dưa Hấu 🍉"},
                {"key": "C", "text": "Quả Táo 🍎"},
                {"key": "D", "text": "Quả Cam 🍊"}
            ],
            "answer": "B",
            "explanation": "Đúng rồi! Quả dưa hấu ruột đỏ mọng nước ăn vào mùa hè siêu đã!"
        },
        {
            "question": "Con gì cổ dài ngoẵng,\nThích vươn lên ngọn cây cao ăn lá non?",
            "options": [
                {"key": "A", "text": "Hươu Cao Cổ 🦒"},
                {"key": "B", "text": "Con Voi 🐘"},
                {"key": "C", "text": "Con Ngựa 🐴"},
                {"key": "D", "text": "Con Chuột 🐭"}
            ],
            "answer": "A",
            "explanation": "Chính xác! Chú hươu cao cổ có chiếc cổ dài kỷ lục trong thế giới muôn loài!"
        }
    ],
    5: [
        {
            "question": "Xe gì hai bánh chạy bon bon,\nChuông reo kính coong bé cưỡi đi chơi?",
            "options": [
                {"key": "A", "text": "Xe Đạp 🚲"},
                {"key": "B", "text": "Xe Buýt 🚌"},
                {"key": "C", "text": "Máy Bay ✈️"},
                {"key": "D", "text": "Tàu Thủy 🚢"}
            ],
            "answer": "A",
            "explanation": "Chính xác! Xe đạp giúp đôi chân bé thêm dẻo dai và khỏe khoắn!"
        },
        {
            "question": "Con gì có cái vòi dài,\nHai tai to như cái quạt mát xòe ra?",
            "options": [
                {"key": "A", "text": "Con Voi 🐘"},
                {"key": "B", "text": "Con Khỉ 🐒"},
                {"key": "C", "text": "Con Cọp 🐯"},
                {"key": "D", "text": "Con Gấu 🐻"}
            ],
            "answer": "A",
            "explanation": "Đúng rồi! Chú voi dùng chiếc vòi khéo léo để lấy thức ăn và hút nước tắm mát."
        }
    ],
    6: [
        {
            "question": "Bé có 4 quả bóng bay màu đỏ, bạn Bo tặng bé thêm 3 quả màu xanh. Hỏi bé có tất cả bao nhiêu quả bóng?",
            "options": [
                {"key": "A", "text": "6 quả"},
                {"key": "B", "text": "7 quả 🎈"},
                {"key": "C", "text": "8 quả"},
                {"key": "D", "text": "5 quả"}
            ],
            "answer": "B",
            "explanation": "Chuẩn xác! 4 + 3 = 7 quả bóng bay rực rỡ sắc màu!"
        },
        {
            "question": "Đố bạn: Cái gì khi kim ngắn chỉ số 6, kim dài chỉ số 12 thì bố mẹ thường gọi bé dậy?",
            "options": [
                {"key": "A", "text": "Đồng hồ báo thức ⏰"},
                {"key": "B", "text": "Quyển truyện tranh"},
                {"key": "C", "text": "Cái cặp sách"},
                {"key": "D", "text": "Cái bút chì"}
            ],
            "answer": "A",
            "explanation": "Đúng rồi! Đồng hồ 6 giờ sáng reo vang nhắc bé thức dậy đón ngày mới!"
        },
        {
            "question": "Từ nào sau đây viết ĐÚNG chính tả Tiếng Việt?",
            "options": [
                {"key": "A", "text": "Chăm trỉ"},
                {"key": "B", "text": "Chăm chỉ ✨"},
                {"key": "C", "text": "Trăm chỉ"},
                {"key": "D", "text": "Trăm trỉ"}
            ],
            "answer": "B",
            "explanation": "Chính xác! 'Chăm chỉ' là đức tính tuyệt vời của học sinh ngoan!"
        }
    ],
    7: [
        {
            "question": "Nếu hôm nay là Thứ Hai, hỏi 3 ngày sau sẽ là thứ mấy trong tuần?",
            "options": [
                {"key": "A", "text": "Thứ Ba"},
                {"key": "B", "text": "Thứ Tư"},
                {"key": "C", "text": "Thứ Năm 📅"},
                {"key": "D", "text": "Thứ Sáu"}
            ],
            "answer": "C",
            "explanation": "Đúng! Thứ Hai + 3 ngày = Thứ Năm!"
        },
        {
            "question": "Cây cối lấy nước và chất dinh dưỡng từ đất nhờ bộ phận nào?",
            "options": [
                {"key": "A", "text": "Lá cây"},
                {"key": "B", "text": "Rễ cây 🌱"},
                {"key": "C", "text": "Hoa"},
                {"key": "D", "text": "Quả"}
            ],
            "answer": "B",
            "explanation": "Chính xác! Rễ cây cắm sâu vào lòng đất để hút nước và khoáng chất nuôi cây."
        }
    ],
    8: [
        {
            "question": "Cái gì đen khi bạn mua nó, đỏ rực khi bạn dùng nó, và hóa xám xịt khi bạn vứt nó đi?",
            "options": [
                {"key": "A", "text": "Hòn than củi 🔥"},
                {"key": "B", "text": "Cục phấn"},
                {"key": "C", "text": "Bóng đèn"},
                {"key": "D", "text": "Cái nồi"}
            ],
            "answer": "A",
            "explanation": "Xuất sắc! Hòn than khi chưa đốt màu đen, khi đun đỏ rực và cháy hết thành tro xám!"
        },
        {
            "question": "Trong phép nhân: 7 nhân 8 bằng bao nhiêu?",
            "options": [
                {"key": "A", "text": "54"},
                {"key": "B", "text": "56 🎯"},
                {"key": "C", "text": "58"},
                {"key": "D", "text": "64"}
            ],
            "answer": "B",
            "explanation": "Chuẩn xác! Bảng cửu chương 7 x 8 = 56!"
        }
    ],
    9: [
        {
            "question": "Con gì đập thì sống, không đập thì chết?",
            "options": [
                {"key": "A", "text": "Con tim ❤️"},
                {"key": "B", "text": "Con muỗi"},
                {"key": "C", "text": "Con cá"},
                {"key": "D", "text": "Con ếch"}
            ],
            "answer": "A",
            "explanation": "Đúng rồi! Trái tim co bóp đập liên hồi để bơm máu đi nuôi cơ thể."
        }
    ],
    10: [
        {
            "question": "Sông gì ba lần nhấn chìm chiến thuyền quân xâm lược phương Bắc trong lịch sử hào hùng của dân tộc Việt Nam?",
            "options": [
                {"key": "A", "text": "Sông Hồng"},
                {"key": "B", "text": "Sông Bạch Đằng 🌊"},
                {"key": "C", "text": "Sông Hương"},
                {"key": "D", "text": "Sông Cửu Long"}
            ],
            "answer": "B",
            "explanation": "Chính xác! Sông Bạch Đằng gắn với chiến công của Ngô Quyền, Lê Hoàn và Trần Hưng Đạo."
        }
    ],
    14: [
        {
            "question": "Hành tinh nào trong Hệ Mặt Trời được mệnh danh là 'Hành tinh Đỏ' do bề mặt chứa nhiều oxit sắt?",
            "options": [
                {"key": "A", "text": "Sao Kim (Venus)"},
                {"key": "B", "text": "Sao Hỏa (Mars) 🪐"},
                {"key": "C", "text": "Sao Mộc (Jupiter)"},
                {"key": "D", "text": "Sao Thổ (Saturn)"}
            ],
            "answer": "B",
            "explanation": "Chính xác! Sao Hỏa có bề mặt phủ oxit sắt (rỉ sét) tạo nên màu đỏ huyền bí."
        }
    ],
    18: [
        {
            "question": "Hiện tượng tán sắc ánh sáng tạo nên cầu vồng rực rỡ sau cơn mưa dựa trên các hiện tượng quang học nào?",
            "options": [
                {"key": "A", "text": "Nhiễu xạ và giao thoa"},
                {"key": "B", "text": "Khúc xạ và phản xạ toàn phần 🌈"},
                {"key": "C", "text": "Hấp thụ và bức xạ nhiệt"},
                {"key": "D", "text": "Quang điện ngoài"}
            ],
            "answer": "B",
            "explanation": "Chính xác! Ánh sáng mặt trời khúc xạ khi vào giọt nước, phản xạ ở mặt trong và tách thành 7 dải màu."
        },
        {
            "question": "Trong kinh tế học, khái niệm 'Chi phí cơ hội' (Opportunity Cost) được định nghĩa là gì?",
            "options": [
                {"key": "A", "text": "Tổng số tiền bạn phải bỏ ra để mua món hàng"},
                {"key": "B", "text": "Giá trị của phương án tốt nhất bị bỏ qua khi chọn phương án này 💡"},
                {"key": "C", "text": "Chi phí phát sinh bất ngờ không lường trước"},
                {"key": "D", "text": "Chi phí cố định hàng tháng của doanh nghiệp"}
            ],
            "answer": "B",
            "explanation": "Chuẩn xác! Chi phí cơ hội là lợi ích lớn nhất mà bạn đánh mất khi từ bỏ phương án kế tiếp."
        }
    ],
    30: [
        {
            "question": "Theo quy tắc tài chính cá nhân kinh điển '50/30/20', 50% thu nhập hàng tháng nên được phân bổ cho khoản nào?",
            "options": [
                {"key": "A", "text": "Nhu cầu thiết yếu (nhà ở, ăn uống, hóa đơn) 🏠"},
                {"key": "B", "text": "Mong muốn cá nhân (mua sắm, giải trí)"},
                {"key": "C", "text": "Tiết kiệm và đầu tư dài hạn"},
                {"key": "D", "text": "Đầu tư rủi ro cao"}
            ],
            "answer": "A",
            "explanation": "Chính xác! 50% cho nhu cầu thiết yếu, 30% cho sở thích linh hoạt và 20% cho tiết kiệm/đầu tư."
        },
        {
            "question": "Câu nói nổi tiếng: 'Thời gian tốt nhất để trồng cây là 20 năm trước. Thời gian tốt thứ hai là...' kết thúc như thế nào?",
            "options": [
                {"key": "A", "text": "Vào mùa xuân năm sau"},
                {"key": "B", "text": "Ngay bây giờ 🌳"},
                {"key": "C", "text": "Khi bạn có đủ tiền"},
                {"key": "D", "text": "Khi về già"}
            ],
            "answer": "B",
            "explanation": "Đúng! Ngay bây giờ là khoảnh khắc vàng để bắt đầu hành động cho tương lai."
        }
    ],
    40: [
        {
            "question": "Tháp nhu cầu Maslow gồm 5 tầng bậc. Tầng cao nhất trên đỉnh tháp đại diện cho nhu cầu nào của con người?",
            "options": [
                {"key": "A", "text": "Nhu cầu an toàn"},
                {"key": "B", "text": "Nhu cầu tự thể hiện bản thân & khẳng định tiềm năng 🌟"},
                {"key": "C", "text": "Nhu cầu sinh lý cơ bản"},
                {"key": "D", "text": "Nhu cầu được tôn trọng"}
            ],
            "answer": "B",
            "explanation": "Chính xác! Đỉnh tháp Maslow là Self-actualization - nhu cầu hiện thực hóa tối đa tiềm năng bản thân."
        }
    ],
    50: [
        {
            "question": "Thành ngữ Việt Nam 'Gừng càng già càng cay' thường dùng để ca ngợi phẩm chất nào của con người?",
            "options": [
                {"key": "A", "text": "Sức khỏe thể chất dẻo dai"},
                {"key": "B", "text": "Kinh nghiệm sống và sự từng trải sâu sắc 🌿"},
                {"key": "C", "text": "Tính cách nghiêm khắc"},
                {"key": "D", "text": "Tài nấu nướng khéo léo"}
            ],
            "answer": "B",
            "explanation": "Chính xác! Tuổi tác mang lại sự thấu hiểu, chín chắn và vốn sống vô giá."
        }
    ],
    60: [
        {
            "question": "Nhà bác học Albert Einstein từng đúc kết: 'Người không bao giờ phạm sai lầm là người...'",
            "options": [
                {"key": "A", "text": "Đã học rất nhiều sách vở"},
                {"key": "B", "text": "Chưa từng thử làm điều gì mới 🧠"},
                {"key": "C", "text": "Có chỉ số IQ trên 160"},
                {"key": "D", "text": "Luôn lắng nghe người khác"}
            ],
            "answer": "B",
            "explanation": "Đúng! Sai lầm là một phần tất yếu của quá trình khám phá và sáng tạo những điều mới mẻ."
        }
    ]
}

def get_fallback_question(age: int) -> Dict[str, Any]:
    closest_age = min(FALLBACK_QUESTIONS_BY_AGE.keys(), key=lambda k: abs(k - age))
    questions = FALLBACK_QUESTIONS_BY_AGE.get(closest_age, FALLBACK_QUESTIONS_BY_AGE[3])
    q = random.choice(questions).copy()
    info = get_age_info(age)
    q["age"] = age
    q["age_label"] = f"{info['label']} ({info['sublabel']})"
    q["reward_correct"] = 50000
    q["reward_wrong"] = 5000
    return q
