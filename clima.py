# Importa o módulo requests para realizar requisições HTTP
import requests

# Importa o módulo json para manipular dados JSON
import json

# Importa o módulo pprint para exibir dados formatados (útil para depuração)
import pprint

# Chave da API do AccuWeather (deve ser substituída por uma válida)
accuweatherAPIKey = '	PFj5L4FjtD8lpCKiG8ZkqblYEnHZJJG6'

# Faz uma requisição HTTP para obter a localização atual via GeoPlugin
r = requests.get('http://www.geoplugin.net/json.gp')

# Verifica se a requisição foi bem-sucedida (código de status 200)
if (r.status_code != 200):
    # Exibe mensagem de erro se não for possível obter a localização
    print('Não foi possível obter a localização.')
else:
    # Converte a resposta da requisição para um dicionário Python
    localizacao = json.loads(r.text)
    
    # Obtém a latitude da localização
    lat = localizacao['geoplugin_latitude']
    
    # Obtém a longitude da localização
    long = localizacao['geoplugin_longitude']
    
    # Define a URL para buscar informações da localização usando a API do AccuWeather
    LocationAPIUrl = (
        "http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey="
        + accuweatherAPIKey
        + "&q="
        + lat
        + "%2C"
        + long
        + "&language=pt-br"
    )
    
    # Faz uma requisição HTTP para obter informações da localização no AccuWeather
    r2 = requests.get(LocationAPIUrl)
    
    # Verifica se a requisição foi bem-sucedida
    if (r2.status_code != 200):
        # Exibe mensagem de erro se não for possível obter as informações da localização
        print('Não foi possível obter a localização.')
    else:
        # Converte a resposta da requisição para um dicionário Python
        locationResponse = json.loads(r2.text)
        
        # Obtém o nome do local formatado (cidade, estado e país)
        nomeLocal = (
            locationResponse['LocalizedName'] + ","
            + locationResponse['AdministrativeArea']['LocalizedName'] + "."
            + locationResponse['Country']['LocalizedName']
        )
        
        # Obtém o código do local para buscar condições climáticas
        codigoLocal = locationResponse['Key']
        
        # Exibe o nome do local
        print("Obtendo clima do local: ", nomeLocal)
        
        # Define a URL para buscar as condições climáticas atuais
        CurrentConditionsAPIUrl = (
            "http://dataservice.accuweather.com/currentconditions/v1/"
            + codigoLocal
            + "?apikey="
            + accuweatherAPIKey
            + "&language=pt-br"
        )
        
        # Faz uma requisição HTTP para obter as condições climáticas
        r3 = requests.get(CurrentConditionsAPIUrl)
        
        # Verifica se a requisição foi bem-sucedida
        if (r3.status_code != 200):
            # Exibe mensagem de erro se não for possível obter as condições climáticas
            print('Não foi possível obter a localização.')
        else:
            # Converte a resposta da requisição para um dicionário Python
            CurrentConditionsResponse = json.loads(r3.text)
            
            # Obtém a descrição do clima atual
            textoClima = CurrentConditionsResponse[0]['WeatherText']
            
            # Obtém a temperatura atual em graus Celsius
            temperatura = CurrentConditionsResponse[0]['Temperature']['Metric']['Value']
            
            # Exibe a descrição do clima atual
            print('Clima no momento: ', textoClima)
            
            # Exibe a temperatura atual
            print('Temperatura no momento: '+ str(temperatura) + ' graus Celsius')
