import streamlit as st
import pandas as pd
import boto3
import os
from io import StringIO, BytesIO
import pyarrow.parquet as pq
from dotenv import load_dotenv, dotenv_values 
# Para gerar indicadores técnicos
import ta
import joblib

load_dotenv() 

aws_access_key = os.getenv('aws_access_key')
aws_secret_key = os.getenv('aws_secret_key')
session_token = os.getenv('session_token')

# Carrega o modelo Randon Forest
model = joblib.load('./model/random_forest_model.joblib')

# Iniciar uma sessão com as credenciais
s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    aws_session_token=session_token  # Inclua isso se houver um token de sessão
)

# Função para deselecionar todas as ações
def clear_selection():
    st.session_state.selected_stocks = []  # Limpa a seleção, mas não remove da lista

# Função para ler dados do S3
def read_data_from_s3(bucket_name, prefix):
    # Listar todos os arquivos parquet dentro do bucket/pasta
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix = prefix)
    arquivos = [content['Key'] for content in response.get('Contents', [])]

    # Lista para armazenar os dataframes
    dataframes = []

    # Ler cada arquivo parquet e adicionar à lista de dataframes
    for arquivo in arquivos:
        obj = s3.get_object(Bucket=bucket_name, Key=arquivo)
        # Verifique o tamanho do arquivo antes de tentar ler
        if obj['ContentLength'] > 0:
            with BytesIO(obj['Body'].read()) as f:
                df = pq.read_table(f).to_pandas()
                dataframes.append(df)

    # Consolidar todos os dataframes em um único dataframe
    df = pd.concat(dataframes, ignore_index=True)

    df['Data'] = pd.to_datetime(df['Data'])

    dia_mais_atual = df['Data'].max()

    df_atual = df[df['Data'] == dia_mais_atual][['Ticker','Fechamento','Data','FechamentoAnterior', 'MaiorValor', 'MenorValor', 'Abertura','MenorValor','MaiorValor','MediaDe200Dias','AltaDe52Semanas','MediaDe50Dias']]

    return df_atual

# Função para prever a tendência de uma ação
def predict_trend(data):
    print(data.columns.to_list())
    return model.predict(data)

# Função para calcular indicadores técnicos
def calculate_indicators(df):
    df['SMA_10'] = ta.trend.sma_indicator(df['Fechamento'], window=10) # Média Móvel Dos Últimos 10 Dias
    df['EMA_10'] = ta.trend.ema_indicator(df['Fechamento'], window=10) # Média Móvel Exponencial
    df['bollinger_hband'] = ta.volatility.bollinger_hband(df['Fechamento'], window=20, window_dev=2) # Banda de Bolliger High
    df['bollinger_lband'] = ta.volatility.bollinger_lband(df['Fechamento'], window=20, window_dev=2) # Banda de Bolliger Low
    return df

def model_predict(df):
    features = ['Abertura','MenorValor','MaiorValor','EMA_10','SMA_10','bollinger_hband','bollinger_lband','MediaDe200Dias','AltaDe52Semanas','MediaDe50Dias']
    dados_full = df.sort_values(by=['Ticker', 'Data'])
    dados_full.groupby('Ticker').apply(calculate_indicators)
    dados_full.dropna(subset=['Data'], inplace=True)
    dados_full.dropna(subset=features, inplace=True)
    dados_predict = dados_full[['Abertura','MenorValor','MaiorValor','EMA_10','SMA_10','bollinger_hband','bollinger_lband','MediaDe200Dias','AltaDe52Semanas','MediaDe50Dias']]
    dados = dados_predict.loc[:, ~dados_predict.columns.duplicated()]
    dados_full['Tendencia'] = predict_trend(dados)
    return dados_full

# Nome do bucket e caminho dos dados
bucket_name = 'techchanllange-fiap2024'
prefix = 'parquet/'

# Ler dados do bucket AWS
df = read_data_from_s3(bucket_name, prefix)

df = calculate_indicators(df)

df = model_predict(df)

df['Percentual'] = ((df['Fechamento'] - df['FechamentoAnterior']) / df['FechamentoAnterior']) * 100


# Filtrar as ações com tendência de alta e baixa
acoes_em_alta = df[(df['Tendencia'] == 2) & (df['Percentual'] != 0.0000) & (df['Percentual'] > 0.0000)][['Ticker', 'Fechamento', 'Percentual']]
acoes_em_baixa = df[(df['Tendencia'] == 0) & (df['Percentual'] != 0.0000) & (df['Percentual'] < 0.0000) ][['Ticker', 'Fechamento', 'Percentual']]

# Configurações iniciais da página
st.set_page_config(page_title="Pos Tech FIAP - Trabalho 3", layout="wide")

st.title("Pos Tech FIAP - Trabalho 3 | Previsão de Tendência de Ações da Bolsa de Valores")

st.sidebar.title('Seleção de Ações')
all_stocks = df[(df['Tendencia'].isin([0,2])) & (df['Percentual'] != 0.0000)]['Ticker'].unique()  # Supondo que tenha uma coluna 'acao' com os nomes

# Inicializar o estado da seleção no session_state
if 'selected_stocks' not in st.session_state:
    st.session_state.selected_stocks = all_stocks  # Inicializa com todas as ações selecionadas

selected_stocks = st.sidebar.multiselect('Escolha as ações:', all_stocks, default=st.session_state.selected_stocks)

# Botão para deselecionar todas as ações
if st.sidebar.button('Deselecionar Todas'):
    clear_selection()
    
if len(selected_stocks) > 1:
    col1, col2 = st.columns(2)
    with col1:
        st.header('Ações em Alta')
        st.table(acoes_em_alta)

    # Exibir DataFrame de ações em baixa na segunda coluna
    with col2:
        st.header('Ações em Baixa')
        st.table(acoes_em_baixa)


elif len(selected_stocks) == 0:
    st.write("Selecione as ações no menu lateral esquerdo para demonstração gráfica.")