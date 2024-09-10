import streamlit as st
import pandas as pd
from assets.styles.css_style import apply_css
from database.connect_db import *
from database.queries import DatabaseQueries
from datetime import date

db_queries = DatabaseQueries()
db_connect = ConnectDataBase()

df_dvrs = db_queries.get_all_dvrs()
df_cameras = db_queries.get_all_cameras()

def app():
    apply_css()
    st.markdown(f"<div style='margin-bottom: 20px;'><h2>Gerenciamento do Digital Video Recorder (DVR)</h2>", unsafe_allow_html=True)
    
    # Instruções para o usuário
    st.markdown("""
⚠️ **Cuidado, todas as alterações feitas serão refletidas em toda a estrutuda do programa e diretamente no banco de dados.** \n
⚠️ **Apenas o administrador pode alterar as câmeras de segurança.** \n
⚠️ **Para que as alterações tenham efeito, reinicie o programa.**
    """)

    st.divider()

    st.markdown('**1. Selecione o DVR a ser alterado:**')

    selected_dvr = st.selectbox("Selecione o DVR", df_dvrs['dvr_nome'])
    if selected_dvr:
        st.markdown(f"Você selecionou: **{selected_dvr}**")

    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs(['DVR Nome', 'Status', 'Modelo e Marca', 'Endereço IP'])

    with tab1:
        st.markdown('**2. Altere o nome do DVR:**')
        new_dvr_name = st.text_input("Novo Nome do DVR", key="new_dvr_name")
        if st.button("Alterar Nome"):
            if new_dvr_name.strip() != "":
                db_queries.update_dvr_name(selected_dvr, new_dvr_name)
                st.success("Nome do DVR atualizado com sucesso!")
            else:
                st.warning("Por favor, insira um nome válido para o DVR.")

    with tab2:
        st.markdown('**3. Altere o status do DVR:**')
        new_dvr_status = st.selectbox("Novo Status do DVR", ['Ativo', 'Inativo'], key="new_dvr_status")
        if st.button("Alterar Status"):
            db_queries.update_dvr_status(selected_dvr, new_dvr_status)
            st.success("Status do DVR atualizado com sucesso!")
        else:
            st.warning("Por favor, selecione um status válido para o DVR.")
    
    with tab3:
        st.markdown('**4. Altere o modelo e marca do DVR:**')
        new_dvr_model = st.text_input("Novo Modelo do DVR", key="new_dvr_model")
        new_dvr_marca = st.text_input("Nova Marca do DVR", key="new_dvr_marca")
        if st.button("Alterar Modelo e Marca"):
            if new_dvr_model.strip() != "" and new_dvr_marca.strip() != "":
                db_queries.update_dvr_model_and_marca(selected_dvr, new_dvr_model, new_dvr_marca)
                st.success("Modelo e marca do DVR atualizados com sucesso!")
            else:
                st.warning("Por favor, insira um modelo e marca válidos para o DVR.")

    with tab4:
        st.markdown('**5. Altere o endereço IP do DVR:**')
        new_dvr_ip = st.text_input("Novo Endereço IP do DVR", key="new_dvr_ip")
        if st.button("Alterar Endereço IP"):
            if new_dvr_ip.strip() != "":
                db_queries.update_dvr_ip(selected_dvr, new_dvr_ip)
                st.success("Endereço IP do DVR atualizado com sucesso!")
            else:
                st.warning("Por favor, insira um endereço IP válido para o DVR.")