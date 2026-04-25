import streamlit as st
import time
import pandas as pd

# 1. إعدادات الهوية (د. مرام الفيومي)
st.set_page_config(page_title="Teacher Pro Live", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .stApp { background-color: #46178f; color: white; }
    .question-style { background: white; color: #46178f; padding: 25px; border-radius: 15px; text-align: center; font-size: 28px; font-weight: bold; border: 4px solid #d89e00; box-shadow: 0 10px 20px rgba(0,0,0,0.2); }
    
    /* أزرار فائقة الوضوح */
    div.stButton > button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 4px solid #d89e00 !important;
        height: 85px !important;
        font-size: 22px !important;
        font-weight: 900 !important;
        display: block !important;
    }
    div.stButton > button:focus { background-color: #ffeb3b !important; border-color: #ff9800 !important; }
    .timer-text { font-size: 40px; font-weight: bold; color: #ff4b4b; background: white; border-radius: 50%; width: 90px; height: 90px; line-height: 90px; margin: 0 auto; border: 5px solid #ff4b4b; text-align: center; }
    .leaderboard-style { background: rgba(255,255,255,0.1); padding: 20px; border-radius: 15px; border: 2px solid #d89e00; }
    </style>
    """, unsafe_allow_html=True)

# 2. الوسائط
bg_music = "https://www.soundjay.com/free-music/sounds/action-movie-trailer-1.mp3"
correct_sfx = "https://www.soundjay.com/buttons/sounds/button-3.mp3"

# 3. قاعدة الأسئلة (10 أسئلة)
if 'questions_db' not in st.session_state:
    st.session_state.questions_db = [
        {"q": "أي الأدوار التالية يمثل 'المعلم كميسر' في بيئة التعلم الرقمي؟", "opts": ["إلقاء المحاضرة بدقة", "تصميم مسارات تعلم ذاتية", "مراقبة الحضور فقط", "تزويد الطلاب بملخصات"], "a": "تصميم مسارات تعلم ذاتية"},
        {"q": "المعلم الذي يمارس 'التأمل الذاتي' يقوم بـ:", "opts": ["مقارنة درجات طلابه", "تحليل أداءه لتطويره", "الالتزام بالدليل حرفياً", "زيادة الواجبات المنزلية"], "a": "تحليل أداءه لتطويره"},
        {"q": "لتحقيق 'الإدارة الصفية الذكية'، يفضل المعلم المحترف:", "opts": ["تعيين قادة ثابتين", "توزيع المهام بناءً على الميول", "منع النقاش الجانبي", "ترك الطلاب دون تدخل"], "a": "توزيع المهام بناءً على الميول"},
        {"q": "أي الممارسات تعزز 'المواطنة الرقمية' لدى الطلاب؟", "opts": ["منع الإنترنت بالكلية", "نقد وتقييم المحتوى الرقمي", "استخدام المنصات للمرح فقط", "حفظ كلمات المرور علانية"], "a": "نقد وتقييم المحتوى الرقمي"},
        {"q": "المعلم المحترف في بناء 'الشراكة المجتمعية' هو من:", "opts": ["يتواصل عند المشاكل فقط", "يشرك المجتمع في تطوير البيئة", "ينعزل بطلابه داخل الفصل", "يرفض تدخل أولياء الأمور"], "a": "يشرك المجتمع في تطوير البيئة"},
        {"q": "التغذية الراجعة 'البناءة' تركز أساساً على:", "opts": ["كشف الأخطاء السابقة", "كيفية تحسين الأداء مستقبلاً", "إعطاء الدرجة النهائية", "مدح الطالب دون توضيح"], "a": "كيفية تحسين الأداء مستقبلاً"},
        {"q": "عند تصميم 'بيئة تعلم محفزة'، الأولوية تكون لـ:", "opts": ["الديكور والألوان", "الأمان النفسي والاجتماعي", "أحدث أنواع الحواسيب", "الصمت التام للطلاب"], "a": "الأمان النفسي والاجتماعي"},
        {"q": "التخطيط الفعال للتدريس الناجح يبدأ من:", "opts": ["أول صفحة في الكتاب", "الأنشطة المتوفرة", "نتاجات التعلم المستهدفة", "عدد ساعات المحاضرة"], "a": "نتاجات التعلم المستهدفة"},
        {"q": "المعلم المبدع يستخدم التقنية في الفصل لـ:", "opts": ["شغل وقت الفراغ", "تعزيز التفكير الناقد والابتكار", "تجنب الكتابة على السبورة", "عرض صور جمالية فقط"], "a": "تعزيز التفكير الناقد والابتكار"},
        {"q": "الهدف الأسمى من برنامج 'Teacher Pro' هو:", "opts": ["حفظ الأدوات الرقمية", "صناعة معلم ملهم ومتمكن", "الحصول على شهادة حضور", "تعلم الطباعة السريعة"], "a": "صناعة معلم ملهم ومتمكن"}
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
    st.write(f"المتواجدون: {', '.join(st.session_state.players_db.keys())}")
    if len(st.session_state.players_db) > 0:
        if st.button("🚀 ابدأ المسابقة", use_container_width=True):
            st.session_state.game_stage = 'quiz'
            st.rerun()

# --- شاشة الأسئلة ---
elif st.session_state.game_stage == 'quiz':
    idx = st.session_state.current_q
    if idx < len(st.session_state.questions_db):
        q = st.session_state.questions_db[idx]
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
            
            if st.session_state.get('temp_choice') == q['a']:
                st.session_state.players_db[st.session_state.current_user] += 100
                st.markdown(f'<audio src="{correct_sfx}" autoplay></audio>', unsafe_allow_html=True)
            st.session_state.time_over = True
            st.rerun()

        else:
            # عرض النتيجة للجميع تلقائياً (نفس كاهوت)
            st.markdown(f"<div class='question-style' style='background:#d4edda; color:#155724;'>انتهى الوقت! الإجابة الصحيحة هي: {q['a']}</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='leaderboard-style'>", unsafe_allow_html=True)
            st.subheader("📊 لوحة الصدارة الحالية (تظهر للجميع)")
            ld = pd.DataFrame(st.session_state.players_db.items(), columns=['الاسم', 'النقاط']).sort_values(by='النقاط', ascending=False)
            st.table(ld)
            st.markdown("</div>", unsafe_allow_html=True)

            if st.button("➡️ الانتقال للسؤال التالي (تحكم المدربة)"):
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
    st.markdown("<h1 style='text-align: center;'>🏆 النتائج النهائية 🏆</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>إشراف د. مرام الفيومي</h3>", unsafe_allow_html=True)
    df_final = pd.DataFrame(st.session_state.players_db.items(), columns=['الاسم', 'النقاط']).sort_values(by='النقاط', ascending=False)
    st.table(df_final)
    if st.button("إعادة المسابقة"): st.session_state.clear(); st.rerun()
