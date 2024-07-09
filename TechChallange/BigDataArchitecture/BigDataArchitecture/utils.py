import requests
import zipfile
import io
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime, timedelta
import boto3
import os
from dotenv import load_dotenv


# Configurar credenciais
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_session_token = os.getenv('AWS_TOKEN')
bucket_name_s3 = 'techchanllange-fiap2024'

# Criar sessão
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)

# Cliente S3
s3 = session.client('s3')

 # Recuperar dia anterior
yesterday = datetime.now() - timedelta(1)

# Padronizar
data_format = yesterday.strftime('%Y-%m-%d')

def download():
    # URL
    url = f'https://arquivos.b3.com.br/apinegocios/tickercsv/{data_format}'

    # Fazer requisição
    response = requests.get(url)

    # Verificar retorno
    if response.status_code == 200:

        # Ler o conteudo do zip
        zip_file = zipfile.ZipFile(io.BytesIO(response.content))

        # Extrair arquivo
        file_list = zip_file.namelist()
        if len(file_list) == 1 and file_list[0].lower().endswith('.txt'):
            file_txt = zip_file.read(file_list[0]).decode('utf-8')

            # Remover cabecalho (separa arquivo em linhas)
            remove_header = file_txt.strip().splitlines()
            file_txt = "\n".join(remove_header[1:])
            return file_txt           
        else:
            raise ValueError('Falha ao extrair arquivo')
    else:
        raise ValueError('Falha ao fazer download do arquivo')
    
def process(file_request):
    try:

        # Converter para pandas
        df = pd.read_csv(io.StringIO(file_request), delimiter = ';', nrows = 100)

        # Converter para parquet
        file_parquet = pa.Table.from_pandas(df)

        # Configurar s3
        bucket_name = bucket_name_s3

        # Particionar arquivo diariamente
        s3_key = f'particionamento_diario/{data_format}/arquivo.parquet'

        # Fazer upload para s3
        with io.BytesIO() as buf:
            pq.write_table(file_parquet, buf)
            buf.seek(0)
            s3.put_object(Bucket = bucket_name, Key = s3_key, Body = buf.read())

        # Retornar conteudo
        return 'Arquivo enviado com sucesso para o s3!'
    except Exception as e:
        raise ValueError(f"Ocorreu um erro durante o upload para o S3: {str(e)}")
    

def load_from_data_s3(bucket_name, s3_key):
    try:
        df = pq.read_csv(f's3://{bucket_name}/{s3_key}').to_pandas()
        return df.head().to_pandas()
    except Exception as e:
        raise ValueError(f'Erro ao ler dados do s3: {str(e)}')