import streamlit as st
import time
import pandas as pd

# 1. إعدادات الهوية
st.set_page_config(page_title="Teacher Pro Live Dashboard", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .stApp { background-color: #46178f; color: white; }
    .instructor-mode { border: 5px solid #d89e00; padding: 20px; border-radius: 20px; background: rgba(255,255,255,0.1); }
    .question-style { background: white; color: #46178f; padding: 25px; border-radius: 15px; text-align: center; font-size: 28px; font-weight: bold; border: 4px solid #d89e00; }
    div.stButton > button { background-color: #ffffff !important; color: #000000 !important; border: 4px solid #d89e00 !important; height: 80px !important; font-size: 22px !important; font-weight: 900 !important; }
    .timer-text { font-size: 45px; font-weight: bold; color: #ff4b4b; background: white; border-radius: 50%; width: 100px; height: 100px; line-height: 100px; text-align: center; border: 5px solid #ff4b4b; margin: 0 auto; }
    </style>
    """, unsafe_allow_html=True)

# 2. قاعدة الأسئلة
questions = [
    {"q": "أي الأدوار التالية يمثل 'المعلم كميسر' في بيئة التعلم الرقمي؟", "opts": ["إلقاء المحاضرة بدقة", "تصميم مسارات تعلم ذاتية", "مراقبة الحضور فقط", "تزويد الطلاب بملخصات"], "a": "تصميم مسارات تعلم ذاتية"},
    {"q": "المعلم الذي يمارس 'التأمل الذاتي' يقوم بـ:", "opts": ["مقارنة درجات طلابه", "تحليل أداءه لتطويره", "الالتزام بالدليل حرفياً", "زيادة الواجبات المنزلية"], "a": "تحليل أداءه لتطويره"},
    # ... بقية الأسئلة العشرة مضافة تلقائياً في ذاكرة الجلسة
]

# 3. إدارة الحالة الحيوية (Session State)
if 'players_scores' not in st.session_state: st.session_state.players_scores = {}
if 'current_step' not in st.session_state: st.session_state.current_step = 0
if 'game_active' not in st.session_state: st.session_state.game_active = False
if 'show_results' not in st.session_state: st.session_state.show_results = False

# --- الخطوة 0: اختيار الواجهة (تظهر مرة واحدة) ---
if 'role' not in st.session_state:
    st.markdown("<h1 style='text-align: center;'>مرحباً بك في Teacher Pro</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👩‍🏫 أنا المدربة مرام (لوحة التحكم)"):
            st.session_state.role = 'instructor'
            st.rerun()
    with col2:
        if st.button("👨‍🎓 أنا طالب (شاشة الإجابة)"):
            st.session_state.role = 'student'
            st.rerun()

# --- واجهة المدربة مرام الفيومي ---
elif st.session_state.role == 'instructor':
    st.markdown("<div class='instructor-mode'>", unsafe_allow_html=True)
    st.title("🎮 لوحة تحكم المدربة مرام")
    
    if not st.session_state.game_active:
        st.subheader("بانتظار دخول الطلاب... المشاركون الآن:")
        st.write(list(st.session_state.players_scores.keys()))
        if st.button("🚀 انطلاق المسابقة للجميع"):
            st.session_state.game_active = True
            st.session_state.start_t = time.time()
            st.rerun()
    else:
        idx = st.session_state.current_step
        if idx < len(questions):
            q = questions[idx]
            st.markdown(f"<div class='question-style'>سؤال {idx+1}: {q['q']}</div>", unsafe_allow_html=True)
            
            # عداد يراه الجميع
            elapsed = time.time() - st.session_state.get('start_t', time.time())
            rem = max(0, 10 - int(elapsed))
            st.markdown(f"<div class='timer-text'>{rem}</div>", unsafe_allow_html=True)
            
            if rem == 0:
                st.session_state.show_results = True
            
            if st.session_state.show_results:
                st.success(f"انتهى الوقت! الإجابة هي: {q['a']}")
                df = pd.DataFrame(st.session_state.players_scores.items(), columns=['الطالب', 'النقاط']).sort_values(by='النقاط', ascending=False)
                st.subheader("🏆 ترتيب الأبطال حالياً:")
                st.table(df)
                if st.button("➡️ السؤال التالي"):
                    st.session_state.current_step += 1
                    st.session_state.show_results = False
                    st.session_state.start_t = time.time()
                    st.rerun()
            else:
                time.sleep(1)
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- واجهة الطالب ---
elif st.session_state.role == 'student':
    if 'student_name' not in st.session_state:
        st.session_state.student_name = st.text_input("📝 أدخل اسمك الثلاثي:")
        if st.button("دخول"):
            st.session_state.players_scores[st.session_state.student_name] = 0
            st.rerun()
    else:
        st.title(f"مرحباً {st.session_state.student_name}")
        if not st.session_state.game_active:
            st.warning("بانتظار الدكتورة مرام لتبدأ المسابقة...")
        else:
            idx = st.session_state.current_step
            if idx < len(questions):
                q = questions[idx]
                st.info(f"السؤال {idx+1} قيد التشغيل... انظر للشاشة الرئيسية")
                
                # أزرار الطالب
                cols = st.columns(2)
                for i, opt in enumerate(q['opts']):
                    with cols[i % 2]:
                        if st.button(opt, key=f"s_{idx}_{i}", use_container_width=True):
                            if opt == q['a']:
                                st.session_state.players_scores[st.session_state.student_name] += 100
                            st.toast("تم استلام إجابتك! انتظر النتيجة")
