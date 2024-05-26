from fastapi import FastAPI
from resources.processamento import get_processamento_tipo, get_processamento, get_processamento_tipo_ano
from resources.producao import get_data_producao, get_data_producao_ano
from resources.comercializacao import get_dados_comercializacao, get_dados_comercializacao_ano
from resources.importacao import get_importacao, get_importacao_ano, get_importacao_tipo
from resources.exportacao import get_exportacao, get_exportacao_tipo, get_exportacao_ano

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Fase 1: Tech Chalange - Machine Learning Enginnering"}


@app.get("/producao")
async def get_producao():
    """ Retorna toda a produção entre os anos de 1970 e 2022, não necessita de parâmetros """
    return get_data_producao()


@app.get("/producao/{ano}")
async def get_producao(ano: str):
    """ Retorna a producao total do ano informado, sendo necessário adicionar o parâmetro [ano], entre os anos de 1970 e 2022 (qualquer valor diferente disso irá retornar como erro)"""
    return get_data_producao_ano(ano)


@app.get("/processamento")
async def processamento():
    """ Retorna todo o processamento entre os anos de 1970 e 2022, não necessita de parâmetros"""
    return get_processamento()


@app.get("/processamento_ano/{ano}")
async def processamento(ano: str):
    """ Retorna todo o processamento do ano informado, sendo necessário adicionar o parâmetro [ano]
        entre os anos de 1970 e 2022 (qualquer valor diferente disso irá retornar como erro)
    """

    return get_processamento(ano)


@app.get("/processamento/{tipo}")
async def processamento_tipo(tipo: str):
    """ Retorna o tipo de processamento entre os anos de 1970 até 2022

    O parâmetro [tipo] deve ser enviado utilizando os números entre 1 e 4 (qualquer valor diferente disso, irá retornar como erro)

    Referência:

        1: Viníferas

        2: Americanas e híbridas

        3: Uvas de mesa

        4: Sem classificação

    """
    return get_processamento_tipo(tipo)


@app.get("/processamento/{tipo}/{ano}")
async def processamento_tipo_ano(tipo: str, ano: str):
    """ Retorna o tipo de processamento do ano informado

    O parâmetro [tipo] deve ser enviado utilizando os números entre 1 e 4 (qualquer valor diferente disso, irá retornar como erro)

    O parâmetro [ano] deve ser enviado entre 1970 e 2022 (qualquer valor diferente disso, irá retornar como erro)

    Referência:

        1: Viníferas

        2: Americanas e híbridas

        3: Uvas de mesa

        4: Sem classificação
    """

    return get_processamento_tipo_ano(tipo, ano)


@app.get("/comercializacao")
async def get_comercializacao():
    """ Retorna toda a comercialização entre os anos de 1970 e 2022, não necessita de parâmetros """
    return get_dados_comercializacao()


@app.get("/comercializacao/{ano}")
async def get_comercializacao(ano: str):
    """ Retorna toda a comercialização do ano informado, sendo necessário adicionar o parâmetro [ano]
        entre os anos de 1970 e 2022 (qualquer valor diferente disso irá retornar como erro)
    """
    return get_dados_comercializacao_ano(ano)


@app.get('/importacao')
async def importacao():
    """ Retorna todos os dados de importação entre os anos de 1970 até 2023 (qualquer valor diferente disso, irá retornar como erro)

    Não necessita de parâmetros
    """
    return get_importacao()


@app.get("/importacao_ano/{ano}")
async def importacao(ano: str):
    """ Retorna os dados de importação entre os anos de 1970 até 2023

    O parâmetro [ano] deve ser enviado utilizando o intervalo de data informado acima (qualquer valor diferente disso, irá retornar como erro)

    """
    return get_importacao(ano)


@app.get('/importacao/{tipo}')
async def importacao_tipo(tipo: str):
    """ Retorna todos os dados de importação entre os anos de 1970 até 2023

    O parâmetro [tipo] deve ser enviado utilizando os números entre 1 e 5 (qualquer valor diferente disso, irá retornar como erro)

    Referência:

        1: Vinhos de mesa

        2: Espumantes

        3: Uvas Frescas

        4: Uvas Passas

        5: Suco de Uva
    """
    return get_importacao_tipo(tipo)


@app.get('/importacao/{tipo}/{ano}')
async def importacao_ano(tipo: str, ano: str):
    """ Retorna todos os dados de importação entre os anos de 1970 até 2023

        O parâmetro [tipo] deve ser enviado utilizando os números entre 1 e 5 (qualquer valor diferente disso, irá retornar como erro)

        O parâmetro [ano] deve ser enviado entre 1970 e 2023 (qualquer valor diferente disso, irá retornar como erro)

        Referência:

            1: Vinhos de mesa

            2: Espumantes

            3: Uvas Frescas

            4: Uvas Passas

            5: Suco de Uva

        """
    return get_importacao_ano(tipo, ano)


@app.get("/exportacao")
async def exportacao():
    """ Retorna todos os dados de exportação entre os anos de 1970 até 2023 (qualquer valor diferente disso, irá retornar como erro)

    Não necessita de parâmetros
    """
    return get_exportacao()


@app.get("/exportacao_ano/{ano}")
async def exportacao(ano: str):
    """ Retorna os dados de exportação entre os anos de 1970 até 2023

    O parâmetro [ano] deve ser enviado utilizando o intervalo de data informado acima (qualquer valor diferente disso, irá retornar como erro)
        """
    return get_exportacao(ano)


@app.get("/exportacao/{tipo}")
async def exportacao_tipo(tipo: str):
    """ Retorna todos os dados de exmportação entre os anos de 1970 até 2023

    O parâmetro [tipo] deve ser enviado utilizando os números entre 1 e 5 (qualquer valor diferente disso, irá retornar como erro)

    Referência:

        1: Vinhos de mesa

        2: Espumantes

        3: Uvas Frescas

        4: Suco de uva
    """
    return get_exportacao_tipo(tipo)


@app.get("/exportacao/{tipo}/{ano}")
async def exportacao(tipo: str, ano: str):
    """ Retorna todos os dados de importação entre os anos de 1970 até 2023

    O parâmetro [tipo] deve ser enviado utilizando os números entre 1 e 5 (qualquer valor diferente disso, irá retornar como erro)

    O parâmetro [ano] deve ser enviado entre 1970 e 2023 (qualquer valor diferente disso, irá retornar como erro)

    Referência:

        1: Vinhos de mesa

        2: Espumantes

        3: Uvas Frescas

        4: Suco de uva
     """
    return get_exportacao_ano(tipo, ano)


# adicionando para testes
if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)