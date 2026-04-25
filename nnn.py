import streamlit as st
import time
import pandas as pd

# 1. إعدادات الصفحة وهوية كاهوت البصرية
st.set_page_config(page_title="Teacher Pro Challenge", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .stApp { background-color: #46178f; color: white; }
    
    /* صندوق السؤال */
    .question-box { background-color: white; color: #333; padding: 25px; border-radius: 15px; text-align: center; font-size: 32px; margin-bottom: 20px; box-shadow: 0 10px 20px rgba(0,0,0,0.2); }
    
    /* تصميم الأزرار (أشكال كاهوت) */
    .stButton>button { height: 100px; font-size: 24px !important; border-radius: 10px; border: none; color: white !important; transition: 0.2s; box-shadow: 0 5px 0 rgba(0,0,0,0.2); }
    .stButton>button:active { transform: translateY(5px); box-shadow: none; }
    
    /* ألوان الأزرار والأيقونات */
    div.stButton > button:first-child { background-color: #e21b3c !important; } /* مثلث - أحمر */
    div.stButton > button:nth-child(2) { background-color: #1368ce !important; } /* معين - أزرق */
    div.stButton > button:nth-child(3) { background-color: #d89e00 !important; } /* دائرة - أصفر */
    div.stButton > button:nth-child(4) { background-color: #26890c !important; } /* مربع - أخضر */
    
    /* لوحة الترتيب */
    .leaderboard-card { background: #331069; padding: 20px; border-radius: 15px; border: 2px solid #d89e00; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. المؤثرات الصوتية (روابط مباشرة)
def play_sound(url):
    st.markdown(f'<audio src="{url}" autoplay></audio>', unsafe_allow_html=True)

correct_sfx = "https://www.soundjay.com/buttons/sounds/button-3.mp3"
wrong_sfx = "https://www.soundjay.com/buttons/sounds/button-10.mp3"
tick_tock = "https://www.soundjay.com/clock/sounds/clock-ticking-2.mp3"

# 3. قاعدة البيانات (10 أسئلة محيرة مع الصور)
if 'questions' not in st.session_state:
    st.session_state.questions = [
        {"q": "أي الممارسات تمثل دور المعلم 'كمصمم لبيئة التعلم'؟", "img": "https://img.freepik.com/free-vector/creative-team-concept-illustration_114360-3754.jpg", "opts": ["▲ تقديم عرض تقديمي طويل", "◆ تنظيم مساحات عمل مرنة", "● الالتزام بالجلوس خلف المكتب", "■ قراءة الكتاب بصوت عالٍ"], "a": "◆ تنظيم مساحات عمل مرنة"},
        {"q": "المعلم المحترف يستخدم 'الذكاء الاصطناعي' بهدف:", "img": "https://img.freepik.com/free-vector/ai-technology-concept-illustration_114360-6949.jpg", "opts": ["▲ استبدال مهارات التفكير", "◆ تخصيص التعلم لكل طالب", "● تقليل وقت التواصل مع الطلاب", "■ إلغاء الاختبارات الورقية"], "a": "◆ تخصيص التعلم لكل طالب"},
        # يمكن تكرار النمط لبقية الـ 10 أسئلة...
    ]

# 4. إدارة حالة اللعبة
if 'game_state' not in st.session_state:
    st.session_state.update({'game_state': 'start', 'score': 0, 'current_q': 0, 'history': []})

# --- شاشة البداية ---
if st.session_state.game_state == 'start':
    st.markdown(f"<h1 style='text-align: center;'>🏆 تحدي المعلم المبدع</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>إشراف: د. مرام الفيومي</h3>", unsafe_allow_html=True)
    name = st.text_input("أدخل اسمك الكريم لبدء المنافسة:", placeholder="اسمك هنا...")
    if st.button("هيا بنا! 🚀"):
        if name:
            st.session_state.player_name = name
            st.session_state.game_state = 'play'
            st.rerun()

# --- شاشة اللعب ---
elif st.session_state.game_state == 'play':
    idx = st.session_state.current_q
    q = st.session_state.questions[idx]
    
    st.markdown(f"<div class='question-box'>{q['q']}</div>", unsafe_allow_html=True)
    st.image(q['img'], use_container_width=True)
    
    play_sound(tick_tock) # صوت تكتكة الساعة للسرعة
    
    start_time = time.time()
    
    cols = st.columns(2)
    for i, opt in enumerate(q['opts']):
        with cols[i % 2]:
            if st.button(opt, key=f"q{idx}o{i}"):
                elapsed = time.time() - start_time
                if opt == q['a']:
                    points = max(100, 1000 - int(elapsed * 100))
                    st.session_state.score += points
                    play_sound(correct_sfx)
                    st.session_state.last_result = f"✅ رائع! حصلت على {points} نقطة"
                else:
                    play_sound(wrong_sfx)
                    st.session_state.last_result = "❌ إجابة خاطئة، حاول في القادم!"
                
                st.session_state.game_state = 'feedback'
                st.rerun()

# --- شاشة الترتيب اللحظي (بعد كل سؤال) ---
elif st.session_state.game_state == 'feedback':
    st.markdown(f"<div class='leaderboard-card'><h2>{st.session_state.last_result}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h3>رصيدك الحالي: {st.session_state.score} نقطة</h3></div>", unsafe_allow_html=True)
    
    # ترتيب وهمي للمنافسة
    st.write("📊 ترتيبك الحالي بين المتسابقين:")
    temp_df = pd.DataFrame([
        {"الاسم": st.session_state.player_name, "النقاط": st.session_state.score},
        {"الاسم": "أحمد", "النقاط": st.session_state.score - 50 if st.session_state.score > 50 else 30},
        {"الاسم": "سارة", "النقاط": st.session_state.score + 20}
    ]).sort_values(by="النقاط", ascending=False)
    st.table(temp_df)
    
    if st.button("السؤال التالي ➡️"):
        if st.session_state.current_q < len(st.session_state.questions) - 1:
            st.session_state.current_q += 1
            st.session_state.game_state = 'play'
        else:
            st.session_state.game_state = 'final'
        st.rerun()

# --- شاشة الفائز النهائي ---
elif st.session_state.game_state == 'final':
    st.balloons()
    st.markdown(f"<div class='question-box' style='color: #46178f;'>🎊 مبارك لإتمام التحدي تحت إشراف د. مرام الفيومي 🎊</div>", unsafe_allow_html=True)
    st.header(f"🏆 بطل اليوم هو: {st.session_state.player_name}")
    st.subheader(f"مجموع النقاط النهائي: {st.session_state.score}")
    
    if st.button("العودة للرئيسية"):
        st.session_state.clear()
        st.rerun()
