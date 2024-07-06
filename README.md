# Machine-Learning-Engineering
Conteúdo desenvolvido durante os estudos da Pós Tech - Machine Learning Engineering

### Pipeline Batch Bovespa:

- Requisito 1: Scrap de dados do site da B3 com dados do pregão D-1;
- Requisito 2: Os dados brutos devem ser ingeridos no s3 em formato parquet com partição diária;
- Requisito 3: O bucket deve acionar uma lambda que por sua vez irá chamar o job de ETL no glue;
- Requisito 4: A lambda pode ser em qualquer linguagem. Ela apenas deverá iniciar o job Glue;
- Requisito 5: O Job Glue deve ser feito no modo visual. Este job deve conter as seguintes transformações obrigatórias:
	- Requisito 5.1: Agrupamento numérico, sumarização, contagem ou soma. 
	- Requisito 5.2: Renomear duas colunas existentes além das de agrupamento. 
	- Requisito 5.3: Realizar um cálculo com campos de data, Exemplo, poder ser duração, comparação, diferença entre datas. 
- Requisito 6: Os dados refinados no job glue devem ser salvos no formato parquet, numa pasta chamada refined, particionado por data e pelo nome ou abreviação da ação do pregão. 
- Requisito 7: O job Glue deve automaticamente catalogar o dado no Glue Catalog e criar uma tabela no banco de dados default do Glue Catalog. 
- Requisito 8: Os dados devem estar disponíveis, legíveis no Athena. 
- Requisito 9: Opcional construir um notebook no Athena para montar uma visualização gráfica dos dados ingeridos.
