# Dag de testes para o ambiente
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

# Definir argumentos padrão
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Criar a DAG
with DAG(
    'my_first_dag',
    default_args=default_args,
    description='Minha primeira DAG no Airflow',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 11, 28),
    catchup=False,
    tags=['exemplo'],
) as dag:

    # Definir as tarefas
    task1 = BashOperator(
        task_id='print_date',
        bash_command='date',
    )

    task2 = BashOperator(
        task_id='say_hello',
        bash_command='echo "Olá, Airflow!"',
    )

    # Configurar a sequência de execução
    task1 >> task2
