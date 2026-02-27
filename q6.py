import pandas as pd
import openmeteo_requests
import requests_cache
from retry_requests import retry

# Gera um DataFrame que apresenta as previsões horárias de pressão atmosférica para 7 dias
def gera_df_pressao_atm_semanal(latitude: float, longitude: float) -> pd.DataFrame:

    # Configura cache e repetição de tentativas para o cliente openmeteo
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)

    # Cria cliente openmeteo
    openmeteo = openmeteo_requests.Client(session=retry_session)
    
    # Define parâmetro da requisição
    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'pressure_msl',
        'timezone': 'America/Sao_Paulo',
        'forecast_days': 7
    }

    # Executa requisição e armazena respostas
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    # Extrai das respostas as previsões horarias de pressão semanal
    previsoes_horarias = response.Hourly()
    pressao_horaria = previsoes_horarias.Variables(0).ValuesAsNumpy()

    # Cria o DataFrame contendo as previsões da pressão atmosférica
    df_pressao_atm_semanal = pd.DataFrame({'id': range(1, len(pressao_horaria) + 1)})
    
    # Cria coluna de faixas horária nesse DataFrame
    df_pressao_atm_semanal['momento'] = pd.date_range(
        start = pd.to_datetime(previsoes_horarias.Time() + response.UtcOffsetSeconds(), unit = "s", utc = True),
        end =  pd.to_datetime(previsoes_horarias.TimeEnd() + response.UtcOffsetSeconds(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = previsoes_horarias.Interval()),
        inclusive = "left"
    )

    # Cria coluna com os valores da pressão atmosférica
    df_pressao_atm_semanal['valor'] = pressao_horaria

    return df_pressao_atm_semanal