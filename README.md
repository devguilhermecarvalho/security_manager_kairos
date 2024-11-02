# Sistema de Gerenciamento de Câmeras de Segurança

Este foi desenvolvido para melhorar o gerenciamento de câmeras e sensores de segunça do estaleiro atráves de dados disponíves em APIs. Ele permite a visualização, verificação e gerenciamento de câmeras e DVRs, permitindo a verificação de funcionamento e qualidade. A aplicação também oferece um dashboard para monitoramento situacional das câmeras, além de permitir o preenchimento de relatórios diários.

## Tecnologias Utilizadas

- Python | Streamlit | OpenCV | Pandas | Folium | SQL | PostgreSQL


## Antes

Imagens de como eram armazenadas as informações antes do novo sistema:

- Dashboard em excel:
![alt text](assets/imagens/antes-01.png)

- Dados armazenados em tabelas:
![alt text](assets/imagens/antes-02.png)

## Depois

- Página Inicial do Sistema Atual
![alt text](assets/imagens/depois-05.png)

- Página de preenchimento do relatório:
![alt text](assets/imagens/depois-03.png)

- Novo modelo do dashboard:
![alt text](assets/imagens/depois-01.png)
![alt text](assets/imagens/depois-02.png)

- Verificação de funcionamento das câmeras através dos IPs:
![alt text](assets/imagens/depois-04.png)

- Banco de dados:
Tabelas:
![alt text](assets/imagens/tabelas-01.png)
![alt text](assets/imagens/tabelas-02.png)
![alt text](assets/imagens/tabelas-03.png)

## Funcionalidades

- **Página Inicial:** Descrição do sistema e mapa interativo com as localizações das câmeras.
- **Dashboard:** Visualização do status das câmeras e DVRs, com gráficos e mapas.
- **Preenchimento de Relatório Diário:** Interface para registrar o status diário das câmeras e DVRs.
- **Verificação das Câmeras:** Verificação do status de câmeras em várias bases via RTSP.
- **Gerenciamento de Câmeras e DVRs:** Interfaces para modificar as informações no banco de dados.

## Estrutura do Projeto

```bash
camera-management-system/
│
├── app.py                    # Arquivo principal da aplicação, responsável por iniciar a interface do Streamlit
│
├── custom_pages/              # Contém as páginas customizadas do sistema, com layout e funcionalidades específicas
│   ├── dashboard              # Páginas referente a dashboardas
│   ├── forms                  # Formulários de preenchimento
│   ├── management             # Gerenciamento de informações
│
├── database/                  # Módulo para gerenciamento de conexões e consultas ao banco de dados
│   ├── connect_db.py          # Script para conectar ao banco de dados
│   └── queries.py             # Consultas SQL usadas no sistema
│
├── assets/                    # Diretório para arquivos de CSS e plugins adicionais para customização visual
│   ├── styles/                # Arquivo de estilos CSS customizados
│   └── plugins/               # Plugins adicionais utilizados pela aplicação
│
├── .env                       # Arquivo de configuração com variáveis de ambiente (credenciais e configurações sensíveis)
│
├── requirements.txt           # Lista de dependências necessárias para rodar o projeto
│
└── README.md                  # Documentação do projeto
