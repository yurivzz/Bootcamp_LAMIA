from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

# Função de callback para sucesso de tarefa
def on_success_task(dict):
    print('on_success_dag')
    print(dict)

# Função de callback para falha de tarefa
def on_failure_task(dict):
    print('on_failure_dag')
    print(dict)

# Argumentos padrão para a DAG
default_args = {
    'start_date': datetime(2019, 1, 1),
    'owner': 'Airflow',
    'retries': 3,
    'retry_delay': timedelta(seconds=60),
    'emails': ['yuri3.zdebis@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False, 
    'on_failure_callback': on_failure_task,
    'on_sucess_callback': on_success_task,
    'execution_timeout': timedelta(seconds=60)
}

# Função de callback para sucesso da DAG
def on_success_dag(dict):
    print('on_success_dag')
    print(dict)

# Função de callback para falha da DAG
def on_failure_dag(dict):
    print('on_failure_dag')
    print(dict)

# Definição da DAG
with DAG(
    dag_id='alert_dag',
    schedule_interval="0 0 * * *",
    default_args=default_args,
    catchup=True,
    dagrun_timeout=timedelta(seconds=75),
    on_sucess_callback=on_success_dag,
    on_failure_callback=on_failure_dag
) as dag:
    
    # Task 1: Comando Bash que falha propositalmente (exit 1)
    t1 = BashOperator(task_id='t1', bash_command="exit 1")
    
    # Task 2: Comando Bash que imprime 'second task'
    t2 = BashOperator(task_id='t2', bash_command="echo 'second task'")

    # Definição da sequência: t1 precede t2
    t1 >> t2
