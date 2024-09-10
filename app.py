# app.py

import streamlit as st
import streamlit_antd_components as sac
from streamlit_option_menu import option_menu

# Configuração inicial do sistema
st.set_page_config(
    page_title="Sistema de Gerenciamento de Câmeras",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🔒"
)

# Importando as páginas do sistema
from custom_pages import (
    main,
    support,
    visual_verification
)

from custom_pages.dashboard import (
    dashboard_cameras
)

from custom_pages.forms import(
    report_daily
)

from custom_pages.management import(
    management_cameras,
    management_dvrs
)

# Sidebar menu
with st.sidebar:
    # Lista de ícones para o menu
    icons = ['house-fill', 'bar-chart-fill', 'file-earmark-binary-fill', 'camera-video-fill', 'check-square-fill', 'device-ssd-fill', 'file-earmark-bar-graph-fill', 'lightning-charge-fill', 'lock-fill']

    # Criação do menu de opções
    selected = option_menu(
        "Menu",
        ["Página Inicial",
        'Dashboard',
        'Preencher Relatório',
        'Verificação das Câmeras',
        'Gerenciamento de Câmeras',
        'Gerenciamento de DVRS',
        'Suporte'],
        icons=icons,
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {},  # Estilo do container do menu
            "icons": {"color": "#000000", "font-size": "15px"},  # Estilo dos ícones não selecionados
            "menu-title": {"font-weight": "bold", "letter-spacing": "1px"},  # Estilo do título do menu
            "nav": {},  # Estilo da navegação
            "nav-item": {},  # Estilo dos itens de navegação
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "font-family": "Segoe UI", "padding-left": "5px", "margin-left": "0", "letter-spacing": "0.1px"},  # Estilo dos links de navegação
            "nav-link-selected": {"background-color": "#005b96", "color": "#FFFFFF", "font-size": "16px", "text-align": "left", "font-weight": "normal", "padding-left": "4px", "margin-left": "0", "letter-spacing": "0", "--icon-color": "#FFFFFF"},  # Estilo dos links selecionados
        }
    )


# Mapeando as páginas às funções correspondentes
if selected == "Página Inicial":
    main.app()
elif selected == "Dashboard":
    dashboard_cameras.app()
elif selected == "Preencher Relatório":
    report_daily.app()
elif selected == "Verificação das Câmeras":
    visual_verification.app()
elif selected == "Gerenciamento de Câmeras":
    management_cameras.app()
elif selected == "Gerenciamento de DVRS":
    management_dvrs.app()
elif selected == "Suporte":
    support.app()
else:
    st.error("Página não encontrada!")