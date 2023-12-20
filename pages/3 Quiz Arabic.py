import streamlit as st
import random
import json

# Load your initial JSON
with open('qa_arabic.json', 'r', encoding='utf-8') as file:
    questions = json.load(file)

# Organize questions by area (translated to Arabic)
areas = ['سياسة الكحول', 'الإشراف', 'الطعام والمعدات', 'الخدمة']

# Shuffle questions within each area and concatenate them in order
def get_ordered_questions_ar():
    ordered_questions_ar = []
    for area in areas:
        area_questions_ar = [q for q in questions if q['area'] == area]
        random.shuffle(area_questions_ar)
        ordered_questions_ar.extend(area_questions_ar[:5])  # Selects 5 questions per area
    return ordered_questions_ar

# Streamlit app
def run_quiz_ar():
    if 'score_ar' not in st.session_state:
        st.session_state.score_ar = 0
        st.session_state.total_questions_ar = 0
        st.session_state.current_questions_ar = get_ordered_questions_ar()

    if 'current_question_index_ar' not in st.session_state:
        st.session_state.current_question_index_ar = 0

    if 'show_answer_ar' not in st.session_state:
        st.session_state.show_answer_ar = False

    question_ar = st.session_state.current_questions_ar[st.session_state.current_question_index_ar]

    if 'options_ar' not in st.session_state or 'question_initialized_ar' not in st.session_state:
        options_ar = question_ar['false_answers'] + [question_ar['answer']]
        random.shuffle(options_ar)
        st.session_state.options_ar = options_ar
        st.session_state.question_initialized_ar = True

    st.subheader(f"{st.session_state.total_questions_ar + 1} سؤال")
    st.write(f"المجال: {question_ar['area']}")
    st.subheader(question_ar['question'])
    answer_ar = st.radio("الخيارات", st.session_state.options_ar, key=str(st.session_state.current_question_index_ar))

    if st.button("إجابة") and not st.session_state.show_answer_ar:
        st.session_state.show_answer_ar = True
        if answer_ar == question_ar['answer']:
            st.session_state.score_ar += 1
            st.success("صحيح!")
        else:
            st.error(f"خطأ. الجواب الصحيح هو: {question_ar['answer']}")

    if st.session_state.show_answer_ar:
        st.write(f"النقاط الحالية: {st.session_state.score_ar}/{st.session_state.total_questions_ar + 1}")
        if st.session_state.current_question_index_ar < len(st.session_state.current_questions_ar) - 1:
            if st.button("السؤال التالي"):
                next_question_ar()

    if st.session_state.current_question_index_ar >= len(st.session_state.current_questions_ar):
        st.write(f"الاختبار مكتمل. النقاط النهائية: {st.session_state.score_ar}/{st.session_state.total_questions_ar}")
        if st.button("إعادة التشغيل"):
            reset_state_ar()

def next_question_ar():
    st.session_state.total_questions_ar += 1
    st.session_state.current_question_index_ar += 1
    del st.session_state.question_initialized_ar
    st.session_state.show_answer_ar = False
    st.rerun()

def reset_state_ar():
    del st.session_state.score_ar
    del st.session_state.total_questions_ar
    del st.session_state.current_questions_ar
    del st.session_state.current_question_index_ar
    del st.session_state.options_ar
    del st.session_state.show_answer_ar
    if 'question_initialized_ar' in st.session_state:
        del st.session_state.question_initialized_ar

st.title("تطبيق الاختبار")
run_quiz_ar()
