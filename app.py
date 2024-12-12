from flask import Flask, request, render_template
import requests
from datetime import datetime
from main import (API_key,
                  get_APIinfo,
                  search_for_name,
                  parsing_weather_data,
                  parsing_weather_data12,
                  determine_weather)

app = Flask(__name__)

# запуск html формы
@app.route('/')
def form():
    return render_template('form.html')

# Обработка кнопки
@app.route('/weather', methods=['POST'])
def weather():
    start_city = request.form['start']
    time_start = request.form['time_start']

    end_city = request.form['end']
    time_end = request.form['time_end']

    if start_city.isalpha() and end_city.isalpha():
        search_for_name(API_key,start_city) # Получение погоды за 12 часов и 5 дней по названию для первого города
        from main import day_5_info, hours_12_info

        # Получаем разницу во времени между текущей датой и введенной
        cur_time_start = datetime(int(time_start[0:4]),int(time_start[5:7]),(int(time_start[8:10])+1 if int(time_start[11:13])+1==24 else int(time_start[8:10])),(0 if int(time_start[11:13])+1==24 else int(time_start[11:13])+1),int(time_start[14:16])) - datetime.now()
        cur_time_end = datetime(int(time_end[0:4]),int(time_end[5:7]),(int(time_end[8:10])+1 if int(time_end[11:13])+1==24 else int(time_end[8:10])),(0 if int(time_end[11:13])+1==24 else int(time_end[11:13])+1),int(time_end[14:16])) - datetime.now()

        # Если нам нужна информация о 12-ти часовой погоде
        if (cur_time_start.seconds+cur_time_start.days*24*60*60)//60//60 < 12:
            start_weather = determine_weather(parsing_weather_data12((cur_time_start.seconds+cur_time_start.days*24*60*60)//60//60)) # итоговые данные
        else:
            if 10 <= (int(time_start[11:13])) <= 21: # Если время от 10 до 9 - это дневная погода
                start_weather = determine_weather(parsing_weather_data(cur_time_start.days,True)) # итоговые данные
            else: # иначе ночная
                start_weather = determine_weather(parsing_weather_data(cur_time_start.days,False)) # итоговые данные

        search_for_name(API_key, end_city)  # Получение погоды за 12 часов и 5 дней по названию для второго города
        from main import day_5_info, hours_12_info

        if (cur_time_end.seconds+cur_time_end.days*24*60*60)//60//60 < 12:
            end_weather = determine_weather(parsing_weather_data12((cur_time_end.seconds+cur_time_end.days*24*60*60)//60//60)) # итоговые данные
        else:
            if 10 <= (int(time_end[11:13])) <= 21: # это день
                end_weather = determine_weather(parsing_weather_data(cur_time_end.days, True)) # итоговые данные
            else: # Иначе ночь
                end_weather = determine_weather(parsing_weather_data(cur_time_end.days, False)) # итоговые данные

    # Если нам нужна информация о 5-ти дневней погоде
    else:
        get_APIinfo(API_key, start_city.split()[0],start_city.split()[1]) # Получение погоды за 12 часов и 5 дней по координатам для первого города
        from main import day_5_info, hours_12_info

        # Получаем разницу во времени между текущей датой и введенной
        cur_time_start = datetime(int(time_start[0:4]), int(time_start[5:7]), (
            int(time_start[8:10]) + 1 if int(time_start[11:13]) + 1 == 24 else int(time_start[8:10])),
                                  (0 if int(time_start[11:13]) + 1 == 24 else int(time_start[11:13]) + 1),
                                  int(time_start[14:16])) - datetime.now()
        cur_time_end = datetime(int(time_end[0:4]), int(time_end[5:7]),
                                (int(time_end[8:10]) + 1 if int(time_end[11:13]) + 1 == 24 else int(time_end[8:10])),
                                (0 if int(time_end[11:13]) + 1 == 24 else int(time_end[11:13]) + 1),
                                int(time_end[14:16])) - datetime.now()

        if (cur_time_start.seconds + cur_time_start.days * 24 * 60 * 60) // 60 // 60 < 12:
            start_weather = determine_weather(
                parsing_weather_data12((cur_time_start.seconds + cur_time_start.days * 24 * 60 * 60) // 60 // 60)) # итоговые данные
        else:
            if 10 <= (int(time_start[11:13])) <= 21:
                start_weather = determine_weather(parsing_weather_data(cur_time_start.days, True)) # итоговые данные
            else:
                start_weather = determine_weather(parsing_weather_data(cur_time_start.days, False)) # итоговые данные

        get_APIinfo(API_key, end_city.split()[0],
                    end_city.split()[1])  # Получение погоды за 12 часов и 5 дней по координатам для второго города
        from main import day_5_info, hours_12_info

        if (cur_time_end.seconds + cur_time_end.days * 24 * 60 * 60) // 60 // 60 < 12:
            end_weather = determine_weather(
                parsing_weather_data12((cur_time_end.seconds + cur_time_end.days * 24 * 60 * 60) // 60 // 60)) # итоговые данные
        else:
            if 10 <= (int(time_end[11:13])) <= 21:
                end_weather = determine_weather(parsing_weather_data(cur_time_end.days, True)) # итоговые данные
            else:
                end_weather = determine_weather(parsing_weather_data(cur_time_end.days, False)) # итоговые данные

    # Вывод пост запроса
    return render_template('result.html', start=start_city, start_weather=start_weather, end=end_city,
                           end_weather=end_weather,start_time = request.form['time_start'].replace('T',' '), end_time = request.form['time_end'].replace('T',' '))

if __name__ == '__main__':
    app.run()
