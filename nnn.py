import streamlit as st
import time
import pandas as pd

# 1. إعدادات الهوية (د. مرام الفيومي)
st.set_page_config(page_title="Teacher Pro Instructor Dashboard", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .stApp { background-color: #46178f; color: white; }
    .question-style { background: white; color: #46178f; padding: 25px; border-radius: 15px; text-align: center; font-size: 28px; font-weight: bold; border: 4px solid #d89e00; }
    
    /* الأزرار التفاعلية */
    div.stButton > button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 4px solid #d89e00 !important;
        height: 80px !important;
        font-size: 20px !important;
        font-weight: 900 !important;
    }
    div.stButton > button:focus { background-color: #ffeb3b !important; border-color: #ff9800 !important; }
    
    .timer-text { font-size: 40px; font-weight: bold; color: #ff4b4b; background: white; border-radius: 50%; width: 90px; height: 90px; line-height: 90px; margin: 0 auto; border: 5px solid #ff4b4b; text-align: center; }
    .admin-panel { background: rgba(0,0,0,0.3); padding: 20px; border-radius: 15px; border: 2px dashed #d89e00; margin-top: 50px; }
    </style>
    """, unsafe_allow_html=True)

# 2. روابط الموسيقى
bg_music = "https://www.soundjay.com/free-music/sounds/action-movie-trailer-1.mp3"
correct_sfx = "https://www.soundjay.com/buttons/sounds/button-3.mp3"

# 3. قاعدة البيانات (10 أسئلة)
questions = [
    {"q": "أي الأدوار التالية يمثل 'المعلم كميسر' في بيئة التعلم الرقمي؟", "opts": ["إلقاء المحاضرة بدقة", "تصميم مسارات تعلم ذاتية", "مراقبة الحضور فقط", "تزويد الطلاب بملخصات"], "a": "تصميم مسارات تعلم ذاتية"},
    {"q": "المعلم الذي يمارس 'التأمل الذاتي' يقوم بـ:", "opts": ["مقارنة درجات طلابه", "تحليل أداءه لتطويره", "الالتزام بالدليل حرفياً", "زيادة الواجبات المنزلية"], "a": "تحليل أداءه لتطويره"},
    # ... (بقية الأسئلة مدمجة)
]

# 4. إدارة الحالة الحية
if 'players_db' not in st.session_state: st.session_state.players_db = {}
if 'game_stage' not in st.session_state: st.session_state.game_stage = 'lobby'
if 'current_q' not in st.session_state: st.session_state.current_q = 0
if 'time_over' not in st.session_state: st.session_state.time_over = False

# --- شاشة اللوبي ---
if st.session_state.game_stage == 'lobby':
    st.markdown("<h1 style='text-align: center;'>🎮 قاعة انتظار Teacher Pro</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>بإشراف د. مرام الفيومي</h3>", unsafe_allow_html=True)
    
    name = st.text_input("📝 سجل اسمك للانضمام:")
    if st.button("انضمام"):
        if name and name not in st.session_state.players_db:
            st.session_state.players_db[name] = 0
            st.session_state.current_user = name
            st.rerun()
    
    st.write(f"المتواجدون حالياً: {', '.join(st.session_state.players_db.keys())}")
    
    if len(st.session_state.players_db) > 0:
        if st.button("🚀 ابدأ المسابقة (تحكم المدربة)", use_container_width=True):
            st.session_state.game_stage = 'quiz'
            st.rerun()

# --- شاشة الأسئلة ---
elif st.session_state.game_stage == 'quiz':
    idx = st.session_state.current_q
    if idx < len(questions):
        q = questions[idx]
        st.markdown(f'<audio src="{bg_music}" autoplay loop></audio>', unsafe_allow_html=True)
        
        st.markdown(f"<div class='question-style'>سؤال {idx+1}: {q['q']}</div>", unsafe_allow_html=True)
        
        timer_placeholder = st.empty()
        
        if not st.session_state.time_over:
            cols = st.columns(2)
            for i, opt in enumerate(q['opts']):
                with cols[i % 2]:
                    if st.button(opt, key=f"q{idx}o{i}", use_container_width=True):
                        st.session_state.temp_choice = opt
            
            for seconds in range(10, -1, -1):
                timer_placeholder.markdown(f"<div class='timer-text'>{seconds}</div>", unsafe_allow_html=True)
                time.sleep(1)
            
            # احتساب النقاط عند انتهاء الوقت
            if st.session_state.get('temp_choice') == q['a']:
                st.session_state.players_db[st.session_state.current_user] += 100
                st.markdown(f'<audio src="{correct_sfx}" autoplay></audio>', unsafe_allow_html=True)
            
            st.session_state.time_over = True
            st.rerun()

        else:
            st.success(f"انتهى الوقت! الإجابة الصحيحة هي: {q['a']}")
            
            # --- لوحة تحكم المدربة مرام (تظهر الفائزين بالسؤال) ---
            with st.expander("📊 لوحة تحكم المدربة مرام (عرض النتائج الحية)"):
                st.markdown("### ترتيب المتسابقين الحالي:")
                # تحويل البيانات لجدول مرتب
                leaderboard = pd.DataFrame(st.session_state.players_db.items(), columns=['اسم المتسابق', 'النقاط'])
                leaderboard = leaderboard.sort_values(by='النقاط', ascending=False)
                st.table(leaderboard)
                st.write(f"بطل السؤال الحالي: {leaderboard.iloc[0]['اسم المتسابق']} 🏆")

            if st.button("➡️ الانتقال للسؤال التالي"):
                st.session_state.time_over = False
                st.session_state.temp_choice = None
                st.session_state.current_q += 1
                st.rerun()
    else:
        st.session_state.game_stage = 'final'
        st.rerun()

# --- الشاشة النهائية ---
elif st.session_state.game_stage == 'final':
    st.balloons()
    st.markdown("<h1 style='text-align: center;'>🏆 منصة التتويج النهائية 🏆</h1>", unsafe_allow_html=True)
    df_final = pd.DataFrame(st.session_state.players_db.items(), columns=['الاسم', 'النقاط']).sort_values(by='النقاط', ascending=False)
    st.table(df_final)
    if st.button("إعادة المسابقة"): st.session_state.clear(); st.rerun()
