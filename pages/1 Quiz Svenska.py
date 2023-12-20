import streamlit as st
import random
import json

# Load your initial JSON
with open('qa_swedish.json', 'r') as file:
    questions = json.load(file)

# Organize questions by area
areas = ['Alkoholpolitik', 'Tillsyn', 'Mat och utrustning', 'Servering']

# Shuffle questions within each area and concatenate them in order
def get_ordered_questions_se():
    ordered_questions_se = []
    for area in areas:
        area_questions_se = [q for q in questions if q['area'] == area]
        random.shuffle(area_questions_se)
        ordered_questions_se.extend(area_questions_se[:5])  # Väljer 5 frågor per område
    return ordered_questions_se

# Streamlit app
def run_quiz_se():
    if 'score_se' not in st.session_state:
        st.session_state.score_se = 0
        st.session_state.total_questions_se = 0
        st.session_state.current_questions_se = get_ordered_questions_se()

    if 'current_question_index_se' not in st.session_state:
        st.session_state.current_question_index_se = 0

    if 'show_answer_se' not in st.session_state:
        st.session_state.show_answer_se = False

    question_se = st.session_state.current_questions_se[st.session_state.current_question_index_se]

    if 'options_se' not in st.session_state or 'question_initialized_se' not in st.session_state:
        options_se = question_se['false_answers'] + [question_se['answer']]
        random.shuffle(options_se)
        st.session_state.options_se = options_se
        st.session_state.question_initialized_se = True

    st.subheader(f"Fråga {st.session_state.total_questions_se + 1}")
    st.write(f"Område: {question_se['area']}")
    st.subheader(question_se['question'])
    answer_se = st.radio("Alternativ", st.session_state.options_se)

    if st.button("Svara") and not st.session_state.show_answer_se:
        st.session_state.show_answer_se = True
        if answer_se == question_se['answer']:
            st.session_state.score_se += 1
            st.success("Rätt!")
        else:
            st.error(f"Fel. Det rätta svaret är: {question_se['answer']}")

    if st.session_state.show_answer_se:
        st.write(f"Aktuell poäng: {st.session_state.score_se}/{st.session_state.total_questions_se + 1}")
        if st.session_state.current_question_index_se < len(st.session_state.current_questions_se) - 1:
            if st.button("Nästa fråga"):
                next_question_se()

    if st.session_state.current_question_index_se >= len(st.session_state.current_questions_se):
        st.write(f"Quizet är färdigt. Din slutpoäng: {st.session_state.score_se}/{st.session_state.total_questions_se}")
        if st.button("Starta om"):
            reset_state_se()

def next_question_se():
    st.session_state.total_questions_se += 1
    st.session_state.current_question_index_se += 1
    del st.session_state.question_initialized_se
    st.session_state.show_answer_se = False
    st.rerun()

def reset_state_se():
    del st.session_state.score_se
    del st.session_state.total_questions_se
    del st.session_state.current_questions_se
    del st.session_state.current_question_index_se
    del st.session_state.options_se
    del st.session_state.show_answer_se
    if 'question_initialized_se' in st.session_state:
        del st.session_state.question_initialized_se

st.title("Quiz-app")
run_quiz_se()
