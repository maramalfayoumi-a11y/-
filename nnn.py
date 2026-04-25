import streamlit as st
import time
import pandas as pd

# 1. إعدادات الهوية البصرية (Kahoot Style)
st.set_page_config(page_title="Teacher Pro Lobby", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .stApp { background-color: #46178f; color: white; }
    .lobby-title { text-align: center; font-size: 50px; font-weight: bold; color: #d89e00; margin-bottom: 10px; }
    .instructor-name { text-align: center; font-size: 25px; color: white; margin-bottom: 30px; }
    .name-tag { background-color: white; color: #46178f; padding: 10px 20px; border-radius: 10px; font-size: 20px; font-weight: bold; margin: 5px; display: inline-block; box-shadow: 2px 2px 10px rgba(0,0,0,0.3); }
    .start-btn { text-align: center; margin-top: 50px; }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة الأسماء المدخلة (باستخدام Session State لمحاكاة الدخول اللحظي)
# ملاحظة: في النسخ المتقدمة نستخدم Firestore، لكن هنا سنعتمد على التحديث التلقائي
if 'players_list' not in st.session_state:
    st.session_state.players_list = []
if 'game_started' not in st.session_state:
    st.session_state.game_started = False

# --- شاشة الانتظار (Lobby) ---
if not st.session_state.game_started:
    st.markdown("<div class='lobby-title'>🏆 مسابقة المعلم المبدع</div>", unsafe_allow_html=True)
    st.markdown("<div class='instructor-name'>بإشراف د. مرام الفيومي</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 📝 انضم الآن")
        new_player = st.text_input("أدخل اسمك للانضمام:")
        if st.button("انضمام"):
            if new_player and new_player not in st.session_state.players_list:
                st.session_state.players_list.append(new_player)
                st.balloons()
                st.rerun()
                
    with col2:
        st.markdown(f"### 👥 المتسابقون الآن ({len(st.session_state.players_list)})")
        # عرض الأسماء بشكل مربعات ملونة كما في كاهوت
        if st.session_state.players_list:
            players_html = "".join([f"<div class='name-tag'>{name}</div>" for name in st.session_state.players_list])
            st.markdown(players_html, unsafe_allow_html=True)
        else:
            st.info("بانتظار دخول الأبطال...")

    # زر بدء اللعبة (يظهر فقط إذا كان هناك لاعبون)
    if len(st.session_state.players_list) > 0:
        st.markdown("<div class='start-btn'>", unsafe_allow_html=True)
        if st.button("🚀 ابدأ التحدي الآن!", use_container_width=True):
            st.session_state.game_started = True
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- شاشة الأسئلة (تبدأ عند الضغط على زر البداية) ---
else:
    # هنا تضعين كود الأسئلة الذي صممناه سابقاً
    st.title("انطلقت المسابقة! 🏁")
    st.write("سيتم عرض السؤال الأول الآن...")
    # (يمكنك دمج كود الأسئلة هنا)
