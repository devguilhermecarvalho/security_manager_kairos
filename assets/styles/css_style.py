import streamlit as st

def apply_css():
    css_content = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300;700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;900&display=swap');        
        body, * {
            font-family: 'Outfit', sans-serif;
            line-height: 1.6;
            border: none;
        }
        .ant-menu-item {
            color: red;
        }

        .material-symbols-outlined {
            font-variation-settings:
            'FILL' 0,
            'wght' 400,
            'GRAD' 0,
            'opsz' 24
        }
        header {
            text-align: left;
            margin-bottom: 15px;
        }
        h1 {
            font-family: 'Outfit';
            font-weight: 600;
            padding: 15px 5px 15px 5px;
            color: #0056b3;
            border-bottom: 2px solid #0056b3;
        }
        h2 {
            padding: 5px;
            color: #0056b3;
            font-weight: bold;
            border-bottom: 2px solid #0056b3;
        }
        h3 {
            color: #000;
            font-weight: bold;
            margin-top: 5px;
            margin-bottom: 0;
            padding-bottom: 0;
        }
        h4 {
            font-family: 'Quicksand';
            color: #000;
            font-weight: bold;
            border-bottom: 1px solid #eee;
            margin-top: 5px;
            margin-bottom: 5px;
            padding: 10px 0;
        }
        .highlight {
            color: #0056b3;
            font-weight: bold;
        }
        .highlight-black {
            color: #000;
            font-weight: bold;
        }
        p {
            font-family: 'Outfit';
            font-weight: 300;
            font-size: 16px;
            letter-spacing: 0.3px;
            line-height: 1.6;
            margin-top: 10px;
            margin-bottom: 5px;
            color: #000;
        }
        .p-homepage {
            font-family: 'Outfit';
            font-weight: 300;
            font-size: 18px;
            letter-spacing: 0.3px;
            line-height: 1.6;
            margin-top: 10px;
            margin-bottom: 5px;
            color: #000;
        }
        .card{
            width: 100%;
            height: 150px;
            float: left;
            padding: 12px;
            border-radius: 8px;
            background: #eee;
            border: 5px solid #dedede;
            padding: 10px 10px;
            text-align: center;
            font-size: 16px;
            color: white;
        }

        .card-title{
            width: 100%;
            height: 40px;
            float: left;
            font-family: 'Outfit';
            font-weight: 600;
            font-size: 1.6rem;
            color: #333;
            text-align: center;
            padding: 10px;
            margin-top: 5px;
        }
        
        .card-value{
            width: 100%;
            height: 60px;
            float: left;
            font-family: 'Outfit';
            font-weight: 600;
            font-size: 50px;
            color: #333;
            padding: 0;
            margin: 0;
            text-align: center;
        }

        .dashboard-title{
            font-family: 'Outfit';
            font-weight: 600;
            font-size: 2.8rem;
            color: #0056b3;
            padding: 10px 0 10px 0;
            margin: 5px 0 5px 0;
            border-bottom: 2px solid #0056b3;
        }

        .dashboard-subtitle{
            width: 100%;
            height: auto;
            float: left;
            font-family: 'Outfit';
            font-size: 1.2rem;
            font-weight: 600;
            color: #000;
            border-bottom: 1px solid #eee;
            padding: 5px 0 5px 0;
            margin: 5px 0 5px 0;
        }

        .dashboard-descricao{
            font-family: 'Outfit';
            font-weight: 600;
            font-size: 17px;
            float: left;
            padding-top: 45px;
        }

    </style>
    """
    st.markdown(css_content, unsafe_allow_html=True)
