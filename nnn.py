import streamlit as st
import time
import pandas as pd

# 1. إعدادات الهوية البصرية (Kahoot Theme)
st.set_page_config(page_title="Teacher Pro Lobby", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .stApp { background-color: #46178f; color: white; }
    .lobby-title { text-align: center; font-size: 45px; font-weight: bold; color: #d89e00; text-shadow: 2px 2px #000; }
    .instructor { text-align: center; font-size: 22px; margin-bottom: 20px; }
    .name-bubble { background-color: #ffffff; color: #46178f; padding: 12px 25px; border-radius: 50px; 
                   font-size: 22px; font-weight: bold; margin: 8px; display: inline-block; 
                   box-shadow: 4px 4px 15px rgba(0,0,0,0.3); border: 2px solid #d89e00; }
    .question-text { background: white; color: #46178f; padding: 30px; border-radius: 20px; 
                     text-align: center; font-size: 30px; font-weight: bold; margin-bottom: 20px; }
    /* ألوان أزرار كاهوت */
    div.stButton > button { height: 80px; font-size: 20px !important; border-radius: 15px; color: white !important; }
    .btn-red > div > button { background-color: #e21b3c !important; }
    .btn-blue > div > button { background-color: #1368ce !important; }
    .btn-yellow > div > button { background-color: #d89e00 !important; }
    .btn-green > div > button { background-color: #26890c !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة حالة اللعبة والبيانات
if 'players' not in st.session_state: st.session_state.players = []
if 'game_stage' not in st.session_state: st.session_state.game_stage = 'lobby'
if 'current_q' not in st.session_state: st.session_state.current_q = 0
if 'score' not in st.session_state: st.session_state.score = 0

questions = [
    {"q": "أي الأدوار التالية يمثل 'المعلم كميسر' في بيئة التعلم الرقمي؟", "img": "https://img.freepik.com/free-vector/teacher-concept-illustration_114360-2166.jpg", "opts": ["إلقاء المحاضرة بدقة", "تصميم مسارات تعلم ذاتية", "مراقبة الحضور فقط", "تزويد الطلاب بملخصات"], "a": "تصميم مسارات تعلم ذاتية"},
    {"q": "المعلم الذي يمارس 'التأمل الذاتي' يقوم بـ:", "img": "https://img.freepik.com/free-vector/thought-process-concept-illustration_114360-10145.jpg", "opts": ["مقارنة درجات طلابه", "تحليل أداءه لتطويره", "الالتزام بالدليل حرفياً", "زيادة الواجبات المنزلية"], "a": "تحليل أداءه لتطويره"},
    # ... يمكن إضافة الـ 8 أسئلة الباقية هنا بنفس النمط
]

# --- المرحلة 1: شاشة اللوبي (Lobby) ---
if st.session_state.game_stage == 'lobby':
    st.markdown("<div class='lobby-title'>🎮 قاعة انتظار مسابقة Teacher Pro</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='instructor'>إشراف الدكتورة: مرام الفيومي</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("📝 سجل اسمك")
        player_name = st.text_input("اكتب اسمك هنا:", key="entry")
        if st.button("انضمام للسباق 🏃‍♂️"):
            if player_name and player_name not in st.session_state.players:
                st.session_state.players.append(player_name)
                st.session_state.player_identity = player_name
                st.rerun()
    
    with col2:
        st.subheader(f"👥 المتسابقون المستعدون ({len(st.session_state.players)})")
        container = st.container()
        if st.session_state.players:
            bubbles = "".join([f"<div class='name-bubble'>{name}</div>" for name in st.session_state.players])
            st.markdown(bubbles, unsafe_allow_html=True)
        else:
            st.write("بانتظار دخول الأبطال... انشر الرابط لطلابك!")

    if len(st.session_state.players) > 0:
        st.markdown("---")
        if st.button("🚀 ارفع الستار وابدأ التحدي!", use_container_width=True):
            st.session_state.game_stage = 'quiz'
            st.rerun()

# --- المرحلة 2: شاشة الأسئلة ---
elif st.session_state.game_stage == 'quiz':
    idx = st.session_state.current_q
    if idx < len(questions):
        q = questions[idx]
        st.markdown(f"<div class='question-text'>{q['q']}</div>", unsafe_allow_html=True)
        st.image(q['img'], width=400)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="btn-red">', unsafe_allow_html=True)
            if st.button(q['opts'][0]): choice = q['opts'][0]
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('<div class="btn-blue">', unsafe_allow_html=True)
            if st.button(q['opts'][1]): choice = q['opts'][1]
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="btn-yellow">', unsafe_allow_html=True)
            if st.button(q['opts'][2]): choice = q['opts'][2]
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('<div class="btn-green">', unsafe_allow_html=True)
            if st.button(q['opts'][3]): choice = q['opts'][3]
            st.markdown('</div>', unsafe_allow_html=True)
        
        # منطق الإجابة (مختصر)
        if 'choice' in locals():
            if choice == q['a']:
                st.session_state.score += 100
                st.success("✅ إجابة صحيحة!")
            else: st.error("❌ إجابة خاطئة!")
            time.sleep(1)
            st.session_state.current_q += 1
            st.rerun()
    else:
        st.session_state.game_stage = 'results'
        st.rerun()

# --- المرحلة 3: النتائج والترتيب ---
elif st.session_state.game_stage == 'results':
    st.balloons()
    st.markdown("<h1 style='text-align: center;'>🏆 منصة التتويج 🏆</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>الفائز الأول: {st.session_state.player_identity}</h2>", unsafe_allow_html=True)
    # هنا يظهر الجدول النهائي كما صممناه سابقاً
