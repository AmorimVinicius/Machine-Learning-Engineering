import requests
import zipfile
import io
from datetime import datetime, timedelta
from django.http import HttpResponse

def download_price(request):
    # Recuperar dia anterior
    ontem = datetime.now() - timedelta(1)

    # Padronizar
    formata_data = ontem.strftime('%Y-%m-%d')

    # URL
    url = f'https://arquivos.b3.com.br/apinegocios/tickercsv/{formata_data}'

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
            remove_cabecalho = file_txt.strip().splitlines()
            file_txt = "\n".join(remove_cabecalho[1:])

            # Retornar conteudo
            return HttpResponse(file_txt, content_type = 'text/plan')
        else:
            return HttpResponse('Falha ao recuperar arquivo txt do zip', status = 500)
    else:
        return HttpResponse(f'Falha ao recuperar dados do pregão de {ontem}', status = 500)
    