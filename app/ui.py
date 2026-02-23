import streamlit as st
from app.session import regions, init, next_region
from core.controller import FluoroController

st.set_page_config(page_title="Science Fair Plaque System")

init()

def handle_pass():
    if not st.session_state.started:
        return
    if st.session_state.finished:
        return

    active = regions[st.session_state.current_index]
    st.session_state.completed[active] += 1

    if st.session_state.completed[active] >= st.session_state.required[active]:
        next_region()

controller = FluoroController(handle_pass)

st.title("Fluorescence Plaque Detection System")

if not st.session_state.started:
    if st.button("Start Session"):
        st.session_state.started = True
        controller.start()

else:
    active = regions[st.session_state.current_index]
    st.subheader(f"Current Region: {active}")

    percent = st.session_state.completed[active] / st.session_state.required[active]
    st.progress(percent)

    if st.session_state.finished:
        st.success("Session Complete 🎉")

st.markdown("---")
st.header("Region Overview")

for r in regions:
    p = st.session_state.completed[r] / st.session_state.required[r]
    st.write(r)
    st.progress(p)