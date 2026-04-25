import streamlit as st
import time
import pandas as pd

# 1. إعدادات الصفحة وهوية مرام الفيومي التعليمية
st.set_page_config(page_title="Teacher Pro Quiz", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .stApp { background-color: #46178f; color: white; }
    
    /* صندوق السؤال ليكون واضحاً جداً */
    .question-style { 
        background: #ffffff; color: #46178f; padding: 30px; 
        border-radius: 20px; text-align: center; font-size: 30px; 
        font-weight: bold; margin-bottom: 25px; border: 5px solid #d89e00;
    }

    /* إصلاح الأزرار لتكون مرئية 100% بدون تمرير الماوس */
    div.stButton > button {
        background-color: #f0f2f6 !important; /* لون فاتح للخلفية */
        color: #46178f !important;           /* لون داكن للنص لضمان الرؤية */
        border: 4px solid #d89e00 !important;
        height: 100px !important;
        font-size: 24px !important;
        font-weight: 900 !important;
        border-radius: 15px !important;
        opacity: 1 !important;
        display: block !important;
        visibility: visible !important;
    }
    
    /* هوية د. مرام في اللوبي */
    .lobby-card { background: rgba(255,255,255,0.1); padding: 20px; border-radius: 20px; border: 1px solid #d89e00; }
    .name-bubble { background: white; color: #46178f; padding: 10px 20px; border-radius: 50px; font-weight: bold; margin: 5px; display: inline-block; }
    </style>
    """, unsafe_allow_html=True)

# 2. الأسئلة الـ 10 الاحترافية (عالية التفكير)
questions_list = [
    {"q": "أي الممارسات التالية تجسد دور المعلم 'كميسر للتعلم'؟", "opts": ["إلقاء المحاضرة بدقة تامة", "تصميم مسارات تعلم ذاتية مرنة", "مراقبة حضور وغياب الطلبة", "تزويد الطلبة بملخصات جاهزة"], "a": "تصميم مسارات تعلم ذاتية مرنة"},
    {"q": "المعلم الذي يمارس 'التأمل الذاتي' يهدف أساساً إلى:", "opts": ["مقارنة درجاته مع زملائه", "تحسين ممارساته التدريسية", "الالتزام الحرفي بالكتاب المدرسي", "زيادة كمية الواجبات المنزلية"], "a": "تحسين ممارساته التدريسية"},
    {"q": "لتحقيق 'إدارة صفية ذكية'، يركز المعلم المحترف على:", "opts": ["تعيين قادة ثابتين للمجموعات", "توزيع الأدوار حسب قدرات الطلبة", "فرض الصمت التام طوال الحصة", "تجنب العمل الجماعي لمنع الضجيج"], "a": "توزيع الأدوار حسب قدرات الطلبة"},
    {"q": "تعزيز 'المواطنة الرقمية' لدى الطلبة يعني تدريبهم على:", "opts": ["تجنب استخدام الإنترنت نهائياً", "الاستخدام الأخلاقي والآمن للتقنية", "حفظ كلمات المرور بشكل علني", "استخدام المنصات للترفيه فقط"], "a": "الاستخدام الأخلاقي والآمن للتقنية"},
    {"q": "المعلم المبدع في 'الشراكة المجتمعية' هو الذي:", "opts": ["ينعزل بطلابه داخل أسوار المدرسة", "يشرك المجتمع في تطوير التعلم", "يتواصل مع الأهل عند المشاكل فقط", "يرفض أي تدخل خارجي في الفصل"], "a": "يشرك المجتمع في تطوير التعلم"},
    {"q": "التغذية الراجعة 'البناءة' هي التي تقدم للطلبة:", "opts": ["نقداً للأخطاء السابقة فقط", "خارطة طريق لتطوير أدائهم", "درجة نهائية دون أي ملاحظات", "مدحاً عاماً غير محدد الأهداف"], "a": "خارطة طريق لتطوير أدائهم"},
    {"q": "عند تصميم 'بيئة تعلم محفزة'، الأولوية تكون لـ:", "opts": ["فخامة الأثاث والديكور", "الأمان النفسي والاجتماعي للطلبة", "عدد الأجهزة اللوحية المتوفرة", "الهدوء المطبق داخل القاعة"], "a": "الأمان النفسي والاجتماعي للطلبة"},
    {"q": "التخطيط الفعال للتدريس الناجح ينطلق دائماً من:", "opts": ["بداية الفصل في الكتاب", "الوسائل التعليمية المتوفرة", "نتاجات التعلم المستهدفة", "الوقت المتاح للمحاضرة"], "a": "نتاجات التعلم المستهدفة"},
    {"q": "المعلم المحترف يدمج التقنية في التعليم بهدف:", "opts": ["توفير جهد الكتابة على السبورة", "تنمية مهارات التفكير العليا", "إشغال الطلبة وقت الفراغ", "عرض الصور ومقاطع الفيديو فقط"], "a": "تنمية مهارات التفكير العليا"},
    {"q": "الهدف الجوهري لبرنامج 'Teacher Pro' هو صناعة معلم:", "opts": ["خبير في تشغيل الأجهزة فقط", "ملهم ومتمكن تربوياً وتقنياً", "قادر على إنهاء المنهج بسرعة", "متخصص في الطباعة الورقية"], "a": "ملهم ومتمكن تربوياً وتقنياً"}
]

# 3. إدارة الجلسة
if 'players' not in st.session_state: st.session_state.players = []
if 'game_stage' not in st.session_state: st.session_state.game_stage = 'lobby'
if 'score' not in st.session_state: st.session_state.score = 0
if 'current_q' not in st.session_state: st.session_state.current_q = 0

# --- شاشة اللوبي (Lobby) ---
if st.session_state.game_stage == 'lobby':
    st.markdown("<h1 style='text-align: center;'>🎓 قاعة انتظار Teacher Pro</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>بإشراف الدكتورة: مرام الفيومي</h3>", unsafe_allow_html=True)
    
    col_in, col_out = st.columns([1, 1])
    with col_in:
        name = st.text_input("📝 اكتب اسمك وانضم للمنافسة:", placeholder="مثال: أحمد")
        if st.button("انضمام للسباق 🚀"):
            if name and name not in st.session_state.players:
                st.session_state.players.append(name)
                st.session_state.user_name = name
                st.rerun()
    with col_out:
        st.markdown("<div class='lobby-card'>", unsafe_allow_html=True)
        st.write(f"👥 المتسابقون الآن: {len(st.session_state.players)}")
        for p in st.session_state.players:
            st.markdown(f"<span class='name-bubble'>{p}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if len(st.session_state.players) > 0:
        st.divider()
        if st.button("🏁 ابدأ المسابقة الآن!", use_container_width=True):
            st.session_state.game_stage = 'play'
            st.rerun()

# --- شاشة الأسئلة والنتائج اللحظية ---
elif st.session_state.game_stage == 'play':
    idx = st.session_state.current_q
    if idx < len(questions_list):
        q = questions_list[idx]
        st.markdown(f"<div class='question-style'>سؤال {idx+1}: {q['q']}</div>", unsafe_allow_html=True)
        
        start_time = time.time()
        
        # أزرار مضمونة الظهور (نص غامق خلفية فاتحة)
        col1, col2 = st.columns(2)
        with col1:
            ans1 = st.button(f"🔴 {q['opts'][0]}", key=f"ans_{idx}_1")
            ans2 = st.button(f"🔵 {q['opts'][1]}", key=f"ans_{idx}_2")
        with col2:
            ans3 = st.button(f"🟡 {q['opts'][2]}", key=f"ans_{idx}_3")
            ans4 = st.button(f"🟢 {q['opts'][3]}", key=f"ans_{idx}_4")

        # معالجة الإجابة
        user_ans = None
        if ans1: user_ans = q['opts'][0]
        if ans2: user_ans = q['opts'][1]
        if ans3: user_ans = q['opts'][2]
        if ans4: user_ans = q['opts'][3]

        if user_ans:
            elapsed = time.time() - start_time
            if user_ans == q['a']:
                points = max(100, 1000 - int(elapsed * 50))
                st.session_state.score += points
                st.success(f"✅ إجابة صحيحة! بطل السؤال: {st.session_state.user_name} (أسرع إجابة)")
            else:
                st.error(f"❌ إجابة خاطئة! الصحيح هو: {q['a']}")
            
            time.sleep(2)
            st.session_state.current_q += 1
            st.rerun()
    else:
        st.session_state.game_stage = 'finish'
        st.rerun()

# --- شاشة التتويج النهائية ---
elif st.session_state.game_stage == 'finish':
    st.balloons()
    st.markdown(f"<h1 style='text-align: center; color: #d89e00;'>🎊 منصة التتويج النهائية 🎊</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>إشراف د. مرام الفيومي</h2>", unsafe_allow_html=True)
    
    # محاكاة الترتيب العام
    leaderboard = [
        {"المركز": "🥇 الأول", "الاسم": st.session_state.user_name, "النقاط": st.session_state.score},
        {"المركز": "🥈 الثاني", "الاسم": "مشارك مميز", "النقاط": st.session_state.score - 150 if st.session_state.score > 150 else 500},
        {"المركز": "🥉 الثالث", "الاسم": "مشارك مجتهد", "النقاط": st.session_state.score - 300 if st.session_state.score > 300 else 400}
    ]
    
    st.table(pd.DataFrame(leaderboard))
    
    if st.button("العودة للقاعة الرئيسية 🔄"):
        st.session_state.clear()
        st.rerun()
