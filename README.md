<<<<<<< HEAD
# TechChallenge 01 - API Embrapa

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)

Esta API foi desenvolvida como parte do trabalho tech challenge da pós-graduação em Engenharia de Machine Learning. Ela foi projetada para ler os dados a partir de um CSV do site da Embrapa e disponibiliza-los de acordo com tema pelas rotas definidas.

## Objetivo do Projeto

O principal objetivo desta API é facilitar a coleta, armazenamento e manipulação de dados que são disponibilizados em um site que contém as informações sobre produção de vinhos, sucos e derivados provenientes do Rio Grande do Sul. Para isso, foi criado as rotas necessárias sobre cada aba do site que englobam: Produção, Processamento, Comercialização, Importação e Exportação.
=======
# TechChallenge 03 - API Yfinance
>>>>>>> f5116793ee86836091332955acb1f64a1baf1596

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white) ![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)  ![AWS](https://img.shields.io/badge/AWS-000.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)

<<<<<<< HEAD
- Criar a rota de produção 🆗
- Criar a rota de processamento 🆗
- Ajustar o encoding da rota de produção 🆗
- Criar a rota de comercialização  🆗
- Criar a rota de importação  🆗
- Criar a rota de exportação  🆗
- Ajustar os filtros de data para deixarmos dinamico e não setado no codigo os anos disponiveis
- Ajustar a estrutura do importação para renomear as colunas inicias e criar um dicionario de cada ano que contenha a quantidade e valor  🆗
- Adicionar o filtro de ano no importação, exportação e processamento 🆗
- Adicionar autenticação (não obrigatório)
- Padronizar estrutura de retorno de todos os métodos
=======
Implementação de uma API em Django que realiza a extração/ingestão de dados financeiros da B3 (Brasil Bolsa Balcão) de ações via integração com o serviço yfinance. Os dados extraídos são armazenados em um bucket no AWS S3 para criar uma base de dados para as análises exploratórias e servem de base para o treinamento de modelos de machine learning. A API foi projetada para suportar o treinamento de algoritmos como Random Forest, K-Nearest Neighbors (KNN) e Gradient Boosting (GBoost), visando prever a tendência de ações (alta, baixa ou neutra). A tendência é prevista se baseando na média móvel de 10 e 50 dias dos valores de abertura e fechamento das ações. O pipeline inclui pré-processamento de dados, cálculo de indicadores financeiros, como médias móveis e RSI, e a divisão dos dados em treino e teste. A branch foca na implementação do backend da API e na preparação dos dados para o estudo e avaliação de modelos preditivos
>>>>>>> f5116793ee86836091332955acb1f64a1baf1596
