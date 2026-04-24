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
        {"q": "أي من هذه الممارسات تعزز 'المواطنة الرقمية' لدى الطلاب؟", "img": "https://img.freepik.com/free-vector/privacy-policy-concept-illustration_114360-7853.jpg", "opts": ["منع استخدام الإنترنت في
