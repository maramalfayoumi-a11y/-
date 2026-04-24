import streamlit as st
import time
import pandas as pd

# 1. إعدادات الهوية البصرية (Kahoot Style)
st.set_page_config(page_title="تحدي المعلم المبدع", page_icon="🎓", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #46178f; color: white; direction: rtl; }
    .question-box { background-color: white; color: #46178f; padding: 25px; border-radius: 15px; text-align: center; font-size: 24px; font-weight: bold; margin-bottom: 20px; border: 4px solid #d89e00; }
    .stButton>button { width: 100%; height: 70px; font-size: 18px; font-weight: bold; color: white; border-radius: 12px; border: 2px solid rgba(255,255,255,0.2); transition: 0.3s; }
    /* ألوان الخيارات الأربعة */
    div.stButton > button:first-child { background-color: #e21b3c; } 
    div.stButton > button:nth-child(2) { background-color: #1368ce; }
    div.stButton > button:nth-child(3) { background-color: #d89e00; }
    div.stButton > button:nth-child(4) { background-color: #26890c; }
    .podium { text-align: center; padding: 20px; background: white; color: #46178f; border-radius: 20px; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. قاعدة البيانات (10 أسئلة عالية التفكير + صور)
if 'questions' not in st.session_state:
    st.session_state.questions = [
        {"q": "أي الأدوار التالية يمثل 'المعلم كميسر' (Facilitator) في بيئة التعلم الرقمي؟", "img": "https://img.freepik.com/free-vector/teacher-concept-illustration_114360-2166.jpg", "opts": ["إلقاء المحاضرة إلكترونياً بدقة", "تصميم مسارات تعلم ذاتية للطلبة", "مراقبة حضور الطلاب عبر المنصة", "تزويد الطلاب بملخصات جاهزة"], "a": "تصميم مسارات تعلم ذاتية للطلبة"},
        {"q": "عند تحليل نتائج الاختبار، وجد المعلم فجوة في مهارات التحليل لدى الطلاب، الإجراء الأنسب هو:", "img": "https://img.freepik.com/free-vector/data-extraction-concept-illustration_114360-4766.jpg", "opts": ["إعادة شرح الدرس بنفس الطريقة", "توجيه الطلاب لحفظ المفاهيم الأساسية", "تصميم أنشطة تعتمد على حل المشكلات", "تجاهل النتائج وضيق الوقت"], "a": "تصميم أنشطة تعتمد على حل المشكلات"},
        {"q": "المعلم الذي يمارس 'التأمل الذاتي' (Reflective Practice) يقوم بـ:", "img": "https://img.freepik.com/free-vector/thought-process-concept-illustration_114360-10145.jpg", "opts": ["مقارنة درجات طلابه بزملائه", "تحليل أداءه التدريسي لتطويره", "الالتزام الحرفي بدليل المعلم", "زيادة عدد الواجبات المنزلية"], "a": "تحليل أداءه التدريسي لتطويره"},
        {"q": "لتحقيق 'الإدارة الصفية الذكية' في مجموعات العمل، يفضل المعلم:", "img": "https://img.freepik.com/free-vector/team-goals-concept-illustration_114360-5175.jpg", "opts": ["تعيين قادة ثابتين طوال العام", "توزيع المهام بناءً على الميول والقدرات", "منع النقاش الجانبي تماماً", "ترك الطلاب دون تدخل توجيهي"], "a": "توزيع المهام بناءً على الميول والقدرات"},
        {"q": "أي من هذه الممارسات تعزز 'المواطنة الرقمية' لدى الطلاب؟", "img": "https://img.freepik.com/free-vector/privacy-policy-concept-illustration_114360-7853.jpg", "opts": ["منع استخدام الإنترنت في المدرسة", "تدريب الطلاب على نقد المحتوى الرقمي", "استخدام وسائل التواصل للمرح فقط", "حفظ كلمات المرور على أجهزة عامة"], "a": "تدريب الطلاب على نقد المحتوى الرقمي"},
        {"q": "المعلم المحترف في بناء 'الشراكة المجتمعية' هو الذي:", "img": "https://img.freepik.com/free-vector/community-concept-illustration_114360-8438.jpg", "opts": ["يتواصل مع أولياء الأمور عند المشاكل فقط", "يشرك المجتمع في تطوير البيئة التعليمية", "يقتصر دوره على داخل أسوار المدرسة", "يرفض تدخل المجتمع في المنهج"], "a": "يشرك المجتمع في تطوير البيئة التعليمية"},
        {"q": "التغذية الراجعة 'البناءة' هي التي تركز على:", "img": "https://img.freepik.com/free-vector/feedback-concept-illustration_114360-5040.jpg", "opts": ["تصحيح الأخطاء باللون الأحمر", "وصف كيفية تحسين الأداء مستقبلاً", "إعطاء درجة نهائية دون تعليق", "مدح الطالب بكلمات عامة دائماً"], "a": "وصف كيفية تحسين الأداء مستقبلاً"},
        {"q": "عند تصميم 'بيئة تعلم محفزة'، يراعي المعلم أولاً:", "img": "https://img.freepik.com/free-vector/creative-workspace-concept-illustration_114360-3125.jpg", "opts": ["جمال الديكورات الصفية", "الأمان النفسي والاجتماعي للطلاب", "توفر أحدث أجهزة الحواسيب", "هدوء الطلاب التام أثناء الحصة"], "a": "الأمان النفسي والاجتماعي للطلاب"},
        {"q": "التخطيط الفعال للتدريس يبدأ من:", "img": "https://img.freepik.com/free-vector/strategy-concept-illustration_114360-5444.jpg", "opts": ["أول صفحة في الكتاب المدرسي", "الأنشطة المتوفرة في المختبر", "نتاجات التعلم المستهدفة", "الوقت المتاح للحصة فقط"], "a": "نتاجات التعلم المستهدفة"},
        {"q": "أقصى درجات التمكن المهني للمعلم تظهر في:", "img": "https://img.freepik.com/free-vector/professional-growth-concept-illustration_114360-3622.jpg", "opts": ["قدرته على إنهاء المنهج مبكراً", "ابتكار حلول تعليمية لمواجهة التحديات", "صعوبة اختباراته التي يضعها للطلاب", "علاقته الرسمية مع الإدارة"], "a": "ابتكار حلول تعليمية لمواجهة التحديات"}
    ]

# 3. تهيئة الحالة
if 'score' not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_q = 0
    st.session_state.game_stage = 'start'

# 4. المنطق البرمجي
if st.session_state.game_stage == 'start':
    st.title("🏆 مسابقة المعلم المبدع (Teacher Pro)")
    st.subheader(f"د. مرام الفايومي")
    name = st.text_input("أدخل اسمك للمنافسة:")
    if st.button("دخول السباق 🚀"):
        if name:
            st.session_state.player_name = name
            st.session_state.game_stage = 'play'
            st.rerun()

elif st.session_state.game_stage == 'play':
    idx = st.session_state.current_q
    q = st.session_state.questions[idx]
    
    st.markdown(f"<div class='question-box'>{q['q']}</div>", unsafe_allow_html=True)
    st.image(q['img'], use_container_width=True)
    
    # حساب وقت البدء للسرعة
    if 'q_start' not in st.session_state:
        st.session_state.q_start = time.time()

    cols = st.columns(2)
    for i, opt in enumerate(q['opts']):
        with cols[i % 2]:
            if st.button(opt, key=f"btn_{idx}_{i}"):
                duration = time.time() - st.session_state.q_start
                if opt == q['a']:
                    # نقاط السرعة: 1000 - (الثواني * 50)
                    points = max(100, 1000 - int(duration * 50))
                    st.session_state.score += points
                    st.success(f"إجابة ذكية! +{points} نقطة")
                else:
                    st.error("للأسف، الإجابة تحتاج إعادة تفكير")
                
                time.sleep(1)
                if st.session_state.current_q < 9:
                    st.session_state.current_q += 1
                    del st.session_state.q_start
                else:
                    st.session_state.game_stage = 'podium'
                st.rerun()

elif st.session_state.game_stage == 'podium':
    st.balloons()
    st.markdown("<div class='podium'><h1>🎊 شاشة التتويج 🎊</h1>", unsafe_allow_html=True)
    
    # بيانات وهمية للمراكز الأخرى للمحاكاة
    leaderboard_data = [
        {"المركز": "🥇 الأول", "الاسم": st.session_state.player_name, "النقاط": st.session_state.score},
        {"المركز": "🥈 الثاني", "الاسم": "أحمد (مشارك)", "النقاط": 7550},
        {"المركز": "🥉 الثالث", "الاسم": "سارة (مشارِكة)", "النقاط": 6200}
    ]
    
    for row in leaderboard_data:
        st.write(f"### {row['المركز']}: {row['الاسم']} - {row['النقاط']} نقطة")
    
    if st.button("عرض ترتيب جميع الطلبة 📊"):
        st.session_state.game_stage = 'full_list'
        st.rerun()

elif st.session_state.game_stage == 'full_list':
    st.header("📊 القائمة الكاملة للمشاركين")
    full_list = [
        {"الترتيب": 1, "الاسم": st.session_state.player_name, "النقاط": st.session_state.score},
        {"الترتيب": 2, "الاسم": "أحمد", "النقاط": 7550},
        {"الترتيب": 3, "الاسم": "سارة", "النقاط": 6200},
        {"الترتيب": 4, "الاسم": "خالد", "النقاط": 5800},
        {"الترتيب": 5, "الاسم": "ليلى", "النقاط": 4200}
    ]
    st.table(pd.DataFrame(full_list))
    
    if st.button("العودة للبداية"):
        st.session_state.game_stage = 'start'
        st.session_state.score = 0
        st.session_state.current_q = 0
        st.rerun()
