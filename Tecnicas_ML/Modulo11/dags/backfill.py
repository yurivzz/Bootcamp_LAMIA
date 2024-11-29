from airflow import DAG
from airflow.operators.bash_operator import BashOperator  # Importa o operador Bash

from datetime import datetime, timedelta

# Definição de argumentos padrão para a DAG
default_args = {
    'start_date': datetime(2019, 1, 1),  
    'owner': 'Airflow'                   
}

# Definição da DAG utilizando um gerenciador de contexto
with DAG(
    dag_id='backfill',                 
    schedule_interval="0 0 * * *",     # Agendamento: uma vez por dia, à meia-noite
    default_args=default_args,         
    catchup=False                      # Não executar tarefas pendentes de períodos anteriores
) as dag:
    
    # Task 1: Executa um comando Bash para imprimir "first task"
    bash_task_1 = BashOperator(
        task_id='bash_task_1',           
        bash_command="echo 'first task'" 
    )
    
    # Task 2: Executa um comando Bash para imprimir "second task"
    bash_task_2 = BashOperator(
        task_id='bash_task_2',           
        bash_command="echo 'second task'"
            )

    # Define a ordem de execução: 'bash_task_1' será executada antes de 'bash_task_2'
    bash_task_1 >> bash_task_2
