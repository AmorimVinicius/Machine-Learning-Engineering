import os
import requests
import yfinance as yf
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import boto3
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

pd.set_option('future.no_silent_downcasting', True)

# Configurações de credenciais e bucket S3
aws_access_key_id = 'xpto'
aws_secret_access_key = 'xpto'
aws_session_token = 'xpto'
bucket_name_s3 = 'techchanllange-fiap2024'

# Criar sessão do boto3
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)

# Cliente S3
s3 = session.client('s3')

# Global
tickers = []
data_tickers = []

def get_ticker():
    url = 'https://www.dadosdemercado.com.br/acoes'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')

    if table:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) > 0:
                link = cols[0].find('a')
                if link:
                    ticker = link.text.strip()
                    tickers.append(ticker)

def fetch_stock_data(ticker):
    empty_ticker = {'Ticker': ticker}
    try:
        stock = yf.Ticker(ticker + ".SA")
        info = stock.info

        loop = 5
        j = 0

        for i in range(loop):
            j+=1
            # Verificar se o ticker é válido
            if info.get('quoteType') != 'NONE':
                # Buscar dados do último ano
                start_date = (datetime.now() - timedelta(days=loop-i)).strftime('%Y-%m-%d')
                end_data = (datetime.now() - timedelta(days=loop-j)).strftime('%Y-%m-%d')
                historical_data = stock.history(start=start_date, end=end_data)

                if not historical_data.empty:
                    opening = round(historical_data['Open'].iloc[0], 2)
                    lowest_value = round(historical_data['Low'].min(), 2)
                    greater_value = round(historical_data['High'].max(), 2)
                    closing = round(historical_data['Close'].iloc[-1], 2)
                    volume = round(historical_data['Volume'].mean(), 2)
                    dividends = round(historical_data['Dividends'].mean(), 2)
                    stock_splits = round(historical_data['Stock Splits'].mean(), 2)
                    city = info.get('city')
                    state = info.get('state')
                    industry = info.get('industry')
                    industryKey = info.get('industryKey')
                    industryDisp = info.get('industryDisp')
                    sector = info.get('sector')
                    sectorKey = info.get('sectorKey')
                    sectorDisp = info.get('sectorDisp')
                    fullTimeEmployees = info.get('fullTimeEmployees')
                    auditRisk = info.get('auditRisk')
                    boardRisk = info.get('boardRisk')
                    compensationRisk = info.get('compensationRisk')
                    shareHolderRightsRisk = info.get('shareHolderRightsRisk')
                    overallRisk = info.get('overallRisk')
                    governanceEpochDate = info.get('governanceEpochDate')
                    maxAge = info.get('maxAge')
                    priceHint = info.get('priceHint')
                    previousClose = info.get('previousClose')
                    regularMarketPreviousClose = info.get('regularMarketPreviousClose')
                    dividendRate = info.get('dividendRate')
                    dividendYield = info.get('dividendYield')
                    exDividendDate = info.get('exDividendDate')
                    payoutRatio = info.get('payoutRatio')
                    fiveYearAvgDividendYield = info.get('fiveYearAvgDividendYield')
                    beta = info.get('beta')
                    trailingPE = info.get('trailingPE')
                    forwardPE = info.get('forwardPE')
                    averageVolume = info.get('averageVolume')
                    averageVolume10days = info.get('averageVolume10days')
                    averageDailyVolume10Day = info.get('averageDailyVolume10Day')
                    bid = info.get('bid')
                    ask = info.get('ask')
                    marketCap = info.get('marketCap')
                    fiftyTwoWeekHigh = info.get('fiftyTwoWeekHigh')
                    priceToSalesTrailing12Months = info.get('priceToSalesTrailing12Months')
                    fiftyDayAverage = info.get('fiftyDayAverage')
                    twoHundredDayAverage = info.get('twoHundredDayAverage')
                    trailingAnnualDividendRate = info.get('trailingAnnualDividendRate')
                    trailingAnnualDividendYield = info.get('trailingAnnualDividendYield')
                    currency = info.get('currency')
                    enterpriseValue = info.get('enterpriseValue')
                    profitMargins = info.get('profitMargins')
                    floatShares = info.get('floatShares')
                    sharesOutstanding = info.get('sharesOutstanding')
                    heldPercentInsiders = info.get('heldPercentInsiders')
                    heldPercentInstitutions = info.get('heldPercentInstitutions')
                    impliedSharesOutstanding = info.get('impliedSharesOutstanding')
                    bookValue = info.get('bookValue')
                    priceToBook = info.get('priceToBook')
                    lastFiscalYearEnd = info.get('lastFiscalYearEnd')
                    nextFiscalYearEnd = info.get('nextFiscalYearEnd')
                    mostRecentQuarter = info.get('mostRecentQuarter')
                    earningsQuarterlyGrowth = info.get('earningsQuarterlyGrowth')
                    netIncomeToCommon = info.get('netIncomeToCommon')
                    trailingEps = info.get('trailingEps')
                    forwardEps = info.get('forwardEps')
                    pegRatio = info.get('pegRatio')
                    lastSplitFactor = info.get('lastSplitFactor')
                    lastSplitDate = info.get('lastSplitDate')
                    enterpriseToRevenue = info.get('enterpriseToRevenue')
                    enterpriseToEbitda = info.get('enterpriseToEbitda')
                    weekChange = info.get('52WeekChange')
                    sandP52WeekChange = info.get('SandP52WeekChange')
                    lastDividendValue = info.get('lastDividendValue')
                    lastDividendDate = info.get('lastDividendDate')
                    exchange = info.get('exchange')
                    quoteType = info.get('quoteType')
                    symbol = info.get('symbol')
                    underlyingSymbol = info.get('underlyingSymbol')
                    shortName = info.get('shortName')
                    longName = info.get('longName')
                    firstTradeDateEpochUtc = info.get('firstTradeDateEpochUtc')
                    timeZoneFullName = info.get('timeZoneFullName')
                    timeZoneShortName = info.get('timeZoneShortName')
                    uuid = info.get('uuid')
                    messageBoardId = info.get('messageBoardId')
                    gmtOffSetMilliseconds = info.get('gmtOffSetMilliseconds')
                    currentPrice = info.get('currentPrice')
                    targetHighPrice = info.get('targetHighPrice')
                    targetLowPrice = info.get('targetLowPrice')
                    targetMeanPrice = info.get('targetMeanPrice')
                    targetMedianPrice = info.get('targetMedianPrice')
                    recommendationMean = info.get('recommendationMean')
                    recommendationKey = info.get('recommendationKey')
                    numberOfAnalystOpinions = info.get('numberOfAnalystOpinions')
                    totalCash = info.get('totalCash')
                    totalCashPerShare = info.get('totalCashPerShare')
                    ebitda = info.get('ebitda')
                    totalDebt = info.get('totalDebt')
                    quickRatio = info.get('quickRatio')
                    currentRatio = info.get('currentRatio')
                    totalRevenue = info.get('totalRevenue')
                    debtToEquity = info.get('debtToEquity')
                    revenuePerShare = info.get('revenuePerShare')
                    returnOnAssets = info.get('returnOnAssets')
                    returnOnEquity = info.get('returnOnEquity')
                    freeCashflow = info.get('freeCashflow')
                    operatingCashflow = info.get('operatingCashflow')
                    earningsGrowth = info.get('earningsGrowth')
                    revenueGrowth = info.get('revenueGrowth')
                    grossMargins = info.get('grossMargins')
                    ebitdaMargins = info.get('ebitdaMargins')
                    operatingMargins = info.get('operatingMargins')
                    financialCurrency = info.get('financialCurrency')
                    trailingPegRatio = info.get('trailingPegRatio')

                    data_tickers.append({
                        'Ticker': ticker,
                        'Data': start_date,
                        'Abertura': opening,
                        'MenorValor': lowest_value,
                        'MaiorValor': greater_value,
                        'Fechamento': closing,
                        'Volume': volume,
                        'Dividendos': dividends,
                        'Desdobramento': stock_splits,
                        'Cidade': city,
                        'Estado': state,
                        'Industria': industry,
                        'ChaveIndustria': industryKey,
                        'DescricaoIndustria': industryDisp,
                        'Setor': sector,
                        'ChaveSetor': sectorKey,
                        'DescricaoSetor': sectorDisp,
                        'EmpregadosEmTempoIntegral': fullTimeEmployees,
                        'RiscoDeAuditoria': auditRisk,
                        'RiscoDoConselho': boardRisk,
                        'RiscoDeCompensacao': compensationRisk,
                        'RiscoDeDireitosDeAcionistas': shareHolderRightsRisk,
                        'RiscoGeral': overallRisk,
                        'DataDaEraDeGovernanca': governanceEpochDate,
                        'IdadeMaxima': maxAge,
                        'DicaDePreco': priceHint,
                        'FechamentoAnterior': previousClose,
                        'FechamentoAnteriorDoMercadoRegular': regularMarketPreviousClose,
                        'TaxaDeDividendo': dividendRate,
                        'RendimentoDeDividendo': dividendYield,
                        'DataExDividendo': exDividendDate,
                        'RelacaoDePagamento': payoutRatio,
                        'RendimentoMedioDeDividendoDeCincoAnos': fiveYearAvgDividendYield,
                        'Beta': beta,
                        'PeRetrospectivo': trailingPE,
                        'PeFuturo': forwardPE,
                        'VolumeMedio': averageVolume,
                        'VolumeMedioDe10Dias': averageVolume10days,
                        'VolumeDiarioMedioDe10Dias': averageDailyVolume10Day,
                        'Oferta': bid,
                        'Pedido': ask,
                        'CapitalizacaoDeMercado': marketCap,
                        'AltaDe52Semanas': fiftyTwoWeekHigh,
                        'PrecoParaVendas12Meses': priceToSalesTrailing12Months,
                        'MediaDe50Dias': fiftyDayAverage,
                        'MediaDe200Dias': twoHundredDayAverage,
                        'TaxaAnualDeDividendoRetrospectivo': trailingAnnualDividendRate,
                        'RendimentoAnualDeDividendoRetrospectivo': trailingAnnualDividendYield,
                        'Moeda': currency,
                        'ValorDaEmpresa': enterpriseValue,
                        'MargensDeLucro': profitMargins,
                        'AcoesEmCirculacao': floatShares,
                        'AcoesEmitidas': sharesOutstanding,
                        'PercentualDetidoPorInsiders': heldPercentInsiders,
                        'PercentualDetidoPorInstituicoes': heldPercentInstitutions,
                        'AcoesEmitidasImplicitas': impliedSharesOutstanding,
                        'ValorContabil': bookValue,
                        'PrecoParaValorContabil': priceToBook,
                        'FimDoUltimoAnoFiscal': lastFiscalYearEnd,
                        'FimDoProximoAnoFiscal': nextFiscalYearEnd,
                        'UltimoTrimestre': mostRecentQuarter,
                        'CrescimentoTrimestralDosLucros': earningsQuarterlyGrowth,
                        'LucroLiquidoParaAcionistas': netIncomeToCommon,
                        'EpsRetrospectivo': trailingEps,
                        'EpsFuturo': forwardEps,
                        'RelacaoPeg': pegRatio,
                        'UltimoFatorDeDesdobramento': lastSplitFactor,
                        'DataDoUltimoDesdobramento': lastSplitDate,
                        'ValorDaEmpresaParaReceitas': enterpriseToRevenue,
                        'ValorDaEmpresaParaEbitda': enterpriseToEbitda,
                        'MudancaDe52Semanas': weekChange,
                        'MudancaDe52SemanasSandP': sandP52WeekChange,
                        'ValorDoUltimoDividendo': lastDividendValue,
                        'DataDoUltimoDividendo': lastDividendDate,
                        'Troca': exchange,
                        'TipoDeCotacao': quoteType,
                        'Simbolo': symbol,
                        'SimboloSubjacente': underlyingSymbol,
                        'NomeCurto': shortName,
                        'NomeCompleto': longName,
                        'DataDaPrimeiraNegociacaoEpochUtc': firstTradeDateEpochUtc,
                        'NomeCompletoDoFusoHorario': timeZoneFullName,
                        'NomeCurtoDoFusoHorario': timeZoneShortName,
                        'Uuid': uuid,
                        'IdDoQuadroDeMensagens': messageBoardId,
                        'OffsetGmtEmMilissegundos': gmtOffSetMilliseconds,
                        'PrecoAtual': currentPrice,
                        'PrecoAlvoMaximo': targetHighPrice,
                        'PrecoAlvoMinimo': targetLowPrice,
                        'PrecoAlvoMedio': targetMeanPrice,
                        'PrecoAlvoMedio': targetMedianPrice,
                        'MediaDasRecomendacoes': recommendationMean,
                        'ChaveDasRecomendacoes': recommendationKey,
                        'NumeroDeOpiniaoDosAnalistas': numberOfAnalystOpinions,
                        'CaixaTotal': totalCash,
                        'CaixaTotalPorAcao': totalCashPerShare,
                        'Ebitda': ebitda,
                        'DividaTotal': totalDebt,
                        'IndiceDeLiquidezImediata': quickRatio,
                        'IndiceDeLiquidezCorrente': currentRatio,
                        'ReceitaTotal': totalRevenue,
                        'DividaParaPatrimonio': debtToEquity,
                        'ReceitaPorAcao': revenuePerShare,
                        'RetornoSobreAtivos': returnOnAssets,
                        'RetornoSobrePatrimonio': returnOnEquity,
                        'FluxoDeCaixaLivre': freeCashflow,
                        'FluxoDeCaixaOperacional': operatingCashflow,
                        'CrescimentoDosLucros': earningsGrowth,
                        'CrescimentoDaReceita': revenueGrowth,
                        'MargensBrutas': grossMargins,
                        'MargensEbitda': ebitdaMargins,
                        'MargensOperacionais': operatingMargins,
                        'MoedaFinanceira': financialCurrency,
                        'RelacaoPegRetrospectiva': trailingPegRatio 
                    })
                else:
                    data_tickers.append(empty_ticker)
            else:
                data_tickers.append(empty_ticker)
    except (ValueError, KeyError, TypeError, Exception) as e:
        data_tickers.append(empty_ticker)

