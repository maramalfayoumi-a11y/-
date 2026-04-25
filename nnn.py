import streamlit as st
import time
import pandas as pd

# 1. إعدادات الهوية الأكاديمية د. مرام الفيومي
st.set_page_config(page_title="Teacher Pro Challenge", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .stApp { background-color: #46178f; color: white; }
    .main-card { background: white; color: #46178f; padding: 30px; border-radius: 20px; text-align: center; border: 5px solid #d89e00; margin-bottom: 20px; }
    div.stButton > button { background-color: #ffffff !important; color: #000000 !important; border: 3px solid #d89e00 !important; height: 70px !important; font-size: 20px !important; font-weight: bold !important; width: 100%; }
    .timer-text { font-size: 50px; font-weight: bold; color: #ff4b4b; background: white; border-radius: 50%; width: 100px; height: 100px; line-height: 100px; text-align: center; border: 5px solid #ff4b4b; margin: 0 auto; }
    .win-card { background: #d4edda; color: #155724; padding: 20px; border-radius: 15px; border: 2px solid #c3e6cb; font-size: 24px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. بنك الأسئلة الكامل (10 أسئلة)
if 'questions' not in st.session_state:
    st.session_state.questions = [
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

# 3. إدارة الحالة الحية
if 'scores' not in st.session_state: st.session_state.scores = {}
if 'step' not in st.session_state: st.session_state.step = 0
if 'status' not in st.session_state: st.session_state.status = 'setup'
if 'time_is_up' not in st.session_state: st.session_state.time_is_up = False

# --- واجهة البداية ---
if st.session_state.status == 'setup':
    st.markdown("<h1 style='text-align: center;'>🎮 مرحباً بكم في تحدي Teacher Pro</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>بإشراف د. مرام الفيومي</h3>", unsafe_allow_html=True)
    
    role = st.radio("اختر دورك:", ["طالب", "المدربة مرام (للتحكم)"], horizontal=True)
    name = st.text_input("ادخل اسمك:")
    
    if st.button("انضمام للعبة"):
        if name:
            st.session_state.my_name = name
            st.session_state.my_role = role
            if name not in st.session_state.scores: st.session_state.scores[name] = 0
            st.session_state.status = 'lobby'
            st.rerun()

# --- قاعة الانتظار ---
elif st.session_state.status == 'lobby':
    st.title("🛋️ قاعة الانتظار")
    st.write(f"المشاركون الآن: {list(st.session_state.scores.keys())}")
    if st.session_state.my_role == "المدربة مرام (للتحكم)":
        if st.button("🚀 ابدأ المسابقة للجميع"):
            st.session_state.status = 'quiz'
            st.session_state.start_time = time.time()
            st.rerun()
    else:
        st.info("بانتظار الدكتورة مرام لتبدأ المسابقة...")
        time.sleep(2)
        st.rerun()

# --- شاشة المسابقة ---
elif st.session_state.status == 'quiz':
    idx = st.session_state.step
    if idx < len(st.session_state.questions):
        q = st.session_state.questions[idx]
        st.markdown(f"<div class='main-card'>السؤال {idx+1}: {q['q']}</div>", unsafe_allow_html=True)
        
        # العداد
        elapsed = time.time() - st.session_state.start_time
        rem = max(0, 10 - int(elapsed))
        
        if rem > 0 and not st.session_state.time_is_up:
            st.markdown(f"<div class='timer-text'>{rem}</div>", unsafe_allow_html=True)
            cols = st.columns(2)
            for i, opt in enumerate(q['opts']):
                with cols[i % 2]:
                    if st.button(opt, key=f"btn_{idx}_{i}"):
                        st.session_state.last_ans = opt
            time.sleep(1)
            st.rerun()
        else:
            # كشف الفائز والترتيب (مثل كاهوت)
            st.session_state.time_is_up = True
            st.markdown(f"<div class='win-card'>✅ الإجابة الصحيحة هي: {q['a']}</div>", unsafe_allow_html=True)
            
            # احتساب النتيجة لمرة واحدة
            if 'last_q_calc' not in st.session_state or st.session_state.last_q_calc != idx:
                if st.session_state.get('last_ans') == q['a']:
                    st.session_state.scores[st.session_state.my_name] += 100
                st.session_state.last_q_calc = idx

            # لوحة الصدارة الحية بعد كل سؤال
            st.subheader("📊 لوحة الصدارة الحالية:")
            df = pd.DataFrame(st.session_state.scores.items(), columns=['الاسم', 'النقاط']).sort_values(by='النقاط', ascending=False)
            st.table(df)

            if st.session_state.my_role == "المدربة مرام (للتحكم)":
                if st.button("➡️ السؤال التالي"):
                    st.session_state.step += 1
                    st.session_state.time_is_up = False
                    st.session_state.last_ans = None
                    st.session_state.start_time = time.time()
                    st.rerun()
            else:
                st.info("بانتظار المدربة للانتقال للسؤال التالي...")
                time.sleep(3)
                st.rerun()
    else:
        st.session_state.status = 'final'
        st.rerun()

# --- النتائج النهائية ---
elif st.session_state.status == 'final':
    st.balloons()
    st.markdown("<h1 style='text-align: center;'>🏆 النتائج النهائية 🏆</h1>", unsafe_allow_html=True)
    df_f = pd.DataFrame(st.session_state.scores.items(), columns=['الاسم', 'النقاط']).sort_values(by='النقاط', ascending=False)
    st.table(df_f)
    if st.button("إعادة اللعبة"):
        st.session_state.clear()
        st.rerun()
