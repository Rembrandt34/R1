pip install request
pip intall Flask

import json
import requests
import urllib.parse

API_key = '4qkveOLEkmb73yTE4SCUsR77AoVXdRct'

day_5_info = ''
hours_12_info = ''

def get_APIinfo(API_key,longitude,latitude): # Функция для получения json-ов 5-ти дней и 12-ти часов по координатам
    global day_5_info, hours_12_info # глобальные переменные для сохранения данных
    try:
        # получаем код города для получения данных о погоде
        url = f"http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={API_key}&q={longitude}%2C%20{latitude}"
        response_base_link = requests.get(url)
        text_base = dict(json.loads(response_base_link.text))

        # Получаем все данные о погоде за 5 дней
        url = f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{text_base['Key']}?apikey={API_key}&details=true"
        response_data_link = requests.get(url)
        text_data = dict(json.loads(response_data_link.text))

        # Получаем все данные о погоде за 12 часов
        url = f"http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/{text_base['Key']}?apikey={API_key}&details=true"
        response_data_link = requests.get(url)
        text_data12 = list(json.loads(response_data_link.text))

        day_5_info, hours_12_info = text_data, text_data12
    except Exception as ex:
        print(ex)
        print('Истек срок действия API ключа, нужен новый')

def search_for_name(API_key, city_name): # Функция для получения json-ов 5-ти дней и 12-ти часов по названию города
    global day_5_info, hours_12_info # глобальные переменные для сохранения данных
    try:
        # получаем код города для получения данных о погоде
        url = f"http://dataservice.accuweather.com/locations/v1/cities/search?apikey={API_key}&q={urllib.parse.quote(str(city_name))}&details=False&offset=1"
        response_base_link = requests.get(url)
        text_base = list(json.loads(response_base_link.text))[0]

        # Получаем все данные о погоде за 5 дней
        url = f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{text_base['Key']}?apikey={API_key}&details=true"
        response_data_link = requests.get(url)
        text_data = dict(json.loads(response_data_link.text))

        # Получаем все данные о погоде за 12 часов
        url = f"http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/{text_base['Key']}?apikey={API_key}&details=true"
        response_data_link = requests.get(url)
        text_data12 = list(json.loads(response_data_link.text))
        day_5_info, hours_12_info = text_data, text_data12

    except Exception as ex:
        print(ex)
        print('Истек срок действия API ключа, нужен новый')

def parsing_weather_data(cur_day,day): # Эта функция парсит json за выбранный день

    main_parse = day_5_info['DailyForecasts'][cur_day-1]

    Day_real_temper = round((main_parse['RealFeelTemperature']['Maximum']['Value']-32)/1.8)
    Day_Rain_Probability = main_parse['Day']['RainProbability']
    Day_Snow_Probability = main_parse['Day']['SnowProbability']
    Day_Wind = round((main_parse['Day']['Wind']['Speed']['Value'])*1.6)
    Day_WindGust = round((main_parse['Day']['WindGust']['Speed']['Value'])*1.6)
    Day_Relative_Humidity = main_parse['Day']['RelativeHumidity']['Average']

    Night_real_temper = round((main_parse['RealFeelTemperature']['Minimum']['Value']-32)/1.8)
    Night_RainProbability = main_parse['Night']['RainProbability']
    Night_Snow_Probability = main_parse['Night']['SnowProbability']
    Night_Wind = round((main_parse['Night']['Wind']['Speed']['Value'])*1.6)
    Night_WindGust = round((main_parse['Night']['WindGust']['Speed']['Value'])*1.6)
    Night_Relative_Humidity = main_parse['Night']['RelativeHumidity']['Average']

    if day:
        return Day_real_temper, Day_Wind, Day_WindGust, Day_Rain_Probability, Day_Snow_Probability, Day_Relative_Humidity
    else:
        return Night_real_temper, Night_Wind, Night_WindGust, Night_RainProbability, Night_Snow_Probability, Night_Relative_Humidity
def parsing_weather_data12(cur_hour): # Эта функция парсит json за выбранный час
    main_parse = hours_12_info[cur_hour]

    temperature = round((main_parse['Temperature']['Value'] - 32) / 1.8)
    real_temper = round((main_parse['RealFeelTemperature']['Value'] - 32) / 1.8)
    real_temper_shade = round((main_parse['RealFeelTemperatureShade']['Value'] - 32) / 1.8)

    Wind = round((main_parse['Wind']['Speed']['Value']) * 1.6)
    WindGust = round((main_parse['WindGust']['Speed']['Value']) * 1.6)

    Rain_Probability = main_parse['RainProbability']
    Snow_Probability = main_parse['SnowProbability']
    Relative_Humidity = main_parse['RelativeHumidity']

    return round((real_temper+real_temper_shade)/2),Wind,WindGust,Rain_Probability,Snow_Probability,Relative_Humidity

def determine_weather(list_data):
    bad_weather = 'Это летняя погода'
    temperature, wind_speed, wind_gust, rain_probability, snow_probability, humidity = list_data
    if rain_probability > 50:
        precipitation = f"C возможным дождем {rain_probability}%"
    elif snow_probability > 50:
        precipitation = f"C возможным снегом {snow_probability}%"
    else:
        precipitation = f"Маловероятные осадки {max(rain_probability,snow_probability)}%"

    if temperature < 0:
        temperature_description = f"Морозная погода {temperature}°"
    elif 0 <= temperature <= 10:
        temperature_description = f"Холодная погода {temperature}°"
    elif 10 < temperature <= 20:
        temperature_description = f"Благоприятная погода {temperature}°"
    elif 20 < temperature < 30:
        temperature_description = f"Теплая погода {temperature}°"
    elif temperature >= 30:
        temperature_description = f"Жаркая погода {temperature}°"

    if wind_speed < 4:
        wind_description = "Безветренно"
    elif 4 <= wind_speed <= 8:
        wind_description = "Спокойный ветер"
    elif 8 < wind_speed <= 15:
        wind_description = "Ветрено"
    elif wind_speed > 15:
        wind_description = "Сильный ветер"
    if temperature < 14 or rain_probability > 50 or wind_gust > 15:
        bad_weather = 'Это не летняя погода, Нужно надеть что-ниудь теплое'
    weather_description = (
        f"{temperature_description}. {precipitation}. "
        f"{wind_description}. "
        f"Уровень влажности составляет {humidity}%. "
        f"Максимальные порывы ветра: {wind_gust} м/с.\n"
        f"{bad_weather}"
    )

    return weather_description
