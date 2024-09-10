# custom_pages/dashboard/dashboard_cameras.py

import pandas as pd
import folium
from streamlit_folium import st_folium
import streamlit as st
import plotly.graph_objects as go
from assets.styles.css_style import apply_css
from database.queries import DatabaseQueries

# Configurações gerais
config = {
    'dashboard_title': "Dashboard Situacional das Câmeras de Segurança",
    'map_location_marui': [-22.8632101, -43.1300769],
    'map_location_ilha': [-22.862, -43.124],
    'default_zoom_start': 16.4,
    'map_tiles_url': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    'map_attr': 'Tiles &copy; Esri'
}

db_queries = DatabaseQueries()

class Report:
    def __init__(self):
        # Carrega os dados necessários
        self.df_dvrs = db_queries.get_all_dvrs()
        self.df_cameras = db_queries.get_all_cameras()
        self.df_categorias_status = db_queries.get_all_categorias_status()
        self.df_relatorio_mestre = db_queries.get_all_relatorio_mestre()
        self.df_relatorio_diario_cameras = db_queries.get_all_relatorio_diario_cameras()
        self.df_relatorio_diario_dvrs = db_queries.get_all_relatorio_diario_dvrs()

        # Verifica se os DataFrames não estão vazios
        self.check_dataframes()

        # Prepara os DataFrames já unidos
        self.df_cameras_gold = self.merge_camera_data()
        self.df_relatorio_mestre_cameras, self.df_relatorio_mestre_dvrs = self.merge_report_data()

    def check_dataframes(self):
        if self.df_dvrs.empty or self.df_cameras.empty or self.df_categorias_status.empty:
            st.error("Alguns dos DataFrames necessários estão vazios. Verifique as fontes de dados.")
            st.stop()

    def merge_camera_data(self):
        df_cameras_gold = pd.merge(self.df_cameras, self.df_categorias_status, on='categoria_status_id', how='inner')
        df_cameras_gold = pd.merge(df_cameras_gold, self.df_dvrs, on='dvr_id', how='inner')
        if 'categoria_status_nome' not in df_cameras_gold.columns:
            st.error("A coluna 'categoria_status_nome' não foi encontrada após a junção dos DataFrames.")
            st.stop()
        return df_cameras_gold[['camera_id', 'camera_nome', 'camera_resolucao', 'categoria_status_nome', 'camera_url', 'camera_lat', 'camera_long', 'dvr_nome']]

    def merge_report_data(self):
        # Junção dos DataFrames relacionados ao relatório diário das câmeras
        df_relatorio_diario_cameras = pd.merge(self.df_relatorio_diario_cameras, self.df_categorias_status, on='categoria_status_id', how='inner')
        df_relatorio_diario_cameras = pd.merge(df_relatorio_diario_cameras, self.df_cameras, on='camera_id', how='inner')
        df_relatorio_diario_cameras = pd.merge(df_relatorio_diario_cameras, self.df_dvrs, on='dvr_id', how='inner')
        df_relatorio_diario_cameras_gold = df_relatorio_diario_cameras[['idrelatorio_diario_cameras', 'idrelatorio_mestre', 'categoria_status_nome', 'camera_nome', 'dvr_nome', 'camera_lat', 'camera_long']]

        # Junção dos DataFrames relacionados ao relatório diário dos DVRs
        df_relatorio_diario_dvrs = pd.merge(self.df_relatorio_diario_dvrs, self.df_categorias_status, on='categoria_status_id', how='inner')
        df_relatorio_diario_dvrs = pd.merge(df_relatorio_diario_dvrs, self.df_dvrs, on='dvr_id', how='inner')
        df_relatorio_diario_dvrs_gold = df_relatorio_diario_dvrs[['idrelatorio_diario_dvrs', 'idrelatorio_mestre', 'dvr_nome', 'categoria_status_nome', 'dvr_modelo', 'dvr_marca', 'dvr_ip']]

        # Junção final dos DataFrames para compilar o relatório mestre
        df_relatorio_mestre_cameras = pd.merge(self.df_relatorio_mestre, df_relatorio_diario_cameras_gold, on='idrelatorio_mestre', how='inner')
        df_relatorio_mestre_dvrs = pd.merge(self.df_relatorio_mestre, df_relatorio_diario_dvrs_gold, on='idrelatorio_mestre', how='inner')

        return df_relatorio_mestre_cameras, df_relatorio_mestre_dvrs

    def filter_by_date(self, df, selected_date):
        return df[df['relatorio_data'] == selected_date]

    def count_status(self, df, status_column):
        if status_column not in df.columns:
            st.error(f"A coluna '{status_column}' não foi encontrada.")
            return pd.DataFrame()
        status_counts = df[status_column].value_counts().reset_index()
        status_counts.columns = ['Status', 'Quantidade']
        return status_counts

    def create_status_bar_chart(self, df, x_column, y_column, status_column, colors, title):
        fig = go.Figure()
        for status, color in colors.items():
            fig.add_trace(go.Bar(
                x=df[df[status_column] == status][x_column],
                y=df[df[status_column] == status][y_column],
                name=status,
                marker_color=color,
                text=df[df[status_column] == status][y_column],
                textposition='inside'
            ))
        fig.update_layout(
            barmode='stack',
            xaxis=dict(title=title),
            yaxis=dict(title='Quantidade'),
            margin=dict(t=1),
            legend=dict(
                orientation='h',
                yanchor='top',
                y=-0.2,
                xanchor='center',
                x=0.5
            )
        )
        return fig

    def render_map(self, df, map_object, latitude_column, longitude_column, status_column, name_column):
        if status_column not in df.columns:
            st.error(f"A coluna '{status_column}' não está presente no DataFrame.")
            return

        for _, row in df.iterrows():
            if pd.notna(row[latitude_column]) and pd.notna(row[longitude_column]):
                try:
                    lat = float(row[latitude_column])
                    long = float(row[longitude_column])
                    color = 'green' if row[status_column] == 'Online' else 'red'
                    folium.CircleMarker(
                        location=[lat, long],
                        radius=4,
                        fill=True,
                        fill_opacity=0.9,
                        weight=2,
                        color='black',
                        fill_color=color,
                        stroke=True,
                        popup=row[name_column]
                    ).add_to(map_object)
                except ValueError:
                    continue

