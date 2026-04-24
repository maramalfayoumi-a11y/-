import streamlit as st
import time
import pandas as pd

# إعدادات الصفحة وهوية كاهوت البصرية
st.set_page_config(page_title="Teacher Pro Challenge", page_icon="🎓", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #46178f; color: white; direction: rtl; }
    .question-box { background-color: white; color: #46178f; padding: 30px; border-radius: 20px; text-align: center; font-size: 28px; font-weight: bold; margin-bottom: 20px; }
    .stButton>button { width: 100%; height: 80px; font-size: 22px; font-weight: bold; color: white; border-radius: 15px; border: none; }
    /* ألوان كاهوت الشهيرة للخيارات */
    div.stButton > button:first-child { background-color: #e21b3c; } /* أحمر */
    div.stButton > button:nth-child(2) { background-color: #1368ce; } /* أزرق */
    </style>
    """, unsafe_allow_html=True)

# الأصوات
def play_sound(url):
    st.markdown(f'<audio src="{url}" autoplay></audio>', unsafe_allow_html=True)

correct_sound = "https://www.soundjay.com/buttons/sounds/button-3.mp3"
wrong_sound = "https://www.soundjay.com/buttons/sounds/button-10.mp3"

# الأسئلة
if 'questions' not in st.session_state:
    st.session_state.questions = [
        {"q": "عند حدوث فوضى رقمية داخل الصف، التصرف الأذكى هو:", "opts": ["إغلاق الميكروفونات فوراً", "طرح سؤال تفاعلي مفاجئ"], "a": "طرح سؤال تفاعلي مفاجئ"},
        {"q": "المعلم المحترف يختار الوسيلة بناءً على:", "opts": ["حداثة التقنية", "خصائص المتعلمين وأهداف الدرس"], "a": "خصائص المتعلمين وأهداف الدرس"},
        {"q": "الذكاء الاصطناعي في نظر المعلم المحترف هو:", "opts": ["بديل لدور المعلم", "مساعد لتخصيص التعلم"], "a": "مساعد لتخصيص التعلم"}
    ]

# تهيئة المخزن
if 'score' not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_q = 0
    st.session_state.game_finished = False

# شاشة البداية
if 'player_name' not in st.session_state:
    st.title("🏆 مسابقة المعلم المحترف")
    st.subheader("إشراف: د. مرام الفايومي")
    name = st.text_input("أدخل اسمك للمنافسة:")
    if st.button("دخول اللعبة"):
        if name:
            st.session_state.player_name = name
            st.rerun()
else:
    if not st.session_state.game_finished:
        q = st.session_state.questions[st.session_state.current_q]
        
        st.markdown(f"<div class='question-box'>{q['q']}</div>", unsafe_allow_html=True)
        
        # عداد السرعة (تفاعلي)
        st.write("⏱️ الوقت المتبقي للإجابة:")
        timer_placeholder = st.empty()
        
        # عرض الخيارات كأزرار كبيرة
        col1, col2 = st.columns(2)
        with col1:
            btn1 = st.button(q['opts'][0])
        with col2:
            btn2 = st.button(q['opts'][1])
            
        # منطق الضغط على الأزرار
        user_choice = None
        if btn1: user_choice = q['opts'][0]
        if btn2: user_choice = q['opts'][1]

        if user_choice:
            if user_choice == q['a']:
                st.session_state.score += 100
                play_sound(correct_sound)
                st.success("إجابة صحيحة! 🎉")
            else:
                play_sound(wrong_sound)
                st.error("إجابة خاطئة! ❌")
            
            time.sleep(1)
            if st.session_state.current_q < len(st.session_state.questions) - 1:
                st.session_state.current_q += 1
            else:
                st.session_state.game_finished = True
            st.rerun()
    else:
        # النتائج النهائية (الترتيب الحقيقي)
        st.balloons()
        st.header("📊 لوحة الصدارة النهائية")
        
        # ترتيب افتراضي للمشاركين (يمكنك ربطه بقاعدة بيانات لاحقاً)
        results = [
            {"الاسم": st.session_state.player_name, "النقاط": st.session_state.score},
            {"الاسم": "مشارك 1", "النقاط": 250},
            {"الاسم": "مشارك 2", "النقاط": 180}
        ]
        df = pd.DataFrame(results).sort_values(by="النقاط", ascending=False)
        
        st.table(df)
        st.success(f"مبارك للفائز بالمركز الأول: {df.iloc[0]['الاسم']}! 🏆")
