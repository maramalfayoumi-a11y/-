import streamlit as st
import time
import pandas as pd

# 1. إعدادات الهوية البصرية (د. مرام الفيومي)
st.set_page_config(page_title="Teacher Pro Master", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .stApp { background-color: #46178f; color: white; }
    .question-style { background: white; color: #46178f; padding: 25px; border-radius: 15px; text-align: center; font-size: 28px; font-weight: bold; margin-bottom: 20px; border: 4px solid #d89e00; }
    
    /* أزرار مضادة للاختفاء: نص أسود واضح جداً على خلفية فاتحة */
    div.stButton > button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 4px solid #d89e00 !important;
        height: 85px !important;
        font-size: 22px !important;
        font-weight: 900 !important;
        display: block !important;
    }
    .winner-tag { background: #26890c; color: white; padding: 15px; border-radius: 10px; text-align: center; font-size: 24px; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. الأسئلة الـ 10
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

# 3. إدارة الحالة (Session State)
if 'players' not in st.session_state: st.session_state.players = {}
if 'game_stage' not in st.session_state: st.session_state.game_stage = 'lobby'
if 'current_q' not in st.session_state: st.session_state.current_q = 0
if 'ans_status' not in st.session_state: st.session_state.ans_status = None

# --- شاشة اللوبي ---
if st.session_state.game_stage == 'lobby':
    st.title("🎮 قاعة انتظار Teacher Pro")
    st.subheader("بإشراف د. مرام الفيومي")
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

# --- شاشة الأسئلة ---
elif st.session_state.game_stage == 'quiz':
    idx = st.session_state.current_q
    if idx < len(questions):
        q = questions[idx]
        st.markdown(f"<div class='question-style'>السؤال {idx+1}: {q['q']}</div>", unsafe_allow_html=True)
        
        # إذا لم تتم الإجابة بعد
        if st.session_state.ans_status is None:
            cols = st.columns(2)
            for i, opt in enumerate(q['opts']):
                with cols[i % 2]:
                    if st.button(opt, key=f"q{idx}o{i}", use_container_width=True):
                        if opt == q['a']:
                            st.session_state.players[st.session_state.current_user] += 100
                            st.session_state.ans_status = "correct"
                        else:
                            st.session_state.ans_status = "wrong"
                        st.rerun()
        
        # بعد الإجابة: شاشة الانتظار والتعليق
        else:
            if st.session_state.ans_status == "correct":
                st.markdown(f"<div class='winner-tag'>✅ إجابة صحيحة! بطل السؤال هو: {st.session_state.current_user}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='winner-tag' style='background:#e21b3c;'>❌ إجابة خاطئة! الإجابة الصحيحة كانت: {q['a']}</div>", unsafe_allow_html=True)
            
            st.info("دكتورة مرام، يمكنكِ التعليق الآن قبل الانتقال...")
            if st.button("➡️ السؤال التالي"):
                st.session_state.ans_status = None
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
