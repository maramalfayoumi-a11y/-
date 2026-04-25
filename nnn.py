import streamlit as st
import time
import pandas as pd

# 1. الإعدادات العامة لهوية د. مرام الفيومي
st.set_page_config(page_title="Teacher Pro Master", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .stApp { background-color: #46178f; color: white; }
    .question-style { background: white; color: #46178f; padding: 25px; border-radius: 15px; text-align: center; font-size: 28px; font-weight: bold; margin-bottom: 20px; border: 4px solid #d89e00; }
    
    /* أزرار مضادة للاختفاء: نص أسود واضح جداً */
    div.stButton > button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 4px solid #d89e00 !important;
        height: 85px !important;
        font-size: 22px !important;
        font-weight: 900 !important;
        display: block !important;
    }
    .timer-text { font-size: 35px; font-weight: bold; color: #ff0000; text-align: center; background: white; border-radius: 50%; width: 80px; height: 80px; line-height: 80px; margin: 0 auto; border: 3px solid #ff0000; }
    .winner-tag { background: #26890c; color: white; padding: 15px; border-radius: 10px; text-align: center; font-size: 24px; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. روابط الأصوات والموسيقى
bg_music = "https://www.soundjay.com/free-music/sounds/action-movie-trailer-1.mp3" # موسيقى حماسية
correct_sound = "https://www.soundjay.com/buttons/sounds/button-3.mp3"
wrong_sound = "https://www.soundjay.com/buttons/sounds/button-10.mp3"

def play_audio(url):
    st.markdown(f'<audio src="{url}" autoplay loop></audio>', unsafe_allow_html=True)

def play_sfx(url):
    st.markdown(f'<audio src="{url}" autoplay></audio>', unsafe_allow_html=True)

# 3. الأسئلة الـ 10
questions = [
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

# 4. إدارة الحالة
if 'players' not in st.session_state: st.session_state.players = {}
if 'game_stage' not in st.session_state: st.session_state.game_stage = 'lobby'
if 'current_q' not in st.session_state: st.session_state.current_q = 0
if 'ans_locked' not in st.session_state: st.session_state.ans_locked = False

# --- شاشة اللوبي ---
if st.session_state.game_stage == 'lobby':
    st.markdown("<h1 style='text-align: center;'>🎮 قاعة انتظار Teacher Pro</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>بإشراف د. مرام الفيومي</h3>", unsafe_allow_html=True)
    
    name = st.text_input("📝 انضم الآن باسمك:")
    if st.button("دخول المسابقة"):
        if name:
            st.session_state.players[name] = 0
            st.session_state.current_user = name
            st.rerun()
    
    st.write(f"المتواجدون: {', '.join(st.session_state.players.keys())}")
    if len(st.session_state.players) > 0:
        if st.button("🚀 ابدأ المسابقة الآن", use_container_width=True):
            st.session_state.game_stage = 'quiz'
            st.rerun()

# --- شاشة الأسئلة مع العداد ---
elif st.session_state.game_stage == 'quiz':
    idx = st.session_state.current_q
    if idx < len(questions):
        q = questions[idx]
        play_audio(bg_music) # تشغيل الموسيقى الحماسية
        
        st.markdown(f"<div class='question-style'>السؤال {idx+1}: {q['q']}</div>", unsafe_allow_html=True)
        
        # عداد الـ 60 ثانية
        timer_placeholder = st.empty()
        
        cols = st.columns(2)
        user_choice = None
        
        # إذا لم يختَر الطالب بعد والوقت متاح
        if not st.session_state.ans_locked:
            for i, opt in enumerate(q['opts']):
                with cols[i % 2]:
                    if st.button(opt, key=f"q{idx}o{i}", use_container_width=True):
                        user_choice = opt
                        st.session_state.ans_locked = True
                        st.session_state.last_choice = opt
                        if opt == q['a']:
                            st.session_state.players[st.session_state.current_user] += 100
                            play_sfx(correct_sound)
                        else:
                            play_sfx(wrong_sound)
                        st.rerun()

            # تشغيل العداد 60 ثانية
            for seconds in range(60, -1, -1):
                timer_placeholder.markdown(f"<div class='timer-text'>{seconds}</div>", unsafe_allow_html=True)
                time.sleep(1)
                if st.session_state.ans_locked: break # يتوقف العداد إذا أجاب الطالب
            
            if seconds == 0:
                st.session_state.ans_locked = True
                st.session_state.last_choice = "انتهى الوقت"
                st.rerun()
        
        # شاشة الانتظار (بعد الإجابة أو انتهاء الوقت)
        else:
            st.markdown(f"<div class='winner-tag'>انتهى وقت السؤال! الإجابة الصحيحة: {q['a']}</div>", unsafe_allow_html=True)
            st.info("دكتورة مرام، بانتظار أمرك للانتقال للسؤال التالي...")
            if st.button("➡️ الانتقال للسؤال التالي"):
                st.session_state.ans_locked = False
                st.session_state.current_q += 1
                st.rerun()
                
    else:
        st.session_state.game_stage = 'final'
        st.rerun()

# --- الشاشة النهائية ---
elif st.session_state.game_stage == 'final':
    st.balloons()
    st.header("🏆 لوحة النتائج النهائية")
    st.subheader(f"إشراف د. مرام الفيومي")
    df = pd.DataFrame(st.session_state.players.items(), columns=['الاسم', 'النقاط']).sort_values(by='النقاط', ascending=False)
    st.table(df)
    if st.button("إعادة"): 
        st.session_state.clear()
        st.rerun()
