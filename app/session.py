import streamlit as st

regions = [
    "Upper Right", "Upper Middle", "Upper Left",
    "Lower Right", "Lower Middle", "Lower Left"
]

def init():
    if "completed" not in st.session_state:
        st.session_state.completed = {r: 0 for r in regions}
    if "required" not in st.session_state:
        st.session_state.required = {r: 3 for r in regions}
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
    if "started" not in st.session_state:
        st.session_state.started = False
    if "finished" not in st.session_state:
        st.session_state.finished = False

def next_region():
    for i in range(6):
        idx = (st.session_state.current_index + 1 + i) % 6
        r = regions[idx]
        if st.session_state.completed[r] < st.session_state.required[r]:
            st.session_state.current_index = idx
            return
    st.session_state.finished = True