def app():
    apply_css()

    report = Report()

    st.markdown(f"<h1 class='dashboard-title'>{config['dashboard_title']}</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        available_dates = report.df_relatorio_mestre['relatorio_data']
        html_content = "<span style='margin-top:15px; float:left;' class='highlight-black'>Data do relatório desejado:</span>"
        st.markdown(html_content, unsafe_allow_html=True)
        report_date = st.selectbox("Selecione uma data", available_dates, format_func=lambda x: x.strftime('%d/%m/%Y'), label_visibility="collapsed")

    with col2:
        st.markdown("<p class='dashboard-descricao'>Este relatório tem por objetivo verificar o funcionamento das câmeras de segurança, garantindo seu perfeito funcionamento e providenciando as manutenções necessárias.</p>", unsafe_allow_html=True)

    st.markdown("<span class='dashboard-subtitle'>Quantitativo Geral:</span>", unsafe_allow_html=True)

    if report_date:
        df_relatorio_filtrado_cameras = report.filter_by_date(report.df_relatorio_mestre_cameras, report_date)
        df_relatorio_filtrado_dvrs = report.filter_by_date(report.df_relatorio_mestre_dvrs, report_date)

        camera_status_counts = report.count_status(df_relatorio_filtrado_cameras, 'categoria_status_nome')
        dvr_status_counts = report.count_status(df_relatorio_filtrado_dvrs, 'categoria_status_nome')

        online_cameras_count = camera_status_counts.loc[camera_status_counts['Status'] == 'Online', 'Quantidade'].sum()
        offline_cameras_count = camera_status_counts.loc[camera_status_counts['Status'] == 'Com defeito', 'Quantidade'].sum()
        online_dvrs_count = dvr_status_counts.loc[dvr_status_counts['Status'] == 'Online', 'Quantidade'].sum()
        offline_dvrs_count = dvr_status_counts.loc[dvr_status_counts['Status'] == 'Offline', 'Quantidade'].sum()

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
                <span class='card'>
                <span class='card-title'>Câmeras 'Online':</span>
                <span class='card-value'>{online_cameras_count}</span>
                </span>
                """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <span class='card'>
                <span class='card-title'>Câmeras 'Com Defeito':</span>
                <span class='card-value'>{offline_cameras_count}</span>
                </span>
                """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <span class='card'>
                <span class='card-title'>DVRs 'Online':</span>
                <span class='card-value'>{online_dvrs_count}</span>
                </span>
                """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
                <span class='card'>
                <span class='card-title'>DVRs 'Offline':</span>
                <span class='card-value'>{offline_dvrs_count}</span>
                </span>
                """, unsafe_allow_html=True)

        st.markdown("<span class='dashboard-subtitle'>Descrição das câmeras e dvrs:</span>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            camera_name_status = df_relatorio_filtrado_cameras[df_relatorio_filtrado_cameras['categoria_status_nome'] == 'Com defeito']
            if not camera_name_status.empty:
                camera_name_status = camera_name_status[['camera_nome', 'dvr_nome']].rename(columns={
                    'camera_nome': 'Câmera com Defeito', 'dvr_nome': 'Nome do DVR'
                })
                st.table(camera_name_status.reset_index(drop=True))
            else:
                st.write("Nenhuma câmera com defeito encontrada.")

            st.divider()

            dvr_name_status = df_relatorio_filtrado_dvrs[df_relatorio_filtrado_dvrs['categoria_status_nome'] == 'Offline']
            if not dvr_name_status.empty:
                dvr_name_status = dvr_name_status[['dvr_nome', 'dvr_ip']].rename(columns={
                    'dvr_nome': 'DVR com Defeito', 'dvr_ip': 'IP do DVR'
                })
                st.table(dvr_name_status.reset_index(drop=True))
            else:
                st.write("Os servidores DVRs estão funcionando com sucesso.")

        with col2:
            camera_counts_by_dvr = df_relatorio_filtrado_cameras.groupby(['dvr_nome', 'categoria_status_nome']).size().reset_index()
            camera_counts_by_dvr.columns = ['DVR', 'Status', 'Quantidade']

            colors = {'Com defeito': '#7C0A02', 'Online': '#003f5c', 'Canal vago': '#ffa600'}
            fig = report.create_status_bar_chart(camera_counts_by_dvr, 'DVR', 'Quantidade', 'Status', colors, 'DVR')
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("<span class='dashboard-subtitle'>Visualização das câmeras por mapa:</span>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            mapa_ilha = folium.Map(
                location=config['map_location_ilha'],
                zoom_start=config['default_zoom_start'],
                tiles=config['map_tiles_url'],
                attr=config['map_attr']
            )
            report.render_map(df_relatorio_filtrado_cameras, mapa_ilha, 'camera_lat', 'camera_long', 'categoria_status_nome', 'camera_nome')
            st_folium(mapa_ilha, use_container_width=True)

        with col2:
            mapa_marui = folium.Map(
                location=[-22.8625333, -43.107546], 
                zoom_start=19, 
                tiles=config['map_tiles_url'], 
                attr=config['map_attr'] 
            )
            report.render_map(df_relatorio_filtrado_cameras, mapa_marui, 'camera_lat', 'camera_long', 'categoria_status_nome', 'camera_nome')
            st_folium(mapa_marui, use_container_width=True)

        st.markdown("<span class='dashboard-subtitle'>Descrição do relatório:</span>", unsafe_allow_html=True)

        relatorio_descricao_filtrado = report.df_relatorio_mestre[report.df_relatorio_mestre['relatorio_data'] == report_date]
        if not relatorio_descricao_filtrado.empty:
            descricao = relatorio_descricao_filtrado.iloc[0]['relatorio_descricao']
            st.markdown(descricao)
        else:
            st.write("Nenhuma descrição encontrada para a data selecionada.")