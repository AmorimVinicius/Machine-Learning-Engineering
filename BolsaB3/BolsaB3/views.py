from .utils import get_ticker, get_data_tickers 
from django.http import HttpResponse
from django.views.decorators.http import require_GET

@require_GET # Este decorator força a view a aceitar apenas requisições POST
def upload_file(request):
    try:
        get_ticker()
        get_data_tickers()
        return HttpResponse('Dados processados com sucesso', status = 200)
    except Exception as e:
        return HttpResponse(f'Erro ao processar dados: {str(e)}', status = 500)