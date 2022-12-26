import streamlit as st
import pandas as pd

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Id do documento do google sheets
SAMPLE_SPREADSHEET_ID = '1rPjh2J-TX5qIjdELLJMIlrMCT80d6dwnV-CcXBngDNc'
SAMPLE_RANGE_NAME = 'Página1!A1:B3'

# função de escrita no google sheets


def update_sheets(creds: str, page: str, valueInput: str):
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                          range=page, valueInputOption="USER_ENTERED",
                          body={"values": valueInput}).execute()


def main_streamlit():
    '''Validação das credenciais e leitura do token ou a criação do token'''
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'venv/client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # ======================Streamlit=====================================
    st.title("Formulários de Diagnóstico")
    st.subheader("Dados do Empreendedor")

    # Metodo Contexto
    
    with st.form(key='forms_dados'):
        col, col_0 = st.columns(2)
        with col:
            complet_name = st.text_input('Nome Completo:')
        with col_0:
            city = st.text_input("Informe a sua Cidade: ")
        col_1, col_2 = st.columns(2)
        with col_1:
            date_birth = st.text_input("Data de Nascimento:")
        with col_2:
            phone = st.text_input("Informe seu Whatsapp com DDD:")
        business_name = st.text_input("Nome do negócios:")
        cnpj = st.radio("Possui CNPJ?", ("SIM","NÃO"))
        cnpj_value = st.text_input("Caso a responsta anterior seja afirmativa, informe o seu CNPJ:")
        if cnpj.upper() == "NÃO" or cnpj.upper() == "NAO":
            cnpj_value = "00.000.000/0000-00"
        discricao= st.text_area("Descreva a sua solução:")
        col_3, col_4 = st.columns(2)
        with col_3:
            area_solution = st.selectbox("Qual o principal segmento de atuação da startup?",
            [
                "Adtech (Advertising)", "Agetech (Saúde e Bem Estar da Pessoa Idosa)",
                "Agtech (Agronegócio)", "Autotech (Setor Automotivo", 
                "Babytech (Setor Infantil)", "Beautytech (Beleza)", "Biotech (Biotecnologia)",
                "CleanTech (Tecnologia limpa)", "Condotech (Condomínio)", "Construtech (Construção Civil)",
                "Cybersecurity (Segurança e defesa)", "Edtech (Educação)", "Energytech (Energia)", "Eventstech (Evento)",
                "Fashiontech (Moda)", "Fintech (Finanças)", "Foodtech (Alimentação)", "Funtech (Entreterimento)",
                "Gametech (Game)","Govtech (Gestão Pública)", "Greentech (Meio Ambiente e Sustentabilidade)",
                "Healthtech e Life Science (Saúde e Bem-Estar)", "Hrtech (Recursos Humanos)", "Indtech (Indústria)",
                "Insurtech (Seguro)", "Lawtech (Direito)", "Logtech (Lógistica)", "Martech (Marketing)",
                "Mineração", "MVNO (TIC e Telecom)", "Nanotech (Nanotecnologia)", "Óleo e Gás",
                "Pettech (Imobiliario)", "Regtech (Compliance)", "Retailtech (Varejo)",
                "Robotech (Robótica)", "Salestech (Vendas)", "Smart City", "Socialtech (Impacto Social)",
                "Sportstech (Esporte)", "Tech (Desevolvimento de Software)", "Turistech (Turismo)"
            ])
        with col_4:
            social_midia = st.text_input("Link do site ou rede social: ")
        col_5,col_6 = st.columns(2)
        with col_5:
            estagio = st.selectbox("Informe o seu estágio:",
            ["Ideação (em desenvolvimento da ideia, estudo do mercado, identificação de oportunidades, nichos e soluções)",
             "Validação (em fase de validação do protótipo - MVP - e dos primeiros clientes)", 
             "Operação (protótipos validados, modelo de negócio definido, conhecimento do mercado)", 
             "Tração (métricas e objetivos definidos, busca de parceiras para crescimento)", 
             "Escala (crescimento médio anual acima de 20% ao ano, em termos de empregados)"])
        with col_6:
            desafios = st.multiselect("Informes seus desafios:", ["Marketing","Finanças","Registro de Marca",
            "Gestao de Times","Precificação", "Captação de recurso","Vendas na internet"])
            if len(desafios) > 0:
                desafios_values = '; '.join(desafios)

        col_7, col_8 = st.columns(2)
        with col_7:
            business_model = st.selectbox("Qual é o principal modelo de negócio da startup:",
            ["API Application Programming Interface (clientes que assinam ou pagam pelo uso de uma API)",
            "Clube de assinatura recorrente (quando algum serviço é disponibilizado através de um plano de assinatura)",
            "Consumer (app gratuito ou de baixo custo entregando valor ou engajamento aos usuários)",
            "Hardware (cobrança pelo hardware e/ou software do hardware e/ou serviços agregados)",
            "Licenciamento (licenciamento de propriedades intelectuais que incluem patentes, marcas comerciais, segredos comerciais)",
            "Marketplace (quando dois ou mais usuários realizam uma transação)",
            "SaaS (software disponibilizado a usuários através de assinatura)",
            "Taxa sobre transações (clientes pagam uma taxa em cima da operação de um serviço)",
            "Venda de dados (serviços de coleta, tratamento, formatação e análise de dados)",
            "Venda direta (venda de produtos online ou presencial gerando receita através de margem sobre produtos vendidos)"
            ])
        with col_8:
            publico = st.selectbox("Qual o principal público-alvo da startup:",
            ["Consumidor final (B2C)", "Empresas (B2B)","Empresas e consumidor final (B2B2C)", "Governo (B2G)",
            "Peer-to-Peer (P2P)", "Startups (B2S)"])
        
        submit_button = st.form_submit_button(label='Concluido')

    if submit_button:
        array = [[complet_name, city, date_birth, phone, business_name, cnpj,cnpj_value, discricao, area_solution, social_midia, estagio, desafios_values, business_model,publico]]
        update_sheets(creds, "Página1!A1", array)
        st.success("Enviado com Sucesso")

if __name__ == '__main__':
    main_streamlit()
