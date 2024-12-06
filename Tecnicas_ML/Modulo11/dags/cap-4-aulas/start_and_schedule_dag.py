# Imports
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator 

from datetime import datetime, timedelta

# Definição de argumentos padrão para a DAG
default_args = {
    'start_date': datetime(2019, 3, 29, 1),  
    'owner': 'Airflow'                       
}

# Definição da DAG utilizando um gerenciador de contexto
with DAG(
    dag_id='start_and_schedule_dag',           
    schedule_interval="0 * * * *",            
    default_args=default_args                 
) as dag:
    
    # Tarefa dummy (placeholder) com identificador 'dummy_task_1'
    dummy_task_1 = DummyOperator(task_id='dummy_task_1')
    
    # Tarefa dummy (placeholder) com identificador 'dummy_task_2'
    dummy_task_2 = DummyOperator(task_id='dummy_task_2')
    
    # Definição da sequência de execução: 'dummy_task_1' será executada antes de 'dummy_task_2'
    dummy_task_1 >> dummy_task_2

    
    # Logs to help you (printed from the web server logs)
    # Uncomment when you use the DAG, comment when not
    # run_dates = dag.get_run_dates(start_date=dag.start_date)
    # next_execution_date = run_dates[-1] if len(run_dates) != 0 else None
    # print('[DAG:start_and_schedule_dag] start_date: {0} - schedule_interval: {1} - Last execution_date: {2} - next execution_date {3} in UTC'.format(
    #     dag.default_args['start_date'], 
    #     dag._schedule_interval, 
    #     dag.latest_execution_date, 
    #     next_execution_date
    #     ))