def get_data_tickers():
    global data_tickers

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_ticker = {executor.submit(fetch_stock_data, ticker): ticker for ticker in tickers }
        for future in as_completed(future_to_ticker):
            future.result()

    # Criar DataFrame com todos os dados coletados
    clean_data_tickers = [item for item in data_tickers if item is not None and isinstance(item, dict)]
    df = pd.DataFrame(clean_data_tickers)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    parquet_filename = f'acoes_historico_{timestamp}.parquet'
    csv_filename = f'acoes_historico_{timestamp}.csv'

    # Salvar arquivos
    df.replace(['Infinity', '-Infinity'], np.nan, inplace=True)
    df.to_csv(csv_filename, index=False, encoding='utf-8')
    df.to_parquet(parquet_filename, index=False)

    # Enviar arquivos para o S3
    upload_to_s3(csv_filename, 'csv')
    upload_to_s3(parquet_filename, 'parquet')

def upload_to_s3(file_name, folder_name):
    try:
        s3_key = f'{folder_name}/{file_name}'
        s3.upload_file(file_name, bucket_name_s3, s3_key)
        print(f'Arquivo {file_name} enviado para o bucket S3 {bucket_name_s3}')
    except Exception as e:
        print(f"Erro ao enviar o arquivo {file_name} para o S3: {e}")

# Executar as funções
get_ticker()
get_data_tickers()
