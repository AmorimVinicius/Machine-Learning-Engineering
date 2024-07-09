from django.http import HttpResponse
from .utils import download,  process, load_from_data_s3
from datetime import datetime, timedelta
from django.shortcuts import render

# Padronizar data
yesterday = datetime.now() - timedelta(1)
data_format = yesterday.strftime('%Y-%m-%d')

def download_and_process(request):
    try:
        # Adicione um breakpoint aqui
        #pdb.set_trace()
        # Download
        file_txt = download()
        result = process(file_txt) 
        return HttpResponse(result)
    except Exception as e:
        return HttpResponse(f'Erro ao processar dados: {str(e)}', status = 500)
    

def view(request):
    try:
        bucket_name = 'techchanllange-fiap2024'
        s3_key = f'particionamento_diario/{data_format}/arquivo.parquet'

        # Chamar funcao
        data_html = load_from_data_s3(bucket_name, s3_key)

        # Render
        return render(request, 'view.html', {'data_html': data_html})

    except Exception as e:
        return HttpResponse(f'Erro ao visualizar os dados: {str(e)}', status = 500)