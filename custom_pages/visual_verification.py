import os
import streamlit as st
import cv2
import numpy as np
from PIL import Image
from dotenv import load_dotenv
import time

from assets.styles.css_style import apply_css

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

def app():
    apply_css()
    st.markdown("<h1>Verificação de Câmeras</h1>", unsafe_allow_html=True)

    # Dicionário de URLs para cada base, junto com o número do range
    dvr_urls = {
        "Administração": {"url": os.getenv("ADMINISTRACAO_URL"), "range": 16},
        "Cais do Carvão": {"url": os.getenv("CAIS_DO_CARVAO_URL"), "range": 10},
        "Casarão": {"url": os.getenv("CASARAO_URL"), "range": 18},
        "Igrejinha": {"url": os.getenv("IGREJINHA_URL"), "range": 18},
        "Lixão": {"url": os.getenv("LIXAO_URL"), "range": 8},
        "Maruí": {"url": os.getenv("MARUI_URL"), "range": 16},
        "Portaria": {"url": os.getenv("PORTARIA_URL"), "range": 18},
        "Produção e Diques": {"url": os.getenv("PRODUCAO_DIQUES_URL"), "range": 16}
    }

    # Função para capturar uma única imagem da câmera e verificar a variância
    def verificar_camera(url_template, i, timeout=30):
        url_do_fluxo = url_template.format(i)
        start_time = time.time()
        cap = cv2.VideoCapture(url_do_fluxo)

        while not cap.isOpened():
            if time.time() - start_time > timeout:
                cap.release()
                return None, f"Tempo de espera excedido ao tentar abrir o fluxo da câmera {i}."
            time.sleep(1)  # Aguardar 1 segundo antes de tentar novamente

        ret, frame = cap.read()
        cap.release()

        if ret:
            variancia = np.var(frame)
            if variancia > 1000:
                return frame, f"<span style='color: green;'>A câmera {i} está ligada. Variância: {variancia:.2f}</span>"
            else:
                return frame, f"<span style='color: red;'>A câmera {i} está desligada. Variância: {variancia:.2f}</span>"
        else:
            return None, f"Erro ao capturar o frame da câmera {i}."

    # Função para processar câmeras sequencialmente
    def processar_cameras_sequencialmente(url_template, num_cameras):
        resultados = []
        for i in range(1, num_cameras + 1):
            resultado = verificar_camera(url_template, i)
            resultados.append(resultado)
        return resultados

    # Botão para verificar uma base específica
    base_selecionada = st.selectbox("Selecione a base para verificar as câmeras:", list(dvr_urls.keys()))
    if st.button(f'Verificar Câmeras da Base "{base_selecionada}"'):
        with st.container():  # Agrupa as imagens em uma tabela
            info_base = dvr_urls[base_selecionada]
            num_base = info_base["range"]

            # Processa todas as câmeras da base selecionada sequencialmente
            resultados = processar_cameras_sequencialmente(info_base["url"], num_base)

            # Exibe os resultados
            columns = st.columns(4)  # Define o número de colunas no grid
            for i, (imagem, mensagem) in enumerate(resultados, start=1):
                if imagem is not None:
                    img_pil = Image.fromarray(cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB))
                    img_resized = img_pil.resize((600, 600))  # Redimensiona a imagem
                    columns[(i - 1) % 4].image(img_resized, caption=f"Câmera {i}", use_column_width=True)
                    columns[(i - 1) % 4].markdown(mensagem, unsafe_allow_html=True)
                else:
                    columns[(i - 1) % 4].markdown(mensagem, unsafe_allow_html=True)