import pytest
from airflow.models import DagBag

class TestDagValidation:
    # Define o limite máximo de tempo de carregamento para DAGs (em segundos)
    LOAD_SECOND_THRESHOLD = 2
    
    # Define o email obrigatório para alertas
    REQUIRED_EMAIL = "owner@test.com"
    
    # Define o número esperado de DAGs no projeto
    EXPECTED_NUMBER_OF_DAGS = 7

    def test_import_dags(self, dagbag):
        """
        Verify that Airflow is able to import all DAGs
        in the repo
        - check for typos
        - check for cycles
        """
        # Verifica se não há erros na importação das DAGs
        assert len(dagbag.import_errors) == 0, "DAG failures detected! Got: {}".format(
            dagbag.import_errors
        )

    def test_time_import_dags(self, dagbag):
        """
        Verify that DAGs load fast enough
        - check for loading time
        """
        # Obtém as estatísticas de carregamento das DAGs
        stats = dagbag.dagbag_stats
        
        # Filtra DAGs que levam mais do que o limite de tempo definido
        slow_dags = list(filter(lambda f: f.duration > self.LOAD_SECOND_THRESHOLD, stats))
        
        # Cria uma string com os nomes das DAGs lentas
        res = ', '.join(map(lambda f: f.file[1:], slow_dags))
        
        # Verifica se não há DAGs que excedem o tempo limite de carregamento
        assert len(slow_dags) == 0, "The following DAGs take more than {0}s to load: {1}".format(
            self.LOAD_SECOND_THRESHOLD,
            res
        )

    @pytest.mark.skip(reason="not yet added to the DAGs")
    def test_default_args_email(self, dagbag):
        """
        Verify that DAGs have the required email
        - Check email
        """
        # Itera sobre todas as DAGs para verificar se o email obrigatório está presente
        for dag_id, dag in dagbag.dags.items():
            emails = dag.default_args.get('email', [])
            
            # Verifica se o email requerido está na lista de emails
            assert self.REQUIRED_EMAIL in emails, "The mail {0} for sending alerts is missing from the DAG {1}".format(self.REQUIRED_EMAIL, dag_id)

    @pytest.mark.skip(reason="not yet added to the DAGs")
    def test_default_args_retries(self, dagbag):
        """
        Verify that DAGs have the required number of retries
        - Check retries
        """
        # Itera sobre todas as DAGs para verificar se o número de retentativas está definido
        for dag_id, dag in dagbag.dags.items():
            retries = dag.default_args.get('retries', None)
            
            # Verifica se o número de retentativas não é None
            assert retries is not None, "You must specify a number of retries in the DAG: {0}".format(dag_id)

    @pytest.mark.skip(reason="not yet added to the DAGs")
    def test_default_args_retry_delay(self, dagbag):
        """
        Verify that DAGs have the required retry_delay expressed in seconds
        - Check retry_delay
        """
        # Itera sobre todas as DAGs para verificar se o atraso de retentativa está definido
        for dag_id, dag in dagbag.dags.items():
            retry_delay = dag.default_args.get('retry_delay', None)
            
            # Verifica se o atraso de retentativa não é None
            assert retry_delay is not None, "You must specify a retry delay (seconds) in the DAG: {0}".format(dag_id)

    def test_number_of_dags(self, dagbag):
        """
        Verify if there is the right number of DAGs in the dag folder
        - Check number of dags
        """
        # Obtém as estatísticas de carregamento das DAGs
        stats = dagbag.dagbag_stats
        
        # Calcula o número total de DAGs
        dag_num = sum([o.dag_num for o in stats])
        
        # Verifica se o número de DAGs corresponde ao número esperado
        assert dag_num == self.EXPECTED_NUMBER_OF_DAGS, "Wrong number of dags, {0} expected got {1} (Can be due to cycles!)".format(self.EXPECTED_NUMBER_OF_DAGS, dag_num)