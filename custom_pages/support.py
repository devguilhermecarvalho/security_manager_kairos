import streamlit as st

def app():
    st.title("Support")
    st.divider()

    # Envie um email para o desenvolvedor
    st.markdown("""
        <div style='margin-bottom: 20px;'>
            <h3>Envie um email para o desenvolvedor:</h3>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("**Email: guilhermerdcarvalho@gmail.com**")