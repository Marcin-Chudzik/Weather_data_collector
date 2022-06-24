import json
from datetime import datetime

import requests
from airflow import DAG
from airflow.operators.python import PythonOperator

# Api key required to get api response
API_key = "7ad87a34dcc3c2be88b7ba506cf382d0"

# Warsaw geographical coordinates
warsaw_lat = 52.237049
warsaw_lon = 21.017532

# Gdańsk geographical coordinates
gdansk_lat = 54.372158
gdansk_lon = 18.638306

# API call attributes
part = ['current']
measurement_units = "metric"
language = "pl"

warsaw_url = f"https://api.openweathermap.org/data/2.5/weather?lat=" \
             f"{warsaw_lat}&lon={warsaw_lon}&appid={API_key}&units{measurement_units}&lang{language}"

gdansk_url = f"https://api.openweathermap.org/data/2.5/weather?lat=" \
             f"{gdansk_lat}&lon={gdansk_lon}&appid={API_key}&units{measurement_units}&lang{language}"

urls_list = [warsaw_url, gdansk_url]


# getting api response and saving data into file
def response_and_save(*args):
    urls = args[0]
    for url in urls:
        response = requests.get(url)
        with open('weather_data', 'a') as file:
            data: str = json.dumps(response, sort_keys=True, indent=4)
            file.write(data)


dag = DAG('collect_weather_data',
          description='Collecting weather data',
          schedule_interval='@hourly',
          start_date=datetime(2022, 4, 26),
          catchup=False
          )

# data collector task ready to execute by scheduler
data_collector = PythonOperator(task_id='collect_weather_data',
                                python_callable=response_and_save,
                                op_args=urls_list,
                                dag=dag
                                )
