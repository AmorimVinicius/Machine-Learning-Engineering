# TechChallenge 01 - API Embrapa

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)

Esta API foi desenvolvida como parte do trabalho tech challenge da pós-graduação em Engenharia de Machine Learning. Ela foi projetada para ler os dados a partir de um CSV do site da Embrapa e disponibiliza-los de acordo com tema pelas rotas definidas.

## Objetivo do Projeto

O principal objetivo desta API é facilitar a coleta, armazenamento e manipulação de dados que são disponibilizados em um site que contém as informações sobre produção de vinhos, sucos e derivados provenientes do Rio Grande do Sul. Para isso, foi criado as rotas necessárias sobre cada aba do site que englobam: Produção, Processamento, Comercialização, Importação e Exportação.

## Índice

- [Instalação](#instalação)
- [Uso](#uso)
- [Endpoints](#endpoints)
  - [GET /producao](#get-producao)
  - [GET /processamento](#get-processamento)
  - [GET /comercializacao](#get-comercializacao)
  - [GET /importacao](#get-importacao)
  - [GET /exportacao](#get-exportacao)
- [Erros](#erros)
- [Arquitetura de Deploy](#arquitetura-de-deploy)
- [Contribuição](#contribuição)

## Instalação

Instruções sobre como instalar e configurar a API.  

### Pré-requisitos

- Python (versão 3.9 ou superior)
- pip (gerenciador de pacotes do Python)
- Git (para clonar o repositório)
- FastAPI

Siga como base o arquivo de requerimentos disponível na pasta 01.

### Passo a Passo

1. **Clone o repositório:**

```sh
git clone https://github.com/AmorimVinicius/Machine-Learning-Engineering.git
cd Machine-Learning-Engineering/TechChallange/01
```

2. **Crie um ambiente virtual:**

Como boa prática, utilize um ambiente virtual para isolar as dependências desse projeto.

```sh
python -m venv venv 
```

3. **Ative o ambiente virtual:** 

    - No Windows:
        ```sh
        venv\Scripts\activate
        ```
    
    - No macOs/Linux:
        ```sh
        source venv/bin/activate
        ```

4. **Instale as dependências:**

```sh
pip install -r requirements.txt
```

5. **Inicie a aplicação**

```sh
python main.py
```

A aplicação estará em execução em **'http:/localhost:8000'**.

## Uso

Quando trata-se de machine learning, em diversos cenários podemos utilizar as informações sobre o conteúdo disponibilizado na API. Alguns dos cenários possíveis:

- **Previsão de Demanda**: Utilizando dados históricos de produção e vendas, é possível treinar um modelo de machine learning para prever a demanda futura por diferentes tipos de bebidas. Esse tipo de previsão pode ajudar os produtores a ajustar suas operações de produção e estoque, minimizando desperdícios e maximizando a eficiência. Com os dados de produção, comercialização, importação e exportação o modelo pode identificar quais os produtos mais vendidos e as quantidades, conseguindo assim elaborar um plano de produção mais acertivo com base nos dados históricos.  
  

- **Otimização da Produção**: Com os dados é possível identificar os produtos que mais vendem e focar a produção nesses produtos chave, onde que otimiza a produção e também otimiza a cadeia de suprimentos. 

## Endpoints


### GET /producao

**Descrição**: Este endpoint retorna dados detalhados sobre a produção de vinhos, incluindo volumes de produção para cada tipo de vinho e subcategoria de vinho.

**Parâmetros**: não tem.

**Exemplo de Requisição:**

```sh
curl -X GET ""http://localhost:8000/producao"
```

**Resposta:**

```json
{
  "1": {
    "id": "1",
    "control": "VINHO DE MESA",
    "produto": "VINHO DE MESA",
    "anos": {
      "1970": "217208604",
      "1971": "154264651",
      "1972": "146953297",
      "1973": "116710345",
      "1974": "193875345",
      "1975": "177401209",
      ...
    }
  }
}
```

### GET /producao/[ano]

**Descrição**: Este endpoint retorna o ano de processamento entre os anos de 1970 até 2022 (qualquer valor diferente disso, irá retornar como erro)

O parâmetro [ano] deve ser enviado utilizando os números entre 1970 e 2022 (qualquer valor diferente disso, irá retornar como erro)


**Parâmetros**:

|   Parâmetro   |   Tipo   |   Descricao   |
|---------------|----------|---------------|
| Ano          | String   | Ano de processamento |

**Exemplo de Requisição:**

```sh
curl -X GET ""http://localhost:8000/producao/1970"
```

**Resposta:**

```json
{
  {
    "id": "1",
    "control": "VINHO DE MESA",
    "produto": "VINHO DE MESA",
    "1970": "217208604"
  },
}
```


### GET /processamento

**Descrição**: Este endpoint retorna dados detalhados sobre a quantidade em kg de uvas processadas no Rio Grande do Sul do ano de 1970 a 2022.

**Parâmetros**: não tem.

**Exemplo de Requisição:**

```sh
curl -X GET ""http://localhost:8000/processamento"
```

**Resposta:**

```json
{
  {
    "id_processamento": 1,
    "tipo_processamento": "Viniferas",
    "dados": {
      "data_TINTAS": {
        "id": "1",
        "control": "TINTAS",
        "cultivar": "TINTAS",
        "anos": {
          "1970": "10448228",
          "1971": "11012833",
          "1972": "10798824",
          "1973": "8213674",
          ...
        }
      }
    }
  }
}
```

### GET /processamento/[tipo]

**Descrição**: Este endpoint retorna dados detalhados sobre a quantidade em kg de uvas processadas no Rio Grande do Sul para categoria selecionada.

O parâmetro [tipo] deve ser enviado utilizando os números entre 1 e 4 (qualquer valor diferente disso, irá retornar como erro)

**Referência**:

| Categoria            | ID de Consulta |
|----------------------|----------------|
|Viníferas             | 1              |
|Americanas e híbridas | 2              |
|Uvas de mesa          | 3              |
|Sem Classificação     | 4              |


**Parâmetros**:

|   Parâmetro   |   Tipo   |   Descricao   |
|---------------|----------|---------------|
| Tipo          | String   | Tipo de processamento |


**Exemplo de Requisição:**

```sh
curl -X GET ""http://localhost:8000/processamento/1"
```

**Resposta:**

```json
{
    {
      "id": "1",
      "control": "TINTAS",
      "cultivar": "TINTAS",
      "1970": "10448228",
      "1971": "11012833",
      "1972": "10798824",
      "1973": "8213674",
      "1974": "17457849",
      "1975": "22593885",
          ...
    }
}
```

### GET /processamento/[tipo]/[ano]

**Descrição**: Este endpoint retorna dados detalhados sobre a quantidade em kg de uvas processadas no Rio Grande do Sul da categoria e do ano selecionado.

O parâmetro [tipo] deve ser enviado utilizando os números entre 1 e 4 (qualquer valor diferente disso, irá retornar como erro)

**Referência**:

| Categoria            | ID de Consulta |
|----------------------|----------------|
|Viníferas             | 1              |
|Americanas e híbridas | 2              |
|Uvas de mesa          | 3              |
|Sem Classificação     | 4              |
|Suco                  | 5              |



**Parâmetros**:

|   Parâmetro   |   Tipo   |   Descricao   |
|---------------|----------|---------------|
| Id          | String   | Id do processamento |
| Ano          | String   | Ano de processamento |


**Exemplo de Requisição:**

```sh
curl -X GET ""http://localhost:8000/processamento/1/1970"
```

**Resposta:**

```json
{
   {
    "id": "1",
    "control": "TINTAS",
    "cultivar": "TINTAS",
    "1970": "10448228"
  },
}
```

### GET /processamento_ano/[ano]

**Descrição**: Esse endpoint retorna o processamento do ano informado

O parâmetro [ano] deve ser enviado entre 1970 e 2022 (qualquer valor diferente disso, irá retornar como erro)

**Referência**: anos de 1970 a 2022.


**Parâmetros**:

|   Parâmetro   |   Tipo   |   Descricao   |
|---------------|----------|---------------|
| Ano          | String   | Ano de referencia |


**Exemplo de Requisição:**

```sh
curl -X GET ""http://localhost:8000/processamento_ano/1970"
```

**Resposta:**

```json
{
  "id_processamento": 1,
  "tipo_processamento": "Viniferas",
  "dados": {
    "data_TINTAS": {
      "id": "1",
      "control": "TINTAS",
      "cultivar": "TINTAS",
      "anos": {
        "1970": "10448228"
      }
    }
  }
}
```

### GET /comercializacao

**Descrição**: Este endpoint retorna dados detalhados sobre a comercialização em quantidade de litros de vinhos e derivados no Rio Grande do Sul do ano de 1970 a 2023.

**Parâmetros**: não tem.

**Exemplo de Requisição:**

```sh
curl -X GET ""http://localhost:8000/comercializacao"
```

**Resposta:**

```json
{
  {
    "id": "1",
    "produto": "VINHO DE MESA",
    "produto_2": "VINHO DE MESA",
    "anos": {
      "1970": "98327606",
      "1971": "114399031",
      "1972": "118377367",
      "1973": "116617910",
      "1974": "94173324",
      ...
    }
  }
}
```

### GET /comercializacao/[ano]

**Descrição**: Este endpoint retorna dados detalhados sobre a comercialização em quantidade de litros de vinhos e derivados no Rio Grande do Sul do ano selecionado.

**Parâmetros**:

|   Parâmetro   |   Tipo   |   Descricao   |
|---------------|----------|---------------|
| Ano          | String   | Ano de referencia |

**Exemplo de Requisição:**

```sh
curl -X GET ""http://localhost:8000/comercializacao/1970"
```

**Resposta:**

```json
{
  {
    "id": "1",
    "produto": "VINHO DE MESA",
    "produto_2": "VINHO DE MESA",
    "1970": "98327606"
  },
  ...
}
```

### GET /importacao

**Descrição**: Este endpoint retorna dados detalhados sobre a quantidade em g e valor dólares (US$) de importação de derivados de uva e os respectivos paises, com dados desde 1970 até 2023.

**Parâmetros**: não tem.

**Exemplo de Requisição:**

```sh
curl -X GET ""http://localhost:8000/importacao"
```

**Resposta:**

```json
{
  {
    "id": 1,
    "tipo_importacao": "Vinhos",
    "Africa do Sul": {
      "id": "1",
      "1970": {
        "quantidade": "0",
        "valor": "0"
      },
      "1971": {
        "quantidade": "0",
        "valor": "0"
      }
      ...
    }
  }
}
```

### GET /importacao/[tipo]

**Descrição**: Este endpoint retorna dados detalhados sobre a quantidade em g e valor dólares (US$) de importação de derivados de uva e os respectivos paises, com dados desde 1970 até 2023 da categoria selecionada.

O parâmetro [tipo] deve ser enviado utilizando os números entre 1 e 5 (qualquer valor diferente disso, irá retornar como erro)

**Referência**:


| Categoria | ID de Consulta |
|-----------|----------------|
|Vinhos     | 1              |
|Espumantes | 2              |
|Frescas    | 3              |
|Passas     | 4              |
|Suco       | 5              |


**Parâmetros**:

|   Parâmetro   |   Tipo   |   Descricao   |
|---------------|----------|---------------|
| ID           | String   | Id do processamento |

**Exemplo de Requisição:**

```sh
curl -X GET ""http://localhost:8000/importacao/3"
```

**Resposta:**

```json
{
 {
    "id": 3,
    "tipo_importacao": "Frescas",
    "Argélia": {
      "id": "1",
      "1970": {
        "quantidade": "0",
        "valor": "0"
      },
      "1971": {
        "quantidade": "0",
        "valor": "0"
      },
      ...
    }
 }
}
```

### GET /importacao/[tipo]/[ano]

**Descrição**: Este endpoint retorna dados detalhados sobre a quantidade em g e valor dólares (US$) de importação de derivados de uva e os respectivos paises, com dados desde 1970 até 2023 da categoria e do ano selecionado.

O parâmetro [tipo] deve ser enviado utilizando os números entre 1 e 5 (qualquer valor diferente disso, irá retornar como erro) e o parâmetro [ano] deve ser um ano valido entre 1970 e 2023.


**Referência**:


| Categoria | ID de Consulta |
|-----------|----------------|
|Vinhos     | 1              |
|Espumantes | 2              |
|Frescas    | 3              |
|Passas     | 4              |
|Suco       | 5              |


**Parâmetros**:

|   Parâmetro   |   Tipo   |   Descricao   |
|---------------|----------|---------------|
| ID           | String   | Id do processamento |
| Ano          | String   | Ano de processamento |

**Exemplo de Requisição:**

```sh
curl -X GET ""http://localhost:8000/importacao/3"
```

**Resposta:**

```json
{
 {
    "id": 3,
    "tipo_importacao": "Frescas",
    "Argélia": {
      "id": "1",
      "1970": {
        "quantidade": "0",
        "valor": "0"
      },
      "1971": {
        "quantidade": "0",
        "valor": "0"
      },
      ...
    }
 }
}
```

### GET /importacao_ano/[ano]

**Descrição**: Este endpoint retorna dados detalhados sobre a quantidade em g e valor dólares (US$) de importação de derivados de uva e os respectivos paises, com dados filtrados a partir do ano selecionado.

O parâmetro [ano] deve ser um ano válido entre 1970 e 2023.


**Referência**:


| Categoria | ID        |
|-----------|-----------|
|Vinhos     | 1         |
|Espumantes | 2         |
|Frescas    | 3         |
|Passas     | 4         |
|Suco       | 5         |


**Parâmetros**:

|   Parâmetro   |   Tipo   |   Descricao   |
|---------------|----------|---------------|
| Ano          | String   | Ano de processamento |

**Exemplo de Requisição:**

```sh
curl -X GET ""http://localhost:8000/importacao_ano/1980"
```

**Resposta:**

```json
{
  "id": 1,
  "tipo_importacao": "Vinhos",
    "Africa do Sul": {
      "1980": {
        "quantidade": "0",
        "valor": "0"
      }
    },
    "Alemanha": {
      "1980": {
        "quantidade": "457033",
        "valor": "704307"
      }
    },
    ...
}
```

### GET /exportacao

**Descrição**: Este endpoint retorna dados detalhados sobre a quantidade em Kg e valor dólares (US$) de exportação de derivados de uva e os respectivos paises, com dados desde 1970 até 2023.

**Parâmetros**: não tem.

**Exemplo de Requisição:**

```sh
curl -X GET ""http://localhost:8000/exportacao"
```

**Resposta:**

```json
{
  {
    "id": 1,
    "tipo_exportacao": "Vinho",
    "Afeganistão": {
      "id": "1",
      "1970": {
        "quantidade": "0",
        "valor": "0"
      },
      ...
    }
  }
}
```

### GET /exportacao/[tipo]

**Descrição**: Este endpoint retorna dados detalhados sobre a quantidade em Kg e valor dólares (US$) de exportação de derivados de uva e os respectivos paises, com dados desde 1970 até 2023 da categoria selecionada.

**Referência**:

| Categoria | ID de Consulta |
|-----------|----------------|
|Vinhos     | 1              |
|Espumantes | 2              |
|Uvas       | 3              |
|Suco       | 4              |


**Parâmetros**:

|   Parâmetro   |   Tipo   |   Descricao   |
|---------------|----------|---------------|
| ID           | String   | Id do processamento |
| Ano          | String   | Ano de processamento |

**Exemplo de Requisição:**

```sh
curl -X GET ""http://localhost:8000/exportacao/2"
```

**Resposta:**

```json
{
  
  {
    "id": 2,
    "tipo_exportacao": "Espumantes",
    "África do Sul": {
      "id": "1",
      "1970": {
        "quantidade": "0",
        "valor": "0"
      },
    }
  }
}
```

### GET /exportacao/[tipo]/[ano]

**Descrição**: Este endpoint retorna dados detalhados sobre a quantidade em Kg e valor dólares (US$) de exportação de derivados de uva e os respectivos paises, com dados desde 1970 até 2023 da categoria e do ano selecionado.

**Referência**:

| Categoria | ID de Consulta |
|-----------|----------------|
|Vinhos     | 1              |
|Espumantes | 2              |
|Uvas       | 3              |
|Suco       | 4              |


**Parâmetros**:

|   Parâmetro   |   Tipo   |   Descricao   |
|---------------|----------|---------------|
| ID           | String   | Id do processamento |

**Exemplo de Requisição:**

```sh
curl -X GET ""http://localhost:8000/exportacao/2/1970"
```

**Resposta:**

```json
{
  
  {
    "id": 2
  },
  {
    "tipo_exportacao": "Espumantes"
  },
  {
    "África do Sul": {
      "quantidade": "0",
      "valor": "0"
    }
    ...
  },
}
```

### GET /exportacao_ano/[ano]

**Descrição**: Este endpoint retorna dados detalhados sobre a quantidade em Kg e valor dólares (US$) de exportação de derivados de uva e os respectivos paises, com dados filtrados a partir do ano selecionado.

O parâmetro [ano] deve ser um ano válido entre 1970 e 2023.

**Referência**:

| Categoria | ID de Consulta |
|-----------|----------------|
|Vinhos     | 1              |
|Espumantes | 2              |
|Uvas       | 3              |
|Suco       | 4              |


**Parâmetros**:

| Parâmetro |   Tipo   | Descricao            |
|-----------|----------|----------------------|
| Ano       | String   | Ano do processamento |

**Exemplo de Requisição:**

```sh
curl -X GET ""http://localhost:8000/exportacao_ano/1970"
```

**Resposta:**

```json
{
    {
      "id": 1,
      "tipo_exportacao": "Vinho",
      "Afeganistão": {
        "1970": {
          "quantidade": "0",
          "valor": "0"
        }
      },
      "África do Sul": {
        "1970": {
          "quantidade": "0",
          "valor": "0"
        }
      },
      "Alemanha, República Democrática": {
        "1970": {
          "quantidade": "0",
          "valor": "0"
        }
    },
    ...
  }
}
```

## Arquitetura de Deploy

![Arquitetura de Deploy](arquitetura.jpg)

## Erros

Tratamentos utilizados para possíveis erros retornados pela API e seus significados.

## Contribuição

Este trabalho foi elaborado em equipe e os alunos responsáveis por ele são:

- Ângelo Cabral - linkedin: https://www.linkedin.com/in/angelocassio/
- Felipe Chagas - linkedin:  
- Gabriela Nogueira - linkedin: https://www.linkedin.com/in/gabriela-nogueira/
- Vinicius Amorim - linkedin: https://www.linkedin.com/in/viniciusdeamorim/