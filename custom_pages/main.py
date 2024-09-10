import streamlit as st
from assets.styles.css_style import apply_css
from assets.plugins.mapa_completo_cameras import mapa_completo_das_cameras

def app():
    """
    Função principal da página inicial.
    """
    apply_css()
    
    # Conteúdo da página 01
    st.markdown("<h1>🔒 - Sistema de Gerenciamento de Câmeras</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # Texto descritivo do sistema de câmeras
        html_content = """
        <p class='p-homepage'>Este sistema é sua ferramenta central para monitorar, gerenciar e analisar as informações vitais das câmeras de segurança que vigiam constantemente a Ilha do Viana. Estrategicamente posicionadas em locais-chave, essas câmeras garantem uma vigilância completa, oferecendo tranquilidade e segurança para nossas operações.</p>
        <p class='p-homepage'>Localizado estrategicamente na Baía da Guanabara, o estaleiro <span class="highlight">RENAVE</span> é uma referência na reparação naval, atendendo a demanda nacional e internacional de embarcações de todos os tipos e portes. Com uma <span class="highlight-black">área de 160.000 m²</span> e uma infraestrutura robusta, nossas instalações oferecem suporte completo a projetos de reparo e manutenção, cumprindo os mais altos padrões de excelência.</p>
        <p class='p-homepage'>Este sistema não apenas permite o acesso rápido e eficiente às imagens das câmeras, mas também fornece recursos de análise para identificar potenciais ameaças ou anomalias. Combinando tecnologia avançada e segurança de ponta, estamos comprometidos em garantir a proteção de nossos colaboradores, instalações e operações.</p>
        <p class='p-homepage'>Explore o mapa interativo para visualizar a localização precisa de cada câmera.</p>
        """
        st.markdown(html_content, unsafe_allow_html=True)

    with col2:
        # Imagem do Mapa Estaleiro Renave
        st.image("assets/imagens/img-terminalnovo.jpg")

    # Conteúdo da página 02
    st.markdown("<h2>🗺️ - Mapa de Distribuição de Câmeras</h2>", unsafe_allow_html=True)
    mapa_completo_das_cameras()

