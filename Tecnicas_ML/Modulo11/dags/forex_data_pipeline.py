# # Imports das bibliotecas
# import airflow
# from airflow import DAG
# from airflow.contrib.sensors.file_sensor import FileSensor
# from airflow.sensors.http_sensor import HttpSensor
# from airflow.operators.bash_operator import BashOperator
# from airflow.operators.python_operator import PythonOperator
# from airflow.operators.hive_operator import HiveOperator
# from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
# from airflow.operators.email_operator import EmailOperator
# from airflow.operators.slack_operator import SlackAPIPostOperator
# from datetime import datetime, timedelta

# import csv
# import requests
# import json

# # Argumentos padrão do DAG
# default_args = {
#             "owner": "Airflow",
#             "start_date": airflow.utils.dates.days_ago(1),
#             "depends_on_past": False,
#             "email_on_failure": False,
#             "email_on_retry": False,
#             "email": "yuri3.zdebis@host.com",
#             "retries": 1,
#             "retry_delay": timedelta(minutes=5)
#         }

# def download_rates():
#     # Abre o arquivo que contém as moedas base e pares de moedas para leitura
#     with open('/usr/local/airflow/dags/files/forex_currencies.csv') as forex_currencies:
#         reader = csv.DictReader(forex_currencies, delimiter=';')  # Lê o arquivo CSV como dicionário, separando por ';'
#         for row in reader:  # Itera sobre cada linha do arquivo CSV
#             base = row['base']  # Obtém a moeda base da linha atual
#             with_pairs = row['with_pairs'].split(' ')  # Separa os pares de moedas em uma lista
#             # Faz uma requisição à API de taxas de câmbio para obter as taxas da moeda base
#             indata = requests.get('https://api.exchangeratesapi.io/latest?base=' + base).json()
#             # Prepara os dados de saída, incluindo a moeda base, as taxas e a data da última atualização
#             outdata = {
#                 'base': base,
#                 'rates': {},  # Dicionário para armazenar as taxas de câmbio dos pares
#                 'last_update': indata['date']  # Data da última atualização fornecida pela API
#             }
#             for pair in with_pairs:  # Itera sobre os pares de moedas
#                 outdata['rates'][pair] = indata['rates'][pair]  # Adiciona a taxa de câmbio do par no dicionário
#             # Abre o arquivo JSON no modo de anexar ('a') para salvar os dados processados
#             with open('/usr/local/airflow/dags/files/forex_rates.json', 'a') as outfile:
#                 json.dump(outdata, outfile)  # Grava os dados em formato JSON no arquivo
#                 outfile.write('\n')  # Adiciona uma nova linha após cada entrada


# # Definição do DAG
# with DAG(dag_id="forex_data_pipeline", schedule_interval="@daily", default_args=default_args, catchup=False) as dag:

#     # Operator para verificar se forex_rates esta disponivel, utilizando um HttpSensor
#     is_forex_rates_available = HttpSensor(
#             task_id="is_forex_rates_available",
#             method="GET",
#             http_conn_id="forex_api",
#             endpoint="latest",
#             response_check=lambda response: "rates" in response.text,
#             poke_interval=5,
#             timeout=20
#     )

#     # Operator para verificar se o arquivo forex_curencies.csv está disponivel
#     # (O endereço forex_paths via json)
#     is_forex_currencies_file_available = FileSensor(
#             task_id="is_forex_currencies_file_available",
#             fs_conn_id="forex_path",
#             filepath="forex_currencies.csv",
#             poke_interval=5,
#             timeout=20
#     )

#     # Python Operator! Possibilita a execução de codigo python pelo operator
#     # Nesse caso executa a função dowload_rates, definida acima
#     downloading_rates = PythonOperator(
#             task_id="downloading_rates",
#             python_callable=download_rates
#     )

#     # Bash Operator. Permite a execução de comandos de terminal.
#     # Nesse caso, serve salvar as taxas de câmbio no HDFS
# saving_rates = BashOperator(
#     task_id="saving_rates",  
#     bash_command="""
#         hdfs dfs -mkdir -p /forex && \  # Cria o diretório '/forex' no HDFS, caso não exista
#         hdfs dfs -put -f $AIRFLOW_HOME/dags/files/forex_rates.json /forex  # Envia o arquivo JSON para o HDFS
#     """
# )

# # Operador Hive para criar uma tabela externa no Hive
# creating_forex_rates_table = HiveOperator(
#     task_id="creating_forex_rates_table",  
#     hive_cli_conn_id="hive_conn",  
#     hql="""
#         CREATE EXTERNAL TABLE IF NOT EXISTS forex_rates(  # Criação da tabela externa
#             base STRING,        
#             last_update DATE,   
#             eur DOUBLE,         
#             usd DOUBLE,         
#             nzd DOUBLE,         
#             gbp DOUBLE,         
#             jpy DOUBLE,         
#             cad DOUBLE          
#         )
#         ROW FORMAT DELIMITED
#         FIELDS TERMINATED BY ',' 
#         STORED AS TEXTFILE        
#     """
# )

# # Operador SparkSubmit para processar os dados no Spark
# forex_processing = SparkSubmitOperator(
#     task_id="forex_processing",  
#     conn_id="spark_conn",        
#     application="/usr/local/airflow/dags/scripts/forex_processing.py",  # Script a ser executado
#     verbose=False  
# )

# # Operador para enviar uma notificação por e-mail
# sending_email_notification = EmailOperator(
#     task_id="sending_email", 
#     to="yuri3.zdebis@host.com"  
#     subject="forex_data_pipeline",  
#     html_content="""
#         <h3>forex_data_pipeline succeeded</h3>  # Conteúdo do e-mail em formato HTML
#     """
# )


# # Definição da sequência de execução das tarefas
# is_forex_rates_available >> is_forex_currencies_file_available >> downloading_rates >> saving_rates
# saving_rates >> creating_forex_rates_table >> forex_processing
