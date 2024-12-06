from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator

# Função para gerar o arquivo
def generate_file():
    with open('/tmp/generated_file.txt', 'w') as f:
        f.write('Este é um arquivo gerado pelo Apache Airflow.\n')
    print('Arquivo gerado em /tmp/generated_file.txt')

# Função para verificar o arquivo
def validate_file():
    try:
        with open('/tmp/generated_file.txt', 'r') as f:
            content = f.read()
        if 'Airflow' in content:
            print('Validação concluída: o arquivo contém a palavra "Airflow".')
        else:
            raise ValueError('Validação falhou: a palavra "Airflow" não foi encontrada.')
    except FileNotFoundError:
        raise FileNotFoundError('O arquivo não foi encontrado.')

# Função para finalizar o processo
def finish_process():
    print('Processo concluído com sucesso!')

# Configuração da DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    'simple_project_dag',
    default_args=default_args,
    description='DAG simples para demonstrar um projeto no Airflow',
    schedule_interval=None,  # Executa manualmente
    start_date=datetime(2023, 11, 28),
    catchup=False,
    tags=['exemplo', 'projeto simples'],
) as dag:

    start = DummyOperator(task_id='start')

    generate_task = PythonOperator(
        task_id='generate_file',
        python_callable=generate_file,
    )

    validate_task = PythonOperator(
        task_id='validate_file',
        python_callable=validate_file,
    )

    finish = PythonOperator(
        task_id='finish_process',
        python_callable=finish_process,
    )

    # Configuração da sequência de tarefas
    start >> generate_task >> validate_task >> finish
