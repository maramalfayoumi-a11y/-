import streamlit as st
import time
import pandas as pd

# إعدادات الصفحة والهوية البصرية
st.set_page_config(page_title="تحدي المعلم المحترف | د. مرام الفايومي", page_icon="🎓", layout="centered")

# تصميم الواجهة (CSS) لجعلها جذابة
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .main-title { color: #2E7D32; text-align: center; font-size: 3rem; font-weight: bold; }
    .question-box { 
        background-color: #ffffff; 
        padding: 25px; 
        border-radius: 15px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-right: 8px solid #2E7D32;
        margin-bottom: 20px;
    }
    .stButton>button { 
        background-color: #2E7D32; 
        color: white; 
        border-radius: 25px; 
        padding: 10px 25px;
        font-size: 1.2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# تهيئة بيانات اللعبة
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'login'
    st.session_state.score = 0
    st.session_state.current_q = 0
    st.session_state.leaderboard = []

# قائمة الأسئلة العشرة (نسخة د. مرام الفايومي)
questions = [
    {"q": "عند حدوث فوضى رقمية داخل الصف الافتراضي، التصرف الأذكى للمعلم هو:", "opts": ["أ- إغلاق الميكروفونات عن الجميع فوراً", "ب- تجاهل الفوضى والاستمرار في الشرح", "ج- طرح سؤال تفاعلي مفاجئ يتطلب إجابة سريعة", "د- توعد الطلاب بخصم نقاط المشاركة"], "a": "ج- طرح سؤال تفاعلي مفاجئ يتطلب إجابة سريعة"},
    {"q": "المعلم المحترف يختار الوسيلة التعليمية بناءً على:", "opts": ["أ- حداثة التقنية المستخدمة فيها", "ب- توصية إدارة المدرسة أو الكلية", "ج- ملاءمتها لخصائص المتعلمين وأهداف الدرس", "د- سهولة تشغيلها لضمان عدم حدوث أعطال"], "a": "ج- ملاءمتها لخصائص المتعلمين وأهداف الدرس"},
    {"q": "في التعليم المدمج (Blended Learning)، الدور الجوهري للمعلم هو:", "opts": ["أ- تقديم المحتوى العلمي بشكل مباشر", "ب- مراقبة حضور وغياب الطلاب إلكترونياً", "ج- تيسير عملية التعلم وتوجيه المسارات الرقمية", "د- تصحيح الواجبات الورقية والإلكترونية"], "a": "ج- تيسير عملية التعلم وتوجيه المسارات الرقمية"},
    {"q": "أي من هذه الصفات هي 'الأكثر تأثيراً' في نجاح المعلم الرقمي؟", "opts": ["أ- السرعة العالية في الكتابة", "ب- المرونة المعرفية والقدرة على التعلم المستمر", "ج- حفظ جميع أوامر برامج الأوفيس", "د- امتلاك أحدث نسخة من الحاسوب"], "a": "ب- المرونة المعرفية والقدرة على التعلم المستمر"},
    {"q": "عند تصميم عرض تقديمي (Canva مثلاً)، يركز المعلم المحترف على:", "opts": ["أ- كثرة الرسوم المتحركة لجذب الانتباه", "ب- وضع أكبر قدر ممكن من المعلومات", "ج- التوازن بين النص والمساحات البيضاء لتقليل الحمل المعرفي", "د- استخدام ألوان صارخة وخطوط مزخرفة"], "a": "ج- التوازن بين النص والمساحات البيضاء لتقليل الحمل المعرفي"},
    {"q": "الذكاء الاصطناعي في نظر المعلم المحترف هو:", "opts": ["أ- أداة لكتابة الأبحاث بدلاً من الطلاب", "ب- بديل مستقبلي لدور المعلم في الصف", "ج- مساعد ذكي لتخصيص التعلم وتقليل المهام الروتينية", "د- مجرد صيحة مؤقتة في عالم التكنولوجيا"], "a": "ج- مساعد ذكي لتخصيص التعلم وتقليل المهام الروتينية"},
    {"q": "التغذية الراجعة الرقمية الفعالة يجب أن تكون:", "opts": ["أ- في نهاية الفصل الدراسي فقط", "ب- مختصرة جداً (مثل: ممتاز)", "ج- فورية، محددة، ومرتبطة بالأداء مباشرة", "د- علنية أمام الجميع لزيادة المنافسة"], "a": "ج- فورية، محددة، ومرتبطة بالأداء مباشرة"},
    {"q": "المواطنة الرقمية لدى المعلم المحترف تعني:", "opts": ["أ- تعليم الطلاب كيفية استخدام الإنترنت بسرعة", "ب- غرس قيم الاستخدام الآمن والأخلاقي للتكنولوجيا", "ج- منع الطلاب من استخدام الهواتف نهائياً", "د- امتلاك حسابات على جميع المنصات"], "a": "ب- غرس قيم الاستخدام الآمن والأخلاقي للتكنولوجيا"},
    {"q": "في استراتيجية 'الصف المقلوب'، متى يشاهد الطالب المحتوى الأساسي؟", "opts": ["أ- أثناء المحاضرة مع المعلم", "ب- قبل وقت المحاضرة (في المنزل)", "ج- بعد انتهاء الفصل كمرجع", "د- خلال الاختبارات النهائية فقط"], "a": "ب- قبل وقت المحاضرة (في المنزل)"},
    {"q": "الهدف الأسمى من Teacher Pro هو تحويل المعلم من ملقن إلى:", "opts": ["أ- خبير تقني في إصلاح الحواسيب", "ب- مراقب أكاديمي صارم", "ج- مصمم لبيئات تعلم تفاعلية وملهمة", "د- مستخدم جيد لمنصات التواصل"], "a": "ج- مصمم لبيئات تعلم تفاعلية وملهمة"}
]

# مرحلة تسجيل الدخول
if st.session_state.game_state == 'login':
    st.markdown("<div class='main-title'>🎓 تحدي المعلم المحترف</div>", unsafe_allow_html=True)
    st.write("---")
    player_name = st.text_input("أدخل اسمك الكريم للانضمام للمنافسة:", placeholder="مثال: د. مرام")
    if st.button("بدأ السباق 🚀"):
        if player_name:
            st.session_state.player_name = player_name
            st.session_state.game_state = 'quiz'
            st.session_state.start_time = time.time()
            st.rerun()
        else:
            st.warning("يرجى إدخال الاسم أولاً")

# مرحلة الأسئلة
elif st.session_state.game_state == 'quiz':
    q_idx = st.session_state.current_q
    
    if q_idx < len(questions):
        st.progress((q_idx) / len(questions))
        st.write(f"**السؤال {q_idx + 1} من {len(questions)}**")
        
        # عرض السؤال في صندوق أنيق
        st.markdown(f"<div class='question-box'><h3>{questions[q_idx]['q']}</h3></div>", unsafe_allow_html=True)
        
        # تسجيل وقت بداية عرض السؤال
        if 'q_start_time' not in st.session_state:
            st.session_state.q_start_time = time.time()

        # عرض الخيارات
        user_choice = st.radio("اختر الإجابة الأدق:", questions[q_idx]['opts'])

        if st.button("تأكيد الإجابة ✔️"):
            q_end_time = time.time()
            elapsed_time = q_end_time - st.session_state.q_start_time
            
            if user_choice == questions[q_idx]['a']:
                # نظام نقاط يعاقب على التأخير: 100 نقطة - (عدد الثواني * 2)
                bonus_points = max(10, int(100 - (elapsed_time * 2)))
                st.session_state.score += bonus_points
                st.success(f"إجابة عبقرية! +{bonus_points} نقطة سرعة")
            else:
                st.error(f"للأسف، الإجابة الأصح تربوياً هي: {questions[q_idx]['a']}")
            
            time.sleep(1)
            st.session_state.current_q += 1
            del st.session_state.q_start_time
            st.rerun()
    else:
        st.session_state.game_state = 'result'
        st.rerun()

# مرحلة إعلان الفائز والترتيب
elif st.session_state.game_state == 'result':
    st.balloons()
    st.markdown("<div class='main-title'>🎊 انتهى التحدي بنجاح 🎊</div>", unsafe_allow_html=True)
    st.write(f"### المبدع/ة: **{st.session_state.player_name}**")
    st.header(f"مجموع نقاطك: {st.session_state.score}")
    
    st.divider()
    st.subheader("📊 لوحة الصدارة (ترتيب اللاعبين)")
    
    # محاكاة بيانات لاعبين آخرين للمنافسة
    mock_data = [
        {"اللاعب": st.session_state.player_name, "النقاط": st.session_state.score, "الحالة": "أنت"},
        {"اللاعب": "د. مرام الفيومي", "النقاط": 980, "الحالة": "المدرب"},
        {"اللاعب": "أحمد (مشارك)", "النقاط": 750, "الحالة": "متصل"},
        {"اللاعب": "سارة (مشارك)", "النقاط": 820, "الحالة": "متصل"}
    ]
    df = pd.DataFrame(mock_data).sort_values(by="النقاط", ascending=False)
    
    # عرض الجدول بشكل أنيق
    st.table(df)

    if st.button("إعادة اللعبة 🔄"):
        st.session_state.game_state = 'login'
        st.session_state.score = 0
        st.session_state.current_q = 0
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("تم تطوير هذه اللعبة لدعم برنامج **Teacher Pro** تحت إشراف **د. مرام الفايومي**.")
