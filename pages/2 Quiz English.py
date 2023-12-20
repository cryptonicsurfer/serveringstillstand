import streamlit as st
import random
import json

# Load your initial JSON
with open('qa_english.json', 'r') as file:
    questions = json.load(file)

# Organize questions by area
areas = ['Alcohol Policy', 'Supervision', 'Food and Equipment', 'Service']

# Shuffle questions within each area and concatenate them in order
def get_ordered_questions_en():
    ordered_questions_en = []
    for area in areas:
        area_questions_en = [q for q in questions if q['area'] == area]
        random.shuffle(area_questions_en)
        ordered_questions_en.extend(area_questions_en[:5])  # Selects 5 questions per area
    return ordered_questions_en

# Streamlit app
def run_quiz_en():
    if 'score_en' not in st.session_state:
        st.session_state.score_en = 0
        st.session_state.total_questions_en = 0
        st.session_state.current_questions_en = get_ordered_questions_en()

    if 'current_question_index_en' not in st.session_state:
        st.session_state.current_question_index_en = 0

    if 'show_answer_en' not in st.session_state:
        st.session_state.show_answer_en = False

    question_en = st.session_state.current_questions_en[st.session_state.current_question_index_en]

    if 'options_en' not in st.session_state or 'question_initialized_en' not in st.session_state:
        options_en = question_en['false_answers'] + [question_en['answer']]
        random.shuffle(options_en)
        st.session_state.options_en = options_en
        st.session_state.question_initialized_en = True

    st.subheader(f"Question {st.session_state.total_questions_en + 1}")
    st.write(f"Area: {question_en['area']}")
    st.subheader(question_en['question'])
    answer_en = st.radio("Options", st.session_state.options_en)

    if st.button("Answer") and not st.session_state.show_answer_en:
        st.session_state.show_answer_en = True
        if answer_en == question_en['answer']:
            st.session_state.score_en += 1
            st.success("Correct!")
        else:
            st.error(f"Wrong. The correct answer is: {question_en['answer']}")

    if st.session_state.show_answer_en:
        st.write(f"Current Score: {st.session_state.score_en}/{st.session_state.total_questions_en + 1}")
        if st.session_state.current_question_index_en < len(st.session_state.current_questions_en) - 1:
            if st.button("Next Question"):
                next_question_en()

    if st.session_state.current_question_index_en >= len(st.session_state.current_questions_en):
        st.write(f"The quiz is complete. Your final score: {st.session_state.score_en}/{st.session_state.total_questions_en}")
        if st.button("Restart"):
            reset_state_en()

def next_question_en():
    st.session_state.total_questions_en += 1
    st.session_state.current_question_index_en += 1
    del st.session_state.question_initialized_en
    st.session_state.show_answer_en = False
    st.rerun()

def reset_state_en():
    del st.session_state.score_en
    del st.session_state.total_questions_en
    del st.session_state.current_questions_en
    del st.session_state.current_question_index_en
    del st.session_state.options_en
    del st.session_state.show_answer_en
    if 'question_initialized_en' in st.session_state:
        del st.session_state.question_initialized_en

st.title("Quiz App")
run_quiz_en()
