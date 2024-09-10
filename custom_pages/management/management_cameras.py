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
    st.markdown(f"<div style='margin-bottom: 20px;'><h2>Gerenciamento das Câmeras de Segurança</h2>", unsafe_allow_html=True)
    
    # Instruções para o usuário
    st.markdown("""
⚠️ **Cuidado, todas as alterações feitas serão refletidas em toda a estrutuda do programa e diretamente no banco de dados.** \n
⚠️ **Apenas o administrador pode alterar as câmeras de segurança.** \n
⚠️ **Para que as alterações tenham efeito, reinicie o programa.**
    """)
    st.divider()

    st.markdown('**1. Selecione onde a câmera está localizada:**')

    selected_dvr = st.selectbox("Selecione o DVR", df_dvrs['dvr_nome'])

    if selected_dvr:
        df_cameras_gold = pd.merge(df_cameras, df_dvrs, on='dvr_id', how='left')
        cameras_dvr_df = df_cameras_gold[df_cameras_gold['dvr_nome'] == selected_dvr]
        camera_options = {row['camera_nome']: row['camera_id'] for index, row in cameras_dvr_df.iterrows()}
        selected_camera = st.selectbox("Selecione a Câmera", list(camera_options.keys()))
        camera_id = camera_options[selected_camera]
        # Exibindo todas as informações da câmera selecionada
        
        df_selected_camera_print = cameras_dvr_df[cameras_dvr_df['camera_id'] == camera_id]
        df_selected_camera_print = df_selected_camera_print[['camera_id', 'camera_nome', 'categoria_status_id_x', 'camera_resolucao', 'camera_url', 'camera_lat', 'camera_long', 'dvr_id', 'dvr_nome', 'ponto_a', 'ponto_b', 'ponto_c', 'ponto_d']]
        st.dataframe(df_selected_camera_print, hide_index=True)

        st.markdown(f"Você selecionou: **{selected_camera} (ID: {camera_id})**")
        st.divider()
    
    # Trocando o nome da câmera

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Alterar Nome da Câmera", "Alterar Resolução", 'Alterar URL', 'Alterar Lat e Long', 'Alterar DVR'])
    
    with tab1:
        st.markdown('2. Altere o nome da câmera:')
        new_camera_name = st.text_input("Novo Nome da Câmera", key="new_camera_name")
        if st.button("Alterar Nome"):
            if new_camera_name.strip() != "":
                db_queries.update_camera_name(camera_id, new_camera_name)
                st.success("Nome da câmera atualizado com sucesso!")
            else:
                st.warning("Por favor, insira um nome válido para a câmera.")
    
    with tab2:
        st.markdown('3. Altere a resolução da câmera:')
        resolucoes = ['720p', '1080p', '2K', '4K']
        new_camera_resolution = st.selectbox("Nova Resolução da Câmera", resolucoes, key="new_camera_resolution")
        if st.button("Alterar Resolução"):
            if new_camera_resolution.strip() != "":
                db_queries.update_camera_resolution(camera_id, new_camera_resolution)
                st.success("Resolução da câmera atualizada com sucesso!")
            else:
                st.warning("Por favor, insira uma resolução válida para a câmera.")

    with tab3:
        st.markdown('4. Altere a URL da câmera:')
        new_camera_url = st.text_input("Nova URL da Câmera", key="new_camera_url")
        if st.button("Alterar URL"):
            if new_camera_url.strip() != "":
                db_queries.update_camera_url(camera_id, new_camera_url)
                st.success("URL da câmera atualizada com sucesso!")
            else:
                st.warning("Por favor, insira uma URL válida para a câmera.")

    with tab4:
        st.markdown('5. Altere a Latitude e Longitude da câmera:')
        new_camera_lat = st.text_input("Nova Latitude", key="new_camera_lat")
        new_camera_long = st.text_input("Nova Longitude", key="new_camera_long")
        if st.button("Alterar Lat e Long"):
            if new_camera_lat.strip() != "":
                db_queries.update_camera_lat_long(camera_id, new_camera_lat, new_camera_long)
                st.success("Latitude e Longitude da câmera atualizados com sucesso!")
            else:
                st.warning("Por favor, insira uma Latitude e Longitude válidas para a câmera.")

    with tab5:
        st.markdown('6. Altere o DVR da câmera:')
        new_camera_dvr = st.selectbox("Novo DVR", df_dvrs['dvr_nome'], key="new_camera_dvr")
        if st.button("Alterar DVR"):
            if new_camera_dvr.strip() != "":
                db_queries.update_camera_dvr(camera_id, new_camera_dvr)
                st.success("DVR da câmera atualizado com sucesso!")
            else:
                st.warning("Por favor, insira um DVR válido para a câmera.")
