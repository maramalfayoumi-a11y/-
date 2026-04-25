import streamlit as st
import time

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="Teacher Pro Challenge", page_icon="🎓", layout="wide")

# 2. تنسيق مبسط ومضمون للظهور
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .stApp { background-color: #46178f; color: white; }
    .question-style { background: white; color: #46178f; padding: 20px; border-radius: 10px; text-align: center; font-size: 24px; font-weight: bold; margin-bottom: 20px; }
    /* تنسيق اسم المتسابق في اللوبي */
    .name-tag { background: #d89e00; color: white; padding: 5px 15px; border-radius: 20px; margin: 5px; display: inline-block; }
    </style>
    """, unsafe_allow_html=True)

# 3. قاعدة البيانات (الـ 10 أسئلة)
if 'questions' not in st.session_state:
    st.session_state.questions = [
        {"q": "أي الأدوار التالية يمثل 'المعلم كميسر' في بيئة التعلم الرقمي؟", "opts": ["🔴 إلقاء المحاضرة بدقة", "🔵 تصميم مسارات تعلم ذاتية", "🟡 مراقبة الحضور فقط", "🟢 تزويد الطلاب بملخصات"], "a": "🔵 تصميم مسارات تعلم ذاتية"},
        {"q": "المعلم الذي يمارس 'التأمل الذاتي' يقوم بـ:", "opts": ["🔴 مقارنة درجات طلابه", "🔵 تحليل أداءه لتطويره", "🟡 الالتزام بالدليل حرفياً", "🟢 زيادة الواجبات المنزلية"], "a": "🔵 تحليل أداءه لتطويره"},
        {"q": "لتحقيق 'الإدارة الصفية الذكية'، يفضل المعلم المحترف:", "opts": ["🔴 تعيين قادة ثابتين", "🔵 توزيع المهام بناءً على الميول", "🟡 منع النقاش الجانبي", "🟢 ترك الطلاب دون تدخل"], "a": "🔵 توزيع المهام بناءً على الميول"},
        {"q": "أي الممارسات تعزز 'المواطنة الرقمية' لدى الطلاب؟", "opts": ["🔴 منع الإنترنت بالكلية", "🔵 نقد وتقييم المحتوى الرقمي", "🟡 استخدام المنصات للمرح فقط", "🟢 حفظ كلمات المرور علانية"], "a": "🔵 نقد وتقييم المحتوى الرقمي"},
        {"q": "المعلم المحترف في بناء 'الشراكة المجتمعية' هو من:", "opts": ["🔴 يتواصل عند المشاكل فقط", "🔵 يشرك المجتمع في تطوير البيئة", "🟡 ينعزل بطلابه داخل الفصل", "🟢 يرفض تدخل أولياء الأمور"], "a": "🔵 يشرك المجتمع في تطوير البيئة"},
        {"q": "التغذية الراجعة 'البناءة' تركز أساساً على:", "opts": ["🔴 كشف الأخطاء السابقة", "🔵 كيفية تحسين الأداء مستقبلاً", "🟡 إعطاء الدرجة النهائية", "🟢 مدح الطالب دون توضيح"], "a": "🔵 كيفية تحسين الأداء مستقبلاً"},
        {"q": "عند تصميم 'بيئة تعلم محفزة'، الأولوية تكون لـ:", "opts": ["🔴 الديكور والألوان", "🔵 الأمان النفسي والاجتماعي", "🟡 أحدث أنواع الحواسيب", "🟢 الصمت التام للطلاب"], "a": "🔵 الأمان النفسي والاجتماعي"},
        {"q": "التخطيط الفعال للتدريس الناجح يبدأ من:", "opts": ["🔴 أول صفحة في الكتاب", "🔵 الأنشطة المتوفرة", "🟡 نتاجات التعلم المستهدفة", "🟢 عدد ساعات المحاضرة"], "a": "🔵 نتاجات التعلم المستهدفة"},
        {"q": "المعلم المبدع يستخدم التقنية في الفصل لـ:", "opts": ["🔴 شغل وقت الفراغ", "🔵 تعزيز التفكير الناقد والابتكار", "🟡 تجنب الكتابة على السبورة", "🟢 عرض صور جمالية فقط"], "a": "🔵 تعزيز التفكير الناقد والابتكار"},
        {"q": "الهدف الأسمى من برنامج 'Teacher Pro' هو:", "opts": ["🔴 حفظ الأدوات الرقمية", "🔵 صناعة معلم ملهم ومتمكن", "🟡 الحصول على شهادة حضور", "🟢 تعلم الطباعة السريعة"], "a": "🔵 صناعة معلم ملهم ومتمكن"}
    ]

# 4. إدارة الحالة
if 'players' not in st.session_state: st.session_state.players = []
if 'game_stage' not in st.session_state: st.session_state.game_stage = 'lobby'
if 'current_q' not in st.session_state: st.session_state.current_q = 0
if 'score' not in st.session_state: st.session_state.score = 0

# --- شاشة اللوبي ---
if st.session_state.game_stage == 'lobby':
    st.header("🎮 قاعة انتظار مسابقة Teacher Pro")
    st.subheader(f"إشراف الدكتورة: مرام الفيومي")
    
    col_reg, col_list = st.columns([1, 1])
    with col_reg:
        name_input = st.text_input("اكتب اسمك هنا:", key="user_name")
        if st.button("انضمام للسباق 🏃‍♂️"):
            if name_input and name_input not in st.session_state.players:
                st.session_state.players.append(name_input)
                st.session_state.player_identity = name_input
                st.rerun()
                
    with col_list:
        st.write(f"👥 المتسابقون الآن: {len(st.session_state.players)}")
        for p in st.session_state.players:
            st.markdown(f"<span class='name-tag'>{p}</span>", unsafe_allow_html=True)

    if len(st.session_state.players) > 0:
        st.divider()
        if st.button("🚀 ابدأ التحدي الآن!", use_container_width=True):
            st.session_state.game_stage = 'play'
            st.rerun()

# --- شاشة الأسئلة ---
elif st.session_state.game_stage == 'play':
    idx = st.session_state.current_q
    if idx < len(st.session_state.questions):
        q = st.session_state.questions[idx]
        
        st.markdown(f"<div class='question-style'>سؤال {idx+1}: {q['q']}</div>", unsafe_allow_html=True)
        
        # أزرار واضحة جداً وبسيطة
        c1, c2 = st.columns(2)
        with c1:
            choice1 = st.button(q['opts'][0], use_container_width=True)
            choice2 = st.button(q['opts'][1], use_container_width=True)
        with c2:
            choice3 = st.button(q['opts'][2], use_container_width=True)
            choice4 = st.button(q['opts'][3], use_container_width=True)
            
        # تحديد الاختيار
        user_choice = None
        if choice1: user_choice = q['opts'][0]
        if choice2: user_choice = q['opts'][1]
        if choice3: user_choice = q['opts'][2]
        if choice4: user_choice = q['opts'][3]
        
        if user_choice:
            if user_choice == q['a']:
                st.session_state.score += 100
                st.success("✅ إجابة صحيحة!")
            else:
                st.error(f"❌ إجابة خاطئة! الصحيح هو: {q['a']}")
            
            time.sleep(1)
            st.session_state.current_q += 1
            st.rerun()
    else:
        st.session_state.game_stage = 'finish'
        st.rerun()

# --- شاشة النهاية ---
elif st.session_state.game_stage == 'finish':
    st.balloons()
    st.header("🏆 النتائج النهائية")
    st.write(f"المبدع/ة: **{st.session_state.get('player_identity', 'مشارك')}**")
    st.subheader(f"مجموع نقاطك: {st.session_state.score} / 1000")
    
    if st.button("العودة للبداية"):
        st.session_state.clear()
        st.rerun()
