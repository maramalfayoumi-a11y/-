import streamlit as st
import time
import pandas as pd

# 1. إعدادات الهوية البصرية (تصحيح التنسيق والأزرار)
st.set_page_config(page_title="Teacher Pro Challenge", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .stApp { background-color: #46178f; color: white; }
    .lobby-title { text-align: center; font-size: 45px; font-weight: bold; color: #d89e00; }
    .instructor { text-align: center; font-size: 22px; margin-bottom: 20px; }
    .question-text { background: white; color: #46178f; padding: 25px; border-radius: 15px; 
                     text-align: center; font-size: 28px; font-weight: bold; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
    
    /* جعل الأزرار مرئية دائماً وواضحة */
    .stButton > button {
        width: 100% !important;
        height: 90px !important;
        font-size: 22px !important;
        font-weight: bold !important;
        color: white !important;
        border-radius: 15px !important;
        margin-bottom: 10px !important;
        border: none !important;
        opacity: 1 !important; /* ضمان الظهور الدائم */
        display: block !important;
    }
    /* ألوان كاهوت الثابتة */
    .btn-red button { background-color: #e21b3c !important; }
    .btn-blue button { background-color: #1368ce !important; }
    .btn-yellow button { background-color: #d89e00 !important; }
    .btn-green button { background-color: #26890c !important; }
    
    .name-bubble { background-color: white; color: #46178f; padding: 10px 20px; border-radius: 50px; 
                   font-size: 20px; font-weight: bold; margin: 5px; display: inline-block; border: 2px solid #d89e00; }
    </style>
    """, unsafe_allow_html=True)

# 2. قاعدة البيانات الشاملة (10 أسئلة عالية التفكير)
if 'questions' not in st.session_state:
    st.session_state.questions = [
        {"q": "أي الأدوار التالية يمثل 'المعلم كميسر' في بيئة التعلم الرقمي؟", "img": "https://img.freepik.com/free-vector/teacher-concept-illustration_114360-2166.jpg", "opts": ["إلقاء المحاضرة بدقة", "تصميم مسارات تعلم ذاتية", "مراقبة الحضور فقط", "تزويد الطلاب بملخصات"], "a": "تصميم مسارات تعلم ذاتية"},
        {"q": "المعلم الذي يمارس 'التأمل الذاتي' (Reflective Practice) يقوم بـ:", "img": "https://img.freepik.com/free-vector/thought-process-concept-illustration_114360-10145.jpg", "opts": ["مقارنة درجات طلابه", "تحليل أداءه لتطويره", "الالتزام بالدليل حرفياً", "زيادة الواجبات المنزلية"], "a": "تحليل أداءه لتطويره"},
        {"q": "لتحقيق 'الإدارة الصفية الذكية'، يفضل المعلم المحترف:", "img": "https://img.freepik.com/free-vector/team-goals-concept-illustration_114360-5175.jpg", "opts": ["تعيين قادة ثابتين", "توزيع المهام بناءً على الميول", "منع النقاش الجانبي", "ترك الطلاب دون تدخل"], "a": "توزيع المهام بناءً على الميول"},
        {"q": "أي الممارسات تعزز 'المواطنة الرقمية' لدى الطلاب؟", "img": "https://img.freepik.com/free-vector/privacy-policy-concept-illustration_114360-7853.jpg", "opts": ["منع الإنترنت بالكلية", "نقد وتقييم المحتوى الرقمي", "استخدام المنصات للمرح فقط", "حفظ كلمات المرور علانية"], "a": "نقد وتقييم المحتوى الرقمي"},
        {"q": "المعلم المحترف في بناء 'الشراكة المجتمعية' هو من:", "img": "https://img.freepik.com/free-vector/community-concept-illustration_114360-8438.jpg", "opts": ["يتواصل عند المشاكل فقط", "يشرك المجتمع في تطوير البيئة", "ينعزل بطلابه داخل الفصل", "يرفض تدخل أولياء الأمور"], "a": "يشرك المجتمع في تطوير البيئة"},
        {"q": "التغذية الراجعة 'البناءة' تركز أساساً على:", "img": "https://img.freepik.com/free-vector/feedback-concept-illustration_114360-5040.jpg", "opts": ["كشف الأخطاء السابقة", "كيفية تحسين الأداء مستقبلاً", "إعطاء الدرجة النهائية", "مدح الطالب دون توضيح"], "a": "كيفية تحسين الأداء مستقبلاً"},
        {"q": "عند تصميم 'بيئة تعلم محفزة'، الأولوية تكون لـ:", "img": "https://img.freepik.com/free-vector/creative-workspace-concept-illustration_114360-3125.jpg", "opts": ["الديكور والألوان", "الأمان النفسي والاجتماعي", "أحدث أنواع الحواسيب", "الصمت التام للطلاب"], "a": "الأمان النفسي والاجتماعي"},
        {"q": "التخطيط الفعال للتدريس الناجح يبدأ من:", "img": "https://img.freepik.com/free-vector/strategy-concept-illustration_114360-5444.jpg", "opts": ["أول صفحة في الكتاب", "الأنشطة المتوفرة", "نتاجات التعلم المستهدفة", "عدد ساعات المحاضرة"], "a": "نتاجات التعلم المستهدفة"},
        {"q": "المعلم المبدع يستخدم التقنية في الفصل لـ:", "img": "https://img.freepik.com/free-vector/creative-team-concept-illustration_114360-3754.jpg", "opts": ["شغل وقت الفراغ", "تعزيز التفكير الناقد والابتكار", "تجنب الكتابة على السبورة", "عرض صور جمالية فقط"], "a": "تعزيز التفكير الناقد والابتكار"},
        {"q": "الهدف الأسمى من برنامج 'Teacher Pro' هو:", "img": "https://img.freepik.com/free-vector/professional-growth-concept-illustration_114360-3622.jpg", "opts": ["حفظ الأدوات الرقمية", "صناعة معلم ملهم ومتمكن", "الحصول على شهادة حضور", "تعلم الطباعة السريعة"], "a": "صناعة معلم ملهم ومتمكن"}
    ]

# 3. إدارة الحالة
if 'players' not in st.session_state: st.session_state.players = []
if 'game_stage' not in st.session_state: st.session_state.game_stage = 'lobby'
if 'current_q' not in st.session_state: st.session_state.current_q = 0
if 'score' not in st.session_state: st.session_state.score = 0

# --- المرحلة 1: شاشة اللوبي (Lobby) ---
if st.session_state.game_stage == 'lobby':
    st.markdown("<div class='lobby-title'>🎮 قاعة انتظار مسابقة Teacher Pro</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='instructor'>إشراف الدكتورة: مرام الفيومي</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("📝 سجل اسمك")
        name_input = st.text_input("اكتب اسمك هنا:", key="p_name")
        if st.button("انضمام للسباق 🏃‍♂️"):
            if name_input and name_input not in st.session_state.players:
                st.session_state.players.append(name_input)
                st.session_state.my_name = name_input
                st.rerun()
    with col2:
        st.subheader(f"👥 المتسابقون ({len(st.session_state.players)})")
        if st.session_state.players:
            bubbles = "".join([f"<div class='name-bubble'>{n}</div>" for n in st.session_state.players])
            st.markdown(bubbles, unsafe_allow_html=True)

    if len(st.session_state.players) > 0:
        if st.button("🚀 ارفع الستار وابدأ التحدي!", use_container_width=True):
            st.session_state.game_stage = 'quiz'
            st.rerun()

# --- المرحلة 2: شاشة الأسئلة ---
elif st.session_state.game_stage == 'quiz':
    idx = st.session_state.current_q
    if idx < len(st.session_state.questions):
        q = st.session_state.questions[idx]
        st.markdown(f"<div class='question-text'>سؤال {idx+1}: {q['q']}</div>", unsafe_allow_html=True)
        st.image(q['img'], width=500)
        
        # عرض الأزرار بتنسيق كاهوت (ثابتة وواضحة)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="btn-red">', unsafe_allow_html=True)
            if st.button(f"▲ {q['opts'][0]}", key=f"b{idx}0"): choice = q['opts'][0]
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="btn-blue">', unsafe_allow_html=True)
            if st.button(f"◆ {q['opts'][1]}", key=f"b{idx}1"): choice = q['opts'][1]
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="btn-yellow">', unsafe_allow_html=True)
            if st.button(f"● {q['opts'][2]}", key=f"b{idx}2"): choice = q['opts'][2]
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="btn-green">', unsafe_allow_html=True)
            if st.button(f"■ {q['opts'][3]}", key=f"b{idx}3"): choice = q['opts'][3]
            st.markdown('</div>', unsafe_allow_html=True)
        
        if 'choice' in locals():
            if choice == q['a']:
                st.session_state.score += 100
                st.balloons()
                st.success("✅ إجابة صحيحة!")
            else: st.error(f"❌ إجابة خاطئة! الصحيح هو: {q['a']}")
            time.sleep(1.5)
            st.session_state.current_q += 1
            st.rerun()
    else:
        st.session_state.game_stage = 'results'
        st.rerun()

# --- المرحلة 3: شاشة النتائج النهائية ---
elif st.session_state.game_stage == 'results':
    st.balloons()
    st.markdown("<h1 style='text-align: center; color: #d89e00;'>🏆 لوحة شرف المعلم المحترف 🏆</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>مبارك للأستاذ/ة: {st.session_state.get('my_name', 'المبدع')}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>مجموع النقاط: {st.session_state.score} / 1000</h3>", unsafe_allow_html=True)
    
    if st.button("العودة للقاعة الرئيسية"):
        st.session_state.clear()
        st.rerun()
