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
        complet_name = st.text_input('Nome Completo:')
        col_1, col_2 = st.columns(2)
        with col_1:
            date_birth = st.text_input("Data de Nascimento:")
        with col_2:
            phone = st.text_input("Informe seu Telefone:")
        business_name = st.text_input("Nome do negócios:")
        cnpj = st.radio("Possui CNPJ?", ("SIM","NÃO"))
        cnpj_value = st.text_input("Caso a responsta anterior seja afirmativa, informe o seu CNPJ:")
        if cnpj.upper() == "NÃO" or cnpj.upper() == "NAO":
            cnpj_value = "00.000.000/0000-00"
        discricao= st.text_area("Descreva a sua solução:")
        col_3,col_4 = st.columns(2)
        with col_3:
            estagio = st.selectbox("Informe o seu estágio:",["Ideação", "MVP - Protótipo", "Validação", "Vendendo", "Escalando"])
        with col_4:
            desafios = st.multiselect("Informes seus desafios:", ["Marketing","Finanças","Registro de Marca",
            "Gestao de Times","Precificação", "Captação de recurso","Vendas na internet"])
            if len(desafios) > 0:
                desafios_values = '; '.join(desafios)

        
        submit_button = st.form_submit_button(label='Concluido')

    if submit_button:
        array = [[complet_name, date_birth, phone, business_name, cnpj,cnpj_value, discricao, estagio, desafios_values]]
        update_sheets(creds, "Página1!A1", array)
        st.success("Enviado com Sucesso")

if __name__ == '__main__':
    main_streamlit()
