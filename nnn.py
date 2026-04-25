import streamlit as st
import pandas as pd
import time

# ---------------------------------------------------------
# 🚨 ملاحظة هامة للدكتورة مرام:
# ضعي رابط ملف جوجل شيت (Editor) بين القوسين أدناه
GOOGLE_SHEET_URL = "ضعي_الرابط_هنا" 
# ---------------------------------------------------------

st.set_page_config(page_title="Teacher Pro Live Challenge", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .stApp { background-color: #46178f; color: white; }
    .question-box { background: white; color: #46178f; padding: 25px; border-radius: 15px; text-align: center; font-size: 28px; font-weight: bold; border: 4px solid #d89e00; }
    .timer-style { font-size: 40px; font-weight: bold; color: #ff4b4b; background: white; border-radius: 50%; width: 90px; height: 90px; line-height: 90px; text-align: center; margin: 10px auto; border: 4px solid #ff4b4b; }
    div.stButton > button { background-color: #ffffff !important; color: #000000 !important; border: 3px solid #d89e00 !important; height: 70px !important; font-size: 22px !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# بنك الأسئلة (الـ 10 أسئلة كاملة)
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

# إدارة الجلسة الجماعية (باستخدام التخزين السحابي المحاكي)
if 'leaderboard' not in st.session_state: st.session_state.leaderboard = {}
if 'current_q_idx' not in st.session_state: st.session_state.current_q_idx = 0
if 'game_started' not in st.session_state: st.session_state.game_started = False

if not st.session_state.game_started:
    st.markdown("<h1 style='text-align: center;'>🎓 تحدي Teacher Pro التفاعلي الجماعي</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>بإشراف د. مرام الفيومي</h3>", unsafe_allow_html=True)
    
    p_name = st.text_input("📝 سجل اسمك للدخول في الغرفة المشتركة:", key="main_name")
    
    if st.button("انضم الآن"):
        if p_name:
            st.session_state.leaderboard[p_name] = 0
            st.session_state.user = p_name
            st.success(f"تم الانضمام بنجاح يا {p_name}")
            
    st.write(f"المشاركون الآن: {list(st.session_state.leaderboard.keys())}")
    
    if len(st.session_state.leaderboard) > 0:
        if st.button("🚀 ابدأ المسابقة للجميع"):
            st.session_state.game_started = True
            st.session_state.start_t = time.time()
            st.rerun()
else:
    idx = st.session_state.current_q_idx
    if idx < len(questions):
        q = questions[idx]
        st.markdown(f"<div class='question-box'>السؤال {idx+1}: {q['q']}</div>", unsafe_allow_html=True)
        
        elapsed = time.time() - st.session_state.start_t
        rem = max(0, 10 - int(elapsed))
        
        if rem > 0:
            st.markdown(f"<div class='timer-style'>{rem}</div>", unsafe_allow_html=True)
            cols = st.columns(2)
            for i, opt in enumerate(q['opts']):
                with cols[i % 2]:
                    if st.button(opt, key=f"q_{idx}_{i}"):
                        if opt == q['a']:
                            st.session_state.leaderboard[st.session_state.user] += (100 + rem)
                        st.toast("تم تسجيل إجابتك!")
            time.sleep(1)
            st.rerun()
        else:
            st.success(f"انتهى الوقت! الإجابة الصحيحة هي: {q['a']}")
            st.subheader("📊 ترتيب الفائزين (يظهر للجميع):")
            df = pd.DataFrame(st.session_state.leaderboard.items(), columns=['الاسم', 'النقاط']).sort_values(by='النقاط', ascending=False)
            st.table(df)
            
            if st.button("السؤال التالي ➡️"):
                st.session_state.current_q_idx += 1
                st.session_state.start_t = time.time()
                st.rerun()
    else:
        st.balloons()
        st.markdown("<h1 style='text-align: center;'>🏆 الفائزون النهائيون 🏆</h1>", unsafe_allow_html=True)
        final_df = pd.DataFrame(st.session_state.leaderboard.items(), columns=['الاسم', 'النقاط']).sort_values(by='النقاط', ascending=False)
        st.table(final_df)
