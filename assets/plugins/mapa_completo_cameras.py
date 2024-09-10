# assets/plugins/mapa_completo_cameras.py

import streamlit as st
import folium
import pandas as pd
from database.connect_db import *
from database.queries import DatabaseQueries

db_queries = DatabaseQueries()

def mapa_completo_das_cameras():
    """
    Função para gerar o mapa com as localizações das câmeras.
    """

    # Cria o mapa com as configurações iniciais
    mapa_completo = folium.Map(
        location=[-22.862219, -43.1210519], 
        zoom_start=16,
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Tiles &copy; Esri',
        zoom_control=True,       # Ativa os controles de zoom
        scrollWheelZoom=False,   # Desativa zoom com o scroll do mouse
        dragging=True,           # Ativa o arrastar do mapa
        touchZoom=True,          # Permite zoom com toque (importante para acesso via dispositivos móveis)
        doubleClickZoom=True     # Ativa o zoom com duplo clique
    )

        # Adiciona marcadores para cada câmera
    df_cameras = db_queries.get_latitude_and_longitude_cameras()
    
    for index, row in df_cameras.iterrows():
        camera_nome = row['camera_nome']
        camera_lat = row['camera_lat']
        camera_long = row['camera_long']
        if pd.notnull(camera_lat) and pd.notnull(camera_long):
            # Converte para float
            lat = float(camera_lat)
            long = float(camera_long)
            icon_color = 'green'
            icon = folium.Icon(color=icon_color, icon='camera', prefix='fa')
            folium.CircleMarker(
                location=[lat, long],
                radius=3,
                popup=camera_nome,
                fill=True,
                fill_opacity=0.9,
                fill_color='green',
                weight=2,
                color='black',
                stroke=True,
                icon=icon
            ).add_to(mapa_completo)
    
    # Adiciona uma linha poligonal no mapa
    coordenadas = [
        (-22.86329090603045, -43.12631600976351),
        (-22.864343900958332, -43.124078713748304),
        (-22.864493534348796, -43.11927909509546),
        (-22.86235009584774, -43.113567127965794),
        (-22.86179229919734, -43.11018869959798),
        (-22.862636824006, -43.107979216677904)
    ]

    folium.PolyLine(coordenadas, color='yellow', weight=5, dash_array='5, 10', opacity=0.5).add_to(mapa_completo)

    st.components.v1.html(mapa_completo._repr_html_(), height=1200)