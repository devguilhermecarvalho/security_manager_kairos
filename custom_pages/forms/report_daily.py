import streamlit as st
from assets.styles.css_style import apply_css
from database.connect_db import *
from database.queries import DatabaseQueries
from datetime import date

db_queries = DatabaseQueries()
db_connect = ConnectDataBase()

def insert_relatorio_mestre(relatorio_data, relatorio_descricao):
    query = """
    INSERT INTO relatorio_mestre (relatorio_data, relatorio_descricao)
    VALUES (%s, %s) RETURNING idrelatorio_mestre
    """
    with db_connect.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (relatorio_data, relatorio_descricao))
            return cur.fetchone()[0]

def insert_relatorio_diario(statuses, idrelatorio_mestre, table_name, device_column):
    query = f"""
    INSERT INTO {table_name} (categoria_status_id, {device_column}, idrelatorio_mestre)
    VALUES (%s, %s, %s)
    """
    with db_connect.get_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany(query, [(status, device_id, idrelatorio_mestre) for device_id, status in statuses.items()])

def app():
    apply_css()
    st.markdown(f"<div style='margin-bottom: 20px;'><h2>Preenchimento do Relatório Diário</h2>", unsafe_allow_html=True)
    
    # Instruções para o usuário
    st.markdown("""
📝 **Instruções para Preenchimento do Relatório** 📝

1. **📅 Seleção da Data:** Escolha a data desejada para o relatório.
2. **🔍 Verificação de Funcionamento:** Confira se cada câmera está operando corretamente.
3. **✅ Revisão dos Dados:** Examine as informações exibidas no dataframe para garantir sua precisão.
4. **📝 Observações:** Caso haja, adicione qualquer observação relacionada ao serviço.
5. **💾 Salvar:** Após verificar todas as informações, clique em salvar.

**❌ Observações: Todas as câmeras com o nome "Vago" serão automaticamente setadas como "Canal Vago".**
    """)

    st.divider()
    # Seleção de data
    report_date = st.date_input("**1. Selecione a Data do Preenchimento do Relatório:**", value=date.today(), max_value=date.today())

    df_cameras = db_queries.get_cameras_with_dvr()
    df_dvrs = db_queries.get_all_dvrs()
    df_categorias = db_queries.get_all_categorias_status()

    status_options = {row['categoria_status_nome']: row['categoria_status_id'] for index, row in df_categorias.iterrows()}
    dvr_status_options = {name: id for name, id in status_options.items() if name in ["Online", "Offline"]}

    # Exibir status das câmeras divididas por DVR
    st.markdown('**2. Faça o preenchimento do status de cada câmera:**')
    camera_statuses = {}
    dvr_names = df_dvrs['dvr_nome']

    for dvr_name in dvr_names:
        st.markdown(f"#### DVR: {dvr_name}")
        cameras_dvr_df = df_cameras[df_cameras['dvr_nome'] == dvr_name]
        colunas_cameras = st.columns(5, gap="small")
        for index, row in cameras_dvr_df.iterrows():
            col = colunas_cameras[index % 5]
            status_label = f"**{row['camera_nome']}**"
            default_status = 'Canal vago' if row['camera_nome'].lower() in ['vago', 'canal vago'] else 'Online'
            status = col.selectbox(status_label, options=list(status_options.keys()), index=list(status_options.keys()).index(default_status), key=f"camera_{row['camera_id']}")
            camera_statuses[row['camera_id']] = status_options[status]
        st.divider()

    # Exibir status dos DVRs
    st.markdown('**3. Faça o preenchimento do status de cada DVR:**')
    dvr_statuses = {}
    colunas_dvrs = st.columns(5, gap="small")
    for index, row in df_dvrs.iterrows():
        col = colunas_dvrs[index % 5]
        status = col.selectbox(f"**{row['dvr_nome']}**", options=list(dvr_status_options.keys()), index=1, key=f"dvr_{row['dvr_id']}")
        dvr_statuses[row['dvr_id']] = dvr_status_options[status]

    # Descrição do relatório
    st.divider()
    st.write('**4. Caso tenha alguma observação relacionada ao relatório ou sobre alguma câmera, informe no campo abaixo:**')
    report_description = st.text_area("Descrição do Relatório")

    # Botão para salvar o relatório
    if st.button('Salvar Relatório'):
        if report_description.strip() == "":
            st.error('A descrição do relatório é obrigatória.')
        else:
            try:
                idrelatorio_mestre = insert_relatorio_mestre(report_date, report_description)
                insert_relatorio_diario(camera_statuses, idrelatorio_mestre, "relatorio_diario_cameras", "camera_id")
                insert_relatorio_diario(dvr_statuses, idrelatorio_mestre, "relatorio_diario_dvrs", "dvr_id")
                st.success(f'Relatório {idrelatorio_mestre} salvo com sucesso!')
                if st.button('Visualizar Relatório'):
                    st.write(f"Visualização do relatório {idrelatorio_mestre} (implementação pendente)")
            except Exception as e:
                st.error(f'Ocorreu um erro ao salvar o relatório: {e}')
