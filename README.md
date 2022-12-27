# 🚀 Mapeamento de startups com Streamlit e Google Sheets
Esse projeto é um MVP (produto mínimo viável) e tem como objetivo ser um mapeamento dinâmico das startups existentes dentro do ecossistema local de inovação do estado de Rondônia. Na versão de MVP ele será um forms online com integração com a API do google sheets onde receberá os dados e alimentará uma dashboard interativa. 

### 📋 Pré-requisitos
O principal requisito deste projeto é a integração com a API do google Sheets e as instalações das bibliotecas de python.
- **[API Google Sheets](https://console.cloud.google.com/apis/dashboard)**
- **[google-auth-oauthlib](https://pypi.org/project/google-auth-oauthlib/)**

```
$ pip install google-auth-oauthlib
```
- **[Streamlit](https://streamlit.io/)**
```
$ pip install streamlit
```
### 🛠️ Executando 
Para testar o projeto basta executar o código em sua máquina.
```
streamlit run Streamlit_Sheet.py
```