from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

from datetime import datetime, timedelta

# Argumentos padrão para a DAG
default_args = {
    'start_date': datetime(2019, 1, 1),
    'owner': 'Airflow'
}

# Função para a segunda tarefa
def second_task():
    print('Hello from second_task')
    #raise ValueError('This will turns the python task in failed state')

# Função para a terceira tarefa
def third_task():
    print('Hello from third_task')
    #raise ValueError('This will turns the python task in failed state')

# Definindo a DAG com um agendamento específico
with DAG(dag_id='depends_task', schedule_interval="0 0 * * *", default_args=default_args) as dag:
    
    # Task 1: Executa um comando Bash simples
    bash_task_1 = BashOperator(task_id='bash_task_1', bash_command="echo 'first task'")
    
    # Task 2: Executa uma função Python que imprime uma mensagem
    python_task_2 = PythonOperator(task_id='python_task_2', python_callable=second_task)

    # Task 3: Executa uma função Python que imprime uma mensagem
    python_task_3 = PythonOperator(task_id='python_task_3', python_callable=third_task)
