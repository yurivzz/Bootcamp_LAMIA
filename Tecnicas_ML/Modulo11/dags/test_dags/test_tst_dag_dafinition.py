import pytest
import collections
import pendulum
from airflow.models import DagBag

# Cria um fixture para recuperar a DAG específica para teste
@pytest.fixture(scope="class")
def dag(dagbag):
    return dagbag.get_dag('tst_dag')

class TestTstDagDefinition:
    # Define o número esperado de tarefas na DAG
    EXPECTED_NB_TASKS = 6
    
    # Lista os IDs das tarefas esperadas na DAG
    EXPECTED_TASKS = ['task_1', 'task_2', 'task_3', 'task_4', 'task_5', 'task_6']
    
    # Função lambda para comparar listas ignorando a ordem dos elementos
    compare = lambda self, x, y: collections.Counter(x) == collections.Counter(y)

    def test_nb_tasks(self, dag):
        """
        Verify the number of tasks in the DAG
        """
        # Conta o número total de tarefas na DAG
        nb_tasks = len(dag.tasks)
        # Verifica se o número de tarefas corresponde ao esperado
        assert nb_tasks == self.EXPECTED_NB_TASKS, "Wrong number of tasks, {0} expected, got {1}".format(self.EXPECTED_NB_TASKS, nb_tasks)

    def test_contain_tasks(self, dag):
        """
        Verify if the DAG is composed of the expected tasks
        """
        # Extrai os IDs de todas as tarefas da DAG
        task_ids = list(map(lambda task: task.task_id, dag.tasks))
        # Verifica se os IDs das tarefas correspondem aos esperados
        assert self.compare(task_ids, self.EXPECTED_TASKS)

    # Teste parametrizado para verificar dependências das tarefas
    @pytest.mark.parametrize("task, expected_upstream, expected_downstream",
    [
        ("task_1", [], ["task_2"]),
        ("task_2", ["task_1"], ["task_3", "task_4", "task_5"]),
        ("task_3", ["task_2"], ["task_6"])
    ]
    )
    def test_dependencies_of_tasks(self, dag, task, expected_upstream, expected_downstream):
        """
        Verify if a given task has the expected upstream and downstream dependencies
        - Parametrized test function so that each task given in the array is tested with the associated parameters
        """
        # Obtém a tarefa específica da DAG
        task = dag.get_task(task)
        # Verifica se as dependências upstream estão corretas
        assert self.compare(task.upstream_task_ids, expected_upstream), "The task {0} doesn't have the expected upstream dependencies".format(task)
        # Verifica se as dependências downstream estão corretas
        assert self.compare(task.downstream_task_ids, expected_downstream), "The task {0} doesn't have the expected downstream dependencies".format(task)

    def test_start_date_and_catchup(self, dag):
        """
        Verify that the start_date is < current date and catchup = False
        """
        # Método atualmente vazio, apenas retorna True
        True

    def test_same_start_date_all_tasks(self, dag):
        """
        Best Practice: All of your tasks should have the same start_date
        """
        # Obtém todas as tarefas da DAG
        tasks = dag.tasks
        # Extrai as datas de início de todas as tarefas
        start_dates = list(map(lambda task: task.start_date, tasks))
        # Verifica se todas as tarefas têm a mesma data de início
        assert len(set(start_dates)) == 1