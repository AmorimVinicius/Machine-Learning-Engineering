import requests
import csv
from io import StringIO


""" Define metodo para recuperar dados  """
def get_importacao_tipo(tipo: str):
    dict_tipo = {
        "1" : "ImpVinhos",
        "2" : "ImpEspumantes",
        "3" : "ImpFrescas",
        "4" : "ImpPassas",
        "5" : "ImpSuco"
    }
    return get_data_importacao(dict_tipo[tipo])

def get_importacao_ano(tipo: str, ano: str):
    dict_tipo = {
        "1" : "ImpVinhos",
        "2" : "ImpEspumantes",
        "3" : "ImpFrescas",
        "4" : "ImpPassas",
        "5" : "ImpSuco"
    }
    return get_data_importacao(dict_tipo[tipo], ano)

def get_importacao(ano = None):
    tipos_importacao = ['Vinhos', 'Espumantes', 'Frescas', 'Passas', 'Suco']
    header = ['id', 'pais'] + [f"{ano}_{coluna}" for ano in range(1970, 2024) for coluna in ['quantidade', 'valor']]
    csv_data = []

    for importacao in tipos_importacao:
        index_aux = tipos_importacao.index(importacao)
        csv_data.append({'id': index_aux + 1, 'tipo_importacao': importacao})
        url = f"http://vitibrasil.cnpuv.embrapa.br/download/Imp{importacao}.csv"
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
                csv_data[tipos_importacao.index(importacao)].update({row['pais']: initial_dict})

    if ano:
        for i, row in enumerate(csv_data):
            for key, value in row.items():
                if key != 'tipo_importacao' and isinstance(value, dict):
                    csv_data[i][key] = {ano: value[ano]}

    return csv_data

def get_data_importacao(file: str, ano: str = None):

    # Verifica se o ano está dentro do intervalo válido, se fornecido
    if ano is not None:
        if int(ano) < 1970 or int(ano) > 2023:
            return "Ano informado é inválido"

    dados = get_importacao()

    csv_data = [{key: value for key, value in row.items() if row['tipo_importacao'] == file[3:]} for row in dados]

    # Filtra por ano, se fornecido
    if ano:
        csv_data = [
            {key: value[ano]} if isinstance(value, dict) and ano in value else {key: value} for row in csv_data for key, value in row.items()
        ]

    csv_data = [temp_dict for temp_dict in csv_data if temp_dict]

    return csv_data