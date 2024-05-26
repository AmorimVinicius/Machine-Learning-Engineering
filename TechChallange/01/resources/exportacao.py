import requests
import csv
from io import StringIO


""" Define metodo para recuperar dados  """
def get_exportacao_tipo(tipo: str):
    dict_tipo = {
        "1" : "ExpVinho",
        "2" : "ExpEspumantes",
        "3" : "ExpUva",
        "4" : "ExpSuco",
    }
    return get_data_exportacao(dict_tipo[tipo])

def get_exportacao_ano(tipo: str, ano: str):
    dict_tipo = {
        "1": "ExpVinho",
        "2": "ExpEspumantes",
        "3": "ExpUva",
        "4": "ExpSuco",
    }
    return get_data_exportacao(dict_tipo[tipo], ano)

def get_exportacao(ano = None):
    tipos_exportacao = ['Vinho', 'Espumantes', 'Uva', 'Suco']
    header = ['id', 'pais'] + [f"{ano}_{coluna}" for ano in range(1970, 2024) for coluna in ['quantidade', 'valor']]
    csv_data = []

    for exportacao in tipos_exportacao:
        index_aux = tipos_exportacao.index(exportacao)
        csv_data.append({'id': index_aux + 1, 'tipo_exportacao': exportacao})
        url = f"http://vitibrasil.cnpuv.embrapa.br/download/Exp{exportacao}.csv"
        response = requests.get(url, headers={'Accept-Charset': 'latin-1'})
        response.encoding = "utf-8"

        with StringIO(response.text) as csv_file:
            reader = csv.DictReader(csv_file, fieldnames=header, delimiter=';')
            next(reader)
            for row in reader:
                initial_dict = {'id': row['id']}
                temp_dict = {
                    f"{ano}": {"quantidade": row.get(f'{ano}_quantidade', '0'), "valor": row.get(f"{ano}_valor", '0')}
                    for ano in range(1970, 2024)}
                initial_dict.update(temp_dict)
                csv_data[tipos_exportacao.index(exportacao)].update({row['pais']: initial_dict})

    if ano:
        for i, row in enumerate(csv_data):
            for key, value in row.items():
                if key != 'tipo_exportacao' and isinstance(value, dict):
                    csv_data[i][key] = {ano: value[ano]}

    return csv_data

def get_data_exportacao(file: str, ano: str = None):
    
    if (ano is not None):
        if (int(ano) < 1970 or int(ano) > 2023):
            return "Ano informado é inválido"

    dados = get_exportacao()

    csv_data = [{key: value for key,value in row.items() if row['tipo_exportacao'] == file[3:]} for row in dados]

    # Filtra por ano, se fornecido
    if ano:
        csv_data = [
            {key: value[ano]} if isinstance(value, dict) and ano in value else {key: value} for row in csv_data for
            key, value in row.items()
        ]

    csv_data = [temp_dict for temp_dict in csv_data if temp_dict]
    
    return csv_data